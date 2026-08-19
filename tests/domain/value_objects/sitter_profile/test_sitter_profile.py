"""Тесты ограничений догситтера."""

import pytest

from src.domain.exceptions import ValidationError
from src.domain.value_objects import CAPACITY_MAX, AcceptedDogSizes, DogSize
from tests.domain.value_objects.sitter_profile.factories import (
    AcceptedDogSizesFactory,
    CapacityFactory,
)


@pytest.mark.parametrize("value", [0, -1])
def test_capacity_below_one_is_rejected(value: int) -> None:
    """Догситтер, не берущий ни одной собаки, услугу не оказывает."""
    with pytest.raises(ValidationError):
        CapacityFactory(value=value)


def test_capacity_of_one_is_accepted() -> None:
    """Единица — выбор брать на передержку только одну собаку."""
    assert CapacityFactory(value=1).value == 1


def test_capacity_above_limit_is_rejected() -> None:
    """Больше предельного числа собак одновременно догситтер не берёт."""
    with pytest.raises(ValidationError):
        CapacityFactory(value=CAPACITY_MAX + 1)


def test_capacity_at_limit_is_accepted() -> None:
    """Граница вместимости включительна."""
    assert CapacityFactory(value=CAPACITY_MAX).value == CAPACITY_MAX


def test_empty_size_selection_is_rejected() -> None:
    """Догситтер обязан назвать хотя бы один размер, иначе заказы ему не подобрать."""
    with pytest.raises(ValidationError) as exc:
        AcceptedDogSizesFactory(values=frozenset())
    assert exc.value.field == "values"


def test_declared_size_is_accepted(accepted_dog_sizes: AcceptedDogSizes) -> None:
    """Объявленный размер принимается."""
    assert accepted_dog_sizes.accepts(DogSize.MEDIUM)


def test_undeclared_size_is_not_accepted(accepted_dog_sizes: AcceptedDogSizes) -> None:
    """Размер вне объявленных не принимается."""
    assert not accepted_dog_sizes.accepts(DogSize.LARGE)
