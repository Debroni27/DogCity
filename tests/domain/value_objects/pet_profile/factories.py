"""Фабрики характеристик питомца."""

from datetime import date
from decimal import Decimal

import factory

from src.domain.value_objects import (
    Breed,
    PetName,
    VaccinationCertificate,
    Weight,
)


class PetNameFactory(factory.Factory):
    """Кличка питомца."""

    class Meta:
        model = PetName

    value = factory.Faker("first_name", locale="ru_RU")


class BreedFactory(factory.Factory):
    """Порода из короткого списка реальных."""

    class Meta:
        model = Breed

    value = factory.Iterator(["Лабрадор", "Такса", "Хаски", "Метис"])


class WeightFactory(factory.Factory):
    """Вес собаки средней категории."""

    class Meta:
        model = Weight

    kilograms = Decimal("12.5")


class VaccinationCertificateFactory(factory.Factory):
    """Прививка от бешенства сроком на год."""

    class Meta:
        model = VaccinationCertificate

    vaccine_name = "Nobivac Rabies"
    issued_on = date(2026, 1, 1)
    valid_until = date(2027, 1, 1)
