"""Временной интервал оказания услуги."""

from dataclasses import dataclass
from datetime import datetime, timedelta

from src.domain.exceptions import ValidationError

__all__ = ("INTERVAL_MAX_DURATION", "TimeInterval")

INTERVAL_MAX_DURATION = timedelta(days=31)


@dataclass(frozen=True, slots=True)
class TimeInterval:
    """Интервал ``(starts_at, ends_at)``. Границы — tz-aware ``datetime`` в UTC."""

    starts_at: datetime
    ends_at: datetime

    def __post_init__(self) -> None:
        if self.starts_at.utcoffset() is None:
            raise ValidationError("starts_at", "должен быть timezone-aware")
        if self.ends_at.utcoffset() is None:
            raise ValidationError("ends_at", "должен быть timezone-aware")
        if self.starts_at >= self.ends_at:
            raise ValidationError("ends_at", "должен быть позже starts_at")
        if self.ends_at - self.starts_at > INTERVAL_MAX_DURATION:
            raise ValidationError(
                "ends_at", f"интервал длиннее {INTERVAL_MAX_DURATION.days} дней"
            )

    @property
    def duration(self) -> timedelta:
        """Длительность интервала."""
        return self.ends_at - self.starts_at

    def overlaps(self, other: "TimeInterval") -> bool:
        """Пересекается ли с другим интервалом. Смежные не пересекаются."""
        return self.starts_at < other.ends_at and other.starts_at < self.ends_at
