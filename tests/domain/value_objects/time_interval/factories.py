"""Фабрики временных интервалов."""

from datetime import UTC, datetime, timedelta

import factory

from src.domain.value_objects import TimeInterval

BASE_MOMENT = datetime(2026, 8, 18, 10, tzinfo=UTC)


class TimeIntervalFactory(factory.Factory):
    """Часовой интервал от фиксированного момента."""

    class Meta:
        model = TimeInterval

    starts_at = BASE_MOMENT
    ends_at = factory.LazyAttribute(lambda o: o.starts_at + timedelta(hours=1))
