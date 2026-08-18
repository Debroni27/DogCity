"""Фикстуры доменных событий."""

import pytest

from src.domain.events import DomainEvent
from tests.domain.events.factories import DomainEventFactory


@pytest.fixture
def domain_event() -> DomainEvent:
    """Событие со значениями по умолчанию."""
    return DomainEventFactory()
