"""Фабрики ограничений догситтера."""

import factory

from src.domain.value_objects import AcceptedDogSizes, Capacity, DogSize


class CapacityFactory(factory.Factory):
    """Догситтер, берущий двух собак одновременно."""

    class Meta:
        model = Capacity

    value = 2


class AcceptedDogSizesFactory(factory.Factory):
    """Догситтер, берущий мелких и средних собак."""

    class Meta:
        model = AcceptedDogSizes

    values = frozenset({DogSize.SMALL, DogSize.MEDIUM})
