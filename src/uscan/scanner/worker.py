"""Scan worker — executes a single platform check."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import httpx

from uscan.scanner.models import ScanResult, ScanStatus, Confidence, PlatformCategory

if TYPE_CHECKING:
    from uscan.platforms.base import Platform
    from uscan.scanner.rate_limiter import RateLimiter
    from uscan.config import ScanConfig


async def check_platform(
    platform: Platform,
    username: str,
    client: httpx.AsyncClient,
    rate_limiter: RateLimiter,
    config: ScanConfig,
) -> ScanResult:
    """Check a single platform for the given username."""
    url = platform.build_url(username)
    start = time.monotonic()

    for attempt in range(1 + config.retries):
        try:
            await rate_limiter.acquire(platform.name)

            response = await client.get(
                url,
                follow_redirects=platform.follow_redirects,
                timeout=config.timeout,
            )
            elapsed_ms = round((time.monotonic() - start) * 1000, 1)

            status, confidence = platform.classify(response)

            return ScanResult(
                username=username,
                platform=platform.name,
                category=PlatformCategory(platform.category),
                status=status,
                profile_url=url if status == ScanStatus.FOUND else None,
                checked_at=datetime.now(timezone.utc),
                http_status=response.status_code,
                response_time_ms=elapsed_ms,
                confidence=confidence,
            )

        except httpx.TimeoutException:
            if attempt < config.retries:
                import asyncio
                await asyncio.sleep(config.retry_delay * (2 ** attempt))
                continue
            return _error_result(username, platform, "timeout", start)

        except httpx.ConnectError:
            return _error_result(username, platform, "connection_failed", start)

        except httpx.TooManyRedirects:
            return _error_result(username, platform, "too_many_redirects", start)

        except Exception as exc:
            return _error_result(username, platform, str(exc)[:120], start)

    return _error_result(username, platform, "max_retries_exceeded", start)


def _error_result(
    username: str, platform: Platform, error: str, start: float
) -> ScanResult:
    return ScanResult(
        username=username,
        platform=platform.name,
        category=PlatformCategory(platform.category),
        status=ScanStatus.ERROR,
        checked_at=datetime.now(timezone.utc),
        response_time_ms=round((time.monotonic() - start) * 1000, 1),
        confidence=Confidence.NONE,
        error=error,
    )
