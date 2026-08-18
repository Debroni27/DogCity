"""Состояние учётной записи участника и причины решений модерации."""

from enum import StrEnum

__all__ = (
    "AccountStatus",
    "BlockReason",
    "VerificationRejectionReason",
    "VerificationStatus",
)


class AccountStatus(StrEnum):
    """Состояние учётной записи."""

    ACTIVE = "active"
    """Учётная запись доступна, участник работает с сервисом."""

    BLOCKED = "blocked"
    """Заблокирована администратором. Новые заказы недоступны."""

    DELETED = "deleted"
    """Удалена по запросу участника: данные обезличены, история заказов цела."""


class VerificationStatus(StrEnum):
    """Результат проверки документов участника администратором."""

    NOT_VERIFIED = "not_verified"
    """Документы не поданы."""

    PENDING = "pending"
    """Документы поданы, ожидают проверки."""

    VERIFIED = "verified"
    """Проверка пройдена."""

    REJECTED = "rejected"
    """Проверка не пройдена. Документы можно подать повторно."""


class BlockReason(StrEnum):
    """Причина блокировки учётной записи администратором."""

    ANIMAL_MISTREATMENT = "animal_mistreatment"
    """Жестокое обращение с питомцем."""

    FRAUD = "fraud"
    """Мошенничество: обман контрагента или расчёты в обход сервиса."""

    FAKE_DOCUMENTS = "fake_documents"
    """Поданы поддельные документы."""

    ABUSIVE_BEHAVIOR = "abusive_behavior"
    """Оскорбления и грубость в адрес другой стороны."""

    REPEATED_CANCELLATIONS = "repeated_cancellations"
    """Систематические срывы подтверждённых заказов."""


class VerificationRejectionReason(StrEnum):
    """Причина отказа в верификации документов."""

    DOCUMENTS_UNREADABLE = "documents_unreadable"
    """Документы нечитаемы: плохое качество снимка или обрезанный кадр."""

    DATA_MISMATCH = "data_mismatch"
    """Данные в документах не совпадают с указанными в профиле."""

    DOCUMENT_EXPIRED = "document_expired"
    """Срок действия документа истёк."""

    WRONG_DOCUMENT_TYPE = "wrong_document_type"
    """Подан документ не того типа, который требуется."""
