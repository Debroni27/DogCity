"""Тесты контактных данных участников."""

import pytest

from src.domain.exceptions import ValidationError
from src.domain.value_objects import (
    EMAIL_MAX_LENGTH,
    NAME_MAX_LENGTH,
    PHONE_MAX_DIGITS,
    PHONE_MIN_DIGITS,
)
from tests.domain.value_objects.contacts.factories import (
    EmailFactory,
    PersonNameFactory,
    PhoneNumberFactory,
)


def test_middle_name_is_optional() -> None:
    """Отчество может отсутствовать."""
    assert PersonNameFactory(middle_name=None).middle_name is None


@pytest.mark.parametrize("field", ["last_name", "first_name", "middle_name"])
def test_name_longer_than_limit_is_rejected(field: str) -> None:
    """Превышение длины отвергается с указанием конкретного поля."""
    with pytest.raises(ValidationError) as exc:
        PersonNameFactory(**{field: "и" * (NAME_MAX_LENGTH + 1)})
    assert exc.value.field == field


def test_name_may_contain_hyphen_and_apostrophe() -> None:
    """Дефисы и апострофы допустимы: «Анна-Мария», «О'Коннор» — реальные имена."""
    name = PersonNameFactory(last_name="О'Коннор", first_name="Анна-Мария")
    assert name.last_name == "О'Коннор"


def test_phone_without_plus_is_rejected() -> None:
    """Без ведущего плюса номер не соответствует E.164."""
    with pytest.raises(ValidationError):
        PhoneNumberFactory(value="79991234567")


def test_phone_with_letters_is_rejected() -> None:
    """После плюса допустимы только цифры."""
    with pytest.raises(ValidationError):
        PhoneNumberFactory(value="+7999abc4567")


def test_phone_with_non_ascii_digits_is_rejected() -> None:
    """Юникодные цифры вроде арабо-индийских не проходят проверку isascii."""
    with pytest.raises(ValidationError):
        PhoneNumberFactory(value="+٧٩٩٩١٢٣٤٥٦٧")


@pytest.mark.parametrize("digits", [PHONE_MIN_DIGITS - 1, PHONE_MAX_DIGITS + 1])
def test_phone_with_wrong_digit_count_is_rejected(digits: int) -> None:
    """Число цифр вне диапазона E.164 отвергается."""
    with pytest.raises(ValidationError):
        PhoneNumberFactory(value="+" + "7" * digits)


@pytest.mark.parametrize("digits", [PHONE_MIN_DIGITS, PHONE_MAX_DIGITS])
def test_phone_at_digit_boundary_is_accepted(digits: int) -> None:
    """Границы диапазона цифр включительны."""
    assert PhoneNumberFactory(value="+" + "7" * digits)


@pytest.mark.parametrize(
    "value",
    ["userexample.com", "@example.com", "user@localhost", "user@"],
)
def test_malformed_email_is_rejected(value: str) -> None:
    """Адрес без собаки, без локальной части или без точки в домене отвергается."""
    with pytest.raises(ValidationError):
        EmailFactory(value=value)


def test_email_longer_than_limit_is_rejected() -> None:
    """Превышение длины отвергается раньше проверки формы."""
    with pytest.raises(ValidationError) as exc:
        EmailFactory(value="и" * (EMAIL_MAX_LENGTH + 1))
    assert exc.value.field == "value"


def test_email_is_not_normalised() -> None:
    """Регистр не приводится: нормализация — забота границы приложения."""
    assert EmailFactory(value="User@Example.com").value == "User@Example.com"
