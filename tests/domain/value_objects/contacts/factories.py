"""Фабрики контактных данных."""

import factory

from src.domain.value_objects import Email, PersonName, PhoneNumber


class PersonNameFactory(factory.Factory):
    """ФИО со случайными русскими именами."""

    class Meta:
        model = PersonName

    last_name = factory.Faker("last_name", locale="ru_RU")
    first_name = factory.Faker("first_name", locale="ru_RU")
    middle_name = factory.Faker("middle_name", locale="ru_RU")


class PhoneNumberFactory(factory.Factory):
    """Номер в формате E.164, уникальный в пределах прогона."""

    class Meta:
        model = PhoneNumber

    value = factory.Sequence(lambda n: f"+7999{n:07d}")


class EmailFactory(factory.Factory):
    """Адрес электронной почты в нижнем регистре."""

    class Meta:
        model = Email

    value = factory.Faker("email")
