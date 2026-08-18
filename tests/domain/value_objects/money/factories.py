"""Фабрики денежных сумм."""

import factory

from src.domain.value_objects import Money


class MoneyFactory(factory.Factory):
    """Положительная сумма в целых рублях."""

    class Meta:
        model = Money

    amount = factory.Faker("random_int", min=100, max=10_000)
