"""Тесты базового доменного события."""

import pytest

from src.domain.exceptions import ValidationError
from tests.domain.events.factories import OCCURRED_AT, DomainEventFactory


def test_naive_moment_is_rejected() -> None:
    """Момент наступления без часового пояса отвергается."""
    with pytest.raises(ValidationError) as exc:
        DomainEventFactory(occurred_at=OCCURRED_AT.replace(tzinfo=None))
    assert exc.value.field == "occurred_at"
