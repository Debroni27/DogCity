"""Агрегат заказа услуги догситтинга."""

from datetime import datetime

from src.domain.events import (
    OrderCancelled,
    OrderCompleted,
    OrderConfirmed,
    OrderEvent,
    OrderPlaced,
    OrderRejected,
    OrderStarted,
)
from src.domain.exceptions import IllegalStateTransitionError, InvariantViolationError
from src.domain.value_objects import (
    Address,
    CancellationReason,
    CorrelationId,
    EventId,
    Money,
    OrderComment,
    OrderId,
    OrderParty,
    OrderStatus,
    OwnerId,
    PetId,
    RejectionReason,
    ServiceOffer,
    SitterId,
    TimeInterval,
)

__all__ = ("Order",)


class Order:
    """Заказ услуги: от оформления владельцем до завершения или прекращения."""

    __slots__ = (
        "_address",
        "_cancelled_by",
        "_interval",
        "_offer",
        "_order_id",
        "_owner_id",
        "_pending_events",
        "_pet_id",
        "_sitter_id",
        "_status",
        "_total",
    )

    _order_id: OrderId
    _owner_id: OwnerId
    _sitter_id: SitterId
    _pet_id: PetId
    _offer: ServiceOffer
    _interval: TimeInterval
    _address: Address
    _status: OrderStatus
    _total: Money | None
    _cancelled_by: OrderParty | None
    _pending_events: list[OrderEvent]

    def __init__(self) -> None:
        """Заготовка заказа: состояние наполняет ``_apply``, создаёт ``place``."""
        self._pending_events = []

    @property
    def order_id(self) -> OrderId:
        """Идентификатор заказа."""
        return self._order_id

    @property
    def owner_id(self) -> OwnerId:
        """Владелец, оформивший заказ."""
        return self._owner_id

    @property
    def sitter_id(self) -> SitterId:
        """Догситтер, у которого заказана услуга."""
        return self._sitter_id

    @property
    def offer(self) -> ServiceOffer:
        """Предложение с ценой, зафиксированной на момент оформления."""
        return self._offer

    @property
    def interval(self) -> TimeInterval:
        """Время оказания услуги."""
        return self._interval

    @property
    def status(self) -> OrderStatus:
        """Текущее состояние заказа."""
        return self._status

    @property
    def total(self) -> Money | None:
        """Стоимость, зафиксированная при подтверждении; до него — ``None``."""
        return self._total

    @property
    def pending_events(self) -> tuple[OrderEvent, ...]:
        """События, накопленные с последнего ``clear_events``."""
        return tuple(self._pending_events)

    @classmethod
    def place(
        cls,
        *,
        order_id: OrderId,
        owner_id: OwnerId,
        sitter_id: SitterId,
        pet_id: PetId,
        offer: ServiceOffer,
        interval: TimeInterval,
        address: Address,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> "Order":
        """Владелец оформляет заказ у выбранного догситтера."""
        if interval.starts_at < occurred_at:
            raise InvariantViolationError("услуга не может начинаться в прошлом")
        order = cls()
        order._record(
            OrderPlaced(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                order_id=order_id,
                owner_id=owner_id,
                sitter_id=sitter_id,
                pet_id=pet_id,
                offer=offer,
                interval=interval,
                address=address,
            )
        )
        return order

    def clear_events(self) -> None:
        """Забыть накопленные события: их забрал прикладной слой."""
        self._pending_events.clear()

    def confirm(
        self, total: Money, occurred_at: datetime, correlation_id: CorrelationId
    ) -> None:
        """Догситтер принимает заказ, стоимость фиксируется."""
        self._ensure_status((OrderStatus.PENDING,), "confirm")
        self._record(
            OrderConfirmed(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                order_id=self._order_id,
                total=total,
            )
        )

    def reject(
        self,
        reason: RejectionReason,
        occurred_at: datetime,
        correlation_id: CorrelationId,
        comment: OrderComment | None = None,
    ) -> None:
        """Догситтер отказывается от заказа до его подтверждения."""
        self._ensure_status((OrderStatus.PENDING,), "reject")
        self._record(
            OrderRejected(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                order_id=self._order_id,
                reason=reason,
                comment=comment,
            )
        )

    def cancel(
        self,
        reason: CancellationReason,
        initiated_by: OrderParty,
        occurred_at: datetime,
        correlation_id: CorrelationId,
        comment: OrderComment | None = None,
    ) -> None:
        """Одна из сторон отменяет заказ до начала оказания услуги."""
        self._ensure_status((OrderStatus.PENDING, OrderStatus.CONFIRMED), "cancel")
        self._record(
            OrderCancelled(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                order_id=self._order_id,
                reason=reason,
                initiated_by=initiated_by,
                comment=comment,
            )
        )

    def start(self, occurred_at: datetime, correlation_id: CorrelationId) -> None:
        """Оказание услуги начинается."""
        self._ensure_status((OrderStatus.CONFIRMED,), "start")
        self._record(
            OrderStarted(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                order_id=self._order_id,
            )
        )

    def complete(self, occurred_at: datetime, correlation_id: CorrelationId) -> None:
        """Услуга оказана."""
        self._ensure_status((OrderStatus.IN_PROGRESS,), "complete")
        self._record(
            OrderCompleted(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                order_id=self._order_id,
            )
        )

    def may_be_reviewed_by(self, party: OrderParty) -> bool:
        """Вправе ли сторона оставить отзыв по этому заказу."""
        match self._status:
            case OrderStatus.COMPLETED:
                return True
            case OrderStatus.REJECTED:
                return party is OrderParty.OWNER
            case OrderStatus.CANCELLED:
                return party is not self._cancelled_by
            case _:
                return False

    def _ensure_status(
        self, allowed: tuple[OrderStatus, ...], transition: str
    ) -> None:
        """Пропустить переход только из перечисленных состояний."""
        if self._status not in allowed:
            raise IllegalStateTransitionError("Order", self._status, transition)

    def _record(self, event: OrderEvent) -> None:
        """Применить событие и запомнить его для публикации."""
        self._apply(event)
        self._pending_events.append(event)

    def _apply(self, event: OrderEvent) -> None:
        """Единственное место, где меняется состояние заказа."""
        match event:
            case OrderPlaced():
                self._order_id = event.order_id
                self._owner_id = event.owner_id
                self._sitter_id = event.sitter_id
                self._pet_id = event.pet_id
                self._offer = event.offer
                self._interval = event.interval
                self._address = event.address
                self._status = OrderStatus.PENDING
                self._total = None
                self._cancelled_by = None
            case OrderConfirmed():
                self._status = OrderStatus.CONFIRMED
                self._total = event.total
            case OrderRejected():
                self._status = OrderStatus.REJECTED
            case OrderCancelled():
                self._status = OrderStatus.CANCELLED
                self._cancelled_by = event.initiated_by
            case OrderStarted():
                self._status = OrderStatus.IN_PROGRESS
            case OrderCompleted():
                self._status = OrderStatus.COMPLETED
