"""Услуги догситтинга и их тарификация."""

from dataclasses import dataclass
from enum import StrEnum

from src.domain.exceptions import ValidationError
from src.domain.value_objects.money import Money

__all__ = (
    "ServiceFormat",
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


class ServiceFormat(StrEnum):
    """Формат оказания услуги: рядом с чужими собаками или наедине."""

    SHARED = "shared"
    """Питомец может оказаться у догситтера одновременно с чужими собаками."""

    INDIVIDUAL = "individual"
    """Догситтер занят только этим питомцем всё время оказания услуги."""


@dataclass(frozen=True, slots=True)
class ServiceOffer:
    """Предложение догситтера: услуга, формат, цена и единица тарификации."""

    service_type: ServiceType
    price: Money
    tarification: Tarification
    service_format: ServiceFormat

    def __post_init__(self) -> None:
        if self.price.amount <= 0:
            raise ValidationError(
                "price", "должна быть положительной"
            )
        if (
            self.service_type is ServiceType.WALKING
            and self.tarification is Tarification.PER_DAY
        ):
            raise ValidationError(
                "tarification", "выгул тарифицируется только почасово"
            )
