"""Фабрики доменных событий."""

from datetime import UTC, datetime

import factory

from src.domain.events import DomainEvent
from src.domain.value_objects import CorrelationId, EventId

OCCURRED_AT = datetime(2026, 8, 18, 10, tzinfo=UTC)


class DomainEventFactory(factory.Factory):
    """Событие с фиксированным моментом наступления."""

    class Meta:
        model = DomainEvent

    event_id = factory.LazyFunction(EventId.new)
    occurred_at = OCCURRED_AT
    correlation_id = factory.LazyFunction(CorrelationId.new)
