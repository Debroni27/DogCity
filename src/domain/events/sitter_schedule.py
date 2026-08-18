"""События расписания догситтера."""

from dataclasses import dataclass

from src.domain.events.base import DomainEvent
from src.domain.value_objects import OrderId, SitterId, TimeInterval

__all__ = (
    "BookingReleased",
    "BookingReserved",
)


@dataclass(frozen=True, slots=True)
class BookingReserved(DomainEvent):
    """Время догситтера занято подтверждённым заказом."""

    sitter_id: SitterId
    order_id: OrderId
    interval: TimeInterval


@dataclass(frozen=True, slots=True)
class BookingReleased(DomainEvent):
    """Время догситтера освободилось: заказ отменён или отклонён."""

    sitter_id: SitterId
    order_id: OrderId
