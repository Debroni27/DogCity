"""Фабрики оценок догситтера."""

import factory

from src.domain.value_objects import RATING_MAX, AggregatedRating, Rating


class RatingFactory(factory.Factory):
    """Оценка в допустимом диапазоне."""

    class Meta:
        model = Rating

    value = RATING_MAX


class AggregatedRatingFactory(factory.Factory):
    """Сводная оценка, согласованная с числом отзывов."""

    class Meta:
        model = AggregatedRating

    reviews_count = 2
    ratings_sum = factory.LazyAttribute(lambda o: RATING_MAX * o.reviews_count)
