"""Фабрики комментария к заказу."""

import factory

from src.domain.value_objects import OrderComment


class OrderCommentFactory(factory.Factory):
    """Комментарий в пределах ограничения длины."""

    class Meta:
        model = OrderComment

    value = factory.Faker("sentence", locale="ru_RU")
