"""Value objects домена DogCity.

Все типы — ``frozen`` dataclass'ы и ``StrEnum``: неизменяемые бизнес-значения
без идентичности.
"""

from src.domain.value_objects.account import AccountStatus
from src.domain.value_objects.address import Address
from src.domain.value_objects.contacts import Email, PersonName, PhoneNumber
from src.domain.value_objects.identifiers import (
    AdminId,
    EntityId,
    OrderId,
    OwnerId,
    PetId,
    ReviewId,
    SitterId,
)
from src.domain.value_objects.money import Currency, Money
from src.domain.value_objects.order_status import (
    CancellationReason,
    OrderStatus,
    RejectionReason,
)
from src.domain.value_objects.pet_profile import (
    Breed,
    DogSize,
    PetGender,
    PetName,
    VaccinationCertificate,
    Weight,
)
from src.domain.value_objects.rating import AggregatedRating, Rating
from src.domain.value_objects.review import ReviewText
from src.domain.value_objects.service import ServiceOffer, ServiceType, Tarification
from src.domain.value_objects.sitter_profile import VerificationStatus
from src.domain.value_objects.time_interval import TimeInterval

__all__ = (
    "AccountStatus",
    "Address",
    "AdminId",
    "AggregatedRating",
    "Breed",
    "CancellationReason",
    "Currency",
    "DogSize",
    "Email",
    "EntityId",
    "Money",
    "OrderId",
    "OrderStatus",
    "OwnerId",
    "PersonName",
    "PetGender",
    "PetId",
    "PetName",
    "PhoneNumber",
    "Rating",
    "RejectionReason",
    "ReviewId",
    "ReviewText",
    "ServiceOffer",
    "ServiceType",
    "SitterId",
    "Tarification",
    "TimeInterval",
    "VaccinationCertificate",
    "VerificationStatus",
    "Weight",
)
