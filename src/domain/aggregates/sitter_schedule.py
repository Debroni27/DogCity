"""Агрегат расписания догситтера."""

from dataclasses import dataclass
from datetime import datetime

from src.domain.events import BookingReleased, BookingReserved, SitterScheduleEvent
from src.domain.exceptions import InvariantViolationError
from src.domain.value_objects import (
    Capacity,
    CorrelationId,
    EventId,
    OrderId,
    ServiceFormat,
    SitterId,
    TimeInterval,
)

__all__ = ("Booking", "SitterSchedule")


@dataclass(frozen=True, slots=True)
class Booking:
    """Время догситтера, занятое под подтверждённый заказ."""

    order_id: OrderId
    interval: TimeInterval
    service_format: ServiceFormat


class SitterSchedule:
    """Занятость догситтера: брони уживаются в пределах вместимости."""

    __slots__ = ("_bookings", "_pending_events", "_sitter_id")

    _sitter_id: SitterId
    _bookings: dict[OrderId, Booking]
    _pending_events: list[SitterScheduleEvent]

    def __init__(self, sitter_id: SitterId) -> None:
        """Пустое расписание: идентификатор задаёт ключ, брони приносят события."""
        self._sitter_id = sitter_id
        self._bookings = {}
        self._pending_events = []

    @property
    def sitter_id(self) -> SitterId:
        """Догситтер, чьё это расписание."""
        return self._sitter_id

    @property
    def bookings(self) -> tuple[Booking, ...]:
        """Занятое время догситтера."""
        return tuple(self._bookings.values())

    @property
    def pending_events(self) -> tuple[SitterScheduleEvent, ...]:
        """События, накопленные с последнего ``clear_events``."""
        return tuple(self._pending_events)

    def clear_events(self) -> None:
        """Забыть накопленные события: их забрал прикладной слой."""
        self._pending_events.clear()

    def reserve(
        self,
        *,
        order_id: OrderId,
        interval: TimeInterval,
        service_format: ServiceFormat,
        capacity: Capacity,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> None:
        """Занять время догситтера под подтверждённый заказ."""
        if order_id in self._bookings:
            raise InvariantViolationError("время под этот заказ уже занято")
        overlapping = self._overlapping(interval)
        if service_format is ServiceFormat.INDIVIDUAL and overlapping:
            raise InvariantViolationError(
                "индивидуальная услуга требует догситтера целиком"
            )
        if any(
            booking.service_format is ServiceFormat.INDIVIDUAL
            for booking in overlapping
        ):
            raise InvariantViolationError(
                "время занято индивидуальной услугой другого владельца"
            )
        if self._peak_concurrency(interval, overlapping) >= capacity.value:
            raise InvariantViolationError("вместимость догситтера исчерпана")
        self._record(
            BookingReserved(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                sitter_id=self._sitter_id,
                order_id=order_id,
                interval=interval,
                service_format=service_format,
            )
        )

    def release(
        self, order_id: OrderId, occurred_at: datetime, correlation_id: CorrelationId
    ) -> None:
        """Освободить время: заказ отменён или отклонён."""
        if order_id not in self._bookings:
            raise InvariantViolationError("брони под этот заказ нет")
        self._record(
            BookingReleased(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                sitter_id=self._sitter_id,
                order_id=order_id,
            )
        )

    def _overlapping(self, interval: TimeInterval) -> tuple[Booking, ...]:
        """Брони, пересекающиеся с указанным интервалом."""
        return tuple(
            booking
            for booking in self._bookings.values()
            if booking.interval.overlaps(interval)
        )

    def _peak_concurrency(
        self, interval: TimeInterval, overlapping: tuple[Booking, ...]
    ) -> int:
        """Наибольшее число одновременных броней внутри интервала."""
        if not overlapping:
            return 0
        moments = [interval.starts_at] + [
            booking.interval.starts_at
            for booking in overlapping
            if booking.interval.starts_at > interval.starts_at
        ]
        return max(
            sum(
                1
                for booking in overlapping
                if booking.interval.starts_at <= moment < booking.interval.ends_at
            )
            for moment in moments
        )

    def _record(self, event: SitterScheduleEvent) -> None:
        """Применить событие и запомнить его для публикации."""
        self._apply(event)
        self._pending_events.append(event)

    def _apply(self, event: SitterScheduleEvent) -> None:
        """Единственное место, где меняется состояние расписания."""
        match event:
            case BookingReserved():
                self._bookings[event.order_id] = Booking(
                    order_id=event.order_id,
                    interval=event.interval,
                    service_format=event.service_format,
                )
            case BookingReleased():
                self._bookings.pop(event.order_id)
