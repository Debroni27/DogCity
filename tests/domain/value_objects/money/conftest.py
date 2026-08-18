"""Фикстуры денежных сумм."""

import pytest

from src.domain.value_objects import Money
from tests.domain.value_objects.money.factories import MoneyFactory

PRICE_AMOUNT = 450


@pytest.fixture
def price() -> Money:
    """Цена, от которой считаются проверки умножения."""
    return Money(PRICE_AMOUNT)


@pytest.fixture
def money() -> Money:
    """Сумма, построенная фабрикой."""
    return MoneyFactory()
