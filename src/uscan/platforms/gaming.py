"""Gaming platform adapters."""

from __future__ import annotations

import httpx
from uscan.platforms.base import Platform
from uscan.scanner.models import ScanStatus, Confidence


class Twitch(Platform):
    name = "Twitch"
    category = "gaming"
    url_pattern = "https://www.twitch.tv/{username}"
    username_regex = r"^[a-zA-Z0-9_]{4,25}$"
    min_length = 4
    max_length = 25
    not_found_indicators = ["content='404'", "Sorry. Unless you've got a time machine"]
    found_indicators = ["twitch.tv", "channel-header"]


class Steam(Platform):
    name = "Steam"
    category = "gaming"
    url_pattern = "https://steamcommunity.com/id/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{2,32}$"
    min_length = 2
    max_length = 32
    not_found_indicators = ["The specified profile could not be found"]
    found_indicators = ["steamcommunity.com", "actual_persona_name", "profile_header"]


class Roblox(Platform):
    name = "Roblox"
    category = "gaming"
    url_pattern = "https://www.roblox.com/user.aspx?username={username}"
    username_regex = r"^[a-zA-Z0-9_]{3,20}$"
    min_length = 3
    max_length = 20
    follow_redirects = True

    def classify(self, response: httpx.Response) -> tuple[ScanStatus, Confidence]:
        if response.status_code == 200:
            url = str(response.url)
            if "/users/" in url and "/profile" in url:
                return ScanStatus.FOUND, Confidence.HIGH
            if "not found" in response.text.lower() or "page cannot" in response.text.lower():
                return ScanStatus.NOT_FOUND, Confidence.HIGH
            return ScanStatus.UNKNOWN, Confidence.LOW
        if response.status_code == 404:
            return ScanStatus.NOT_FOUND, Confidence.HIGH
        return super().classify(response)


class Xbox(Platform):
    name = "Xbox"
    category = "gaming"
    url_pattern = "https://www.xbox.com/en-US/play/user/{username}"
    username_regex = r"^[a-zA-Z0-9 ]{1,15}$"
    max_length = 15
    not_found_indicators = ["not found", "404"]
    found_indicators = ["xbox.com", "gamertag"]

    def classify(self, response: httpx.Response) -> tuple[ScanStatus, Confidence]:
        if response.status_code == 404:
            return ScanStatus.NOT_FOUND, Confidence.MEDIUM
        if response.status_code == 200:
            return ScanStatus.UNKNOWN, Confidence.LOW
        return super().classify(response)


class Chess(Platform):
    name = "Chess.com"
    category = "gaming"
    url_pattern = "https://www.chess.com/member/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{3,25}$"
    min_length = 3
    max_length = 25
    not_found_indicators = ["Username is not valid", "not found"]
    found_indicators = ["chess.com/member", "profile-card"]


class MinecraftServer(Platform):
    name = "NameMC"
    category = "gaming"
    url_pattern = "https://namemc.com/profile/{username}"
    username_regex = r"^[a-zA-Z0-9_]{3,16}$"
    min_length = 3
    max_length = 16
    not_found_indicators = ["Profile Not Found"]
    found_indicators = ["namemc.com", "player-skin"]


GAMING_PLATFORMS: list[type[Platform]] = [
    Twitch, Steam, Roblox, Xbox, Chess, MinecraftServer,
]
