"""Свободный комментарий к заказу."""

from dataclasses import dataclass

from src.domain.exceptions import ValidationError

__all__ = ("ORDER_COMMENT_MAX_LENGTH", "OrderComment")

ORDER_COMMENT_MAX_LENGTH = 500


@dataclass(frozen=True, slots=True)
class OrderComment:
    """Уточнение к заказу: причина отказа или отмены своими словами."""

    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValidationError("value", "пустой: комментария нет — это None")
        if len(self.value) > ORDER_COMMENT_MAX_LENGTH:
            raise ValidationError(
                "value", f"длиннее {ORDER_COMMENT_MAX_LENGTH} символов"
            )
