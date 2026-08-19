"""Характеристики питомца, влияющие на оказание услуги."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import Self

from src.domain.exceptions import ValidationError

__all__ = (
    "BREED_MAX_LENGTH",
    "MEDIUM_MAX_KG",
    "PET_NAME_MAX_LENGTH",
    "SMALL_MAX_KG",
    "VACCINE_NAME_MAX_LENGTH",
    "WEIGHT_MAX_KG",
    "BehaviorTrait",
    "BirthDate",
    "Breed",
    "DogSize",
    "PetGender",
    "PetName",
    "VaccinationCertificate",
    "Weight",
)

SMALL_MAX_KG = Decimal("10")
MEDIUM_MAX_KG = Decimal("25")
WEIGHT_MAX_KG = Decimal("150")
PET_NAME_MAX_LENGTH = 50
BREED_MAX_LENGTH = 100
VACCINE_NAME_MAX_LENGTH = 100


@dataclass(frozen=True, slots=True)
class PetName:
    """Кличка питомца."""

    value: str

    def __post_init__(self) -> None:
        if len(self.value) > PET_NAME_MAX_LENGTH:
            raise ValidationError("value", f"длиннее {PET_NAME_MAX_LENGTH} символов")


@dataclass(frozen=True, slots=True)
class Breed:
    """Порода собаки — свободная строка, а не перечисление."""

    value: str

    def __post_init__(self) -> None:
        if len(self.value) > BREED_MAX_LENGTH:
            raise ValidationError("value", f"длиннее {BREED_MAX_LENGTH} символов")


@dataclass(frozen=True, slots=True)
class BirthDate:
    """Дата рождения питомца."""

    value: date

    def age_in_years(self, reference_date: date) -> int:
        """Полных лет на указанную дату."""
        if reference_date < self.value:
            raise ValidationError("reference_date", "раньше даты рождения")
        years = reference_date.year - self.value.year
        if (reference_date.month, reference_date.day) < (
            self.value.month,
            self.value.day,
        ):
            years -= 1
        return years


class PetGender(StrEnum):
    """Пол питомца."""

    MALE = "male"
    FEMALE = "female"


class BehaviorTrait(StrEnum):
    """Особенность поведения собаки, по которой догситтер решает, брать ли заказ."""

    AGGRESSIVE_TO_DOGS = "aggressive_to_dogs"
    AGGRESSIVE_TO_PEOPLE = "aggressive_to_people"
    AFRAID_OF_DOGS = "afraid_of_dogs"
    AFRAID_OF_NOISE = "afraid_of_noise"
    PULLS_ON_LEASH = "pulls_on_leash"
    ESCAPE_PRONE = "escape_prone"
    SEPARATION_ANXIETY = "separation_anxiety"
    NOT_HOUSE_TRAINED = "not_house_trained"
    BARKS_A_LOT = "barks_a_lot"


@dataclass(frozen=True, slots=True)
class Weight:
    """Вес питомца в килограммах."""

    kilograms: Decimal

    def __post_init__(self) -> None:
        if not self.kilograms.is_finite():
            raise ValidationError("kilograms", "должен быть конечным числом")
        if self.kilograms <= 0:
            raise ValidationError("kilograms", "должен быть положительным")
        if self.kilograms > WEIGHT_MAX_KG:
            raise ValidationError("kilograms", f"больше {WEIGHT_MAX_KG} кг")


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

    def __post_init__(self) -> None:
        if len(self.vaccine_name) > VACCINE_NAME_MAX_LENGTH:
            raise ValidationError(
                "vaccine_name", f"длиннее {VACCINE_NAME_MAX_LENGTH} символов"
            )
        if self.valid_until <= self.issued_on:
            raise ValidationError("valid_until", "должна быть позже issued_on")
