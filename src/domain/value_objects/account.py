"""Состояние учётной записи участника и причины её блокировки."""

from enum import StrEnum

__all__ = ("AccountStatus", "BlockReason")


class AccountStatus(StrEnum):
    """Состояние учётной записи."""

    ACTIVE = "active"
    """Учётная запись доступна, участник работает с сервисом."""

    BLOCKED = "blocked"
    """Заблокирована администратором. Новые заказы недоступны."""

    DELETED = "deleted"
    """Удалена по запросу участника: данные обезличены, история заказов цела."""


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
