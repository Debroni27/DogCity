"""Тесты агрегата владельца питомцев."""

from decimal import Decimal

import pytest

from src.domain.aggregates import PETS_MAX, Owner
from src.domain.events import (
    OwnerAddressChanged,
    OwnerContactsChanged,
    OwnerRegistered,
    PetRemoved,
)
from src.domain.exceptions import InvariantViolationError
from src.domain.value_objects import (
    BehaviorTrait,
    CorrelationId,
    DogSize,
    PetId,
    Rating,
    VaccinationCertificate,
    Weight,
)
from tests.domain.aggregates.owner.factories import add_pet
from tests.domain.events.factories import OCCURRED_AT
from tests.domain.value_objects.address.factories import AddressFactory
from tests.domain.value_objects.contacts.factories import (
    EmailFactory,
    PersonNameFactory,
    PhoneNumberFactory,
)


def test_registration_lays_out_the_owner(owner: Owner) -> None:
    """Первое событие раскладывается по полям владельца."""
    (event,) = owner.pending_events
    assert isinstance(event, OwnerRegistered)
    assert owner.owner_id == event.owner_id


def test_fresh_owner_has_no_pets_and_no_reviews(owner: Owner) -> None:
    """Аккаунт заводится до питомцев, оценок у нового владельца нет."""
    assert owner.pets == ()
    assert owner.rating.average is None


def test_added_pet_belongs_to_the_owner(owner: Owner) -> None:
    """Заведённый питомец принадлежит владельцу."""
    pet_id = add_pet(owner)
    assert owner.has_pet(pet_id)
    assert len(owner.pets) == 1


def test_stranger_pet_does_not_belong_to_the_owner(owner: Owner) -> None:
    """Чужой питомец владельцу не принадлежит."""
    add_pet(owner)
    assert not owner.has_pet(PetId.new())


def test_pets_are_limited_in_number(owner: Owner) -> None:
    """Питомцев у владельца не больше предельного числа."""
    for _ in range(PETS_MAX):
        add_pet(owner)
    with pytest.raises(InvariantViolationError):
        add_pet(owner)


def test_same_pet_cannot_be_added_twice(owner: Owner) -> None:
    """Повторное заведение того же питомца отвергается."""
    pet_id = add_pet(owner)
    with pytest.raises(InvariantViolationError):
        add_pet(owner, pet_id=pet_id)


def test_removed_pet_leaves_the_owner(owner: Owner) -> None:
    """Удалённый питомец исчезает у владельца."""
    pet_id = add_pet(owner)
    owner.remove_pet(pet_id, OCCURRED_AT, CorrelationId.new())
    assert not owner.has_pet(pet_id)
    assert isinstance(owner.pending_events[-1], PetRemoved)


def test_unknown_pet_cannot_be_removed(owner: Owner) -> None:
    """Удалить можно только своего питомца."""
    with pytest.raises(InvariantViolationError):
        owner.remove_pet(PetId.new(), OCCURRED_AT, CorrelationId.new())


def test_updated_weight_changes_the_size_category(owner: Owner) -> None:
    """Вес хранится, размерная категория выводится из него заново."""
    pet_id = add_pet(owner)
    owner.update_pet_weight(
        pet_id, Weight(Decimal("40")), OCCURRED_AT, CorrelationId.new()
    )
    (pet,) = owner.pets
    assert pet.weight == Weight(Decimal("40"))
    assert DogSize.from_weight(pet.weight) is DogSize.LARGE


def test_weight_of_unknown_pet_cannot_be_updated(owner: Owner) -> None:
    """Уточнять вес можно только своему питомцу."""
    with pytest.raises(InvariantViolationError):
        owner.update_pet_weight(
            PetId.new(), Weight(Decimal("10")), OCCURRED_AT, CorrelationId.new()
        )


def test_vaccinations_accumulate(
    owner: Owner, certificate: VaccinationCertificate
) -> None:
    """Отметки о прививках копятся, а не замещают друг друга."""
    pet_id = add_pet(owner)
    owner.add_vaccination(pet_id, certificate, OCCURRED_AT, CorrelationId.new())
    owner.add_vaccination(pet_id, certificate, OCCURRED_AT, CorrelationId.new())
    (pet,) = owner.pets
    assert len(pet.vaccinations) == 2


def test_vaccination_of_unknown_pet_is_refused(
    owner: Owner, certificate: VaccinationCertificate
) -> None:
    """Прививку можно добавить только своему питомцу."""
    with pytest.raises(InvariantViolationError):
        owner.add_vaccination(
            PetId.new(), certificate, OCCURRED_AT, CorrelationId.new()
        )


def test_behavior_traits_are_replaced_wholesale(owner: Owner) -> None:
    """Набор особенностей поведения меняется целиком."""
    pet_id = add_pet(owner, behavior_traits=frozenset({BehaviorTrait.BARKS_A_LOT}))
    owner.update_pet_behavior(
        pet_id,
        frozenset({BehaviorTrait.AFRAID_OF_DOGS}),
        OCCURRED_AT,
        CorrelationId.new(),
    )
    (pet,) = owner.pets
    assert pet.behavior_traits == frozenset({BehaviorTrait.AFRAID_OF_DOGS})


def test_behavior_of_unknown_pet_cannot_be_updated(owner: Owner) -> None:
    """Уточнять поведение можно только своему питомцу."""
    with pytest.raises(InvariantViolationError):
        owner.update_pet_behavior(
            PetId.new(), frozenset(), OCCURRED_AT, CorrelationId.new()
        )


def test_review_moves_the_rating(owner: Owner) -> None:
    """Отзывы о владельце двусторонние: догситтер тоже оценивает."""
    owner.receive_review(Rating(3), OCCURRED_AT, CorrelationId.new())
    assert owner.rating.reviews_count == 1
    assert owner.rating.average == 3


def test_contacts_change_is_recorded(owner: Owner) -> None:
    """Смена контактов оставляет след в потоке событий."""
    owner.change_contacts(
        PersonNameFactory(),
        PhoneNumberFactory(),
        EmailFactory(),
        OCCURRED_AT,
        CorrelationId.new(),
    )
    assert isinstance(owner.pending_events[-1], OwnerContactsChanged)


def test_address_change_is_recorded(owner: Owner) -> None:
    """Смена адреса оставляет след в потоке событий."""
    owner.change_address(AddressFactory(), OCCURRED_AT, CorrelationId.new())
    assert isinstance(owner.pending_events[-1], OwnerAddressChanged)


def test_events_are_forgotten_once_taken(owner: Owner) -> None:
    """После выгрузки прикладным слоем агрегат событий не хранит."""
    owner.clear_events()
    assert owner.pending_events == ()
