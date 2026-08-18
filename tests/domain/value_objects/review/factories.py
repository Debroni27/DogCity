"""Фабрики текста отзыва."""

import factory

from src.domain.value_objects import ReviewText


class ReviewTextFactory(factory.Factory):
    """Текст отзыва в пределах ограничения длины."""

    class Meta:
        model = ReviewText

    value = factory.Faker("text", max_nb_chars=200)
