"""Контактные данные участников: имя, телефон, email."""

from dataclasses import dataclass

__all__ = (
    "Email",
    "PersonName",
    "PhoneNumber",
)


@dataclass(frozen=True, slots=True)
class PersonName:
    """ФИО участника. Отчество опционально."""

    last_name: str
    first_name: str
    middle_name: str | None = None


@dataclass(frozen=True, slots=True)
class PhoneNumber:
    """Номер телефона в формате E.164, например ``+79991234567``."""

    value: str


@dataclass(frozen=True, slots=True)
class Email:
    """Адрес электронной почты в нижнем регистре."""

    value: str
