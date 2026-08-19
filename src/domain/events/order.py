"""События заказа."""

from dataclasses import dataclass

from src.domain.events.base import DomainEvent
from src.domain.value_objects import (
    Address,
    CancellationReason,
    Money,
    OrderComment,
    OrderId,
    OrderParty,
    OwnerId,
    PetId,
    RejectionReason,
    ServiceOffer,
    SitterId,
    TimeInterval,
)

__all__ = (
    "OrderCancelled",
    "OrderCompleted",
    "OrderConfirmed",
    "OrderPlaced",
    "OrderRejected",
    "OrderStarted",
)


@dataclass(frozen=True, slots=True)
class OrderPlaced(DomainEvent):
    """Владелец оформил заказ."""

    order_id: OrderId
    owner_id: OwnerId
    sitter_id: SitterId
    pet_id: PetId
    offer: ServiceOffer
    interval: TimeInterval
    address: Address


@dataclass(frozen=True, slots=True)
class OrderConfirmed(DomainEvent):
    """Ситтер принял заказ, стоимость зафиксирована."""

    order_id: OrderId
    total: Money


@dataclass(frozen=True, slots=True)
class OrderRejected(DomainEvent):
    """Ситтер отказался от заказа до его подтверждения."""

    order_id: OrderId
    reason: RejectionReason
    comment: OrderComment | None = None


@dataclass(frozen=True, slots=True)
class OrderCancelled(DomainEvent):
    """Заказ отменён до начала оказания услуги."""

    order_id: OrderId
    reason: CancellationReason
    initiated_by: OrderParty
    comment: OrderComment | None = None


@dataclass(frozen=True, slots=True)
class OrderStarted(DomainEvent):
    """Оказание услуги началось."""

    order_id: OrderId


@dataclass(frozen=True, slots=True)
class OrderCompleted(DomainEvent):
    """Услуга оказана."""

    order_id: OrderId
