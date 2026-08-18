"""Фикстуры предложений догситтера."""

import pytest

from src.domain.value_objects import ServiceOffer
from tests.domain.value_objects.service.factories import ServiceOfferFactory


@pytest.fixture
def service_offer() -> ServiceOffer:
    """Предложение с допустимой парой услуги и тарификации."""
    return ServiceOfferFactory()
