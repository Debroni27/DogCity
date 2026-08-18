"""Тесты временного интервала оказания услуги."""

from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from hypothesis import given
from hypothesis import strategies as st

from src.domain.exceptions import ValidationError
from src.domain.value_objects import TimeInterval
from tests.domain.value_objects.time_interval.factories import TimeIntervalFactory

aware_moments = st.datetimes(
    min_value=datetime(2020, 1, 1, tzinfo=UTC),
    max_value=datetime(2030, 1, 1, tzinfo=UTC),
    timezones=st.just(UTC),
)


def test_naive_start_is_rejected(base_moment: datetime) -> None:
    """Начало без часового пояса отвергается."""
    with pytest.raises(ValidationError) as exc:
        TimeIntervalFactory(starts_at=base_moment.replace(tzinfo=None))
    assert exc.value.field == "starts_at"


def test_naive_end_is_rejected(base_moment: datetime) -> None:
    """Конец без часового пояса отвергается."""
    with pytest.raises(ValidationError) as exc:
        TimeIntervalFactory(ends_at=base_moment.replace(tzinfo=None))
    assert exc.value.field == "ends_at"


def test_end_before_start_is_rejected(base_moment: datetime) -> None:
    """Конец обязан быть позже начала."""
    with pytest.raises(ValidationError) as exc:
        TimeIntervalFactory(ends_at=base_moment - timedelta(hours=1))
    assert exc.value.field == "ends_at"


def test_zero_length_interval_is_rejected(base_moment: datetime) -> None:
    """Услуга нулевой длительности не услуга."""
    with pytest.raises(ValidationError):
        TimeIntervalFactory(ends_at=base_moment)


def test_interval_in_the_past_is_accepted() -> None:
    """Прошедший интервал валиден: отношение к «сейчас» проверяет агрегат."""
    assert TimeIntervalFactory(starts_at=datetime(2020, 1, 1, tzinfo=UTC))


def test_duration_is_difference_of_bounds(base_moment: datetime) -> None:
    """Длительность — разность границ, без округления до единиц тарификации."""
    interval = TimeIntervalFactory(ends_at=base_moment + timedelta(hours=23))
    assert interval.duration == timedelta(hours=23)


def test_adjacent_intervals_do_not_overlap(hour_interval: TimeInterval) -> None:
    """Смежные интервалы не пересекаются, ситтер не возьмёт две прогулки подряд."""
    following = TimeIntervalFactory(starts_at=hour_interval.ends_at)
    assert not hour_interval.overlaps(following)


def test_shifted_intervals_overlap(
    hour_interval: TimeInterval, base_moment: datetime
) -> None:
    """Частично наложенные интервалы пересекаются."""
    shifted = TimeIntervalFactory(starts_at=base_moment + timedelta(minutes=30))
    assert hour_interval.overlaps(shifted)


def test_nested_interval_overlaps(base_moment: datetime) -> None:
    """Вложенный интервал пересекается с объемлющим."""
    outer = TimeIntervalFactory(ends_at=base_moment + timedelta(hours=4))
    inner = TimeIntervalFactory(
        starts_at=base_moment + timedelta(hours=1),
        ends_at=base_moment + timedelta(hours=2),
    )
    assert outer.overlaps(inner)


def test_disjoint_intervals_do_not_overlap(
    hour_interval: TimeInterval, base_moment: datetime
) -> None:
    """Разнесённые во времени интервалы не пересекаются."""
    distant = TimeIntervalFactory(starts_at=base_moment + timedelta(hours=5))
    assert not hour_interval.overlaps(distant)


def test_same_instant_in_another_timezone_overlaps(
    hour_interval: TimeInterval,
) -> None:
    """Сравнение идёт по моменту времени, а не по локальному представлению."""
    moscow = datetime(2026, 8, 18, 13, tzinfo=ZoneInfo("Europe/Moscow"))
    assert hour_interval.overlaps(TimeIntervalFactory(starts_at=moscow))


@given(
    first_start=aware_moments,
    first_hours=st.integers(min_value=1, max_value=48),
    second_start=aware_moments,
    second_hours=st.integers(min_value=1, max_value=48),
)
def test_overlaps_is_symmetric(
    first_start: datetime,
    first_hours: int,
    second_start: datetime,
    second_hours: int,
) -> None:
    """Пересечение симметрично для любой пары интервалов."""
    first = TimeInterval(first_start, first_start + timedelta(hours=first_hours))
    second = TimeInterval(second_start, second_start + timedelta(hours=second_hours))
    assert first.overlaps(second) == second.overlaps(first)


@given(start=aware_moments, hours=st.integers(min_value=1, max_value=48))
def test_interval_always_overlaps_itself(start: datetime, hours: int) -> None:
    """Интервал всегда пересекается сам с собой."""
    interval = TimeInterval(start, start + timedelta(hours=hours))
    assert interval.overlaps(interval)
