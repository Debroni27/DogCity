"""События владельца питомца."""

from dataclasses import dataclass

from src.domain.events.base import DomainEvent
from src.domain.value_objects import (
    Address,
    BehaviorTrait,
    BirthDate,
    Breed,
    Email,
    OwnerId,
    PersonName,
    PetGender,
    PetId,
    PetName,
    PhoneNumber,
    Rating,
    VaccinationCertificate,
    Weight,
)

__all__ = (
    "OwnerAddressChanged",
    "OwnerContactsChanged",
    "OwnerEvent",
    "OwnerRegistered",
    "OwnerReviewReceived",
    "PetAdded",
    "PetBehaviorUpdated",
    "PetRemoved",
    "PetWeightUpdated",
    "VaccinationAdded",
)


@dataclass(frozen=True, slots=True)
class OwnerRegistered(DomainEvent):
    """Владелец завёл аккаунт."""

    owner_id: OwnerId
    name: PersonName
    phone: PhoneNumber
    email: Email
    address: Address


@dataclass(frozen=True, slots=True)
class OwnerContactsChanged(DomainEvent):
    """Владелец изменил контактные данные."""

    owner_id: OwnerId
    name: PersonName
    phone: PhoneNumber
    email: Email


@dataclass(frozen=True, slots=True)
class OwnerAddressChanged(DomainEvent):
    """Владелец изменил адрес."""

    owner_id: OwnerId
    address: Address


@dataclass(frozen=True, slots=True)
class PetAdded(DomainEvent):
    """Владелец завёл питомца."""

    owner_id: OwnerId
    pet_id: PetId
    name: PetName
    breed: Breed
    gender: PetGender
    birth_date: BirthDate
    weight: Weight
    is_neutered: bool
    behavior_traits: frozenset[BehaviorTrait]


@dataclass(frozen=True, slots=True)
class PetRemoved(DomainEvent):
    """Владелец удалил питомца."""

    owner_id: OwnerId
    pet_id: PetId


@dataclass(frozen=True, slots=True)
class PetWeightUpdated(DomainEvent):
    """Вес питомца изменился, вместе с ним может смениться размерная категория."""

    owner_id: OwnerId
    pet_id: PetId
    weight: Weight


@dataclass(frozen=True, slots=True)
class VaccinationAdded(DomainEvent):
    """К питомцу добавлена отметка о прививке."""

    owner_id: OwnerId
    pet_id: PetId
    certificate: VaccinationCertificate


@dataclass(frozen=True, slots=True)
class PetBehaviorUpdated(DomainEvent):
    """Владелец уточнил особенности поведения питомца."""

    owner_id: OwnerId
    pet_id: PetId
    behavior_traits: frozenset[BehaviorTrait]


@dataclass(frozen=True, slots=True)
class OwnerReviewReceived(DomainEvent):
    """О владельце оставлен отзыв с оценкой, рейтинг пересчитан."""

    owner_id: OwnerId
    rating: Rating


type OwnerEvent = (
    OwnerAddressChanged
    | OwnerContactsChanged
    | OwnerRegistered
    | OwnerReviewReceived
    | PetAdded
    | PetBehaviorUpdated
    | PetRemoved
    | PetWeightUpdated
    | VaccinationAdded
)
"""Любое событие владельца, включая события его питомцев."""
