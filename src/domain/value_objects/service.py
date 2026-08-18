"""Услуги догситтинга и их тарификация."""

from dataclasses import dataclass
from enum import StrEnum

from src.domain.exceptions import ValidationError
from src.domain.value_objects.money import Money

__all__ = (
    "ServiceOffer",
    "ServiceType",
    "Tarification",
)


class ServiceType(StrEnum):
    """Тип услуги."""

    WALKING = "walking"
    """Выгул: ситтер забирает питомца и гуляет с ним."""

    BOARDING = "boarding"
    """Передержка: питомец живёт у ситтера."""


class Tarification(StrEnum):
    """Единица тарификации."""

    PER_HOUR = "per_hour"
    PER_DAY = "per_day"


@dataclass(frozen=True, slots=True)
class ServiceOffer:
    """Предложение ситтера: услуга, цена и единица тарификации."""

    service_type: ServiceType
    price: Money
    tarification: Tarification

    def __post_init__(self) -> None:
        if self.price.amount <= 0:
            raise ValidationError("price", "должна быть положительной")
        if (
            self.service_type is ServiceType.WALKING
            and self.tarification is Tarification.PER_DAY
        ):
            raise ValidationError("tarification", "выгул тарифицируется только почасово")
