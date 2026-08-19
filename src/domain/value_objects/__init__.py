"""Value objects домена DogCity."""

from src.domain.value_objects.account import (
    AccountStatus,
    BlockReason,
    VerificationRejectionReason,
    VerificationStatus,
)
from src.domain.value_objects.address import (
    BUILDING_MAX_LENGTH,
    CITY_MAX_LENGTH,
    STREET_MAX_LENGTH,
    Address,
)
from src.domain.value_objects.contacts import (
    EMAIL_MAX_LENGTH,
    NAME_MAX_LENGTH,
    PHONE_MAX_DIGITS,
    PHONE_MIN_DIGITS,
    Email,
    PersonName,
    PhoneNumber,
)
from src.domain.value_objects.identifiers import (
    AdminId,
    CorrelationId,
    EntityId,
    EventId,
    OrderId,
    OwnerId,
    PetId,
    ReviewId,
    SitterId,
)
from src.domain.value_objects.money import Currency, Money
from src.domain.value_objects.order_comment import (
    ORDER_COMMENT_MAX_LENGTH,
    OrderComment,
)
from src.domain.value_objects.order_party import OrderParty
from src.domain.value_objects.order_status import (
    CancellationReason,
    OrderStatus,
    RejectionReason,
)
from src.domain.value_objects.pet_profile import (
    BREED_MAX_LENGTH,
    MEDIUM_MAX_KG,
    PET_NAME_MAX_LENGTH,
    SMALL_MAX_KG,
    VACCINE_NAME_MAX_LENGTH,
    WEIGHT_MAX_KG,
    BehaviorTrait,
    BirthDate,
    Breed,
    DogSize,
    PetGender,
    PetName,
    VaccinationCertificate,
    Weight,
)
from src.domain.value_objects.rating import (
    RATING_MAX,
    RATING_MIN,
    AggregatedRating,
    Rating,
)
from src.domain.value_objects.review import REVIEW_TEXT_MAX_LENGTH, ReviewText
from src.domain.value_objects.service import (
    ServiceFormat,
    ServiceOffer,
    ServiceType,
    Tarification,
)
from src.domain.value_objects.sitter_profile import (
    CAPACITY_MAX,
    AcceptedDogSizes,
    Capacity,
)
from src.domain.value_objects.time_interval import TimeInterval

__all__ = (
    "BREED_MAX_LENGTH",
    "BUILDING_MAX_LENGTH",
    "CAPACITY_MAX",
    "CITY_MAX_LENGTH",
    "EMAIL_MAX_LENGTH",
    "MEDIUM_MAX_KG",
    "NAME_MAX_LENGTH",
    "ORDER_COMMENT_MAX_LENGTH",
    "PET_NAME_MAX_LENGTH",
    "PHONE_MAX_DIGITS",
    "PHONE_MIN_DIGITS",
    "RATING_MAX",
    "RATING_MIN",
    "REVIEW_TEXT_MAX_LENGTH",
    "SMALL_MAX_KG",
    "STREET_MAX_LENGTH",
    "VACCINE_NAME_MAX_LENGTH",
    "WEIGHT_MAX_KG",
    "AcceptedDogSizes",
    "AccountStatus",
    "Address",
    "AdminId",
    "AggregatedRating",
    "BehaviorTrait",
    "BirthDate",
    "BlockReason",
    "Breed",
    "CancellationReason",
    "Capacity",
    "CorrelationId",
    "Currency",
    "DogSize",
    "Email",
    "EntityId",
    "EventId",
    "Money",
    "OrderComment",
    "OrderId",
    "OrderParty",
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
    "ServiceFormat",
    "ServiceOffer",
    "ServiceType",
    "SitterId",
    "Tarification",
    "TimeInterval",
    "VaccinationCertificate",
    "VerificationRejectionReason",
    "VerificationStatus",
    "Weight",
)
