"""Фикстуры адресов."""

import pytest

from src.domain.value_objects import Address
from tests.domain.value_objects.address.factories import AddressFactory


@pytest.fixture
def address() -> Address:
    """Адрес, построенный фабрикой со значениями по умолчанию."""
    return AddressFactory()
