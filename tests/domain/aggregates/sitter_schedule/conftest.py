"""Фикстуры расписаний догситтера."""

import pytest

from src.domain.aggregates import SitterSchedule
from src.domain.value_objects import SitterId


@pytest.fixture
def schedule() -> SitterSchedule:
    """Пустое расписание догситтера."""
    return SitterSchedule(SitterId.new())
