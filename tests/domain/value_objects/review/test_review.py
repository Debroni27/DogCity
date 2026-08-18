"""Тесты текста отзыва."""

import pytest

from src.domain.exceptions import ValidationError
from src.domain.value_objects import REVIEW_TEXT_MAX_LENGTH
from tests.domain.value_objects.review.factories import ReviewTextFactory


def test_text_longer_than_limit_is_rejected() -> None:
    """Превышение длины отвергается с указанием поля."""
    with pytest.raises(ValidationError) as exc:
        ReviewTextFactory(value="о" * (REVIEW_TEXT_MAX_LENGTH + 1))
    assert exc.value.field == "value"


def test_text_at_limit_is_accepted() -> None:
    """Граница длины включительна."""
    assert ReviewTextFactory(value="о" * REVIEW_TEXT_MAX_LENGTH)
