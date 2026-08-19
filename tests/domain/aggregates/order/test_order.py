"""Тесты агрегата заказа."""

from datetime import timedelta

import pytest

from src.domain.aggregates import Order
from src.domain.events import (
    OrderCancelled,
    OrderCompleted,
    OrderConfirmed,
    OrderPlaced,
    OrderRejected,
    OrderStarted,
)
from src.domain.exceptions import IllegalStateTransitionError, InvariantViolationError
from src.domain.value_objects import (
    CancellationReason,
    CorrelationId,
    OrderParty,
    OrderStatus,
    RejectionReason,
)
from tests.domain.aggregates.order.factories import PLACED_AT, TOTAL, OrderFactory
from tests.domain.value_objects.time_interval.factories import BASE_MOMENT


def test_placed_order_awaits_the_sitter(order: Order) -> None:
    """Оформленный заказ ждёт ответа догситтера и стоимости ещё не имеет."""
    assert order.status is OrderStatus.PENDING
    assert order.total is None


def test_placing_lays_out_the_order_from_its_first_event(order: Order) -> None:
    """Первое событие описывает рождение заказа и раскладывается по его полям."""
    (event,) = order.pending_events
    assert isinstance(event, OrderPlaced)
    assert order.order_id == event.order_id
    assert order.owner_id == event.owner_id
    assert order.sitter_id == event.sitter_id
    assert order.offer == event.offer
    assert order.interval == event.interval


def test_service_starting_in_the_past_is_rejected() -> None:
    """Заказ на прошедшее время не оформляется."""
    with pytest.raises(InvariantViolationError):
        OrderFactory(occurred_at=BASE_MOMENT + timedelta(hours=1))


def test_service_starting_at_the_moment_of_placing_is_accepted() -> None:
    """Начало ровно в момент оформления прошлым не считается."""
    assert OrderFactory(occurred_at=BASE_MOMENT)


def test_confirmation_fixes_the_total(confirmed_order: Order) -> None:
    """Подтверждение переводит заказ в CONFIRMED и фиксирует стоимость."""
    assert confirmed_order.status is OrderStatus.CONFIRMED
    assert confirmed_order.total == TOTAL
    assert isinstance(confirmed_order.pending_events[-1], OrderConfirmed)


def test_rejection_closes_the_order(rejected_order: Order) -> None:
    """Отказ догситтера прекращает заказ."""
    assert rejected_order.status is OrderStatus.REJECTED
    assert isinstance(rejected_order.pending_events[-1], OrderRejected)


def test_cancellation_remembers_the_initiator(order_cancelled_by_owner: Order) -> None:
    """Отмена фиксирует, какая из сторон её инициировала."""
    event = order_cancelled_by_owner.pending_events[-1]
    assert isinstance(event, OrderCancelled)
    assert event.initiated_by is OrderParty.OWNER


def test_confirmed_order_can_still_be_cancelled(confirmed_order: Order) -> None:
    """Отмена возможна до начала услуги, а не только до подтверждения."""
    confirmed_order.cancel(
        CancellationReason.PET_ILLNESS,
        OrderParty.OWNER,
        PLACED_AT,
        CorrelationId.new(),
    )
    assert confirmed_order.status is OrderStatus.CANCELLED


def test_started_service_moves_order_in_progress(started_order: Order) -> None:
    """Начало оказания услуги переводит заказ в IN_PROGRESS."""
    assert started_order.status is OrderStatus.IN_PROGRESS
    assert isinstance(started_order.pending_events[-1], OrderStarted)


def test_completion_closes_the_order(completed_order: Order) -> None:
    """Завершение услуги закрывает заказ."""
    assert completed_order.status is OrderStatus.COMPLETED
    assert isinstance(completed_order.pending_events[-1], OrderCompleted)


def test_order_cannot_be_confirmed_twice(confirmed_order: Order) -> None:
    """Повторное подтверждение недопустимо."""
    with pytest.raises(IllegalStateTransitionError) as exc:
        confirmed_order.confirm(TOTAL, PLACED_AT, CorrelationId.new())
    assert exc.value.transition == "confirm"
    assert exc.value.current_state == OrderStatus.CONFIRMED


def test_sitter_cannot_reject_after_confirming(confirmed_order: Order) -> None:
    """Отказ возможен только до подтверждения, дальше остаётся отмена."""
    with pytest.raises(IllegalStateTransitionError):
        confirmed_order.reject(
            RejectionReason.PET_NOT_SUITABLE, PLACED_AT, CorrelationId.new()
        )


def test_service_cannot_start_before_confirmation(order: Order) -> None:
    """Неподтверждённый заказ не начинают."""
    with pytest.raises(IllegalStateTransitionError):
        order.start(PLACED_AT, CorrelationId.new())


def test_service_cannot_complete_before_it_starts(confirmed_order: Order) -> None:
    """Завершить можно только начатую услугу."""
    with pytest.raises(IllegalStateTransitionError):
        confirmed_order.complete(PLACED_AT, CorrelationId.new())


def test_started_service_cannot_be_cancelled(started_order: Order) -> None:
    """После начала услуги отмена недоступна обеим сторонам."""
    with pytest.raises(IllegalStateTransitionError):
        started_order.cancel(
            CancellationReason.PLANS_CHANGED,
            OrderParty.SITTER,
            PLACED_AT,
            CorrelationId.new(),
        )


def test_completed_order_accepts_no_transitions(completed_order: Order) -> None:
    """Завершённый заказ терминален."""
    with pytest.raises(IllegalStateTransitionError):
        completed_order.start(PLACED_AT, CorrelationId.new())


@pytest.mark.parametrize("party", list(OrderParty))
def test_both_parties_review_a_completed_order(
    completed_order: Order, party: OrderParty
) -> None:
    """После оказанной услуги стороны видели друг друга, отзыв симметричен."""
    assert completed_order.may_be_reviewed_by(party)


def test_only_owner_reviews_a_rejected_order(rejected_order: Order) -> None:
    """На отказ высказывается пострадавшая сторона — владелец."""
    assert rejected_order.may_be_reviewed_by(OrderParty.OWNER)
    assert not rejected_order.may_be_reviewed_by(OrderParty.SITTER)


def test_initiator_of_cancellation_cannot_review(
    order_cancelled_by_owner: Order,
) -> None:
    """Отзыв пишет сторона, пострадавшая от чужого решения, а не инициатор."""
    assert order_cancelled_by_owner.may_be_reviewed_by(OrderParty.SITTER)
    assert not order_cancelled_by_owner.may_be_reviewed_by(OrderParty.OWNER)


@pytest.mark.parametrize("party", list(OrderParty))
def test_unfinished_order_cannot_be_reviewed(order: Order, party: OrderParty) -> None:
    """Пока услуга не завершена и не прекращена, отзыву неоткуда взяться."""
    assert not order.may_be_reviewed_by(party)


def test_events_accumulate_until_cleared(confirmed_order: Order) -> None:
    """События копятся с оформления, пока их не забрал прикладной слой."""
    assert len(confirmed_order.pending_events) == 2
    confirmed_order.clear_events()
    assert confirmed_order.pending_events == ()
