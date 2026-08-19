"""Фабрики отзывов."""

from datetime import datetime
from typing import TypedDict, Unpack

import factory

from src.domain.aggregates import Review
from src.domain.value_objects import (
    CorrelationId,
    OrderId,
    OrderParty,
    OwnerId,
    Rating,
    ReviewId,
    ReviewText,
    SitterId,
)
from tests.domain.events.factories import OCCURRED_AT
from tests.domain.value_objects.rating.factories import RatingFactory
from tests.domain.value_objects.review.factories import ReviewTextFactory


class PublishArguments(TypedDict):
    """Именованные аргументы ``Review.publish``."""

    review_id: ReviewId
    order_id: OrderId
    owner_id: OwnerId
    sitter_id: SitterId
    author: OrderParty
    text: ReviewText
    rating: Rating | None
    occurred_at: datetime
    correlation_id: CorrelationId


class ReviewFactory(factory.Factory):
    """Отзыв владельца о догситтере за состоявшуюся услугу, с оценкой."""

    class Meta:
        model = Review

    review_id = factory.LazyFunction(ReviewId.new)
    order_id = factory.LazyFunction(OrderId.new)
    owner_id = factory.LazyFunction(OwnerId.new)
    sitter_id = factory.LazyFunction(SitterId.new)
    author = OrderParty.OWNER
    text = factory.SubFactory(ReviewTextFactory)
    rating = factory.SubFactory(RatingFactory)
    occurred_at = OCCURRED_AT
    correlation_id = factory.LazyFunction(CorrelationId.new)

    @classmethod
    def _create(
        cls, model_class: type[Review], **kwargs: Unpack[PublishArguments]
    ) -> Review:
        """Отзыв рождается фабричным методом агрегата."""
        return model_class.publish(**kwargs)
