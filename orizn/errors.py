"""Custom exceptions for Orizn SDK."""


class OriznError(Exception):
    def __init__(self, message: str, status_code: int = 0, code: str = "UNKNOWN"):
        super().__init__(message)
        self.status_code = status_code
        self.code = code


class OriznAuthError(OriznError):
    def __init__(self, message: str = "API key required. Get one free at https://visa.orizn.app"):
        super().__init__(message, 401, "AUTH_REQUIRED")


class OriznRateLimitError(OriznError):
    def __init__(self, message: str = "Rate limit exceeded. Upgrade at https://visa.orizn.app"):
        super().__init__(message, 429, "RATE_LIMIT")


class OriznNotFoundError(OriznError):
    def __init__(self, passport: str, destination: str):
        super().__init__(f"No visa data for {passport} \u2192 {destination}", 404, "NOT_FOUND")
