"""События догситтера."""

from dataclasses import dataclass

from src.domain.events.base import DomainEvent
from src.domain.value_objects import (
    AcceptedDogSizes,
    Address,
    Capacity,
    Email,
    Money,
    PersonName,
    PhoneNumber,
    Rating,
    ServiceFormat,
    ServiceType,
    SitterId,
    Tarification,
)

__all__ = (
    "AcceptedDogSizesChanged",
    "CapacityChanged",
    "OfferPublished",
    "OfferWithdrawn",
    "SitterAddressChanged",
    "SitterContactsChanged",
    "SitterEvent",
    "SitterRegistered",
    "SitterReviewReceived",
)


@dataclass(frozen=True, slots=True)
class SitterRegistered(DomainEvent):
    """Догситтер завёл аккаунт."""

    sitter_id: SitterId
    name: PersonName
    phone: PhoneNumber
    email: Email
    address: Address
    capacity: Capacity
    accepted_dog_sizes: AcceptedDogSizes


@dataclass(frozen=True, slots=True)
class SitterContactsChanged(DomainEvent):
    """Догситтер изменил контактные данные."""

    sitter_id: SitterId
    name: PersonName
    phone: PhoneNumber
    email: Email


@dataclass(frozen=True, slots=True)
class SitterAddressChanged(DomainEvent):
    """Догситтер изменил адрес."""

    sitter_id: SitterId
    address: Address


@dataclass(frozen=True, slots=True)
class OfferPublished(DomainEvent):
    """Догситтер выставил предложение по услуге."""

    sitter_id: SitterId
    service_type: ServiceType
    tarification: Tarification
    service_format: ServiceFormat
    price: Money


@dataclass(frozen=True, slots=True)
class OfferWithdrawn(DomainEvent):
    """Догситтер снял предложение."""

    sitter_id: SitterId
    service_type: ServiceType
    tarification: Tarification
    service_format: ServiceFormat


@dataclass(frozen=True, slots=True)
class CapacityChanged(DomainEvent):
    """Догситтер изменил число питомцев, которых берёт одновременно."""

    sitter_id: SitterId
    capacity: Capacity


@dataclass(frozen=True, slots=True)
class AcceptedDogSizesChanged(DomainEvent):
    """Догситтер изменил набор размеров собак, которых готов принять."""

    sitter_id: SitterId
    accepted_dog_sizes: AcceptedDogSizes


@dataclass(frozen=True, slots=True)
class SitterReviewReceived(DomainEvent):
    """О догситтере оставлен отзыв с оценкой, рейтинг пересчитан."""

    sitter_id: SitterId
    rating: Rating


type SitterEvent = (
    AcceptedDogSizesChanged
    | CapacityChanged
    | OfferPublished
    | OfferWithdrawn
    | SitterAddressChanged
    | SitterContactsChanged
    | SitterRegistered
    | SitterReviewReceived
)
"""Любое событие догситтера."""
