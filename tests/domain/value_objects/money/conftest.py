"""Фикстуры денежных сумм."""

import pytest

from src.domain.value_objects import Money

PRICE_AMOUNT = 450


@pytest.fixture
def price() -> Money:
    """Цена, от которой считаются проверки умножения."""
    return Money(PRICE_AMOUNT)
