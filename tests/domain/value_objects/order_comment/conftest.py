"""Фикстуры комментария к заказу."""

import pytest

from src.domain.value_objects import OrderComment
from tests.domain.value_objects.order_comment.factories import OrderCommentFactory


@pytest.fixture
def order_comment() -> OrderComment:
    """Комментарий со значением по умолчанию."""
    return OrderCommentFactory()
