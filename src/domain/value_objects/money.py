"""Денежные суммы."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum

__all__ = (
    "Currency",
    "Money",
)


class Currency(StrEnum):
    """Валюта расчётов. Единственный вариант — рубль."""

    RUB = "RUB"


@dataclass(frozen=True, slots=True)
class Money:
    """Денежная сумма в рублях. Точность — два знака после запятой."""

    amount: Decimal
    currency: Currency = field(default=Currency.RUB, init=False)
