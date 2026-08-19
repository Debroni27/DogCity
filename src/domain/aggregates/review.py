"""Агрегат отзыва о стороне заказа."""

from datetime import datetime

from src.domain.events import ReviewEvent, ReviewPublished
from src.domain.value_objects import (
    CorrelationId,
    EventId,
    OrderId,
    OrderParty,
    OwnerId,
    Rating,
    ReviewId,
    ReviewText,
    SitterId,
)

__all__ = ("Review",)


class Review:
    """Отзыв стороны заказа: текст всегда, оценка — только за состоявшуюся услугу."""

    __slots__ = (
        "_author",
        "_order_id",
        "_owner_id",
        "_pending_events",
        "_rating",
        "_review_id",
        "_sitter_id",
        "_text",
    )

    _review_id: ReviewId
    _order_id: OrderId
    _owner_id: OwnerId
    _sitter_id: SitterId
    _author: OrderParty
    _text: ReviewText
    _rating: Rating | None
    _pending_events: list[ReviewEvent]

    def __init__(self) -> None:
        """Заготовка отзыва: состояние наполняет ``_apply``."""
        self._pending_events = []

    @property
    def review_id(self) -> ReviewId:
        """Идентификатор отзыва."""
        return self._review_id

    @property
    def order_id(self) -> OrderId:
        """Заказ, по которому оставлен отзыв."""
        return self._order_id

    @property
    def owner_id(self) -> OwnerId:
        """Владелец — сторона заказа."""
        return self._owner_id

    @property
    def sitter_id(self) -> SitterId:
        """Догситтер — сторона заказа."""
        return self._sitter_id

    @property
    def author(self) -> OrderParty:
        """Сторона, оставившая отзыв."""
        return self._author

    @property
    def text(self) -> ReviewText:
        """Текст отзыва."""
        return self._text

    @property
    def rating(self) -> Rating | None:
        """Оценка или ``None``, если услуга не состоялась."""
        return self._rating

    @property
    def pending_events(self) -> tuple[ReviewEvent, ...]:
        """События, накопленные с последнего ``clear_events``."""
        return tuple(self._pending_events)

    @classmethod
    def publish(
        cls,
        *,
        review_id: ReviewId,
        order_id: OrderId,
        owner_id: OwnerId,
        sitter_id: SitterId,
        author: OrderParty,
        text: ReviewText,
        occurred_at: datetime,
        correlation_id: CorrelationId,
        rating: Rating | None = None,
    ) -> "Review":
        """Сторона заказа оставляет отзыв о другой стороне."""
        review = cls()
        review._record(
            ReviewPublished(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                review_id=review_id,
                order_id=order_id,
                owner_id=owner_id,
                sitter_id=sitter_id,
                author=author,
                text=text,
                rating=rating,
            )
        )
        return review

    def clear_events(self) -> None:
        """Забыть накопленные события: их забрал прикладной слой."""
        self._pending_events.clear()

    def _record(self, event: ReviewEvent) -> None:
        """Применить событие и запомнить его для публикации."""
        self._apply(event)
        self._pending_events.append(event)

    def _apply(self, event: ReviewEvent) -> None:
        """Единственное место, где меняется состояние отзыва."""
        match event:
            case ReviewPublished():
                self._review_id = event.review_id
                self._order_id = event.order_id
                self._owner_id = event.owner_id
                self._sitter_id = event.sitter_id
                self._author = event.author
                self._text = event.text
                self._rating = event.rating
