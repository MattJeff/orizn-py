"""Orizn Visa API SDK — 39,585 passport-destination pairs in 15 languages."""

from .client import Orizn
from .types import (
    VisaData, VisaCheckResult, CountryInfo, VisaRequirement, Language,
    # Extended intelligence (32 data points)
    TransitHub, TransitVisa,
    MoneyAmount, VisaFee, ProcessingDays,
    PhotoSpecs,
    InsuranceRequired, HealthRequirements,
    MinorRules, OverstayPenalty, EntryByMode,
    RemoteWorkVisa, ExtensionRules,
    ReciprocityChange, SafetyInfo,
    EmbassyInfo, EmbassyData,
)
from .errors import OriznError, OriznAuthError, OriznRateLimitError, OriznNotFoundError

__version__ = "1.1.0"
__all__ = [
    "Orizn",
    # Core
    "VisaData", "VisaCheckResult", "CountryInfo",
    "VisaRequirement", "Language",
    # Extended intelligence
    "TransitHub", "TransitVisa",
    "MoneyAmount", "VisaFee", "ProcessingDays",
    "PhotoSpecs",
    "InsuranceRequired", "HealthRequirements",
    "MinorRules", "OverstayPenalty", "EntryByMode",
    "RemoteWorkVisa", "ExtensionRules",
    "ReciprocityChange", "SafetyInfo",
    "EmbassyInfo", "EmbassyData",
    # Errors
    "OriznError", "OriznAuthError", "OriznRateLimitError", "OriznNotFoundError",
]
