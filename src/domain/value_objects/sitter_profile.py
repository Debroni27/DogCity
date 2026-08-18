"""Профиль догситтера: атрибуты, отличающие его от обычного участника."""

from enum import StrEnum

__all__ = ("VerificationStatus",)


class VerificationStatus(StrEnum):
    """Результат проверки документов догситтера администратором."""

    NOT_VERIFIED = "not_verified"
    """Документы не поданы."""

    PENDING = "pending"
    """Документы поданы, ожидают проверки."""

    VERIFIED = "verified"
    """Проверка пройдена."""

    REJECTED = "rejected"
    """Проверка не пройдена. Документы можно подать повторно."""
