"""Фикстуры временных интервалов."""

from datetime import datetime

import pytest

from src.domain.value_objects import TimeInterval
from tests.domain.value_objects.time_interval.factories import (
    BASE_MOMENT,
    TimeIntervalFactory,
)


@pytest.fixture
def base_moment() -> datetime:
    """Момент, от которого строятся интервалы в тестах."""
    return BASE_MOMENT


@pytest.fixture
def hour_interval() -> TimeInterval:
    """Часовой интервал от базового момента."""
    return TimeIntervalFactory()
