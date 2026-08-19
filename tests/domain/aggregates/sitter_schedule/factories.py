"""Фабрики расписаний догситтера."""

from datetime import timedelta

from src.domain.aggregates import SitterSchedule
from src.domain.value_objects import (
    Capacity,
    CorrelationId,
    OrderId,
    ServiceFormat,
    TimeInterval,
)
from tests.domain.events.factories import OCCURRED_AT
from tests.domain.value_objects.time_interval.factories import BASE_MOMENT


def hours(start: int, end: int) -> TimeInterval:
    """Интервал, заданный часами от опорного момента."""
    return TimeInterval(
        BASE_MOMENT + timedelta(hours=start), BASE_MOMENT + timedelta(hours=end)
    )


def reserve(
    schedule: SitterSchedule,
    interval: TimeInterval,
    capacity: Capacity,
    service_format: ServiceFormat = ServiceFormat.SHARED,
    order_id: OrderId | None = None,
) -> OrderId:
    """Занять время догситтера и вернуть идентификатор заказа."""
    if order_id is None:
        order_id = OrderId.new()
    schedule.reserve(
        order_id=order_id,
        interval=interval,
        service_format=service_format,
        capacity=capacity,
        occurred_at=OCCURRED_AT,
        correlation_id=CorrelationId.new(),
    )
    return order_id
