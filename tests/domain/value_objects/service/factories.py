"""Фабрики предложений догситтера."""

import factory

from src.domain.value_objects import (
    ServiceFormat,
    ServiceOffer,
    ServiceType,
    Tarification,
)
from tests.domain.value_objects.money.factories import MoneyFactory


class ServiceOfferFactory(factory.Factory):
    """Групповая передержка с посуточной тарификацией — допустимая пара."""

    class Meta:
        model = ServiceOffer

    service_type = ServiceType.BOARDING
    price = factory.SubFactory(MoneyFactory)
    tarification = Tarification.PER_DAY
    service_format = ServiceFormat.SHARED
