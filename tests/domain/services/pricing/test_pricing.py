"""Тесты расчёта стоимости заказа."""

from datetime import timedelta

import pytest
from hypothesis import given
from hypothesis import strategies as st

from src.domain.services import calculate_total
from src.domain.value_objects import INTERVAL_MAX_DURATION, Money, Tarification
from tests.domain.value_objects.service.factories import ServiceOfferFactory
from tests.domain.value_objects.time_interval.factories import (
    BASE_MOMENT,
    TimeIntervalFactory,
)

PRICE = Money(500)
MAX_HOURS = INTERVAL_MAX_DURATION // timedelta(hours=1)
MAX_MINUTES = INTERVAL_MAX_DURATION // timedelta(minutes=1)


@pytest.mark.parametrize(
    ("duration", "tarification", "expected_units"),
    [
        (timedelta(hours=2), Tarification.PER_HOUR, 2),
        (timedelta(hours=1, minutes=20), Tarification.PER_HOUR, 2),
        (timedelta(minutes=1), Tarification.PER_HOUR, 1),
        (timedelta(days=2), Tarification.PER_DAY, 2),
        (timedelta(hours=23), Tarification.PER_DAY, 1),
        (timedelta(hours=25), Tarification.PER_DAY, 2),
        (timedelta(minutes=1), Tarification.PER_DAY, 1),
    ],
)
def test_started_unit_is_paid_in_full(
    duration: timedelta, tarification: Tarification, expected_units: int
) -> None:
    """Начатая единица тарификации оплачивается целиком."""
    offer = ServiceOfferFactory(price=PRICE, tarification=tarification)
    interval = TimeIntervalFactory(ends_at=BASE_MOMENT + duration)
    assert calculate_total(offer, interval) == PRICE * expected_units


@given(hours=st.integers(min_value=1, max_value=MAX_HOURS))
def test_whole_hours_are_not_rounded_up(hours: int) -> None:
    """Точное число часов не превращается в лишний оплаченный час."""
    offer = ServiceOfferFactory(price=PRICE, tarification=Tarification.PER_HOUR)
    interval = TimeIntervalFactory(ends_at=BASE_MOMENT + timedelta(hours=hours))
    assert calculate_total(offer, interval) == PRICE * hours


@given(minutes=st.integers(min_value=1, max_value=MAX_MINUTES))
def test_any_interval_costs_at_least_one_unit(minutes: int) -> None:
    """Услуга не бывает бесплатной: длительность строго положительна."""
    offer = ServiceOfferFactory(price=PRICE, tarification=Tarification.PER_DAY)
    interval = TimeIntervalFactory(ends_at=BASE_MOMENT + timedelta(minutes=minutes))
    assert calculate_total(offer, interval).amount >= PRICE.amount


@given(
    first=st.integers(min_value=1, max_value=MAX_MINUTES),
    second=st.integers(min_value=1, max_value=MAX_MINUTES),
)
def test_longer_interval_never_costs_less(first: int, second: int) -> None:
    """Более длинный интервал не может стоить дешевле короткого."""
    offer = ServiceOfferFactory(price=PRICE, tarification=Tarification.PER_HOUR)
    shorter, longer = sorted([first, second])
    shorter_total = calculate_total(
        offer, TimeIntervalFactory(ends_at=BASE_MOMENT + timedelta(minutes=shorter))
    )
    longer_total = calculate_total(
        offer, TimeIntervalFactory(ends_at=BASE_MOMENT + timedelta(minutes=longer))
    )
    assert shorter_total.amount <= longer_total.amount
