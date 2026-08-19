"""Фикстуры заказов."""

import pytest

from src.domain.aggregates import Order
from src.domain.value_objects import (
    CancellationReason,
    CorrelationId,
    OrderParty,
    RejectionReason,
)
from tests.domain.aggregates.order.factories import PLACED_AT, TOTAL, OrderFactory


@pytest.fixture
def order() -> Order:
    """Оформленный заказ, ожидающий ответа догситтера."""
    return OrderFactory()


@pytest.fixture
def confirmed_order(order: Order) -> Order:
    """Заказ, принятый догситтером."""
    order.confirm(TOTAL, PLACED_AT, CorrelationId.new())
    return order


@pytest.fixture
def started_order(confirmed_order: Order) -> Order:
    """Заказ, услуга по которому оказывается прямо сейчас."""
    confirmed_order.start(PLACED_AT, CorrelationId.new())
    return confirmed_order


@pytest.fixture
def completed_order(started_order: Order) -> Order:
    """Заказ с оказанной услугой."""
    started_order.complete(PLACED_AT, CorrelationId.new())
    return started_order


@pytest.fixture
def rejected_order(order: Order) -> Order:
    """Заказ, от которого догситтер отказался до подтверждения."""
    order.reject(RejectionReason.SCHEDULE_CONFLICT, PLACED_AT, CorrelationId.new())
    return order


@pytest.fixture
def order_cancelled_by_owner(order: Order) -> Order:
    """Заказ, отменённый владельцем."""
    order.cancel(
        CancellationReason.PLANS_CHANGED,
        OrderParty.OWNER,
        PLACED_AT,
        CorrelationId.new(),
    )
    return order
