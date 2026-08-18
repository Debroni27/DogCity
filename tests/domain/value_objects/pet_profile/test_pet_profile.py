"""Тесты характеристик питомца."""

from datetime import date
from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from src.domain.exceptions import ValidationError
from src.domain.value_objects import (
    BREED_MAX_LENGTH,
    MEDIUM_MAX_KG,
    PET_NAME_MAX_LENGTH,
    SMALL_MAX_KG,
    VACCINE_NAME_MAX_LENGTH,
    WEIGHT_MAX_KG,
    DogSize,
    PetGender,
    Weight,
)
from tests.domain.value_objects.pet_profile.factories import (
    BreedFactory,
    PetNameFactory,
    VaccinationCertificateFactory,
    WeightFactory,
)

SIZE_ORDER = (DogSize.SMALL, DogSize.MEDIUM, DogSize.LARGE)


def test_pet_name_longer_than_limit_is_rejected() -> None:
    """Кличка ограничена по длине."""
    with pytest.raises(ValidationError):
        PetNameFactory(value="к" * (PET_NAME_MAX_LENGTH + 1))


def test_pet_name_at_limit_is_accepted() -> None:
    """Граница длины включительна."""
    assert PetNameFactory(value="к" * PET_NAME_MAX_LENGTH)


def test_breed_longer_than_limit_is_rejected() -> None:
    """Порода ограничена по длине."""
    with pytest.raises(ValidationError):
        BreedFactory(value="п" * (BREED_MAX_LENGTH + 1))


def test_breed_accepts_mixed_breed() -> None:
    """Порода — свободная строка, поэтому метис выразим."""
    assert BreedFactory(value="Метис лабрадора и хаски").value


@pytest.mark.parametrize(
    ("gender", "expected"),
    [(PetGender.MALE, "male"), (PetGender.FEMALE, "female")],
)
def test_gender_value_is_stable(gender: PetGender, expected: str) -> None:
    """Значение зафиксировано контрактом: переименование ломает совместимость."""
    assert gender.value == expected


def test_weight_must_be_positive() -> None:
    """Нулевой вес отвергается."""
    with pytest.raises(ValidationError):
        WeightFactory(kilograms=Decimal("0"))


def test_weight_rejects_not_a_number() -> None:
    """NaN отсекается проверкой is_finite до сравнений, которые с ним всегда ложны."""
    with pytest.raises(ValidationError) as exc:
        WeightFactory(kilograms=Decimal("NaN"))
    assert "конечным" in exc.value.reason


def test_weight_above_sanity_limit_is_rejected() -> None:
    """Верхняя граница ловит ввод в граммах вместо килограммов."""
    with pytest.raises(ValidationError):
        WeightFactory(kilograms=Decimal("15000"))


def test_weight_at_upper_limit_is_accepted() -> None:
    """Граница веса включительна."""
    assert WeightFactory(kilograms=WEIGHT_MAX_KG)


@pytest.mark.parametrize(
    ("kilograms", "expected"),
    [
        (Decimal("0.5"), DogSize.SMALL),
        (SMALL_MAX_KG, DogSize.SMALL),
        (SMALL_MAX_KG + Decimal("0.01"), DogSize.MEDIUM),
        (MEDIUM_MAX_KG, DogSize.MEDIUM),
        (MEDIUM_MAX_KG + Decimal("0.01"), DogSize.LARGE),
        (WEIGHT_MAX_KG, DogSize.LARGE),
    ],
)
def test_size_boundaries(kilograms: Decimal, expected: DogSize) -> None:
    """Границы категорий включительны по верхнему краю."""
    assert DogSize.from_weight(Weight(kilograms)) is expected


@given(
    first=st.decimals(min_value=Decimal("0.1"), max_value=WEIGHT_MAX_KG, places=2),
    second=st.decimals(min_value=Decimal("0.1"), max_value=WEIGHT_MAX_KG, places=2),
)
def test_size_never_decreases_with_weight(first: Decimal, second: Decimal) -> None:
    """Более тяжёлая собака никогда не получает меньшую категорию."""
    lighter, heavier = sorted([first, second])
    lighter_size = SIZE_ORDER.index(DogSize.from_weight(Weight(lighter)))
    heavier_size = SIZE_ORDER.index(DogSize.from_weight(Weight(heavier)))
    assert lighter_size <= heavier_size


def test_certificate_expiring_before_issue_is_rejected() -> None:
    """Срок действия обязан быть позже даты выдачи."""
    with pytest.raises(ValidationError) as exc:
        VaccinationCertificateFactory(valid_until=date(2025, 1, 1))
    assert exc.value.field == "valid_until"


def test_certificate_valid_on_issue_day_is_rejected() -> None:
    """Нулевой срок действия бессмыслен."""
    with pytest.raises(ValidationError):
        VaccinationCertificateFactory(valid_until=date(2026, 1, 1))


def test_certificate_in_the_past_is_accepted() -> None:
    """Истёкшая прививка — валидное значение: срок проверяет агрегат, не тип."""
    assert VaccinationCertificateFactory(
        issued_on=date(2020, 1, 1), valid_until=date(2021, 1, 1)
    )


def test_vaccine_name_longer_than_limit_is_rejected() -> None:
    """Название препарата ограничено по длине."""
    with pytest.raises(ValidationError):
        VaccinationCertificateFactory(
            vaccine_name="н" * (VACCINE_NAME_MAX_LENGTH + 1)
        )
