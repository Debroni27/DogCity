"""Тесты почтового адреса."""

import pytest

from src.domain.exceptions import ValidationError
from src.domain.value_objects import (
    BUILDING_MAX_LENGTH,
    CITY_MAX_LENGTH,
    STREET_MAX_LENGTH,
    Address,
)
from tests.domain.value_objects.address.factories import AddressFactory

LIMITS = [
    ("city", CITY_MAX_LENGTH),
    ("street", STREET_MAX_LENGTH),
    ("building", BUILDING_MAX_LENGTH),
    ("apartment", BUILDING_MAX_LENGTH),
]


def test_apartment_is_optional(address: Address) -> None:
    """Квартира не обязательна: у частного дома её нет."""
    assert address.apartment is None


def test_building_may_contain_letters() -> None:
    """Дом — строка, а не число: корпуса и строения вида «12к3» допустимы."""
    assert AddressFactory(building="12к3").building == "12к3"


@pytest.mark.parametrize(("field", "limit"), LIMITS)
def test_field_longer_than_limit_is_rejected(field: str, limit: int) -> None:
    """Превышение длины отвергается с указанием конкретного поля."""
    with pytest.raises(ValidationError) as exc:
        AddressFactory(**{field: "а" * (limit + 1)})
    assert exc.value.field == field


@pytest.mark.parametrize(("field", "limit"), LIMITS)
def test_field_at_limit_is_accepted(field: str, limit: int) -> None:
    """Граница длины включительна."""
    assert AddressFactory(**{field: "а" * limit})
