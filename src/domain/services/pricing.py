"""Расчёт стоимости заказа по предложению догситтера."""

from datetime import timedelta
from math import ceil

from src.domain.value_objects import Money, ServiceOffer, Tarification, TimeInterval

__all__ = ("calculate_total",)


def calculate_total(offer: ServiceOffer, interval: TimeInterval) -> Money:
    """Стоимость услуги: цена за единицу, взятая столько раз, сколько единиц занято."""
    return offer.price * _units(interval.duration, _unit_of(offer.tarification))


def _unit_of(tarification: Tarification) -> timedelta:
    """Длительность одной единицы тарификации."""
    match tarification:
        case Tarification.PER_HOUR:
            return timedelta(hours=1)
        case Tarification.PER_DAY:
            return timedelta(days=1)


def _units(duration: timedelta, unit: timedelta) -> int:
    """Число единиц в длительности: начатая единица считается полной."""
    return ceil(duration / unit)
