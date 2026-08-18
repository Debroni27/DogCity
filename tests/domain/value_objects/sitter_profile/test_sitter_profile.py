"""Тесты статуса проверки документов догситтера."""

import pytest

from src.domain.value_objects import VerificationStatus


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (VerificationStatus.NOT_VERIFIED, "not_verified"),
        (VerificationStatus.PENDING, "pending"),
        (VerificationStatus.VERIFIED, "verified"),
        (VerificationStatus.REJECTED, "rejected"),
    ],
)
def test_status_value_is_stable(status: VerificationStatus, expected: str) -> None:
    """Значение зафиксировано контрактом: переименование ломает совместимость."""
    assert status.value == expected


def test_unknown_status_is_rejected() -> None:
    """Множество статусов проверки закрыто: значения вне перечисления недопустимы."""
    with pytest.raises(ValueError, match="expired"):
        VerificationStatus("expired")
