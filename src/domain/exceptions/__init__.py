"""Ошибки домена DogCity."""

from src.domain.exceptions.base import (
    DomainError,
    IllegalStateTransitionError,
    InvariantViolationError,
    ValidationError,
)

__all__ = (
    "DomainError",
    "IllegalStateTransitionError",
    "InvariantViolationError",
    "ValidationError",
)
