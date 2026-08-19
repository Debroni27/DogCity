"""Фабрики заказов."""

from datetime import datetime, timedelta
from typing import TypedDict, Unpack

import factory

from src.domain.aggregates import Order
from src.domain.value_objects import (
    Address,
    CorrelationId,
    Money,
    OrderId,
    OwnerId,
    PetId,
    ServiceOffer,
    SitterId,
    TimeInterval,
)
from tests.domain.value_objects.address.factories import AddressFactory
from tests.domain.value_objects.service.factories import ServiceOfferFactory
from tests.domain.value_objects.time_interval.factories import (
    BASE_MOMENT,
    TimeIntervalFactory,
)

PLACED_AT = BASE_MOMENT - timedelta(days=1)
TOTAL = Money(1500)


class PlaceArguments(TypedDict):
    """Именованные аргументы ``Order.place``."""

    order_id: OrderId
    owner_id: OwnerId
    sitter_id: SitterId
    pet_id: PetId
    offer: ServiceOffer
    interval: TimeInterval
    address: Address
    occurred_at: datetime
    correlation_id: CorrelationId


class OrderFactory(factory.Factory):
    """Заказ на передержку, оформленный за сутки до начала услуги."""

    class Meta:
        model = Order

    order_id = factory.LazyFunction(OrderId.new)
    owner_id = factory.LazyFunction(OwnerId.new)
    sitter_id = factory.LazyFunction(SitterId.new)
    pet_id = factory.LazyFunction(PetId.new)
    offer = factory.SubFactory(ServiceOfferFactory)
    interval = factory.SubFactory(TimeIntervalFactory)
    address = factory.SubFactory(AddressFactory)
    occurred_at = PLACED_AT
    correlation_id = factory.LazyFunction(CorrelationId.new)

    @classmethod
    def _create(
        cls, model_class: type[Order], **kwargs: Unpack[PlaceArguments]
    ) -> Order:
        """Заказ рождается фабричным методом агрегата, а не конструктором."""
        return model_class.place(**kwargs)
