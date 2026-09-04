"""Data models for scan results."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ScanStatus(str, Enum):
    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    UNKNOWN = "UNKNOWN"
    RATE_LIMITED = "RATE_LIMITED"
    BLOCKED = "BLOCKED"
    ERROR = "ERROR"


class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"


class PlatformCategory(str, Enum):
    SOCIAL = "social"
    DEVELOPER = "developer"
    GAMING = "gaming"
    CONTENT = "content"
    PROFESSIONAL = "professional"
    OTHER = "other"


class PlatformMeta(BaseModel):
    display_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    followers: int | None = None
    following: int | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class ScanResult(BaseModel):
    username: str
    platform: str
    category: PlatformCategory
    status: ScanStatus
    profile_url: str | None = None
    checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    http_status: int | None = None
    response_time_ms: float | None = None
    confidence: Confidence = Confidence.NONE
    error: str | None = None
    metadata: PlatformMeta | None = None

    @property
    def is_found(self) -> bool:
        return self.status == ScanStatus.FOUND


class ScanSummary(BaseModel):
    found: int = 0
    not_found: int = 0
    unknown: int = 0
    rate_limited: int = 0
    blocked: int = 0
    errors: int = 0

    @property
    def total(self) -> int:
        return self.found + self.not_found + self.unknown + self.rate_limited + self.blocked + self.errors

    @classmethod
    def from_results(cls, results: list[ScanResult]) -> ScanSummary:
        summary = cls()
        for r in results:
            match r.status:
                case ScanStatus.FOUND:
                    summary.found += 1
                case ScanStatus.NOT_FOUND:
                    summary.not_found += 1
                case ScanStatus.UNKNOWN:
                    summary.unknown += 1
                case ScanStatus.RATE_LIMITED:
                    summary.rate_limited += 1
                case ScanStatus.BLOCKED:
                    summary.blocked += 1
                case ScanStatus.ERROR:
                    summary.errors += 1
        return summary


class ScanReport(BaseModel):
    tool: str = "USCAN"
    version: str = "1.0.0"
    username: str
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None
    duration_seconds: float | None = None
    platforms_checked: int = 0
    concurrency: int = 10
    summary: ScanSummary = Field(default_factory=ScanSummary)
    results: list[ScanResult] = Field(default_factory=list)

    def finalize(self) -> None:
        self.completed_at = datetime.now(timezone.utc)
        if self.started_at:
            self.duration_seconds = round(
                (self.completed_at - self.started_at).total_seconds(), 2
            )
        self.platforms_checked = len(self.results)
        self.summary = ScanSummary.from_results(self.results)

    def to_dict(self) -> dict:
        return {
            "tool": self.tool,
            "version": self.version,
            "target": {"username": self.username},
            "scan": {
                "started_at": self.started_at.isoformat(),
                "completed_at": self.completed_at.isoformat() if self.completed_at else None,
                "duration_seconds": self.duration_seconds,
                "platforms_checked": self.platforms_checked,
            },
            "summary": {
                "found": self.summary.found,
                "not_found": self.summary.not_found,
                "unknown": self.summary.unknown,
                "errors": self.summary.errors,
            },
            "results": [
                {
                    "platform": r.platform,
                    "category": r.category.value,
                    "status": r.status.value,
                    "profile_url": r.profile_url,
                    "confidence": r.confidence.value,
                    "http_status": r.http_status,
                    "response_time_ms": r.response_time_ms,
                    "checked_at": r.checked_at.isoformat(),
                    "error": r.error,
                }
                for r in self.results
            ],
        }
