"""Ошибки домена DogCity."""

from src.domain.exceptions.base import (
    DomainError,
    IllegalStateTransition,
    InvariantViolation,
    ValidationError,
)

__all__ = (
    "DomainError",
    "IllegalStateTransition",
    "InvariantViolation",
    "ValidationError",
)
