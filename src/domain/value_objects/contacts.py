"""Контактные данные участников: имя, телефон, email."""

from dataclasses import dataclass

from src.domain.exceptions import ValidationError

__all__ = (
    "Email",
    "PersonName",
    "PhoneNumber",
)

NAME_MAX_LENGTH = 100
EMAIL_MAX_LENGTH = 254
PHONE_MIN_DIGITS = 8
PHONE_MAX_DIGITS = 15


@dataclass(frozen=True, slots=True)
class PersonName:
    """ФИО участника. Отчество опционально."""

    last_name: str
    first_name: str
    middle_name: str | None = None

    def __post_init__(self) -> None:
        if len(self.last_name) > NAME_MAX_LENGTH:
            raise ValidationError("last_name", f"длиннее {NAME_MAX_LENGTH} символов")
        if len(self.first_name) > NAME_MAX_LENGTH:
            raise ValidationError("first_name", f"длиннее {NAME_MAX_LENGTH} символов")
        if self.middle_name is not None and len(self.middle_name) > NAME_MAX_LENGTH:
            raise ValidationError("middle_name", f"длиннее {NAME_MAX_LENGTH} символов")


@dataclass(frozen=True, slots=True)
class PhoneNumber:
    """Номер телефона в формате E.164, например ``+79991234567``."""

    value: str

    def __post_init__(self) -> None:
        if not self.value.startswith("+"):
            raise ValidationError("value", "должен начинаться с +")
        digits = self.value[1:]
        if not (digits.isascii() and digits.isdigit()):
            raise ValidationError("value", "после + допустимы только цифры")
        if not PHONE_MIN_DIGITS <= len(digits) <= PHONE_MAX_DIGITS:
            raise ValidationError("value", "неверное количество цифр")


@dataclass(frozen=True, slots=True)
class Email:
    """Адрес электронной почты в нижнем регистре."""

    value: str

    def __post_init__(self) -> None:
        if len(self.value) > EMAIL_MAX_LENGTH:
            raise ValidationError(
                "value", f"длиннее {EMAIL_MAX_LENGTH} символов"
            )
        local, separator, host = self.value.partition("@")
        if not separator or not local or "." not in host:
            raise ValidationError(
                "value", "не похож на адрес электронной почты"
            )
