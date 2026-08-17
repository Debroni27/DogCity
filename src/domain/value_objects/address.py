"""Адрес места оказания услуги.

Хранится структурой, а не одной строкой: город нужен отдельным полем для
фильтрации предложений. Координат нет — подбор ситтера по близости в MVP
не поддерживается, см. ``docs/dev/memory_bank.md``.
"""

from dataclasses import dataclass

__all__ = ("Address",)


@dataclass(frozen=True, slots=True)
class Address:
    """Почтовый адрес."""

    city: str
    street: str
    building: str
    apartment: str | None = None
