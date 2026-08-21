"""Фикстуры отзывов."""

import pytest

from src.domain.aggregates import Review
from tests.domain.aggregates.review.factories import ReviewFactory


@pytest.fixture
def review() -> Review:
    """Отзыв владельца о догситтере за состоявшуюся услугу, с оценкой."""
    return ReviewFactory()
