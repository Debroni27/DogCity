"""Агрегат модерации учётной записи участника."""

from datetime import datetime

from src.domain.events import (
    AccountBlocked,
    AccountDeleted,
    AccountModerationEvent,
    AccountUnblocked,
    AccountVerified,
    DocumentsSubmitted,
    ModerationOpened,
    VerificationRejected,
)
from src.domain.exceptions import IllegalStateTransitionError
from src.domain.value_objects import (
    AccountStatus,
    AdminId,
    BlockReason,
    CorrelationId,
    EventId,
    OwnerId,
    SitterId,
    VerificationRejectionReason,
    VerificationStatus,
)

__all__ = ("AccountModeration",)


class AccountModeration:
    """Модерационное состояние участника: доступ к сервису и проверка документов."""

    __slots__ = (
        "_account_id",
        "_account_status",
        "_pending_events",
        "_verification_status",
    )

    _account_id: OwnerId | SitterId
    _account_status: AccountStatus
    _verification_status: VerificationStatus
    _pending_events: list[AccountModerationEvent]

    def __init__(self) -> None:
        """Заготовка записи: состояние наполняет ``_apply``."""
        self._pending_events = []

    @property
    def account_id(self) -> OwnerId | SitterId:
        """Участник, к которому относится запись."""
        return self._account_id

    @property
    def account_status(self) -> AccountStatus:
        """Доступ участника к сервису."""
        return self._account_status

    @property
    def verification_status(self) -> VerificationStatus:
        """Результат проверки документов участника."""
        return self._verification_status

    @property
    def pending_events(self) -> tuple[AccountModerationEvent, ...]:
        """События, накопленные с последнего ``clear_events``."""
        return tuple(self._pending_events)

    @classmethod
    def open(
        cls,
        *,
        account_id: OwnerId | SitterId,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> "AccountModeration":
        """Завести модерационную запись новому участнику."""
        moderation = cls()
        moderation._record(
            ModerationOpened(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                account_id=account_id,
            )
        )
        return moderation

    def clear_events(self) -> None:
        """Забыть накопленные события: их забрал прикладной слой."""
        self._pending_events.clear()

    def submit_documents(
        self, occurred_at: datetime, correlation_id: CorrelationId
    ) -> None:
        """Участник подаёт документы на проверку."""
        self._ensure_alive("submit_documents")
        self._ensure_verification(
            (VerificationStatus.NOT_VERIFIED, VerificationStatus.REJECTED),
            "submit_documents",
        )
        self._record(
            DocumentsSubmitted(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                account_id=self._account_id,
            )
        )

    def verify(
        self, admin_id: AdminId, occurred_at: datetime, correlation_id: CorrelationId
    ) -> None:
        """Администратор подтверждает поданные документы."""
        self._ensure_alive("verify")
        self._ensure_verification((VerificationStatus.PENDING,), "verify")
        self._record(
            AccountVerified(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                account_id=self._account_id,
                admin_id=admin_id,
            )
        )

    def reject_verification(
        self,
        admin_id: AdminId,
        reason: VerificationRejectionReason,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> None:
        """Администратор отклоняет документы, подать их можно заново."""
        self._ensure_alive("reject_verification")
        self._ensure_verification((VerificationStatus.PENDING,), "reject_verification")
        self._record(
            VerificationRejected(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                account_id=self._account_id,
                admin_id=admin_id,
                reason=reason,
            )
        )

    def block(
        self,
        admin_id: AdminId,
        reason: BlockReason,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> None:
        """Администратор блокирует учётную запись."""
        self._ensure_account((AccountStatus.ACTIVE,), "block")
        self._record(
            AccountBlocked(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                account_id=self._account_id,
                admin_id=admin_id,
                reason=reason,
            )
        )

    def unblock(
        self, admin_id: AdminId, occurred_at: datetime, correlation_id: CorrelationId
    ) -> None:
        """Администратор снимает блокировку."""
        self._ensure_account((AccountStatus.BLOCKED,), "unblock")
        self._record(
            AccountUnblocked(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                account_id=self._account_id,
                admin_id=admin_id,
            )
        )

    def delete(self, occurred_at: datetime, correlation_id: CorrelationId) -> None:
        """Участник удаляет учётную запись, данные обезличиваются."""
        self._ensure_account(
            (AccountStatus.ACTIVE, AccountStatus.BLOCKED), "delete"
        )
        self._record(
            AccountDeleted(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                account_id=self._account_id,
            )
        )

    def _ensure_alive(self, transition: str) -> None:
        """Над удалённой учётной записью не совершают действий."""
        if self._account_status is AccountStatus.DELETED:
            raise IllegalStateTransitionError(
                "AccountModeration", self._account_status, transition
            )

    def _ensure_account(
        self, allowed: tuple[AccountStatus, ...], transition: str
    ) -> None:
        """Пропустить переход только из перечисленных состояний доступа."""
        if self._account_status not in allowed:
            raise IllegalStateTransitionError(
                "AccountModeration", self._account_status, transition
            )

    def _ensure_verification(
        self, allowed: tuple[VerificationStatus, ...], transition: str
    ) -> None:
        """Пропустить переход только из перечисленных состояний проверки."""
        if self._verification_status not in allowed:
            raise IllegalStateTransitionError(
                "AccountModeration", self._verification_status, transition
            )

    def _record(self, event: AccountModerationEvent) -> None:
        """Применить событие и запомнить его для публикации."""
        self._apply(event)
        self._pending_events.append(event)

    def _apply(self, event: AccountModerationEvent) -> None:
        """Единственное место, где меняется модерационное состояние."""
        match event:
            case ModerationOpened():
                self._account_id = event.account_id
                self._account_status = AccountStatus.ACTIVE
                self._verification_status = VerificationStatus.NOT_VERIFIED
            case DocumentsSubmitted():
                self._verification_status = VerificationStatus.PENDING
            case AccountVerified():
                self._verification_status = VerificationStatus.VERIFIED
            case VerificationRejected():
                self._verification_status = VerificationStatus.REJECTED
            case AccountBlocked():
                self._account_status = AccountStatus.BLOCKED
            case AccountUnblocked():
                self._account_status = AccountStatus.ACTIVE
            case AccountDeleted():
                self._account_status = AccountStatus.DELETED
