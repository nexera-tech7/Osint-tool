"""Mock/demo mode — deterministic fake results for offline testing."""

from __future__ import annotations

import random
from datetime import datetime, timezone

from uscan.scanner.models import (
    ScanResult, ScanReport, ScanStatus, Confidence, PlatformCategory,
)
from uscan.platforms.base import Platform


_MOCK_PROFILES: dict[str, tuple[ScanStatus, Confidence]] = {
    "Instagram": (ScanStatus.FOUND, Confidence.HIGH),
    "X (Twitter)": (ScanStatus.FOUND, Confidence.MEDIUM),
    "Facebook": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "TikTok": (ScanStatus.FOUND, Confidence.HIGH),
    "Snapchat": (ScanStatus.UNKNOWN, Confidence.NONE),
    "Threads": (ScanStatus.FOUND, Confidence.MEDIUM),
    "Bluesky": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Mastodon (mastodon.social)": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Pinterest": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Tumblr": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "VK": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Telegram": (ScanStatus.UNKNOWN, Confidence.NONE),
    "Reddit": (ScanStatus.FOUND, Confidence.HIGH),
    "GitHub": (ScanStatus.FOUND, Confidence.HIGH),
    "GitLab": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Bitbucket": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Codeberg": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Stack Overflow": (ScanStatus.UNKNOWN, Confidence.NONE),
    "HackerRank": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "LeetCode": (ScanStatus.FOUND, Confidence.MEDIUM),
    "CodePen": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Replit": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Kaggle": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Dev.to": (ScanStatus.FOUND, Confidence.MEDIUM),
    "SourceForge": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Twitch": (ScanStatus.FOUND, Confidence.HIGH),
    "Steam": (ScanStatus.FOUND, Confidence.MEDIUM),
    "Roblox": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Xbox": (ScanStatus.UNKNOWN, Confidence.NONE),
    "Chess.com": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "NameMC": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "YouTube": (ScanStatus.FOUND, Confidence.HIGH),
    "Vimeo": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Medium": (ScanStatus.FOUND, Confidence.MEDIUM),
    "Substack": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "SoundCloud": (ScanStatus.FOUND, Confidence.HIGH),
    "Spotify": (ScanStatus.UNKNOWN, Confidence.NONE),
    "Flickr": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Dailymotion": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "LinkedIn": (ScanStatus.BLOCKED, Confidence.NONE),
    "Behance": (ScanStatus.FOUND, Confidence.MEDIUM),
    "Dribbble": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Gravatar": (ScanStatus.FOUND, Confidence.LOW),
    "About.me": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Linktree": (ScanStatus.FOUND, Confidence.MEDIUM),
    "Patreon": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Buy Me a Coffee": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Product Hunt": (ScanStatus.FOUND, Confidence.MEDIUM),
    "Hacker News": (ScanStatus.FOUND, Confidence.HIGH),
    "Keybase": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Fiverr": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Imgur": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Giphy": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Wikipedia": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Hugging Face": (ScanStatus.FOUND, Confidence.MEDIUM),
    "npm": (ScanStatus.FOUND, Confidence.HIGH),
    "PyPI": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Hashnode": (ScanStatus.FOUND, Confidence.MEDIUM),
    "GitHub Gist": (ScanStatus.FOUND, Confidence.HIGH),
    "Docker Hub": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "TryHackMe": (ScanStatus.FOUND, Confidence.MEDIUM),
    "Hack The Box": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Disqus": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Goodreads": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Instructables": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Mixcloud": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Letterboxd": (ScanStatus.NOT_FOUND, Confidence.NONE),
    "Last.fm": (ScanStatus.FOUND, Confidence.MEDIUM),
}


def generate_mock_result(
    username: str,
    platform: Platform,
    *,
    deterministic: bool = True,
) -> ScanResult:
    if deterministic and platform.name in _MOCK_PROFILES:
        status, confidence = _MOCK_PROFILES[platform.name]
    else:
        rng = random.Random(f"{username}:{platform.name}")
        roll = rng.random()
        if roll < 0.25:
            status, confidence = ScanStatus.FOUND, rng.choice([Confidence.HIGH, Confidence.MEDIUM])
        elif roll < 0.75:
            status, confidence = ScanStatus.NOT_FOUND, Confidence.NONE
        elif roll < 0.85:
            status, confidence = ScanStatus.UNKNOWN, Confidence.NONE
        else:
            status, confidence = ScanStatus.ERROR, Confidence.NONE

    rng_time = random.Random(f"{username}:{platform.name}:time")

    return ScanResult(
        username=username,
        platform=platform.name,
        category=PlatformCategory(platform.category),
        status=status,
        profile_url=platform.build_url(username) if status == ScanStatus.FOUND else None,
        checked_at=datetime.now(timezone.utc),
        http_status=200 if status == ScanStatus.FOUND else (404 if status == ScanStatus.NOT_FOUND else None),
        response_time_ms=round(rng_time.uniform(50, 800), 1),
        confidence=confidence,
        error="mock_error" if status == ScanStatus.ERROR else None,
    )


def generate_mock_report(
    username: str,
    platforms: list[Platform],
) -> ScanReport:
    report = ScanReport(
        username=username,
        started_at=datetime.now(timezone.utc),
        concurrency=10,
    )
    for p in platforms:
        report.results.append(generate_mock_result(username, p))
    report.finalize()
    return report
