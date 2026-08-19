"""Агрегат владельца питомцев."""

from dataclasses import dataclass, replace
from datetime import datetime

from src.domain.events import (
    OwnerAddressChanged,
    OwnerContactsChanged,
    OwnerEvent,
    OwnerRegistered,
    OwnerReviewReceived,
    PetAdded,
    PetBehaviorUpdated,
    PetRemoved,
    PetWeightUpdated,
    VaccinationAdded,
)
from src.domain.exceptions import InvariantViolationError
from src.domain.value_objects import (
    Address,
    AggregatedRating,
    BehaviorTrait,
    BirthDate,
    Breed,
    CorrelationId,
    Email,
    EventId,
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

__all__ = ("PETS_MAX", "Owner", "Pet")

PETS_MAX = 5


@dataclass(frozen=True, slots=True)
class Pet:
    """Питомец владельца: сущность внутри агрегата, опознаётся по ``pet_id``."""

    pet_id: PetId
    name: PetName
    breed: Breed
    gender: PetGender
    birth_date: BirthDate
    weight: Weight
    is_neutered: bool
    behavior_traits: frozenset[BehaviorTrait]
    vaccinations: tuple[VaccinationCertificate, ...]


class Owner:
    """Владелец питомцев: профиль, питомцы и сводная оценка от догситтеров."""

    __slots__ = (
        "_address",
        "_email",
        "_name",
        "_owner_id",
        "_pending_events",
        "_pets",
        "_phone",
        "_rating",
    )

    _owner_id: OwnerId
    _name: PersonName
    _phone: PhoneNumber
    _email: Email
    _address: Address
    _pets: dict[PetId, Pet]
    _rating: AggregatedRating
    _pending_events: list[OwnerEvent]

    def __init__(self) -> None:
        """Заготовка владельца: состояние наполняет ``_apply``."""
        self._pending_events = []

    @property
    def owner_id(self) -> OwnerId:
        """Идентификатор владельца."""
        return self._owner_id

    @property
    def pets(self) -> tuple[Pet, ...]:
        """Питомцы владельца."""
        return tuple(self._pets.values())

    @property
    def rating(self) -> AggregatedRating:
        """Сводная оценка владельца по отзывам догситтеров."""
        return self._rating

    @property
    def pending_events(self) -> tuple[OwnerEvent, ...]:
        """События, накопленные с последнего ``clear_events``."""
        return tuple(self._pending_events)

    @classmethod
    def register(
        cls,
        *,
        owner_id: OwnerId,
        name: PersonName,
        phone: PhoneNumber,
        email: Email,
        address: Address,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> "Owner":
        """Владелец заводит аккаунт: питомцы добавляются отдельно."""
        owner = cls()
        owner._record(
            OwnerRegistered(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                owner_id=owner_id,
                name=name,
                phone=phone,
                email=email,
                address=address,
            )
        )
        return owner

    def clear_events(self) -> None:
        """Забыть накопленные события: их забрал прикладной слой."""
        self._pending_events.clear()

    def has_pet(self, pet_id: PetId) -> bool:
        """Принадлежит ли питомец этому владельцу."""
        return pet_id in self._pets

    def change_contacts(
        self,
        name: PersonName,
        phone: PhoneNumber,
        email: Email,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> None:
        """Владелец меняет контактные данные."""
        self._record(
            OwnerContactsChanged(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                owner_id=self._owner_id,
                name=name,
                phone=phone,
                email=email,
            )
        )

    def change_address(
        self, address: Address, occurred_at: datetime, correlation_id: CorrelationId
    ) -> None:
        """Владелец меняет адрес."""
        self._record(
            OwnerAddressChanged(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                owner_id=self._owner_id,
                address=address,
            )
        )

    def add_pet(
        self,
        *,
        pet_id: PetId,
        name: PetName,
        breed: Breed,
        gender: PetGender,
        birth_date: BirthDate,
        weight: Weight,
        is_neutered: bool,
        behavior_traits: frozenset[BehaviorTrait],
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> None:
        """Владелец заводит питомца."""
        if len(self._pets) >= PETS_MAX:
            raise InvariantViolationError(f"питомцев не может быть больше {PETS_MAX}")
        if pet_id in self._pets:
            raise InvariantViolationError("такой питомец у владельца уже есть")
        self._record(
            PetAdded(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                owner_id=self._owner_id,
                pet_id=pet_id,
                name=name,
                breed=breed,
                gender=gender,
                birth_date=birth_date,
                weight=weight,
                is_neutered=is_neutered,
                behavior_traits=behavior_traits,
            )
        )

    def remove_pet(
        self, pet_id: PetId, occurred_at: datetime, correlation_id: CorrelationId
    ) -> None:
        """Владелец удаляет питомца."""
        self._ensure_pet(pet_id)
        self._record(
            PetRemoved(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                owner_id=self._owner_id,
                pet_id=pet_id,
            )
        )

    def update_pet_weight(
        self,
        pet_id: PetId,
        weight: Weight,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> None:
        """Владелец уточняет вес питомца, размерная категория выводится из него."""
        self._ensure_pet(pet_id)
        self._record(
            PetWeightUpdated(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                owner_id=self._owner_id,
                pet_id=pet_id,
                weight=weight,
            )
        )

    def update_pet_behavior(
        self,
        pet_id: PetId,
        behavior_traits: frozenset[BehaviorTrait],
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> None:
        """Владелец уточняет особенности поведения питомца."""
        self._ensure_pet(pet_id)
        self._record(
            PetBehaviorUpdated(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                owner_id=self._owner_id,
                pet_id=pet_id,
                behavior_traits=behavior_traits,
            )
        )

    def add_vaccination(
        self,
        pet_id: PetId,
        certificate: VaccinationCertificate,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> None:
        """Владелец добавляет питомцу отметку о прививке."""
        self._ensure_pet(pet_id)
        self._record(
            VaccinationAdded(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                owner_id=self._owner_id,
                pet_id=pet_id,
                certificate=certificate,
            )
        )

    def receive_review(
        self, rating: Rating, occurred_at: datetime, correlation_id: CorrelationId
    ) -> None:
        """О владельце оставлен отзыв с оценкой, сводный рейтинг пересчитывается."""
        self._record(
            OwnerReviewReceived(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                owner_id=self._owner_id,
                rating=rating,
            )
        )

    def _ensure_pet(self, pet_id: PetId) -> None:
        """Пропустить действие только для питомца этого владельца."""
        if pet_id not in self._pets:
            raise InvariantViolationError("такого питомца у владельца нет")

    def _record(self, event: OwnerEvent) -> None:
        """Применить событие и запомнить его для публикации."""
        self._apply(event)
        self._pending_events.append(event)

    def _apply(self, event: OwnerEvent) -> None:
        """Единственное место, где меняется состояние владельца и его питомцев."""
        match event:
            case OwnerRegistered():
                self._owner_id = event.owner_id
                self._name = event.name
                self._phone = event.phone
                self._email = event.email
                self._address = event.address
                self._pets = {}
                self._rating = AggregatedRating.empty()
            case OwnerContactsChanged():
                self._name = event.name
                self._phone = event.phone
                self._email = event.email
            case OwnerAddressChanged():
                self._address = event.address
            case PetAdded():
                self._pets[event.pet_id] = Pet(
                    pet_id=event.pet_id,
                    name=event.name,
                    breed=event.breed,
                    gender=event.gender,
                    birth_date=event.birth_date,
                    weight=event.weight,
                    is_neutered=event.is_neutered,
                    behavior_traits=event.behavior_traits,
                    vaccinations=(),
                )
            case PetRemoved():
                self._pets.pop(event.pet_id)
            case PetWeightUpdated():
                self._pets[event.pet_id] = replace(
                    self._pets[event.pet_id], weight=event.weight
                )
            case PetBehaviorUpdated():
                self._pets[event.pet_id] = replace(
                    self._pets[event.pet_id], behavior_traits=event.behavior_traits
                )
            case VaccinationAdded():
                pet = self._pets[event.pet_id]
                self._pets[event.pet_id] = replace(
                    pet, vaccinations=(*pet.vaccinations, event.certificate)
                )
            case OwnerReviewReceived():
                self._rating = self._rating.with_review(event.rating)
