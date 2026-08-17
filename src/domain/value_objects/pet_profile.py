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
    """Порода собаки.

    Свободная строка, а не перечисление: список пород — справочник, который
    ведут вне домена, и метисы в него всё равно не укладываются.
    """

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
    """Размер собаки.

    Влияет на тариф и на то, возьмётся ли ситтер за питомца. Границы категорий
    заданы включительно по верхнему краю: ``SMALL`` — до 10 кг, ``MEDIUM`` —
    свыше 10 и до 25 кг, ``LARGE`` — свыше 25 кг.

    Хранится не размер, а вес: категория выводится из него через
    :meth:`from_weight`, поэтому пересмотр границ не требует миграции данных.
    """

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
