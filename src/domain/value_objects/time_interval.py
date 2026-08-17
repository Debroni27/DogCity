"""Временной интервал оказания услуги."""

from dataclasses import dataclass
from datetime import datetime

__all__ = ("TimeInterval",)


@dataclass(frozen=True, slots=True)
class TimeInterval:
    """Интервал ``(starts_at, ends_at)``.

    Обе границы — timezone-aware ``datetime`` в UTC. Наивные ``datetime``
    в домен не попадают: время приводится к UTC на границе приложения.
    """

    starts_at: datetime
    ends_at: datetime
