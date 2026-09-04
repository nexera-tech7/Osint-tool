"""Developer platform adapters."""

from __future__ import annotations

import httpx
from uscan.platforms.base import Platform
from uscan.scanner.models import ScanStatus, Confidence


class GitHub(Platform):
    name = "GitHub"
    category = "developer"
    url_pattern = "https://github.com/{username}"
    username_regex = r"^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?$"
    max_length = 39
    not_found_indicators = ["Not Found"]
    found_indicators = ["github.com", "avatar", "repositories"]


class GitLab(Platform):
    name = "GitLab"
    category = "developer"
    url_pattern = "https://gitlab.com/{username}"
    username_regex = r"^[a-zA-Z0-9._-]{2,255}$"
    min_length = 2
    not_found_indicators = ["Page Not Found"]
    found_indicators = ["gitlab.com", "user-avatar"]


class Bitbucket(Platform):
    name = "Bitbucket"
    category = "developer"
    url_pattern = "https://bitbucket.org/{username}/"
    username_regex = r"^[a-zA-Z0-9_-]{1,30}$"
    max_length = 30
    not_found_indicators = ["We can't find that page"]
    found_indicators = ["bitbucket.org", "avatar"]


class Codeberg(Platform):
    name = "Codeberg"
    category = "developer"
    url_pattern = "https://codeberg.org/{username}"
    username_regex = r"^[a-zA-Z0-9._-]{1,40}$"
    max_length = 40
    not_found_indicators = ["Page Not Found"]
    found_indicators = ["codeberg.org", "avatar"]


class StackOverflow(Platform):
    name = "Stack Overflow"
    category = "developer"
    url_pattern = "https://stackoverflow.com/users/{username}"
    username_regex = r"^[0-9]+$"

    def classify(self, response: httpx.Response) -> tuple[ScanStatus, Confidence]:
        if response.status_code == 404:
            return ScanStatus.NOT_FOUND, Confidence.HIGH
        if response.status_code == 200:
            if "user-card" in response.text or "profile-user" in response.text:
                return ScanStatus.FOUND, Confidence.MEDIUM
        return ScanStatus.UNKNOWN, Confidence.LOW


class HackerRank(Platform):
    name = "HackerRank"
    category = "developer"
    url_pattern = "https://www.hackerrank.com/profile/{username}"
    username_regex = r"^[a-zA-Z0-9_]{2,30}$"
    min_length = 2
    max_length = 30
    not_found_indicators = ["Page Not Found", "404"]
    found_indicators = ["hackerrank.com", "profile-heading"]


class LeetCode(Platform):
    name = "LeetCode"
    category = "developer"
    url_pattern = "https://leetcode.com/u/{username}/"
    username_regex = r"^[a-zA-Z0-9_-]{1,20}$"
    max_length = 20
    not_found_indicators = ["That page doesn't exist"]
    found_indicators = ["leetcode.com", "profile"]


class CodePen(Platform):
    name = "CodePen"
    category = "developer"
    url_pattern = "https://codepen.io/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{1,30}$"
    max_length = 30
    not_found_indicators = ["404! - CodePen"]
    found_indicators = ["codepen.io", "profile-header"]


class Replit(Platform):
    name = "Replit"
    category = "developer"
    url_pattern = "https://replit.com/@{username}"
    username_regex = r"^[a-zA-Z0-9_]{2,20}$"
    min_length = 2
    max_length = 20
    not_found_indicators = ["not found"]
    found_indicators = ["replit.com", "profile"]


class Kaggle(Platform):
    name = "Kaggle"
    category = "developer"
    url_pattern = "https://www.kaggle.com/{username}"
    username_regex = r"^[a-zA-Z0-9]{3,20}$"
    min_length = 3
    max_length = 20
    not_found_indicators = ["404", "Page not found"]
    found_indicators = ["kaggle.com", "profile"]


class DevTo(Platform):
    name = "Dev.to"
    category = "developer"
    url_pattern = "https://dev.to/{username}"
    username_regex = r"^[a-zA-Z0-9_]{1,30}$"
    max_length = 30
    not_found_indicators = ["Not Found"]
    found_indicators = ["dev.to", "crayons-avatar"]


class SourceForge(Platform):
    name = "SourceForge"
    category = "developer"
    url_pattern = "https://sourceforge.net/u/{username}/profile/"
    username_regex = r"^[a-zA-Z0-9_-]{1,30}$"
    max_length = 30
    not_found_indicators = ["Invalid Path"]
    found_indicators = ["sourceforge.net", "profile"]


DEVELOPER_PLATFORMS: list[type[Platform]] = [
    GitHub, GitLab, Bitbucket, Codeberg, StackOverflow,
    HackerRank, LeetCode, CodePen, Replit, Kaggle, DevTo, SourceForge,
]
