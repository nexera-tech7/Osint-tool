"""Per-platform rate limiting."""

from __future__ import annotations

import asyncio
import time
from collections import defaultdict


class RateLimiter:
    """Token-bucket rate limiter keyed by platform name."""

    def __init__(self, default_rps: float = 5.0):
        self._default_rps = default_rps
        self._limits: dict[str, float] = {}
        self._last_request: dict[str, float] = defaultdict(float)
        self._lock = asyncio.Lock()

    def set_limit(self, platform: str, rps: float) -> None:
        self._limits[platform] = rps

    async def acquire(self, platform: str) -> None:
        rps = self._limits.get(platform, self._default_rps)
        interval = 1.0 / rps if rps > 0 else 0

        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_request[platform]
            if elapsed < interval:
                await asyncio.sleep(interval - elapsed)
            self._last_request[platform] = time.monotonic()
