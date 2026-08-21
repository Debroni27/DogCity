"""Тесты агрегата догситтера."""

import pytest

from src.domain.aggregates import Sitter
from src.domain.events import (
    AcceptedDogSizesChanged,
    CapacityChanged,
    OfferWithdrawn,
    SitterAddressChanged,
    SitterContactsChanged,
    SitterRegistered,
)
from src.domain.exceptions import InvariantViolationError
from src.domain.value_objects import (
    Capacity,
    CorrelationId,
    DogSize,
    Money,
    Rating,
    ServiceFormat,
    ServiceOffer,
    ServiceType,
    Tarification,
)
from tests.domain.aggregates.sitter.factories import SitterFactory
from tests.domain.events.factories import OCCURRED_AT
from tests.domain.value_objects.address.factories import AddressFactory
from tests.domain.value_objects.contacts.factories import (
    EmailFactory,
    PersonNameFactory,
    PhoneNumberFactory,
)
from tests.domain.value_objects.sitter_profile.factories import AcceptedDogSizesFactory

INDIVIDUAL_OFFER = ServiceOffer(
    service_type=ServiceType.BOARDING,
    price=Money(3000),
    tarification=Tarification.PER_DAY,
    service_format=ServiceFormat.INDIVIDUAL,
)


def test_registration_lays_out_the_sitter(sitter: Sitter) -> None:
    """Первое событие раскладывается по полям догситтера."""
    (event,) = sitter.pending_events
    assert isinstance(event, SitterRegistered)
    assert sitter.sitter_id == event.sitter_id
    assert sitter.capacity == event.capacity
    assert sitter.accepted_dog_sizes == event.accepted_dog_sizes


def test_fresh_sitter_has_no_offers_and_no_reviews(sitter: Sitter) -> None:
    """Только что зарегистрированный догситтер ничего не предлагает и не оценён."""
    assert sitter.offers == ()
    assert sitter.rating.average is None


def test_published_offer_joins_the_catalogue(
    sitter: Sitter, shared_offer: ServiceOffer
) -> None:
    """Выставленное предложение попадает в перечень услуг."""
    sitter.publish_offer(shared_offer, OCCURRED_AT, CorrelationId.new())
    assert sitter.offers == (shared_offer,)


def test_offers_differ_by_format(sitter: Sitter, shared_offer: ServiceOffer) -> None:
    """Групповое и индивидуальное предложения одной услуги живут раздельно."""
    sitter.publish_offer(shared_offer, OCCURRED_AT, CorrelationId.new())
    sitter.publish_offer(INDIVIDUAL_OFFER, OCCURRED_AT, CorrelationId.new())
    assert len(sitter.offers) == 2


def test_withdrawn_offer_leaves_the_catalogue(
    sitter: Sitter, shared_offer: ServiceOffer
) -> None:
    """Снятое предложение исчезает из перечня."""
    sitter.publish_offer(shared_offer, OCCURRED_AT, CorrelationId.new())
    sitter.withdraw_offer(
        shared_offer.service_type,
        shared_offer.tarification,
        shared_offer.service_format,
        OCCURRED_AT,
        CorrelationId.new(),
    )
    assert sitter.offers == ()
    assert isinstance(sitter.pending_events[-1], OfferWithdrawn)


def test_unknown_offer_cannot_be_withdrawn(sitter: Sitter) -> None:
    """Снять можно только выставленное предложение."""
    with pytest.raises(InvariantViolationError):
        sitter.withdraw_offer(
            ServiceType.WALKING,
            Tarification.PER_HOUR,
            ServiceFormat.SHARED,
            OCCURRED_AT,
            CorrelationId.new(),
        )


def test_individual_offer_needs_room_for_more_than_one_dog() -> None:
    """Догситтер на одну собаку продавал бы за наценку то, что делает всегда."""
    sitter = SitterFactory(capacity=Capacity(1))
    with pytest.raises(InvariantViolationError):
        sitter.publish_offer(INDIVIDUAL_OFFER, OCCURRED_AT, CorrelationId.new())


def test_capacity_of_one_is_refused_while_individual_offer_stands(
    sitter: Sitter,
) -> None:
    """Инвариант держится и с другой стороны: вместимость нельзя срезать до одного."""
    sitter.publish_offer(INDIVIDUAL_OFFER, OCCURRED_AT, CorrelationId.new())
    with pytest.raises(InvariantViolationError):
        sitter.change_capacity(Capacity(1), OCCURRED_AT, CorrelationId.new())


def test_capacity_of_one_is_allowed_without_individual_offers(sitter: Sitter) -> None:
    """Без индивидуальных предложений вместимость свободно опускается до одного."""
    sitter.change_capacity(Capacity(1), OCCURRED_AT, CorrelationId.new())
    assert sitter.capacity == Capacity(1)
    assert isinstance(sitter.pending_events[-1], CapacityChanged)


def test_accepted_sizes_are_replaced_wholesale(sitter: Sitter) -> None:
    """Набор принимаемых размеров меняется целиком."""
    sizes = AcceptedDogSizesFactory(values=frozenset({DogSize.LARGE}))
    sitter.change_accepted_dog_sizes(sizes, OCCURRED_AT, CorrelationId.new())
    assert sitter.accepted_dog_sizes.accepts(DogSize.LARGE)
    assert not sitter.accepted_dog_sizes.accepts(DogSize.SMALL)
    assert isinstance(sitter.pending_events[-1], AcceptedDogSizesChanged)


def test_review_moves_the_rating(sitter: Sitter) -> None:
    """Полученный отзыв пересчитывает сводную оценку."""
    sitter.receive_review(Rating(4), OCCURRED_AT, CorrelationId.new())
    assert sitter.rating.reviews_count == 1
    assert sitter.rating.average == 4


def test_contacts_change_is_recorded(sitter: Sitter) -> None:
    """Смена контактов оставляет след в потоке событий."""
    sitter.change_contacts(
        PersonNameFactory(),
        PhoneNumberFactory(),
        EmailFactory(),
        OCCURRED_AT,
        CorrelationId.new(),
    )
    assert isinstance(sitter.pending_events[-1], SitterContactsChanged)


def test_address_change_is_recorded(sitter: Sitter) -> None:
    """Смена адреса оставляет след в потоке событий."""
    sitter.change_address(AddressFactory(), OCCURRED_AT, CorrelationId.new())
    assert isinstance(sitter.pending_events[-1], SitterAddressChanged)


def test_events_are_forgotten_once_taken(sitter: Sitter) -> None:
    """После выгрузки прикладным слоем агрегат событий не хранит."""
    sitter.clear_events()
    assert sitter.pending_events == ()
