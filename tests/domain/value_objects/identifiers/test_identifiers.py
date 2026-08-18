"""Тесты типизированных идентификаторов."""

from uuid import uuid4

from src.domain.value_objects import OwnerId, PetId


def test_different_types_with_same_uuid_are_not_equal() -> None:
    """Номинальная типизация: один UUID в разных типах — разные значения."""
    value = uuid4()
    assert OwnerId(value) != PetId(value)
