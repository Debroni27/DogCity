"""Фикстуры владельцев питомцев."""

import pytest

from src.domain.aggregates import Owner
from tests.domain.aggregates.owner.factories import OwnerFactory


@pytest.fixture
def owner() -> Owner:
    """Владелец, ещё не заведший ни одного питомца."""
    return OwnerFactory()
