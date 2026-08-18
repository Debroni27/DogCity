"""Тесты состояния учётной записи."""

import pytest

from src.domain.value_objects import AccountStatus, BlockReason


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


@pytest.mark.parametrize(
    ("reason", "expected"),
    [
        (BlockReason.ANIMAL_MISTREATMENT, "animal_mistreatment"),
        (BlockReason.FRAUD, "fraud"),
        (BlockReason.FAKE_DOCUMENTS, "fake_documents"),
        (BlockReason.ABUSIVE_BEHAVIOR, "abusive_behavior"),
        (BlockReason.REPEATED_CANCELLATIONS, "repeated_cancellations"),
    ],
)
def test_block_reason_value_is_stable(reason: BlockReason, expected: str) -> None:
    """Значение зафиксировано контрактом: переименование ломает совместимость."""
    assert reason.value == expected


def test_unknown_block_reason_is_rejected() -> None:
    """Множество причин закрыто: блокировать можно только по названной причине."""
    with pytest.raises(ValueError, match="other"):
        BlockReason("other")
