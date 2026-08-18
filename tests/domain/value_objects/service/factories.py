"""Фабрики предложений догситтера."""

import factory

from src.domain.value_objects import ServiceOffer, ServiceType, Tarification
from tests.domain.value_objects.money.factories import MoneyFactory


class ServiceOfferFactory(factory.Factory):
    """Передержка с посуточной тарификацией — допустимая пара по умолчанию."""

    class Meta:
        model = ServiceOffer

    service_type = ServiceType.BOARDING
    price = factory.SubFactory(MoneyFactory)
    tarification = Tarification.PER_DAY
