"""Услуги догситтинга и их тарификация."""

from dataclasses import dataclass
from enum import StrEnum

from src.domain.value_objects.money import Money

__all__ = (
    "Tarification",
    "ServiceOffer",
    "ServiceType",
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
    unit: Tarification
