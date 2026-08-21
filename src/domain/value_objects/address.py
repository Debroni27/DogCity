"""Адрес места оказания услуги."""

from dataclasses import dataclass

from src.domain.exceptions import ValidationError

__all__ = ("BUILDING_MAX_LENGTH", "CITY_MAX_LENGTH", "STREET_MAX_LENGTH", "Address")

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
        if not self.city.strip():
            raise ValidationError("city", "пустое или из одних пробелов")
        if len(self.city) > CITY_MAX_LENGTH:
            raise ValidationError("city", f"длиннее {CITY_MAX_LENGTH} символов")
        if not self.street.strip():
            raise ValidationError("street", "пустое или из одних пробелов")
        if len(self.street) > STREET_MAX_LENGTH:
            raise ValidationError("street", f"длиннее {STREET_MAX_LENGTH} символов")
        if not self.building.strip():
            raise ValidationError("building", "пустое или из одних пробелов")
        if len(self.building) > BUILDING_MAX_LENGTH:
            raise ValidationError("building", f"длиннее {BUILDING_MAX_LENGTH} символов")
        if self.apartment is None:
            return
        if not self.apartment.strip():
            raise ValidationError("apartment", "пустое: квартиры нет — это None")
        if len(self.apartment) > BUILDING_MAX_LENGTH:
            raise ValidationError(
                "apartment", f"длиннее {BUILDING_MAX_LENGTH} символов"
            )
