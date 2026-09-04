"""Content platform adapters."""

from __future__ import annotations

import httpx
from uscan.platforms.base import Platform
from uscan.scanner.models import ScanStatus, Confidence


class YouTube(Platform):
    name = "YouTube"
    category = "content"
    url_pattern = "https://www.youtube.com/@{username}"
    username_regex = r"^[a-zA-Z0-9._-]{1,30}$"
    max_length = 30
    not_found_indicators = ["This page isn't available", "404 Not Found"]
    found_indicators = ["youtube.com", "channel-header", "subscriber"]


class Vimeo(Platform):
    name = "Vimeo"
    category = "content"
    url_pattern = "https://vimeo.com/{username}"
    username_regex = r"^[a-zA-Z0-9_]{1,30}$"
    max_length = 30
    not_found_indicators = ["Page not found", "Sorry, we couldn't find that page"]
    found_indicators = ["vimeo.com", "profile_header"]


class Medium(Platform):
    name = "Medium"
    category = "content"
    url_pattern = "https://medium.com/@{username}"
    username_regex = r"^[a-zA-Z0-9._]{1,30}$"
    max_length = 30
    not_found_indicators = ["PAGE NOT FOUND", "We couldn't find this page"]
    found_indicators = ["medium.com", "u-username"]


class Substack(Platform):
    name = "Substack"
    category = "content"
    url_pattern = "https://{username}.substack.com/"
    username_regex = r"^[a-zA-Z0-9-]{3,30}$"
    min_length = 3
    max_length = 30
    not_found_indicators = ["page doesn't exist"]
    found_indicators = ["substack.com", "publication-title", "subscribe-btn"]


class SoundCloud(Platform):
    name = "SoundCloud"
    category = "content"
    url_pattern = "https://soundcloud.com/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{3,25}$"
    min_length = 3
    max_length = 25
    not_found_indicators = ["We can't find that user"]
    found_indicators = ["soundcloud.com", "userAvatar", "user-main"]


class Spotify(Platform):
    name = "Spotify"
    category = "content"
    url_pattern = "https://open.spotify.com/user/{username}"
    username_regex = r"^[a-zA-Z0-9._]{1,30}$"
    max_length = 30

    def classify(self, response: httpx.Response) -> tuple[ScanStatus, Confidence]:
        if response.status_code == 200:
            if "user-profile" in response.text or "public-playlists" in response.text:
                return ScanStatus.FOUND, Confidence.MEDIUM
            return ScanStatus.UNKNOWN, Confidence.LOW
        if response.status_code == 404:
            return ScanStatus.NOT_FOUND, Confidence.MEDIUM
        return super().classify(response)


class Flickr(Platform):
    name = "Flickr"
    category = "content"
    url_pattern = "https://www.flickr.com/people/{username}/"
    username_regex = r"^[a-zA-Z0-9@_-]{1,30}$"
    max_length = 30
    not_found_indicators = ["member not found"]
    found_indicators = ["flickr.com", "avatar"]


class DailyMotion(Platform):
    name = "Dailymotion"
    category = "content"
    url_pattern = "https://www.dailymotion.com/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{3,25}$"
    min_length = 3
    max_length = 25
    not_found_indicators = ["Page not available"]
    found_indicators = ["dailymotion.com", "channel-infos"]


CONTENT_PLATFORMS: list[type[Platform]] = [
    YouTube, Vimeo, Medium, Substack, SoundCloud, Spotify, Flickr, DailyMotion,
]
