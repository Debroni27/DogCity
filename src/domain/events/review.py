"""События отзыва."""

from dataclasses import dataclass

from src.domain.events.base import DomainEvent
from src.domain.value_objects import (
    OrderId,
    OrderParty,
    OwnerId,
    Rating,
    ReviewId,
    ReviewText,
    SitterId,
)

__all__ = ("ReviewEvent", "ReviewPublished")


@dataclass(frozen=True, slots=True)
class ReviewPublished(DomainEvent):
    """Одна из сторон заказа оставила отзыв."""

    review_id: ReviewId
    order_id: OrderId
    owner_id: OwnerId
    sitter_id: SitterId
    author: OrderParty
    text: ReviewText
    rating: Rating | None = None


type ReviewEvent = ReviewPublished
"""Любое событие отзыва."""
