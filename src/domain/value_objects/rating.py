"""Оценка ситтера в отзыве и её агрегат по всем отзывам."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Self

from src.domain.exceptions import ValidationError

__all__ = (
    "RATING_MAX",
    "RATING_MIN",
    "AggregatedRating",
    "Rating",
)

RATING_MIN = 1
RATING_MAX = 5


@dataclass(frozen=True, slots=True)
class Rating:
    """Оценка по шкале от ``RATING_MIN`` до ``RATING_MAX`` включительно."""

    value: int

    def __post_init__(self) -> None:
        if not RATING_MIN <= self.value <= RATING_MAX:
            raise ValidationError("value", f"вне диапазона {RATING_MIN}–{RATING_MAX}")


@dataclass(frozen=True, slots=True)
class AggregatedRating:
    """Сводная оценка по всем отзывам."""

    ratings_sum: int
    reviews_count: int

    def __post_init__(self) -> None:
        if self.reviews_count < 0:
            raise ValidationError("reviews_count", "не может быть отрицательным")
        lowest = RATING_MIN * self.reviews_count
        highest = RATING_MAX * self.reviews_count
        if not lowest <= self.ratings_sum <= highest:
            raise ValidationError("ratings_sum", "несовместима с числом отзывов")

    @classmethod
    def empty(cls) -> Self:
        """Сводная оценка без отзывов."""
        return cls(ratings_sum=0, reviews_count=0)

    @property
    def average(self) -> Decimal | None:
        """Средняя оценка или ``None``, если отзывов ещё нет."""
        if self.reviews_count == 0:
            return None
        return Decimal(self.ratings_sum) / Decimal(self.reviews_count)

    def with_review(self, rating: Rating) -> "AggregatedRating":
        """Вернуть сводную оценку с учётом ещё одного отзыва."""
        return AggregatedRating(
            ratings_sum=self.ratings_sum + rating.value,
            reviews_count=self.reviews_count + 1,
        )
