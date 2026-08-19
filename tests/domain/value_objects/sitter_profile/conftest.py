"""Фикстуры ограничений догситтера."""

import pytest

from src.domain.value_objects import AcceptedDogSizes
from tests.domain.value_objects.sitter_profile.factories import AcceptedDogSizesFactory


@pytest.fixture
def accepted_dog_sizes() -> AcceptedDogSizes:
    """Догситтер, берущий мелких и средних собак."""
    return AcceptedDogSizesFactory()
