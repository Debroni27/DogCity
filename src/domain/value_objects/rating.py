"""Оценка ситтера в отзыве и её агрегат по всем отзывам."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Self

__all__ = (
    "AggregatedRating",
    "Rating",
)

RATING_MIN = 1
RATING_MAX = 5


@dataclass(frozen=True, slots=True)
class Rating:
    """Оценка по шкале от ``RATING_MIN`` до ``RATING_MAX`` включительно."""

    value: int


@dataclass(frozen=True, slots=True)
class AggregatedRating:
    """Сводная оценка догситтера по всем его отзывам.

    Хранится сумма оценок, а не среднее: пересчёт среднего от среднего
    накапливает погрешность и не позволяет добавить отзыв, не зная всей
    истории.
    """

    ratings_sum: int
    reviews_count: int

    @classmethod
    def empty(cls) -> Self:
        """Сводная оценка ситтера без отзывов."""
        return cls(ratings_sum=0, reviews_count=0)

    @property
    def average(self) -> Decimal | None:
        """Средняя оценка или ``None``, если отзывов ещё нет.

        Отсутствие оценок — не то же самое, что нулевая оценка, поэтому
        ``None``, а не ``Decimal(0)``.
        """
        if self.reviews_count == 0:
            return None
        return Decimal(self.ratings_sum) / Decimal(self.reviews_count)

    def with_review(self, rating: Rating) -> "AggregatedRating":
        """Вернуть сводную оценку с учётом ещё одного отзыва.

        Исходный экземпляр не меняется: добавление отзыва — это новое
        значение, а не правка старого.
        """
        return AggregatedRating(
            ratings_sum=self.ratings_sum + rating.value,
            reviews_count=self.reviews_count + 1,
        )
