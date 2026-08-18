"""Тесты стороны заказа."""

import pytest

from src.domain.value_objects import OrderParty


@pytest.mark.parametrize(
    ("party", "expected"),
    [
        (OrderParty.OWNER, "owner"),
        (OrderParty.SITTER, "sitter"),
    ],
)
def test_wire_value_is_stable(party: OrderParty, expected: str) -> None:
    """Значение зафиксировано контрактом: переименование ломает совместимость."""
    assert party.value == expected


def test_unknown_party_is_rejected() -> None:
    """Множество сторон закрыто: третьего участника у заказа нет."""
    with pytest.raises(ValueError, match="admin"):
        OrderParty("admin")
