"""Orizn Visa API SDK — 39,585 passport-destination pairs in 15 languages."""

from .client import Orizn
from .types import VisaData, VisaCheckResult, CountryInfo, VisaRequirement, Language
from .errors import OriznError, OriznAuthError, OriznRateLimitError, OriznNotFoundError

__version__ = "1.0.0"
__all__ = [
    "Orizn",
    "VisaData", "VisaCheckResult", "CountryInfo",
    "VisaRequirement", "Language",
    "OriznError", "OriznAuthError", "OriznRateLimitError", "OriznNotFoundError",
]
