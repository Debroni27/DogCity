"""Тесты состояния учётной записи."""

import pytest

from src.domain.value_objects import (
    AccountStatus,
    BlockReason,
    VerificationRejectionReason,
    VerificationStatus,
)


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


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (VerificationStatus.NOT_VERIFIED, "not_verified"),
        (VerificationStatus.PENDING, "pending"),
        (VerificationStatus.VERIFIED, "verified"),
        (VerificationStatus.REJECTED, "rejected"),
    ],
)
def test_verification_status_value_is_stable(
    status: VerificationStatus, expected: str
) -> None:
    """Значение зафиксировано контрактом: переименование ломает совместимость."""
    assert status.value == expected


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


@pytest.mark.parametrize(
    ("reason", "expected"),
    [
        (VerificationRejectionReason.DOCUMENTS_UNREADABLE, "documents_unreadable"),
        (VerificationRejectionReason.DATA_MISMATCH, "data_mismatch"),
        (VerificationRejectionReason.DOCUMENT_EXPIRED, "document_expired"),
        (VerificationRejectionReason.WRONG_DOCUMENT_TYPE, "wrong_document_type"),
    ],
)
def test_verification_rejection_value_is_stable(
    reason: VerificationRejectionReason, expected: str
) -> None:
    """Значение зафиксировано контрактом: переименование ломает совместимость."""
    assert reason.value == expected
