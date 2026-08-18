"""Фикстуры контактных данных."""

import pytest

from src.domain.value_objects import Email, PersonName, PhoneNumber
from tests.domain.value_objects.contacts.factories import (
    EmailFactory,
    PersonNameFactory,
    PhoneNumberFactory,
)


@pytest.fixture
def person_name() -> PersonName:
    """ФИО со значениями по умолчанию."""
    return PersonNameFactory()


@pytest.fixture
def phone_number() -> PhoneNumber:
    """Номер телефона в формате E.164."""
    return PhoneNumberFactory()


@pytest.fixture
def email() -> Email:
    """Адрес электронной почты."""
    return EmailFactory()
