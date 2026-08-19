"""События расписания догситтера."""

from dataclasses import dataclass

from src.domain.events.base import DomainEvent
from src.domain.value_objects import OrderId, ServiceFormat, SitterId, TimeInterval

__all__ = (
    "BookingReleased",
    "BookingReserved",
    "SitterScheduleEvent",
)


@dataclass(frozen=True, slots=True)
class BookingReserved(DomainEvent):
    """Время догситтера занято подтверждённым заказом."""

    sitter_id: SitterId
    order_id: OrderId
    interval: TimeInterval
    service_format: ServiceFormat


@dataclass(frozen=True, slots=True)
class BookingReleased(DomainEvent):
    """Время догситтера освободилось: заказ отменён или отклонён."""

    sitter_id: SitterId
    order_id: OrderId


type SitterScheduleEvent = BookingReleased | BookingReserved
"""Любое событие расписания догситтера."""
