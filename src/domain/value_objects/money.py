"""Денежные суммы."""

from dataclasses import dataclass, field
from enum import StrEnum

from src.domain.exceptions import ValidationError

__all__ = (
    "Currency",
    "Money",
)


class Currency(StrEnum):
    """Валюта расчётов. Единственный вариант — рубль."""

    RUB = "RUB"


@dataclass(frozen=True, slots=True)
class Money:
    """Денежная сумма в целых рублях."""

    amount: int
    currency: Currency = field(default=Currency.RUB, init=False)

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValidationError("amount", "не может быть отрицательной")

    def __mul__(self, units: int) -> "Money":
        """Сумма, взятая указанное число раз."""
        return Money(self.amount * units)
