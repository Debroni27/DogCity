"""Фабрики владельцев питомцев."""

from datetime import datetime
from typing import TypedDict, Unpack

import factory

from src.domain.aggregates import Owner
from src.domain.value_objects import (
    Address,
    BehaviorTrait,
    CorrelationId,
    Email,
    OwnerId,
    PersonName,
    PetGender,
    PetId,
    PhoneNumber,
)
from tests.domain.events.factories import OCCURRED_AT
from tests.domain.value_objects.address.factories import AddressFactory
from tests.domain.value_objects.contacts.factories import (
    EmailFactory,
    PersonNameFactory,
    PhoneNumberFactory,
)
from tests.domain.value_objects.pet_profile.factories import (
    BirthDateFactory,
    BreedFactory,
    PetNameFactory,
    WeightFactory,
)


class RegisterArguments(TypedDict):
    """Именованные аргументы ``Owner.register``."""

    owner_id: OwnerId
    name: PersonName
    phone: PhoneNumber
    email: Email
    address: Address
    occurred_at: datetime
    correlation_id: CorrelationId


class OwnerFactory(factory.Factory):
    """Владелец без питомцев: питомцы заводятся отдельной командой."""

    class Meta:
        model = Owner

    owner_id = factory.LazyFunction(OwnerId.new)
    name = factory.SubFactory(PersonNameFactory)
    phone = factory.SubFactory(PhoneNumberFactory)
    email = factory.SubFactory(EmailFactory)
    address = factory.SubFactory(AddressFactory)
    occurred_at = OCCURRED_AT
    correlation_id = factory.LazyFunction(CorrelationId.new)

    @classmethod
    def _create(
        cls, model_class: type[Owner], **kwargs: Unpack[RegisterArguments]
    ) -> Owner:
        """Владелец рождается фабричным методом агрегата."""
        return model_class.register(**kwargs)


def add_pet(
    owner: Owner,
    pet_id: PetId | None = None,
    behavior_traits: frozenset[BehaviorTrait] = frozenset(),
) -> PetId:
    """Завести владельцу питомца с типовыми данными и вернуть его идентификатор."""
    if pet_id is None:
        pet_id = PetId.new()
    owner.add_pet(
        pet_id=pet_id,
        name=PetNameFactory(),
        breed=BreedFactory(),
        gender=PetGender.MALE,
        birth_date=BirthDateFactory(),
        weight=WeightFactory(),
        is_neutered=True,
        behavior_traits=behavior_traits,
        occurred_at=OCCURRED_AT,
        correlation_id=CorrelationId.new(),
    )
    return pet_id
