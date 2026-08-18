"""Общие настройки тестов."""

import factory.random
import pytest

FAKER_SEED = 0


@pytest.fixture(autouse=True)
def _fixed_faker_seed() -> None:
    """Фиксирует данные фабрик, чтобы упавший тест воспроизводился."""
    factory.random.reseed_random(FAKER_SEED)
