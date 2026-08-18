"""События домена DogCity."""

from src.domain.events.account_moderation import (
    AccountBlocked,
    AccountDeleted,
    AccountUnblocked,
    AccountVerified,
    DocumentsSubmitted,
    ModerationOpened,
    VerificationRejected,
)
from src.domain.events.base import DomainEvent
from src.domain.events.order import (
    OrderCancelled,
    OrderCompleted,
    OrderConfirmed,
    OrderPlaced,
    OrderRejected,
    OrderStarted,
)
from src.domain.events.owner import (
    OwnerAddressChanged,
    OwnerContactsChanged,
    OwnerRegistered,
    OwnerReviewReceived,
    PetAdded,
    PetRemoved,
    PetWeightUpdated,
    VaccinationAdded,
)
from src.domain.events.review import ReviewPublished
from src.domain.events.sitter import (
    OfferPublished,
    OfferWithdrawn,
    SitterAddressChanged,
    SitterContactsChanged,
    SitterRegistered,
    SitterReviewReceived,
)
from src.domain.events.sitter_schedule import BookingReleased, BookingReserved

__all__ = (
    "AccountBlocked",
    "AccountDeleted",
    "AccountUnblocked",
    "AccountVerified",
    "BookingReleased",
    "BookingReserved",
    "DocumentsSubmitted",
    "DomainEvent",
    "ModerationOpened",
    "OfferPublished",
    "OfferWithdrawn",
    "OrderCancelled",
    "OrderCompleted",
    "OrderConfirmed",
    "OrderPlaced",
    "OrderRejected",
    "OrderStarted",
    "OwnerAddressChanged",
    "OwnerContactsChanged",
    "OwnerRegistered",
    "OwnerReviewReceived",
    "PetAdded",
    "PetRemoved",
    "PetWeightUpdated",
    "ReviewPublished",
    "SitterAddressChanged",
    "SitterContactsChanged",
    "SitterRegistered",
    "SitterReviewReceived",
    "VaccinationAdded",
    "VerificationRejected",
)
