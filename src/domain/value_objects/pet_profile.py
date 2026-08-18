"""Характеристики питомца, влияющие на оказание услуги."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import Self

__all__ = (
    "Breed",
    "DogSize",
    "PetGender",
    "PetName",
    "VaccinationCertificate",
    "Weight",
)

SMALL_MAX_KG = Decimal("10")
MEDIUM_MAX_KG = Decimal("25")


@dataclass(frozen=True, slots=True)
class PetName:
    """Кличка питомца."""

    value: str


@dataclass(frozen=True, slots=True)
class Breed:
    """Порода собаки — свободная строка, а не перечисление."""

    value: str


class PetGender(StrEnum):
    """Пол питомца."""

    MALE = "male"
    FEMALE = "female"


@dataclass(frozen=True, slots=True)
class Weight:
    """Вес питомца в килограммах."""

    kilograms: Decimal


class DogSize(StrEnum):
    """Размер собаки. Не хранится, а выводится из веса через :meth:`from_weight`."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

    @classmethod
    def from_weight(cls, weight: Weight) -> Self:
        """Определить категорию по весу питомца."""
        if weight.kilograms <= SMALL_MAX_KG:
            return cls(cls.SMALL)
        if weight.kilograms <= MEDIUM_MAX_KG:
            return cls(cls.MEDIUM)
        return cls(cls.LARGE)


@dataclass(frozen=True, slots=True)
class VaccinationCertificate:
    """Отметка о прививке. Для передержки требуется действующая."""

    vaccine_name: str
    issued_on: date
    valid_until: date
