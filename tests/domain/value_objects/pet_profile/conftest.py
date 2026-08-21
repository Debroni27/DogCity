"""Фикстуры характеристик питомца."""

import pytest

from src.domain.value_objects import BirthDate
from tests.domain.value_objects.pet_profile.factories import BirthDateFactory


@pytest.fixture
def birth_date() -> BirthDate:
    """Дата рождения взрослой собаки."""
    return BirthDateFactory()
