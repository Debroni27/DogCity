"""Фикстуры владельцев питомцев."""

import pytest

from src.domain.aggregates import Owner
from src.domain.value_objects import VaccinationCertificate
from tests.domain.aggregates.owner.factories import OwnerFactory
from tests.domain.value_objects.pet_profile.factories import (
    VaccinationCertificateFactory,
)


@pytest.fixture
def owner() -> Owner:
    """Владелец, ещё не заведший ни одного питомца."""
    return OwnerFactory()


@pytest.fixture
def certificate() -> VaccinationCertificate:
    """Отметка о прививке от бешенства, которую владелец заводит питомцу."""
    return VaccinationCertificateFactory()
