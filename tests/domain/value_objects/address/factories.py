"""Фабрики адресов."""

import factory

from src.domain.value_objects import Address


class AddressFactory(factory.Factory):
    """Адрес российского города, квартира не задана."""

    class Meta:
        model = Address

    city = factory.Faker("city_name", locale="ru_RU")
    street = factory.Faker("street_name", locale="ru_RU")
    building = factory.Faker("building_number", locale="ru_RU")
    apartment = None
