"""Содержимое отзыва о догситтере."""

from dataclasses import dataclass

from src.domain.exceptions import ValidationError

__all__ = ("REVIEW_TEXT_MAX_LENGTH", "ReviewText")

REVIEW_TEXT_MAX_LENGTH = 2000


@dataclass(frozen=True, slots=True)
class ReviewText:
    """Текст отзыва длиной не более ``REVIEW_TEXT_MAX_LENGTH`` символов."""

    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValidationError("value", "пустой: отзыв без текста не публикуется")
        if len(self.value) > REVIEW_TEXT_MAX_LENGTH:
            raise ValidationError("value", f"длиннее {REVIEW_TEXT_MAX_LENGTH} символов")
