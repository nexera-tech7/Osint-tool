"""Professional platform adapters."""

from __future__ import annotations

import httpx
from uscan.platforms.base import Platform
from uscan.scanner.models import ScanStatus, Confidence


class LinkedIn(Platform):
    name = "LinkedIn"
    category = "professional"
    url_pattern = "https://www.linkedin.com/in/{username}"
    username_regex = r"^[a-zA-Z0-9-]{3,100}$"
    min_length = 3
    max_length = 100
    follow_redirects = False

    def classify(self, response: httpx.Response) -> tuple[ScanStatus, Confidence]:
        if response.status_code == 404:
            return ScanStatus.NOT_FOUND, Confidence.HIGH
        if response.status_code in (301, 302, 303):
            location = response.headers.get("location", "")
            if "/authwall" in location or "/login" in location:
                return ScanStatus.UNKNOWN, Confidence.LOW
            if f"/in/" in location:
                return ScanStatus.FOUND, Confidence.LOW
        if response.status_code == 200:
            return ScanStatus.FOUND, Confidence.LOW
        if response.status_code == 999:
            return ScanStatus.BLOCKED, Confidence.HIGH
        return super().classify(response)


class Behance(Platform):
    name = "Behance"
    category = "professional"
    url_pattern = "https://www.behance.net/{username}"
    username_regex = r"^[a-zA-Z0-9_]{1,30}$"
    max_length = 30
    not_found_indicators = ["Oops! We can't find that page"]
    found_indicators = ["behance.net", "profile-card"]


class Dribbble(Platform):
    name = "Dribbble"
    category = "professional"
    url_pattern = "https://dribbble.com/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{1,20}$"
    max_length = 20
    not_found_indicators = ["Page not found"]
    found_indicators = ["dribbble.com", "profile-info", "bio"]


class Gravatar(Platform):
    name = "Gravatar"
    category = "professional"
    url_pattern = "https://gravatar.com/{username}"
    username_regex = r"^[a-zA-Z0-9._-]{1,30}$"
    max_length = 30
    not_found_indicators = ["Profile not found"]
    found_indicators = ["gravatar.com", "profile"]


class AboutMe(Platform):
    name = "About.me"
    category = "professional"
    url_pattern = "https://about.me/{username}"
    username_regex = r"^[a-zA-Z0-9._]{1,30}$"
    max_length = 30
    not_found_indicators = ["page not found", "This page is no longer available"]
    found_indicators = ["about.me", "profile"]


class Linktree(Platform):
    name = "Linktree"
    category = "professional"
    url_pattern = "https://linktr.ee/{username}"
    username_regex = r"^[a-zA-Z0-9._]{1,30}$"
    max_length = 30
    not_found_indicators = ["Nothing to see here"]
    found_indicators = ["linktr.ee", "profile"]


PROFESSIONAL_PLATFORMS: list[type[Platform]] = [
    LinkedIn, Behance, Dribbble, Gravatar, AboutMe, Linktree,
]
