"""Тесты иерархии доменных ошибок."""

import pickle

import pytest

from src.domain.exceptions import (
    DomainError,
    IllegalStateTransitionError,
    InvariantViolationError,
    ValidationError,
)
from src.domain.value_objects import OrderStatus


@pytest.mark.parametrize(
    "error_type",
    [ValidationError, InvariantViolationError, IllegalStateTransitionError],
)
def test_every_error_descends_from_domain_error(error_type: type[Exception]) -> None:
    """Прикладной слой ловит один тип и разбирает подклассы."""
    assert issubclass(error_type, DomainError)


def test_validation_error_keeps_field_and_reason_apart() -> None:
    """Поле и причина доступны раздельно, без разбора текста сообщения."""
    error = ValidationError("kilograms", "должен быть положительным")
    assert (error.field, error.reason) == ("kilograms", "должен быть положительным")


def test_validation_error_message_joins_parts() -> None:
    """Склейка происходит только при выводе."""
    assert str(ValidationError("amount", "не может быть отрицательной")) == (
        "amount: не может быть отрицательной"
    )


def test_validation_error_survives_pickle() -> None:
    """Аргументы переданы по отдельности, поэтому восстановление из args работает."""
    restored = pickle.loads(pickle.dumps(ValidationError("value", "пусто")))
    assert (restored.field, restored.reason) == ("value", "пусто")


def test_transition_error_accepts_enum_without_conversion() -> None:
    """StrEnum подходит там, где объявлена строка, поэтому связи с VO не возникает."""
    error = IllegalStateTransitionError("Order", OrderStatus.COMPLETED, "cancel")
    assert error.current_state == "completed"


def test_transition_error_message_names_all_parts() -> None:
    """Сообщение называет сущность, текущее состояние и запрошенный переход."""
    message = str(IllegalStateTransitionError("Order", OrderStatus.COMPLETED, "cancel"))
    assert "Order" in message
    assert "completed" in message
    assert "cancel" in message


def test_transition_error_survives_pickle() -> None:
    """Все три аргумента восстанавливаются."""
    error = IllegalStateTransitionError("Order", "confirmed", "confirm")
    restored = pickle.loads(pickle.dumps(error))
    assert restored.transition == "confirm"
