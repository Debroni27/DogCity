"""Фикстуры характеристик питомца."""

import pytest

from src.domain.value_objects import (
    BirthDate,
    Breed,
    PetName,
    VaccinationCertificate,
    Weight,
)
from tests.domain.value_objects.pet_profile.factories import (
    BirthDateFactory,
    BreedFactory,
    PetNameFactory,
    VaccinationCertificateFactory,
    WeightFactory,
)


@pytest.fixture
def pet_name() -> PetName:
    """Кличка питомца."""
    return PetNameFactory()


@pytest.fixture
def breed() -> Breed:
    """Порода собаки."""
    return BreedFactory()


@pytest.fixture
def weight() -> Weight:
    """Вес собаки средней категории."""
    return WeightFactory()


@pytest.fixture
def birth_date() -> BirthDate:
    """Дата рождения взрослой собаки."""
    return BirthDateFactory()


@pytest.fixture
def vaccination_certificate() -> VaccinationCertificate:
    """Прививка от бешенства сроком на год."""
    return VaccinationCertificateFactory()
