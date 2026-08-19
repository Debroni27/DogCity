"""Фикстуры догситтеров."""

import pytest

from src.domain.aggregates import Sitter
from tests.domain.aggregates.sitter.factories import SitterFactory


@pytest.fixture
def sitter() -> Sitter:
    """Догситтер на двух собак, предложений ещё не выставил."""
    return SitterFactory()
