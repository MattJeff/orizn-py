"""Orizn Visa API client."""

from __future__ import annotations
import os
import sys
import warnings
from typing import Optional
import requests

from .types import VisaData, VisaCheckResult, Language
from .errors import OriznError, OriznAuthError, OriznRateLimitError, OriznNotFoundError

DEFAULT_BASE_URL = "https://visa.orizn.app"
DEFAULT_TIMEOUT = 10


class Orizn:
    """Client for the Orizn Visa API.

    Args:
        api_key: Your API key. Falls back to ORIZN_API_KEY env var.
        base_url: API base URL.
        timeout: Request timeout in seconds.

    Example:
        >>> client = Orizn()
        >>> result = client.check("FRA", "JPN")
        >>> print(result.requirement)  # "visa_free"
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self.api_key = api_key or os.environ.get("ORIZN_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "orizn-py/1.0.0"
        self._session.headers["Accept"] = "application/json"

        if not self.api_key and not getattr(Orizn, "_hinted", False):
            Orizn._hinted = True
            print(
                "[orizn] No API key found. Free mode: quick checks only.\n"
                "[orizn] Get your free key → https://visa.orizn.app\n"
                '[orizn] Then pass it: Orizn(api_key="orizn_visa_...")',
                file=sys.stderr,
            )

    def check(self, passport: str, destination: str) -> VisaCheckResult:
        """Quick visa check. No API key needed."""
        data = self._get("/api/v1/visa/check", {
            "passport": passport.upper(),
            "destination": destination.upper(),
        }, auth=False)
        return VisaCheckResult.from_dict(data["data"])

    def get_visa(
        self, passport: str, destination: str, lang: Language = "en"
    ) -> VisaData:
        """Full visa details. Requires API key."""
        data = self._get("/api/v1/visa", {
            "passport": passport.upper(),
            "destination": destination.upper(),
            "lang": lang,
        }, auth=True)
        return VisaData.from_dict(data["data"])

    def bulk(self, passport: str, lang: Language = "en") -> list[VisaData]:
        """All destinations for a passport. Requires Pro plan."""
        data = self._get("/api/v1/visa/bulk", {
            "passport": passport.upper(),
            "lang": lang,
        }, auth=True)
        return [VisaData.from_dict(d) for d in data["data"]]

    def changes(
        self,
        passport: Optional[str] = None,
        destination: Optional[str] = None,
    ) -> list[dict]:
        """Recent policy changes. Requires Starter plan."""
        params: dict[str, str] = {}
        if passport:
            params["passport"] = passport.upper()
        if destination:
            params["destination"] = destination.upper()
        data = self._get("/api/v1/visa/changes", params, auth=True)
        return data["data"]

    def stats(self) -> dict:
        """Coverage statistics. No API key needed."""
        return self._get("/api/v1/visa/stats", {}, auth=False)

    def _get(self, path: str, params: dict, auth: bool) -> dict:
        if auth and not self.api_key:
            raise OriznAuthError()

        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        try:
            resp = self._session.get(
                f"{self.base_url}{path}",
                params=params,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise OriznError("Request timed out", 0, "TIMEOUT")
        except requests.exceptions.ConnectionError:
            raise OriznError("Connection failed", 0, "CONNECTION_ERROR")

        if resp.status_code == 401 or resp.status_code == 403:
            raise OriznAuthError()
        if resp.status_code == 429:
            raise OriznRateLimitError()
        if resp.status_code == 404:
            raise OriznNotFoundError(
                params.get("passport", "?"),
                params.get("destination", "?"),
            )
        if not resp.ok:
            raise OriznError(f"API error: {resp.status_code}", resp.status_code, "API_ERROR")

        return resp.json()
