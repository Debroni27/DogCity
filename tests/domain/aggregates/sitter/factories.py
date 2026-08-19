"""Фабрики догситтеров."""

from datetime import datetime
from typing import TypedDict, Unpack

import factory

from src.domain.aggregates import Sitter
from src.domain.value_objects import (
    AcceptedDogSizes,
    Address,
    Capacity,
    CorrelationId,
    Email,
    PersonName,
    PhoneNumber,
    SitterId,
)
from tests.domain.events.factories import OCCURRED_AT
from tests.domain.value_objects.address.factories import AddressFactory
from tests.domain.value_objects.contacts.factories import (
    EmailFactory,
    PersonNameFactory,
    PhoneNumberFactory,
)
from tests.domain.value_objects.sitter_profile.factories import (
    AcceptedDogSizesFactory,
    CapacityFactory,
)


class RegisterArguments(TypedDict):
    """Именованные аргументы ``Sitter.register``."""

    sitter_id: SitterId
    name: PersonName
    phone: PhoneNumber
    email: Email
    address: Address
    capacity: Capacity
    accepted_dog_sizes: AcceptedDogSizes
    occurred_at: datetime
    correlation_id: CorrelationId


class SitterFactory(factory.Factory):
    """Догситтер на двух собак мелкого и среднего размера, без предложений."""

    class Meta:
        model = Sitter

    sitter_id = factory.LazyFunction(SitterId.new)
    name = factory.SubFactory(PersonNameFactory)
    phone = factory.SubFactory(PhoneNumberFactory)
    email = factory.SubFactory(EmailFactory)
    address = factory.SubFactory(AddressFactory)
    capacity = factory.SubFactory(CapacityFactory)
    accepted_dog_sizes = factory.SubFactory(AcceptedDogSizesFactory)
    occurred_at = OCCURRED_AT
    correlation_id = factory.LazyFunction(CorrelationId.new)

    @classmethod
    def _create(
        cls, model_class: type[Sitter], **kwargs: Unpack[RegisterArguments]
    ) -> Sitter:
        """Догситтер рождается фабричным методом агрегата."""
        return model_class.register(**kwargs)
