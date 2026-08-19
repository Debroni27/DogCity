"""Тесты агрегата модерации учётной записи."""

import pytest

from src.domain.aggregates import AccountModeration
from src.domain.events import AccountDeleted, ModerationOpened
from src.domain.exceptions import IllegalStateTransitionError
from src.domain.value_objects import (
    AccountStatus,
    AdminId,
    BlockReason,
    CorrelationId,
    OwnerId,
    VerificationRejectionReason,
    VerificationStatus,
)
from tests.domain.events.factories import OCCURRED_AT

REJECTION = VerificationRejectionReason.DOCUMENTS_UNREADABLE
BLOCKING = BlockReason.ANIMAL_MISTREATMENT


def test_opened_record_is_active_and_unverified(moderation: AccountModeration) -> None:
    """Новый участник допущен к сервису, но документов ещё не подавал."""
    (event,) = moderation.pending_events
    assert isinstance(event, ModerationOpened)
    assert moderation.account_id == event.account_id
    assert moderation.account_status is AccountStatus.ACTIVE
    assert moderation.verification_status is VerificationStatus.NOT_VERIFIED


def test_owner_is_moderated_by_the_same_record() -> None:
    """Логика модерации одинакова для владельца и догситтера."""
    moderation = AccountModeration.open(
        account_id=OwnerId.new(),
        occurred_at=OCCURRED_AT,
        correlation_id=CorrelationId.new(),
    )
    assert moderation.account_status is AccountStatus.ACTIVE


def test_submitted_documents_await_review(
    pending_moderation: AccountModeration,
) -> None:
    """Поданные документы ждут решения администратора."""
    assert pending_moderation.verification_status is VerificationStatus.PENDING


def test_verification_passes(
    pending_moderation: AccountModeration, admin_id: AdminId
) -> None:
    """Подтверждённые документы переводят участника в VERIFIED."""
    pending_moderation.verify(admin_id, OCCURRED_AT, CorrelationId.new())
    assert pending_moderation.verification_status is VerificationStatus.VERIFIED


def test_rejected_documents_can_be_submitted_again(
    pending_moderation: AccountModeration, admin_id: AdminId
) -> None:
    """Отказ в верификации не окончателен: документы подают повторно."""
    pending_moderation.reject_verification(
        admin_id, REJECTION, OCCURRED_AT, CorrelationId.new()
    )
    assert pending_moderation.verification_status is VerificationStatus.REJECTED
    pending_moderation.submit_documents(OCCURRED_AT, CorrelationId.new())
    assert pending_moderation.verification_status is VerificationStatus.PENDING


def test_documents_cannot_be_submitted_twice(
    pending_moderation: AccountModeration,
) -> None:
    """Пока документы на проверке, подать их заново нельзя."""
    with pytest.raises(IllegalStateTransitionError):
        pending_moderation.submit_documents(OCCURRED_AT, CorrelationId.new())


def test_unsubmitted_documents_cannot_be_verified(
    moderation: AccountModeration, admin_id: AdminId
) -> None:
    """Подтверждать нечего, пока документы не поданы."""
    with pytest.raises(IllegalStateTransitionError) as exc:
        moderation.verify(admin_id, OCCURRED_AT, CorrelationId.new())
    assert exc.value.transition == "verify"


def test_blocking_closes_access(
    moderation: AccountModeration, admin_id: AdminId
) -> None:
    """Блокировка закрывает участнику доступ к сервису."""
    moderation.block(admin_id, BLOCKING, OCCURRED_AT, CorrelationId.new())
    assert moderation.account_status is AccountStatus.BLOCKED


def test_blocked_account_cannot_be_blocked_again(
    moderation: AccountModeration, admin_id: AdminId
) -> None:
    """Повторная блокировка недопустима."""
    moderation.block(admin_id, BLOCKING, OCCURRED_AT, CorrelationId.new())
    with pytest.raises(IllegalStateTransitionError):
        moderation.block(admin_id, BLOCKING, OCCURRED_AT, CorrelationId.new())


def test_unblocking_returns_access(
    moderation: AccountModeration, admin_id: AdminId
) -> None:
    """Снятая блокировка возвращает участника к работе."""
    moderation.block(admin_id, BLOCKING, OCCURRED_AT, CorrelationId.new())
    moderation.unblock(admin_id, OCCURRED_AT, CorrelationId.new())
    assert moderation.account_status is AccountStatus.ACTIVE


def test_active_account_cannot_be_unblocked(
    moderation: AccountModeration, admin_id: AdminId
) -> None:
    """Снимать нечего, если блокировки не было."""
    with pytest.raises(IllegalStateTransitionError):
        moderation.unblock(admin_id, OCCURRED_AT, CorrelationId.new())


def test_blocked_account_can_still_be_deleted(
    moderation: AccountModeration, admin_id: AdminId
) -> None:
    """Блокировка не запирает участника в сервисе навсегда."""
    moderation.block(admin_id, BLOCKING, OCCURRED_AT, CorrelationId.new())
    moderation.delete(OCCURRED_AT, CorrelationId.new())
    assert moderation.account_status is AccountStatus.DELETED


def test_deletion_is_recorded(deleted_moderation: AccountModeration) -> None:
    """Удаление учётной записи оставляет след в потоке событий."""
    assert isinstance(deleted_moderation.pending_events[-1], AccountDeleted)


def test_deleted_account_accepts_no_moderation(
    deleted_moderation: AccountModeration, admin_id: AdminId
) -> None:
    """Над удалённой учётной записью не совершают действий."""
    with pytest.raises(IllegalStateTransitionError):
        deleted_moderation.block(admin_id, BLOCKING, OCCURRED_AT, CorrelationId.new())


def test_deleted_account_accepts_no_documents(
    deleted_moderation: AccountModeration,
) -> None:
    """Удалённая учётная запись не подаёт документы на проверку."""
    with pytest.raises(IllegalStateTransitionError):
        deleted_moderation.submit_documents(OCCURRED_AT, CorrelationId.new())


def test_deleted_account_cannot_be_deleted_twice(
    deleted_moderation: AccountModeration,
) -> None:
    """Удаление терминально."""
    with pytest.raises(IllegalStateTransitionError):
        deleted_moderation.delete(OCCURRED_AT, CorrelationId.new())


def test_events_are_forgotten_once_taken(moderation: AccountModeration) -> None:
    """После выгрузки прикладным слоем агрегат событий не хранит."""
    moderation.clear_events()
    assert moderation.pending_events == ()
