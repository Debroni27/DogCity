"""Статус заказа.

Допустимый жизненный цикл::

    PENDING ──confirm──> CONFIRMED ──start──> IN_PROGRESS ──complete──> COMPLETED
       │                     │
       ├──reject──> REJECTED │
       └──cancel──> CANCELLED <──cancel──┘

``COMPLETED``, ``CANCELLED`` и ``REJECTED`` — терминальные. Проверка переходов
живёт в агрегате ``Order``, здесь — только перечисление состояний.
"""

from enum import StrEnum

__all__ = (
    "CancellationReason",
    "OrderStatus",
    "RejectionReason",
)


class OrderStatus(StrEnum):
    """Состояние заказа."""

    PENDING = "pending"
    """Оформлен владельцем, ожидает ответа ситтера."""

    CONFIRMED = "confirmed"
    """Ситтер принял заказ."""

    REJECTED = "rejected"
    """Ситтер отказался от заказа."""

    CANCELLED = "cancelled"
    """Отменён владельцем или ситтером до начала оказания услуги."""

    IN_PROGRESS = "in_progress"
    """Услуга оказывается прямо сейчас."""

    COMPLETED = "completed"
    """Услуга оказана."""


class RejectionReason(StrEnum):
    """Причина отказа ситтера от заказа — переход в ``REJECTED``."""

    SCHEDULE_CONFLICT = "schedule_conflict"
    """Время заказа занято другим заказом."""

    PET_NOT_SUITABLE = "pet_not_suitable"
    """Ситтер не работает с таким питомцем: размер, характер, состояние."""

    VACCINATION_MISSING = "vaccination_missing"
    """Нет действующей прививки, требуемой для услуги."""

    OTHER = "other"
    """Иная причина. Уточнение — в свободном комментарии заказа."""


class CancellationReason(StrEnum):
    """Причина отмены заказа — переход в ``CANCELLED``.

    Отделена от :class:`RejectionReason`: отказ возможен только до
    подтверждения и только со стороны ситтера, отмена — с обеих сторон
    и до начала оказания услуги. Инициатор фиксируется в событии отмены,
    здесь — только причина.
    """

    PLANS_CHANGED = "plans_changed"
    """Планы изменились."""

    PET_ILLNESS = "pet_illness"
    """Питомец заболел."""

    SITTER_UNAVAILABLE = "sitter_unavailable"
    """Ситтер не может оказать услугу после подтверждения."""

    TERMS_DISAGREEMENT = "terms_disagreement"
    """Стороны не договорились об условиях."""

    OTHER = "other"
    """Иная причина. Уточнение — в свободном комментарии заказа."""
