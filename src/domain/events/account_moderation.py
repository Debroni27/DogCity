"""События модерации учётной записи."""

from dataclasses import dataclass

from src.domain.events.base import DomainEvent
from src.domain.value_objects import (
    AdminId,
    BlockReason,
    OwnerId,
    SitterId,
    VerificationRejectionReason,
)

__all__ = (
    "AccountBlocked",
    "AccountDeleted",
    "AccountModerationEvent",
    "AccountUnblocked",
    "AccountVerified",
    "DocumentsSubmitted",
    "ModerationOpened",
    "VerificationRejected",
)


@dataclass(frozen=True, slots=True)
class ModerationOpened(DomainEvent):
    """Заведена модерационная запись для нового участника."""

    account_id: OwnerId | SitterId


@dataclass(frozen=True, slots=True)
class DocumentsSubmitted(DomainEvent):
    """Участник подал документы на проверку."""

    account_id: OwnerId | SitterId


@dataclass(frozen=True, slots=True)
class AccountVerified(DomainEvent):
    """Администратор подтвердил документы."""

    account_id: OwnerId | SitterId
    admin_id: AdminId


@dataclass(frozen=True, slots=True)
class VerificationRejected(DomainEvent):
    """Администратор отклонил документы, подать их можно повторно."""

    account_id: OwnerId | SitterId
    admin_id: AdminId
    reason: VerificationRejectionReason


@dataclass(frozen=True, slots=True)
class AccountBlocked(DomainEvent):
    """Администратор заблокировал учётную запись."""

    account_id: OwnerId | SitterId
    admin_id: AdminId
    reason: BlockReason


@dataclass(frozen=True, slots=True)
class AccountUnblocked(DomainEvent):
    """Администратор снял блокировку."""

    account_id: OwnerId | SitterId
    admin_id: AdminId


@dataclass(frozen=True, slots=True)
class AccountDeleted(DomainEvent):
    """Участник удалил учётную запись, данные обезличены."""

    account_id: OwnerId | SitterId


type AccountModerationEvent = (
    AccountBlocked
    | AccountDeleted
    | AccountUnblocked
    | AccountVerified
    | DocumentsSubmitted
    | ModerationOpened
    | VerificationRejected
)
"""Любое событие модерации учётной записи."""
