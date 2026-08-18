"""Базовый тип доменного события."""

from dataclasses import dataclass
from datetime import datetime

from src.domain.exceptions import ValidationError
from src.domain.value_objects import CorrelationId, EventId

__all__ = ("DomainEvent",)


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Факт, произошедший в домене."""

    event_id: EventId
    occurred_at: datetime
    correlation_id: CorrelationId

    def __post_init__(self) -> None:
        if self.occurred_at.utcoffset() is None:
            raise ValidationError("occurred_at", "должен быть timezone-aware")
