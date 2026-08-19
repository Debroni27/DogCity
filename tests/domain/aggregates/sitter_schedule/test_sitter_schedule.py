"""Тесты агрегата расписания догситтера."""

import pytest

from src.domain.aggregates import SitterSchedule
from src.domain.events import BookingReleased, BookingReserved
from src.domain.exceptions import InvariantViolationError
from src.domain.value_objects import (
    Capacity,
    CorrelationId,
    OrderId,
    ServiceFormat,
)
from tests.domain.aggregates.sitter_schedule.factories import hours, reserve
from tests.domain.events.factories import OCCURRED_AT

ONE = Capacity(1)
TWO = Capacity(2)
THREE = Capacity(3)


def test_reserved_time_becomes_a_booking(schedule: SitterSchedule) -> None:
    """Занятое время появляется в расписании вместе с событием."""
    order_id = reserve(schedule, hours(10, 12), TWO)
    (booking,) = schedule.bookings
    assert booking.order_id == order_id
    event = schedule.pending_events[-1]
    assert isinstance(event, BookingReserved)
    assert event.sitter_id == schedule.sitter_id


def test_same_order_cannot_take_time_twice(schedule: SitterSchedule) -> None:
    """Повторная бронь под тот же заказ отвергается."""
    order_id = reserve(schedule, hours(10, 12), TWO)
    with pytest.raises(InvariantViolationError):
        reserve(schedule, hours(14, 16), TWO, order_id=order_id)


def test_adjacent_intervals_do_not_collide(schedule: SitterSchedule) -> None:
    """Смежные брони не пересекаются: догситтер берёт две прогулки подряд."""
    reserve(schedule, hours(10, 11), ONE)
    reserve(schedule, hours(11, 12), ONE)
    assert len(schedule.bookings) == 2


def test_separate_intervals_ignore_capacity(schedule: SitterSchedule) -> None:
    """Вместимость ограничивает одновременность, а не общее число броней."""
    reserve(schedule, hours(10, 11), ONE)
    reserve(schedule, hours(14, 15), ONE)
    reserve(schedule, hours(18, 19), ONE)
    assert len(schedule.bookings) == 3


def test_overlapping_bookings_fill_capacity(schedule: SitterSchedule) -> None:
    """Пересечение само по себе не нарушение: при вместимости в двоих их двое."""
    reserve(schedule, hours(10, 14), TWO)
    reserve(schedule, hours(12, 16), TWO)
    assert len(schedule.bookings) == 2


def test_capacity_beyond_the_limit_is_refused(schedule: SitterSchedule) -> None:
    """Третья одновременная бронь при вместимости в двоих отвергается."""
    reserve(schedule, hours(10, 14), TWO)
    reserve(schedule, hours(12, 16), TWO)
    with pytest.raises(InvariantViolationError):
        reserve(schedule, hours(13, 15), TWO)


def test_capacity_counts_concurrency_not_overlaps(schedule: SitterSchedule) -> None:
    """Считается наибольшая одновременность, а не число пересекающихся броней."""
    reserve(schedule, hours(10, 12), TWO)
    reserve(schedule, hours(12, 14), TWO)
    reserve(schedule, hours(11, 13), TWO)
    assert len(schedule.bookings) == 3


def test_individual_booking_needs_the_sitter_whole(schedule: SitterSchedule) -> None:
    """Индивидуальная услуга не встаёт рядом с чужой бронью, даже если место есть."""
    reserve(schedule, hours(10, 14), THREE)
    with pytest.raises(InvariantViolationError):
        reserve(schedule, hours(12, 16), THREE, ServiceFormat.INDIVIDUAL)


def test_individual_booking_blocks_the_others(schedule: SitterSchedule) -> None:
    """Ограничение двустороннее: поверх индивидуальной брони не встать никому."""
    reserve(schedule, hours(10, 14), THREE, ServiceFormat.INDIVIDUAL)
    with pytest.raises(InvariantViolationError):
        reserve(schedule, hours(12, 16), THREE)


def test_individual_booking_allows_neighbours_in_time(
    schedule: SitterSchedule,
) -> None:
    """Индивидуальность занимает интервал, а не весь день."""
    reserve(schedule, hours(10, 14), THREE, ServiceFormat.INDIVIDUAL)
    reserve(schedule, hours(14, 16), THREE)
    assert len(schedule.bookings) == 2


def test_released_time_leaves_the_schedule(schedule: SitterSchedule) -> None:
    """Освобождённое время исчезает из расписания."""
    order_id = reserve(schedule, hours(10, 12), ONE)
    schedule.release(order_id, OCCURRED_AT, CorrelationId.new())
    assert schedule.bookings == ()
    assert isinstance(schedule.pending_events[-1], BookingReleased)


def test_released_time_can_be_taken_again(schedule: SitterSchedule) -> None:
    """После отмены заказа время снова доступно."""
    order_id = reserve(schedule, hours(10, 12), ONE)
    schedule.release(order_id, OCCURRED_AT, CorrelationId.new())
    reserve(schedule, hours(10, 12), ONE)
    assert len(schedule.bookings) == 1


def test_unknown_booking_cannot_be_released(schedule: SitterSchedule) -> None:
    """Освободить можно только занятое время."""
    with pytest.raises(InvariantViolationError):
        schedule.release(OrderId.new(), OCCURRED_AT, CorrelationId.new())


def test_events_are_forgotten_once_taken(schedule: SitterSchedule) -> None:
    """После выгрузки прикладным слоем агрегат событий не хранит."""
    reserve(schedule, hours(10, 12), ONE)
    schedule.clear_events()
    assert schedule.pending_events == ()
