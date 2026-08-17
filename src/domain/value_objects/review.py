"""Содержимое отзыва о догситтере."""

from dataclasses import dataclass

__all__ = ("ReviewText",)

REVIEW_TEXT_MAX_LENGTH = 2000


@dataclass(frozen=True, slots=True)
class ReviewText:
    """Текст отзыва длиной не более ``REVIEW_TEXT_MAX_LENGTH`` символов."""

    value: str
