"""Адрес места оказания услуги."""

from dataclasses import dataclass

__all__ = ("Address",)


@dataclass(frozen=True, slots=True)
class Address:
    """Почтовый адрес."""

    city: str
    street: str
    building: str
    apartment: str | None = None
