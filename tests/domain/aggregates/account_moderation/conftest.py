"""Фикстуры модерации учётных записей."""

import pytest

from src.domain.aggregates import AccountModeration
from src.domain.value_objects import AdminId, CorrelationId, SitterId
from tests.domain.events.factories import OCCURRED_AT


@pytest.fixture
def admin_id() -> AdminId:
    """Администратор, принимающий решения модерации."""
    return AdminId.new()


@pytest.fixture
def moderation() -> AccountModeration:
    """Только что заведённая модерационная запись догситтера."""
    return AccountModeration.open(
        account_id=SitterId.new(),
        occurred_at=OCCURRED_AT,
        correlation_id=CorrelationId.new(),
    )


@pytest.fixture
def pending_moderation(moderation: AccountModeration) -> AccountModeration:
    """Запись с поданными на проверку документами."""
    moderation.submit_documents(OCCURRED_AT, CorrelationId.new())
    return moderation


@pytest.fixture
def deleted_moderation(moderation: AccountModeration) -> AccountModeration:
    """Запись удалённой учётной записи."""
    moderation.delete(OCCURRED_AT, CorrelationId.new())
    return moderation
