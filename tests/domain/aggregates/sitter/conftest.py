"""Фикстуры догситтеров."""

import pytest

from src.domain.aggregates import Sitter
from src.domain.value_objects import ServiceOffer
from tests.domain.aggregates.sitter.factories import SitterFactory
from tests.domain.value_objects.service.factories import ServiceOfferFactory


@pytest.fixture
def sitter() -> Sitter:
    """Догситтер на двух собак, предложений ещё не выставил."""
    return SitterFactory()


@pytest.fixture
def shared_offer() -> ServiceOffer:
    """Групповое предложение, которое догситтер выставляет в перечень услуг."""
    return ServiceOfferFactory()
