"""Base platform interface."""

from __future__ import annotations

import re

import httpx

from uscan.scanner.models import ScanStatus, Confidence


class Platform:
    """Base class for all platform adapters.

    Subclasses override class attributes. Lists are declared as tuples
    to avoid the mutable-default-shared-across-instances pitfall.
    """

    name: str = ""
    category: str = "other"
    url_pattern: str = ""
    follow_redirects: bool = True

    not_found_indicators: list[str] | tuple[str, ...] = ()
    found_indicators: list[str] | tuple[str, ...] = ()
    error_indicators: list[str] | tuple[str, ...] = ()

    username_regex: str = r"^[a-zA-Z0-9._-]+$"
    min_length: int = 1
    max_length: int = 64

    rate_limit_rps: float = 5.0

    def validate_username(self, username: str) -> bool:
        if len(username) < self.min_length or len(username) > self.max_length:
            return False
        return bool(re.match(self.username_regex, username))

    def build_url(self, username: str) -> str:
        return self.url_pattern.format(username=username)

    def classify(self, response: httpx.Response) -> tuple[ScanStatus, Confidence]:
        from uscan.scanner.classifier import ResponseClassifier
        return ResponseClassifier.classify(
            response.status_code,
            response.text,
            not_found_indicators=list(self.not_found_indicators),
            found_indicators=list(self.found_indicators),
            error_body_indicators=list(self.error_indicators),
        )

    def __repr__(self) -> str:
        return f"<Platform {self.name}>"
