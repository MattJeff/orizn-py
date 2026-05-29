"""Type definitions for Orizn Visa API."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Optional, Any

VisaRequirement = Literal[
    "visa_free", "visa_required", "e_visa",
    "visa_on_arrival", "eta", "no_admission"
]

Language = Literal[
    "en", "fr", "es", "pt", "de",
    "ja", "ko", "zh", "ru", "it",
    "ar", "hi", "th", "vi", "tl"
]


# ─── Core ─────────────────────────────────────────────────────────────────

@dataclass
class CountryInfo:
    currency: str
    language: str
    timezone: str
    capital: str


# ─── Transit ──────────────────────────────────────────────────────────────

@dataclass
class TransitHub:
    airport: str
    city: str
    transit_visa_required: bool
    transit_free_hours: int
    conditions: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "TransitHub":
        return cls(
            airport=d.get("airport", ""),
            city=d.get("city", ""),
            transit_visa_required=d.get("transit_visa_required", False),
            transit_free_hours=d.get("transit_free_hours", 0),
            conditions=d.get("conditions"),
        )


@dataclass
class TransitVisa:
    hubs: list[TransitHub] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "TransitVisa":
        return cls(hubs=[TransitHub.from_dict(h) for h in d.get("hubs", [])])


# ─── Fees & processing ────────────────────────────────────────────────────

@dataclass
class MoneyAmount:
    amount: float
    currency: str

    @classmethod
    def from_dict(cls, d: dict) -> "MoneyAmount":
        return cls(amount=d.get("amount", 0), currency=d.get("currency", ""))


@dataclass
class VisaFee:
    single_entry: Optional[MoneyAmount] = None
    multiple_entry: Optional[MoneyAmount] = None

    @classmethod
    def from_dict(cls, d: dict) -> "VisaFee":
        return cls(
            single_entry=MoneyAmount.from_dict(d["single_entry"]) if d.get("single_entry") else None,
            multiple_entry=MoneyAmount.from_dict(d["multiple_entry"]) if d.get("multiple_entry") else None,
        )


@dataclass
class ProcessingDays:
    standard: Optional[int] = None
    express: Optional[int] = None
    rush: Optional[int] = None

    @classmethod
    def from_dict(cls, d: dict) -> "ProcessingDays":
        return cls(standard=d.get("standard"), express=d.get("express"), rush=d.get("rush"))


# ─── Photo & documents ────────────────────────────────────────────────────

@dataclass
class PhotoSpecs:
    width_mm: Optional[float] = None
    height_mm: Optional[float] = None
    background: Optional[str] = None
    glasses_allowed: Optional[bool] = None
    head_covering_allowed: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "PhotoSpecs":
        return cls(
            width_mm=d.get("width_mm"),
            height_mm=d.get("height_mm"),
            background=d.get("background"),
            glasses_allowed=d.get("glasses_allowed"),
            head_covering_allowed=d.get("head_covering_allowed"),
        )


# ─── Insurance & health ───────────────────────────────────────────────────

@dataclass
class InsuranceRequired:
    required: Optional[bool] = None
    min_coverage: Optional[float] = None
    currency: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "InsuranceRequired":
        return cls(
            required=d.get("required"),
            min_coverage=d.get("min_coverage"),
            currency=d.get("currency"),
        )


@dataclass
class HealthRequirements:
    covid_test: Optional[bool] = None
    vaccination_proof: Optional[bool] = None
    health_declaration: Optional[bool] = None
    quarantine_days: Optional[int] = None
    ebola_screening: Optional[bool] = None

    @classmethod
    def from_dict(cls, d: dict) -> "HealthRequirements":
        return cls(
            covid_test=d.get("covid_test"),
            vaccination_proof=d.get("vaccination_proof"),
            health_declaration=d.get("health_declaration"),
            quarantine_days=d.get("quarantine_days"),
            ebola_screening=d.get("ebola_screening"),
        )


# ─── Travelers & rules ────────────────────────────────────────────────────

@dataclass
class MinorRules:
    solo_travel_min_age: Optional[int] = None
    single_parent_letter_required: Optional[bool] = None
    notarized_consent_required: Optional[bool] = None

    @classmethod
    def from_dict(cls, d: dict) -> "MinorRules":
        return cls(
            solo_travel_min_age=d.get("solo_travel_min_age"),
            single_parent_letter_required=d.get("single_parent_letter_required"),
            notarized_consent_required=d.get("notarized_consent_required"),
        )


@dataclass
class OverstayPenalty:
    fine_per_day: Optional[str] = None
    ban_days: Optional[int] = None
    criminal: Optional[bool] = None
    details: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "OverstayPenalty":
        return cls(
            fine_per_day=d.get("fine_per_day"),
            ban_days=d.get("ban_days"),
            criminal=d.get("criminal"),
            details=d.get("details"),
        )


@dataclass
class EntryByMode:
    air: Optional[int] = None
    land: Optional[int] = None
    sea: Optional[int] = None

    @classmethod
    def from_dict(cls, d: dict) -> "EntryByMode":
        return cls(air=d.get("air"), land=d.get("land"), sea=d.get("sea"))


@dataclass
class RemoteWorkVisa:
    available: Optional[bool] = None
    duration_months: Optional[int] = None
    fee: Optional[MoneyAmount] = None
    requirements: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "RemoteWorkVisa":
        return cls(
            available=d.get("available"),
            duration_months=d.get("duration_months"),
            fee=MoneyAmount.from_dict(d["fee"]) if d.get("fee") else None,
            requirements=d.get("requirements", []),
        )


@dataclass
class ExtensionRules:
    possible: Optional[bool] = None
    max_days: Optional[int] = None
    fee: Optional[str] = None
    where: Optional[str] = None
    notes: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "ExtensionRules":
        return cls(
            possible=d.get("possible"),
            max_days=d.get("max_days"),
            fee=d.get("fee"),
            where=d.get("where"),
            notes=d.get("notes"),
        )


@dataclass
class ReciprocityChange:
    date: str
    from_status: str
    to_status: str
    note: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "ReciprocityChange":
        return cls(
            date=d.get("date", ""),
            from_status=d.get("from", ""),
            to_status=d.get("to", ""),
            note=d.get("note"),
        )


@dataclass
class SafetyInfo:
    level: Optional[int] = None
    advisory: Optional[str] = None
    source: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "SafetyInfo":
        return cls(
            level=d.get("level"),
            advisory=d.get("advisory"),
            source=d.get("source"),
            updated_at=d.get("updated_at"),
        )


# ─── Embassies ────────────────────────────────────────────────────────────

@dataclass
class EmbassyInfo:
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    emergency_phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "EmbassyInfo":
        return cls(
            name=d.get("name"),
            address=d.get("address"),
            city=d.get("city"),
            phone=d.get("phone"),
            emergency_phone=d.get("emergency_phone"),
            email=d.get("email"),
            website=d.get("website"),
        )


@dataclass
class EmbassyData:
    """Embassy contact info for emergencies and visa applications."""
    your_embassy_at_destination: Optional[EmbassyInfo] = None
    """Your country's embassy at the destination (emergency help)."""
    visa_application_embassy: Optional[EmbassyInfo] = None
    """Destination country's embassy in your country (where to apply for visa)."""

    @classmethod
    def from_dict(cls, d: dict) -> "EmbassyData":
        return cls(
            your_embassy_at_destination=EmbassyInfo.from_dict(d["your_embassy_at_destination"])
                if d.get("your_embassy_at_destination") else None,
            visa_application_embassy=EmbassyInfo.from_dict(d["visa_application_embassy"])
                if d.get("visa_application_embassy") else None,
        )


# ─── Main visa data ───────────────────────────────────────────────────────

@dataclass
class VisaData:
    # Core (always present)
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

    # Extended intelligence (optional)
    embassy: Optional[EmbassyData] = None
    transit_visa: Optional[TransitVisa] = None
    passport_validity_months: Optional[int] = None
    visa_fee: Optional[VisaFee] = None
    processing_days: Optional[ProcessingDays] = None
    photo_specs: Optional[PhotoSpecs] = None
    vaccinations_required: list[str] = field(default_factory=list)
    insurance_required: Optional[InsuranceRequired] = None
    dual_nationality_warnings: list[str] = field(default_factory=list)
    stamp_warnings: list[str] = field(default_factory=list)
    minor_rules: Optional[MinorRules] = None
    overstay_penalty: Optional[OverstayPenalty] = None
    entry_by_mode: Optional[EntryByMode] = None
    remote_work_visa: Optional[RemoteWorkVisa] = None
    extension_rules: Optional[ExtensionRules] = None
    reciprocity_history: list[ReciprocityChange] = field(default_factory=list)
    safety: Optional[SafetyInfo] = None
    best_apply_period: Optional[str] = None
    health_requirements: Optional[HealthRequirements] = None

    @classmethod
    def from_dict(cls, d: dict) -> "VisaData":
        def _opt(key: str, ctor: Any) -> Any:
            v = d.get(key)
            return ctor.from_dict(v) if v else None

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
            embassy=_opt("embassy", EmbassyData),
            transit_visa=_opt("transit_visa", TransitVisa),
            passport_validity_months=d.get("passport_validity_months"),
            visa_fee=_opt("visa_fee", VisaFee),
            processing_days=_opt("processing_days", ProcessingDays),
            photo_specs=_opt("photo_specs", PhotoSpecs),
            vaccinations_required=d.get("vaccinations_required", []),
            insurance_required=_opt("insurance_required", InsuranceRequired),
            dual_nationality_warnings=d.get("dual_nationality_warnings", []),
            stamp_warnings=d.get("stamp_warnings", []),
            minor_rules=_opt("minor_rules", MinorRules),
            overstay_penalty=_opt("overstay_penalty", OverstayPenalty),
            entry_by_mode=_opt("entry_by_mode", EntryByMode),
            remote_work_visa=_opt("remote_work_visa", RemoteWorkVisa),
            extension_rules=_opt("extension_rules", ExtensionRules),
            reciprocity_history=[ReciprocityChange.from_dict(r) for r in d.get("reciprocity_history", [])],
            safety=_opt("safety", SafetyInfo),
            best_apply_period=d.get("best_apply_period"),
            health_requirements=_opt("health_requirements", HealthRequirements),
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
