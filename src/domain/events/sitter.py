"""События догситтера."""

from dataclasses import dataclass

from src.domain.events.base import DomainEvent
from src.domain.value_objects import (
    Address,
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
    "OfferPublished",
    "OfferWithdrawn",
    "SitterAddressChanged",
    "SitterContactsChanged",
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
class SitterReviewReceived(DomainEvent):
    """О догситтере оставлен отзыв с оценкой, рейтинг пересчитан."""

    sitter_id: SitterId
    rating: Rating
