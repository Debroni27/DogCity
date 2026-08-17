"""Типизированные идентификаторы доменных сущностей.

Каждый идентификатор — отдельный тип, а не голый UUID. Это даёт номинальную
типизацию: mypy не позволит передать ``PetId`` туда, где ожидается ``OwnerId``.

"""

from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

__all__ = (
    "AdminId",
    "EntityId",
    "OrderId",
    "OwnerId",
    "PetId",
    "ReviewId",
    "SitterId",
)


@dataclass(frozen=True, slots=True)
class EntityId:
    """Базовый идентификатор сущности."""

    value: UUID

    @classmethod
    def new(cls) -> Self:
        """Сгенерировать новый идентификатор."""
        return cls(uuid4())


class OwnerId(EntityId):
    """Идентификатор владельца питомца."""

    __slots__ = ()


class PetId(EntityId):
    """Идентификатор питомца."""

    __slots__ = ()


class SitterId(EntityId):
    """Идентификатор догситтера."""

    __slots__ = ()


class OrderId(EntityId):
    """Идентификатор заказа."""

    __slots__ = ()


class ReviewId(EntityId):
    """Идентификатор отзыва."""

    __slots__ = ()


class AdminId(EntityId):
    """Идентификатор администратора сервиса."""

    __slots__ = ()
