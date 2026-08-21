"""Тесты агрегата отзыва."""

from src.domain.aggregates import Review
from src.domain.events import ReviewPublished
from src.domain.value_objects import OrderParty
from tests.domain.aggregates.review.factories import ReviewFactory


def test_publishing_lays_out_the_review(review: Review) -> None:
    """Единственное событие отзыва раскладывается по его полям."""
    (event,) = review.pending_events
    assert isinstance(event, ReviewPublished)
    assert review.review_id == event.review_id
    assert review.order_id == event.order_id
    assert review.owner_id == event.owner_id
    assert review.sitter_id == event.sitter_id
    assert review.author == event.author
    assert review.text == event.text
    assert review.rating == event.rating


def test_review_without_rating_carries_only_text() -> None:
    """На отказ и отмену отзыв несёт текст и в рейтинг не попадает."""
    review = ReviewFactory(rating=None, author=OrderParty.OWNER)
    assert review.rating is None
    assert review.text.value


def test_sitter_reviews_the_owner_too() -> None:
    """Отзывы двусторонние: автором бывает и догситтер."""
    review = ReviewFactory(author=OrderParty.SITTER)
    assert review.author is OrderParty.SITTER


def test_events_are_forgotten_once_taken(review: Review) -> None:
    """После выгрузки прикладным слоем агрегат событий не хранит."""
    review.clear_events()
    assert review.pending_events == ()
