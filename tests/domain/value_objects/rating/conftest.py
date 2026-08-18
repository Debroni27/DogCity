"""Фикстуры оценок догситтера."""

import pytest

from src.domain.value_objects import AggregatedRating


@pytest.fixture
def empty_rating() -> AggregatedRating:
    """Сводная оценка ситтера, у которого ещё нет отзывов."""
    return AggregatedRating.empty()
