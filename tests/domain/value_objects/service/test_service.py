"""Тесты услуг догситтинга и их тарификации."""

import pytest

from src.domain.exceptions import ValidationError
from src.domain.value_objects import Money, ServiceType, Tarification
from tests.domain.value_objects.service.factories import ServiceOfferFactory


@pytest.mark.parametrize(
    ("member", "expected"),
    [
        (ServiceType.WALKING, "walking"),
        (ServiceType.BOARDING, "boarding"),
        (Tarification.PER_HOUR, "per_hour"),
        (Tarification.PER_DAY, "per_day"),
    ],
)
def test_value_is_stable(member: ServiceType | Tarification, expected: str) -> None:
    """Значение зафиксировано контрактом: переименование ломает совместимость."""
    assert member.value == expected


def test_free_offer_is_rejected() -> None:
    """Нулевая цена допустима для суммы, но не для прайса."""
    with pytest.raises(ValidationError) as exc:
        ServiceOfferFactory(price=Money(0))
    assert exc.value.field == "price"


def test_daily_walking_is_rejected() -> None:
    """Посуточный выгул бессмыслен — единственная запрещённая пара."""
    with pytest.raises(ValidationError) as exc:
        ServiceOfferFactory(
            service_type=ServiceType.WALKING, tarification=Tarification.PER_DAY
        )
    assert exc.value.field == "tarification"


@pytest.mark.parametrize(
    ("service_type", "tarification"),
    [
        (ServiceType.WALKING, Tarification.PER_HOUR),
        (ServiceType.BOARDING, Tarification.PER_HOUR),
        (ServiceType.BOARDING, Tarification.PER_DAY),
    ],
)
def test_allowed_pairs_are_accepted(
    service_type: ServiceType, tarification: Tarification
) -> None:
    """Передержка бывает и почасовой, и посуточной: собаку необязательно оставлять."""
    assert ServiceOfferFactory(
        service_type=service_type, tarification=tarification
    )
