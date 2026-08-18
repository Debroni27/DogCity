"""Тесты состояния учётной записи."""

import pytest

from src.domain.value_objects import AccountStatus


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (AccountStatus.ACTIVE, "active"),
        (AccountStatus.BLOCKED, "blocked"),
        (AccountStatus.DELETED, "deleted"),
    ],
)
def test_wire_value_is_stable(status: AccountStatus, expected: str) -> None:
    """Значение зафиксировано контрактом: переименование ломает совместимость."""
    assert status.value == expected


def test_unknown_status_is_rejected() -> None:
    """Множество состояний закрыто: значения вне перечисления недопустимы."""
    with pytest.raises(ValueError, match="suspended"):
        AccountStatus("suspended")
