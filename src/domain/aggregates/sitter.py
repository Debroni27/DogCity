"""Агрегат догситтера."""

from datetime import datetime

from src.domain.events import (
    AcceptedDogSizesChanged,
    CapacityChanged,
    OfferPublished,
    OfferWithdrawn,
    SitterAddressChanged,
    SitterContactsChanged,
    SitterEvent,
    SitterRegistered,
    SitterReviewReceived,
)
from src.domain.exceptions import InvariantViolationError
from src.domain.value_objects import (
    AcceptedDogSizes,
    Address,
    AggregatedRating,
    Capacity,
    CorrelationId,
    Email,
    EventId,
    PersonName,
    PhoneNumber,
    Rating,
    ServiceFormat,
    ServiceOffer,
    ServiceType,
    SitterId,
    Tarification,
)

__all__ = ("Sitter",)

type OfferKey = tuple[ServiceType, Tarification, ServiceFormat]


class Sitter:
    """Догситтер: профиль, ограничения на приём питомцев и предложения услуг."""

    __slots__ = (
        "_accepted_dog_sizes",
        "_address",
        "_capacity",
        "_email",
        "_name",
        "_offers",
        "_pending_events",
        "_phone",
        "_rating",
        "_sitter_id",
    )

    _sitter_id: SitterId
    _name: PersonName
    _phone: PhoneNumber
    _email: Email
    _address: Address
    _capacity: Capacity
    _accepted_dog_sizes: AcceptedDogSizes
    _offers: dict[OfferKey, ServiceOffer]
    _rating: AggregatedRating
    _pending_events: list[SitterEvent]

    def __init__(self) -> None:
        """Заготовка догситтера: состояние наполняет ``_apply``."""
        self._pending_events = []

    @property
    def sitter_id(self) -> SitterId:
        """Идентификатор догситтера."""
        return self._sitter_id

    @property
    def capacity(self) -> Capacity:
        """Сколько питомцев догситтер берёт одновременно."""
        return self._capacity

    @property
    def accepted_dog_sizes(self) -> AcceptedDogSizes:
        """Размеры собак, которых догситтер готов принять."""
        return self._accepted_dog_sizes

    @property
    def offers(self) -> tuple[ServiceOffer, ...]:
        """Выставленные предложения услуг."""
        return tuple(self._offers.values())

    @property
    def rating(self) -> AggregatedRating:
        """Сводная оценка догситтера по отзывам владельцев."""
        return self._rating

    @property
    def pending_events(self) -> tuple[SitterEvent, ...]:
        """События, накопленные с последнего ``clear_events``."""
        return tuple(self._pending_events)

    @classmethod
    def register(
        cls,
        *,
        sitter_id: SitterId,
        name: PersonName,
        phone: PhoneNumber,
        email: Email,
        address: Address,
        capacity: Capacity,
        accepted_dog_sizes: AcceptedDogSizes,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> "Sitter":
        """Догситтер заводит аккаунт с профилем и ограничениями на приём."""
        sitter = cls()
        sitter._record(
            SitterRegistered(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                sitter_id=sitter_id,
                name=name,
                phone=phone,
                email=email,
                address=address,
                capacity=capacity,
                accepted_dog_sizes=accepted_dog_sizes,
            )
        )
        return sitter

    def clear_events(self) -> None:
        """Забыть накопленные события: их забрал прикладной слой."""
        self._pending_events.clear()

    def change_contacts(
        self,
        name: PersonName,
        phone: PhoneNumber,
        email: Email,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> None:
        """Догситтер меняет контактные данные."""
        self._record(
            SitterContactsChanged(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                sitter_id=self._sitter_id,
                name=name,
                phone=phone,
                email=email,
            )
        )

    def change_address(
        self, address: Address, occurred_at: datetime, correlation_id: CorrelationId
    ) -> None:
        """Догситтер меняет адрес оказания услуг."""
        self._record(
            SitterAddressChanged(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                sitter_id=self._sitter_id,
                address=address,
            )
        )

    def change_capacity(
        self, capacity: Capacity, occurred_at: datetime, correlation_id: CorrelationId
    ) -> None:
        """Догситтер меняет число питомцев, которых берёт одновременно."""
        if capacity.value == 1 and self._has_individual_offer():
            raise InvariantViolationError(
                "вместимость в одного питомца обесценивает индивидуальные предложения"
            )
        self._record(
            CapacityChanged(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                sitter_id=self._sitter_id,
                capacity=capacity,
            )
        )

    def change_accepted_dog_sizes(
        self,
        accepted_dog_sizes: AcceptedDogSizes,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> None:
        """Догситтер меняет набор размеров собак, которых готов принять."""
        self._record(
            AcceptedDogSizesChanged(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                sitter_id=self._sitter_id,
                accepted_dog_sizes=accepted_dog_sizes,
            )
        )

    def publish_offer(
        self, offer: ServiceOffer, occurred_at: datetime, correlation_id: CorrelationId
    ) -> None:
        """Догситтер выставляет предложение услуги."""
        if (
            offer.service_format is ServiceFormat.INDIVIDUAL
            and self._capacity.value == 1
        ):
            raise InvariantViolationError(
                "индивидуальная услуга не продаётся при вместимости в одного питомца"
            )
        self._record(
            OfferPublished(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                sitter_id=self._sitter_id,
                service_type=offer.service_type,
                tarification=offer.tarification,
                service_format=offer.service_format,
                price=offer.price,
            )
        )

    def withdraw_offer(
        self,
        service_type: ServiceType,
        tarification: Tarification,
        service_format: ServiceFormat,
        occurred_at: datetime,
        correlation_id: CorrelationId,
    ) -> None:
        """Догситтер снимает выставленное предложение."""
        if (service_type, tarification, service_format) not in self._offers:
            raise InvariantViolationError("такого предложения у догситтера нет")
        self._record(
            OfferWithdrawn(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                sitter_id=self._sitter_id,
                service_type=service_type,
                tarification=tarification,
                service_format=service_format,
            )
        )

    def receive_review(
        self, rating: Rating, occurred_at: datetime, correlation_id: CorrelationId
    ) -> None:
        """О догситтере оставлен отзыв с оценкой, сводный рейтинг пересчитывается."""
        self._record(
            SitterReviewReceived(
                event_id=EventId.new(),
                occurred_at=occurred_at,
                correlation_id=correlation_id,
                sitter_id=self._sitter_id,
                rating=rating,
            )
        )

    def _has_individual_offer(self) -> bool:
        """Есть ли среди предложений индивидуальный формат."""
        return any(
            offer.service_format is ServiceFormat.INDIVIDUAL
            for offer in self._offers.values()
        )

    def _record(self, event: SitterEvent) -> None:
        """Применить событие и запомнить его для публикации."""
        self._apply(event)
        self._pending_events.append(event)

    def _apply(self, event: SitterEvent) -> None:
        """Единственное место, где меняется состояние догситтера."""
        match event:
            case SitterRegistered():
                self._sitter_id = event.sitter_id
                self._name = event.name
                self._phone = event.phone
                self._email = event.email
                self._address = event.address
                self._capacity = event.capacity
                self._accepted_dog_sizes = event.accepted_dog_sizes
                self._offers = {}
                self._rating = AggregatedRating.empty()
            case SitterContactsChanged():
                self._name = event.name
                self._phone = event.phone
                self._email = event.email
            case SitterAddressChanged():
                self._address = event.address
            case CapacityChanged():
                self._capacity = event.capacity
            case AcceptedDogSizesChanged():
                self._accepted_dog_sizes = event.accepted_dog_sizes
            case OfferPublished():
                self._offers[
                    (event.service_type, event.tarification, event.service_format)
                ] = ServiceOffer(
                    service_type=event.service_type,
                    price=event.price,
                    tarification=event.tarification,
                    service_format=event.service_format,
                )
            case OfferWithdrawn():
                self._offers.pop(
                    (event.service_type, event.tarification, event.service_format)
                )
            case SitterReviewReceived():
                self._rating = self._rating.with_review(event.rating)
