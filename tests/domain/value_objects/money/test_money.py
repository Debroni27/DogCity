"""Тесты денежных сумм."""

import pytest

from src.domain.exceptions import ValidationError
from src.domain.value_objects import Currency, Money


def test_currency_is_always_rubles(price: Money) -> None:
    """Валюта всегда рубль — других в домене не существует."""
    assert price.currency is Currency.RUB


def test_currency_is_not_accepted_by_constructor() -> None:
    """Валюту нельзя передать в конструктор: поле объявлено как init=False."""
    with pytest.raises(TypeError, match="positional"):
        Money(100, Currency.RUB)


def test_zero_is_allowed() -> None:
    """Нулевая сумма допустима: запрещены только отрицательные."""
    assert Money(0).amount == 0


def test_negative_amount_is_rejected() -> None:
    """Отрицательная сумма отвергается с указанием поля."""
    with pytest.raises(ValidationError) as exc:
        Money(-1)
    assert exc.value.field == "amount"


@pytest.mark.parametrize(
    ("units", "expected"),
    [(0, 0), (1, 450), (3, 1_350), (100, 45_000)],
)
def test_multiplication_scales_amount(price: Money, units: int, expected: int) -> None:
    """Умножение на число единиц масштабирует сумму."""
    assert (price * units).amount == expected


def test_multiplication_by_negative_is_rejected(price: Money) -> None:
    """Отрицательный множитель ловится валидацией конструктора."""
    with pytest.raises(ValidationError):
        _ = price * -1
