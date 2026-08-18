"""Сторона заказа."""

from enum import StrEnum

__all__ = ("OrderParty",)


class OrderParty(StrEnum):
    """Сторона заказа: кто из двух участников совершил действие."""

    OWNER = "owner"
    """Владелец питомца."""

    SITTER = "sitter"
    """Догситтер."""
