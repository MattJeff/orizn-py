# orizn

Official Python SDK for the [Orizn Visa API](https://visa.orizn.app).

Check visa requirements for **39,585 passport-destination pairs** in **15 languages**, with **32 data points per visa** — fees, processing times, photo specs, transit visas, embassies, overstay penalties, safety advisories, and more.

## Install

```bash
pip install orizn
```

## Quick start

```python
from orizn import Orizn

# No API key needed for quick checks
client = Orizn()
result = client.check("FRA", "JPN")
print(result.requirement)    # "visa_free"
print(result.visa_free_days) # 90

# Full details (get free key at visa.orizn.app)
client = Orizn(api_key="your-key")
visa = client.get_visa("USA", "CHN", lang="fr")
print(visa.documents_required)
print(visa.process)
print(visa.tips)
```

## Methods

| Method | Auth | Description |
|--------|------|-------------|
| `check(passport, destination)` | None | Quick visa check |
| `get_visa(passport, destination, lang?)` | Key | Full details (32 data points) |
| `bulk(passport, lang?)` | Key (Pro) | All destinations |
| `changes(passport?, destination?)` | Key (Starter) | Policy changes |
| `stats()` | None | Coverage stats |

## What's in `get_visa()`: 32 data points

Every full visa response now includes the following fields. Anything not relevant to a given pair is `None` or omitted (e.g. `remote_work_visa` only appears when a digital nomad visa exists).

### Core (always present)

| Field | Type | Description |
|---|---|---|
| `passport` | `str` | ISO 3166-1 alpha-3 (e.g. `"FRA"`) |
| `destination` | `str` | ISO 3166-1 alpha-3 (e.g. `"JPN"`) |
| `requirement` | `VisaRequirement` | `visa_free` \| `visa_required` \| `e_visa` \| `visa_on_arrival` \| `eta` \| `no_admission` |
| `visa_free_days` | `int \| None` | Max stay in days for visa-free travel |
| `visa_required` | `bool` | True if any visa formality is needed |
| `description` | `str` | Localized human-readable summary |
| `documents_required` | `list[str]` | Documents to bring/submit |
| `process` | `list[str]` | Step-by-step application process |
| `tips` | `list[str]` | Travel tips |
| `country_info` | `CountryInfo` | Currency, language, timezone, capital |
| `verified` | `bool` | Verified against an official source |

### Extended intelligence (optional)

| Field | Type | What it tells you |
|---|---|---|
| `transit_visa` | `TransitVisa` | Transit visa rules + free transit hours at top hubs (DXB, IST, DOH, SIN, ...) |
| `passport_validity_months` | `int` | Minimum passport validity required at entry (typically 3 or 6) |
| `visa_fee` | `VisaFee` | Cost of single-entry and multiple-entry visas, with currency |
| `processing_days` | `ProcessingDays` | Standard / express / rush processing times |
| `photo_specs` | `PhotoSpecs` | Dimensions in mm, background color, glasses & head covering rules |
| `vaccinations_required` | `list[str]` | Mandatory vaccines (e.g. `"yellow_fever"`) |
| `insurance_required` | `InsuranceRequired` | Min travel insurance coverage required |
| `dual_nationality_warnings` | `list[str]` | Warnings for dual-nationals (e.g. mandatory military service) |
| `stamp_warnings` | `list[str]` | Passport stamps that may block entry (e.g. Israeli stamp in some countries) |
| `minor_rules` | `MinorRules` | Rules for travelers under 18 (consent letters, solo travel age) |
| `overstay_penalty` | `OverstayPenalty` | Fine per day, ban duration, criminal liability |
| `entry_by_mode` | `EntryByMode` | Different stay limits for `air` / `land` / `sea` arrivals |
| `remote_work_visa` | `RemoteWorkVisa` | Digital nomad visa availability, duration, fee, requirements |
| `extension_rules` | `ExtensionRules` | Whether the stay can be extended, max days, fee, where |
| `reciprocity_history` | `list[ReciprocityChange]` | Historical policy changes between the two countries |
| `safety` | `SafetyInfo` | Travel advisory level (1–4) with source and last update |
| `best_apply_period` | `str` | Recommended window to apply (e.g. `"30–90 days before"`) |
| `health_requirements` | `HealthRequirements` | COVID test, vaccination proof, quarantine days, screenings |
| `embassy` | `EmbassyData` | Your embassy at destination (emergency) + destination's embassy in your country (where to apply) |

### Example: using the extended fields

```python
from orizn import Orizn

client = Orizn(api_key="your-key")
visa = client.get_visa("FRA", "JPN", lang="en")

# Cost & timing
if visa.visa_fee and visa.visa_fee.single_entry:
    print(f"Single entry: {visa.visa_fee.single_entry.amount} {visa.visa_fee.single_entry.currency}")

if visa.processing_days:
    print(f"Standard: {visa.processing_days.standard} days")

# Transit
if visa.transit_visa:
    for hub in visa.transit_visa.hubs:
        print(f"{hub.airport} ({hub.city}): {hub.transit_free_hours}h transit-free")

# Health & safety
if visa.health_requirements:
    print(f"COVID test: {visa.health_requirements.covid_test}")
if visa.safety:
    print(f"Advisory level: {visa.safety.level}")

# Penalties
if visa.overstay_penalty:
    print(f"Overstay fine: {visa.overstay_penalty.fine_per_day}")
print(f"Passport validity: {visa.passport_validity_months} months")

# Remote work
if visa.remote_work_visa and visa.remote_work_visa.available:
    print(f"Digital nomad visa: {visa.remote_work_visa.duration_months} months")

# Embassy
if visa.embassy and visa.embassy.your_embassy_at_destination:
    e = visa.embassy.your_embassy_at_destination
    print(f"Emergency: {e.name} — {e.emergency_phone}")
```

All types are exported — `from orizn import VisaData, TransitVisa, EmbassyData, ...`.

## Feedback

Building a travel agent or visa tool? We'd love to hear what you're building.

→ **api@orizn.app** — Feature requests, partnerships, and questions welcome.

## Links

- [Get free API key](https://visa.orizn.app)
- [API Docs](https://visa.orizn.app/visa-api/dashboard/docs)
- [MCP Server](https://github.com/MattJeff/orizn-mcp-server)
- [npm SDK](https://www.npmjs.com/package/orizn)
