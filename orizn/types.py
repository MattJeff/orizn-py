"""Type definitions for Orizn Visa API."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional

VisaRequirement = Literal[
    "visa_free", "visa_required", "e_visa",
    "visa_on_arrival", "eta", "no_admission"
]

Language = Literal[
    "en", "fr", "es", "pt", "de",
    "ja", "ko", "zh", "ru", "it",
    "ar", "hi", "th", "vi", "tl"
]


@dataclass
class CountryInfo:
    currency: str
    language: str
    timezone: str
    capital: str


@dataclass
class VisaData:
    passport: str
    destination: str
    requirement: VisaRequirement
    visa_free_days: Optional[int]
    visa_required: bool
    description: str
    documents_required: list[str]
    process: list[str]
    tips: list[str]
    country_info: CountryInfo
    verified: bool

    @classmethod
    def from_dict(cls, d: dict) -> "VisaData":
        return cls(
            passport=d["passport"],
            destination=d["destination"],
            requirement=d["requirement"],
            visa_free_days=d.get("visa_free_days"),
            visa_required=d["visa_required"],
            description=d.get("description", ""),
            documents_required=d.get("documents_required", []),
            process=d.get("process", []),
            tips=d.get("tips", []),
            country_info=CountryInfo(**d["country_info"]) if "country_info" in d else CountryInfo("", "", "", ""),
            verified=d.get("verified", False),
        )


@dataclass
class VisaCheckResult:
    passport: str
    destination: str
    requirement: VisaRequirement
    visa_free_days: Optional[int]
    visa_required: bool

    @classmethod
    def from_dict(cls, d: dict) -> "VisaCheckResult":
        return cls(
            passport=d["passport"],
            destination=d["destination"],
            requirement=d["requirement"],
            visa_free_days=d.get("visa_free_days"),
            visa_required=d["visa_required"],
        )
