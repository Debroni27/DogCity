"""Тесты оценки догситтера и её агрегата."""

from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from src.domain.exceptions import ValidationError
from src.domain.value_objects import (
    RATING_MAX,
    RATING_MIN,
    AggregatedRating,
    Rating,
)
from tests.domain.value_objects.rating.factories import (
    AggregatedRatingFactory,
    RatingFactory,
)


@pytest.mark.parametrize("value", [RATING_MIN, RATING_MAX])
def test_rating_at_boundary_is_accepted(value: int) -> None:
    """Границы шкалы включительны."""
    assert RatingFactory(value=value).value == value


@pytest.mark.parametrize("value", [RATING_MIN - 1, RATING_MAX + 1])
def test_rating_outside_scale_is_rejected(value: int) -> None:
    """Оценка вне шкалы отвергается."""
    with pytest.raises(ValidationError):
        RatingFactory(value=value)


def test_empty_has_no_average(empty_rating: AggregatedRating) -> None:
    """Отсутствие оценок — не нулевая оценка, поэтому None."""
    assert empty_rating.average is None


def test_average_is_computed_from_sum() -> None:
    """Среднее считается от суммы, а не накапливается от предыдущего среднего."""
    aggregated = AggregatedRatingFactory(reviews_count=2, ratings_sum=9)
    assert aggregated.average == Decimal("4.5")


def test_with_review_accumulates(empty_rating: AggregatedRating) -> None:
    """Каждый отзыв увеличивает и сумму, и счётчик."""
    aggregated = empty_rating.with_review(Rating(5)).with_review(Rating(4))
    assert (aggregated.ratings_sum, aggregated.reviews_count) == (9, 2)


def test_negative_reviews_count_is_rejected() -> None:
    """Отрицательное число отзывов невозможно."""
    with pytest.raises(ValidationError) as exc:
        AggregatedRatingFactory(reviews_count=-1, ratings_sum=0)
    assert exc.value.field == "reviews_count"


def test_sum_above_maximum_possible_is_rejected() -> None:
    """Сумма выше максимума для такого числа отзывов означает битые данные."""
    with pytest.raises(ValidationError) as exc:
        AggregatedRatingFactory(reviews_count=2, ratings_sum=RATING_MAX * 2 + 1)
    assert exc.value.field == "ratings_sum"


def test_sum_below_minimum_possible_is_rejected() -> None:
    """Сумма ниже минимума для такого числа отзывов означает битые данные."""
    with pytest.raises(ValidationError):
        AggregatedRatingFactory(reviews_count=2, ratings_sum=RATING_MIN * 2 - 1)


def test_sum_without_reviews_is_rejected() -> None:
    """При нуле отзывов границы схлопываются в ноль."""
    with pytest.raises(ValidationError):
        AggregatedRatingFactory(reviews_count=0, ratings_sum=5)


@given(
    ratings=st.lists(
        st.integers(min_value=RATING_MIN, max_value=RATING_MAX),
        min_size=1,
        max_size=50,
    )
)
def test_average_stays_within_scale(ratings: list[int]) -> None:
    """После любой последовательности отзывов среднее остаётся внутри шкалы."""
    aggregated = AggregatedRating.empty()
    for value in ratings:
        aggregated = aggregated.with_review(Rating(value))
    assert aggregated.average is not None
    assert RATING_MIN <= aggregated.average <= RATING_MAX
