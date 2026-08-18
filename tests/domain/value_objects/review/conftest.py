"""Фикстуры текста отзыва."""

import pytest

from src.domain.value_objects import ReviewText
from tests.domain.value_objects.review.factories import ReviewTextFactory


@pytest.fixture
def review_text() -> ReviewText:
    """Текст отзыва со значением по умолчанию."""
    return ReviewTextFactory()
