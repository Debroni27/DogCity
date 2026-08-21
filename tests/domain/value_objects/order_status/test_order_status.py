"""Тесты статусов заказа и причин его прекращения."""

import pytest

from src.domain.value_objects import CancellationReason, OrderStatus, RejectionReason


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (OrderStatus.PENDING, "pending"),
        (OrderStatus.CONFIRMED, "confirmed"),
        (OrderStatus.REJECTED, "rejected"),
        (OrderStatus.CANCELLED, "cancelled"),
        (OrderStatus.IN_PROGRESS, "in_progress"),
        (OrderStatus.COMPLETED, "completed"),
    ],
)
def test_status_value_is_stable(status: OrderStatus, expected: str) -> None:
    """Значение зафиксировано контрактом: переименование ломает совместимость."""
    assert status.value == expected


def test_reason_types_are_separated_only_by_typing() -> None:
    """StrEnum сравнивается как строка, поэтому причины разделяет лишь mypy."""
    assert RejectionReason.OTHER == CancellationReason.OTHER
    assert RejectionReason.OTHER is not CancellationReason.OTHER
