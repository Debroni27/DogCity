"""Временной интервал оказания услуги."""

from dataclasses import dataclass
from datetime import datetime

__all__ = ("TimeInterval",)


@dataclass(frozen=True, slots=True)
class TimeInterval:
    """Интервал ``(starts_at, ends_at)``. Границы — tz-aware ``datetime`` в UTC."""

    starts_at: datetime
    ends_at: datetime
