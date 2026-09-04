"""Social media platform adapters."""

from __future__ import annotations

import httpx
from uscan.platforms.base import Platform
from uscan.scanner.models import ScanStatus, Confidence


class Instagram(Platform):
    name = "Instagram"
    category = "social"
    url_pattern = "https://www.instagram.com/{username}/"
    username_regex = r"^[a-zA-Z0-9._]{1,30}$"
    min_length = 1
    max_length = 30
    not_found_indicators = ["Sorry, this page isn't available", "Page Not Found"]
    found_indicators = ["instagram.com", "profilePage", "is_private"]


class X(Platform):
    name = "X (Twitter)"
    category = "social"
    url_pattern = "https://x.com/{username}"
    username_regex = r"^[a-zA-Z0-9_]{1,15}$"
    max_length = 15
    not_found_indicators = ["This account doesn't exist", "Hmm...this page doesn't exist"]
    found_indicators = ["twitter.com", "profile_image"]

    def classify(self, response: httpx.Response) -> tuple[ScanStatus, Confidence]:
        if response.status_code == 200:
            return ScanStatus.FOUND, Confidence.MEDIUM
        if response.status_code in (302, 301):
            return ScanStatus.UNKNOWN, Confidence.LOW
        if response.status_code == 404:
            return ScanStatus.NOT_FOUND, Confidence.HIGH
        return super().classify(response)


class Facebook(Platform):
    name = "Facebook"
    category = "social"
    url_pattern = "https://www.facebook.com/{username}"
    username_regex = r"^[a-zA-Z0-9.]{5,50}$"
    min_length = 5
    max_length = 50
    follow_redirects = False

    def classify(self, response: httpx.Response) -> tuple[ScanStatus, Confidence]:
        if response.status_code == 404:
            return ScanStatus.NOT_FOUND, Confidence.HIGH
        if response.status_code in (302, 301):
            location = response.headers.get("location", "")
            if "/login" in location or "checkpoint" in location:
                return ScanStatus.UNKNOWN, Confidence.LOW
            return ScanStatus.FOUND, Confidence.MEDIUM
        if response.status_code == 200:
            if "page not found" in response.text.lower():
                return ScanStatus.NOT_FOUND, Confidence.MEDIUM
            return ScanStatus.FOUND, Confidence.LOW
        return super().classify(response)


class TikTok(Platform):
    name = "TikTok"
    category = "social"
    url_pattern = "https://www.tiktok.com/@{username}"
    username_regex = r"^[a-zA-Z0-9._]{2,24}$"
    min_length = 2
    max_length = 24
    not_found_indicators = ["Couldn't find this account", "user-not-found"]
    found_indicators = ["tiktok.com", "uniqueId", "user-page"]


class Snapchat(Platform):
    name = "Snapchat"
    category = "social"
    url_pattern = "https://www.snapchat.com/add/{username}"
    username_regex = r"^[a-zA-Z][a-zA-Z0-9._-]{2,14}$"
    min_length = 3
    max_length = 15
    not_found_indicators = ["not found", "404"]
    found_indicators = ["snapchat.com/add", "bitmoji"]


class Threads(Platform):
    name = "Threads"
    category = "social"
    url_pattern = "https://www.threads.net/@{username}"
    username_regex = r"^[a-zA-Z0-9._]{1,30}$"
    max_length = 30
    not_found_indicators = ["Sorry, this page isn't available"]
    found_indicators = ["threads.net", "profile"]


class Bluesky(Platform):
    name = "Bluesky"
    category = "social"
    url_pattern = "https://bsky.app/profile/{username}.bsky.social"
    username_regex = r"^[a-zA-Z0-9._-]{3,20}$"
    min_length = 3
    max_length = 20
    not_found_indicators = ["Profile not found", "could not find user"]
    found_indicators = ["bsky.app", "displayName", "avatar"]


class Mastodon(Platform):
    name = "Mastodon (mastodon.social)"
    category = "social"
    url_pattern = "https://mastodon.social/@{username}"
    username_regex = r"^[a-zA-Z0-9_]{1,30}$"
    max_length = 30
    not_found_indicators = ["The page you are looking for isn't here"]
    found_indicators = ["mastodon.social", "account__header", "public-account-header"]


class Pinterest(Platform):
    name = "Pinterest"
    category = "social"
    url_pattern = "https://www.pinterest.com/{username}/"
    username_regex = r"^[a-zA-Z0-9_]{3,30}$"
    min_length = 3
    max_length = 30
    not_found_indicators = ["Not Found", "404"]
    found_indicators = ["pinterest.com", "pinterestapp:"]


class Tumblr(Platform):
    name = "Tumblr"
    category = "social"
    url_pattern = "https://{username}.tumblr.com/"
    username_regex = r"^[a-zA-Z0-9-]{1,32}$"
    max_length = 32
    not_found_indicators = ["There's nothing here", "Not found"]
    found_indicators = ["tumblr.com", "avatar"]


class VK(Platform):
    name = "VK"
    category = "social"
    url_pattern = "https://vk.com/{username}"
    username_regex = r"^[a-zA-Z0-9._]{5,32}$"
    min_length = 5
    max_length = 32
    not_found_indicators = ["Page not found", "404"]
    found_indicators = ["vk.com", "page_name", "profile"]


class Telegram(Platform):
    name = "Telegram"
    category = "social"
    url_pattern = "https://t.me/{username}"
    username_regex = r"^[a-zA-Z][a-zA-Z0-9_]{4,31}$"
    min_length = 5
    max_length = 32
    not_found_indicators = ["If you have <strong>Telegram</strong>, you can"]

    def classify(self, response: httpx.Response) -> tuple[ScanStatus, Confidence]:
        if response.status_code == 200:
            text = response.text
            if "tgme_page_icon" in text or "tgme_page_title" in text:
                if any(ind in text for ind in self.not_found_indicators):
                    return ScanStatus.NOT_FOUND, Confidence.HIGH
                return ScanStatus.FOUND, Confidence.MEDIUM
            return ScanStatus.UNKNOWN, Confidence.LOW
        return super().classify(response)


class Reddit(Platform):
    name = "Reddit"
    category = "social"
    url_pattern = "https://www.reddit.com/user/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{3,20}$"
    min_length = 3
    max_length = 20
    not_found_indicators = ["page not found", "Sorry, nobody on Reddit goes by that name"]
    found_indicators = ["reddit.com/user/", "profileId"]


SOCIAL_PLATFORMS: list[type[Platform]] = [
    Instagram, X, Facebook, TikTok, Snapchat, Threads,
    Bluesky, Mastodon, Pinterest, Tumblr, VK, Telegram, Reddit,
]
