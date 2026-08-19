"""Агрегаты домена DogCity."""

from src.domain.aggregates.account_moderation import AccountModeration
from src.domain.aggregates.order import Order
from src.domain.aggregates.owner import PETS_MAX, Owner, Pet
from src.domain.aggregates.review import Review
from src.domain.aggregates.sitter import Sitter
from src.domain.aggregates.sitter_schedule import Booking, SitterSchedule

__all__ = (
    "PETS_MAX",
    "AccountModeration",
    "Booking",
    "Order",
    "Owner",
    "Pet",
    "Review",
    "Sitter",
    "SitterSchedule",
)
