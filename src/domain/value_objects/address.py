"""Адрес места оказания услуги."""

from dataclasses import dataclass

from src.domain.exceptions import ValidationError

__all__ = ("Address",)

CITY_MAX_LENGTH = 100
STREET_MAX_LENGTH = 200
BUILDING_MAX_LENGTH = 20


@dataclass(frozen=True, slots=True)
class Address:
    """Физический адрес."""

    city: str
    street: str
    building: str
    apartment: str | None = None

    def __post_init__(self) -> None:
        if len(self.city) > CITY_MAX_LENGTH:
            raise ValidationError(
                "city", f"длиннее {CITY_MAX_LENGTH} символов"
            )
        if len(self.street) > STREET_MAX_LENGTH:
            raise ValidationError(
                "street", f"длиннее {STREET_MAX_LENGTH} символов"
            )
        if len(self.building) > BUILDING_MAX_LENGTH:
            raise ValidationError(
                "building", f"длиннее {BUILDING_MAX_LENGTH} символов"
            )
        if self.apartment is not None and len(self.apartment) > BUILDING_MAX_LENGTH:
            raise ValidationError(
                "apartment", f"длиннее {BUILDING_MAX_LENGTH} символов"
            )
