"""Тесты комментария к заказу."""

import pytest

from src.domain.exceptions import ValidationError
from src.domain.value_objects import ORDER_COMMENT_MAX_LENGTH
from tests.domain.value_objects.order_comment.factories import OrderCommentFactory


def test_comment_longer_than_limit_is_rejected() -> None:
    """Превышение длины отвергается с указанием поля."""
    with pytest.raises(ValidationError) as exc:
        OrderCommentFactory(value="к" * (ORDER_COMMENT_MAX_LENGTH + 1))
    assert exc.value.field == "value"


def test_comment_at_limit_is_accepted() -> None:
    """Граница длины включительна."""
    assert OrderCommentFactory(value="к" * ORDER_COMMENT_MAX_LENGTH)
