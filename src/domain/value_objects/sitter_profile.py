"""Ограничения догситтера на приём питомцев."""

from dataclasses import dataclass

from src.domain.exceptions import ValidationError
from src.domain.value_objects.pet_profile import DogSize

__all__ = (
    "CAPACITY_MAX",
    "AcceptedDogSizes",
    "Capacity",
)

CAPACITY_MAX = 3


@dataclass(frozen=True, slots=True)
class Capacity:
    """Сколько питомцев догситтер берёт одновременно по одной услуге."""

    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise ValidationError("value", "должна быть не меньше одного питомца")
        if self.value > CAPACITY_MAX:
            raise ValidationError("value", f"больше {CAPACITY_MAX} питомцев")


@dataclass(frozen=True, slots=True)
class AcceptedDogSizes:
    """Размеры собак, которых догситтер готов принять."""

    values: frozenset[DogSize]

    def __post_init__(self) -> None:
        if not self.values:
            raise ValidationError("values", "должен быть указан хотя бы один размер")

    def accepts(self, size: DogSize) -> bool:
        """Берёт ли догситтер собаку такого размера."""
        return size in self.values
