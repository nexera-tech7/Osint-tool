"""Core scanning engine with async concurrency control."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import AsyncIterator, Callable

import httpx

from uscan.config import ScanConfig
from uscan.scanner.models import ScanReport, ScanResult
from uscan.scanner.rate_limiter import RateLimiter
from uscan.scanner.worker import check_platform
from uscan.platforms.base import Platform

logger = logging.getLogger("uscan.engine")


class ScanEngine:
    """Orchestrates concurrent platform scanning."""

    def __init__(
        self,
        platforms: list[Platform],
        config: ScanConfig,
    ):
        self.platforms = platforms
        self.config = config
        self.rate_limiter = RateLimiter()
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    async def scan(
        self,
        username: str,
        on_result: Callable[[ScanResult, int, int], None] | None = None,
    ) -> ScanReport:
        report = ScanReport(
            username=username,
            started_at=datetime.now(timezone.utc),
            concurrency=self.config.concurrency,
        )

        semaphore = asyncio.Semaphore(self.config.concurrency)
        results: list[ScanResult] = []
        total = len(self.platforms)
        completed = 0

        async with httpx.AsyncClient(
            headers={"User-Agent": self.config.user_agent},
            follow_redirects=False,
            http2=False,
        ) as client:

            async def _check(platform: Platform, index: int) -> ScanResult | None:
                nonlocal completed
                if self._cancelled:
                    return None
                async with semaphore:
                    if self._cancelled:
                        return None
                    result = await check_platform(
                        platform, username, client, self.rate_limiter, self.config
                    )
                    completed += 1
                    if on_result:
                        on_result(result, completed, total)
                    return result

            tasks = [
                asyncio.create_task(_check(p, i))
                for i, p in enumerate(self.platforms)
            ]

            try:
                done = await asyncio.gather(*tasks, return_exceptions=True)
            except asyncio.CancelledError:
                for t in tasks:
                    t.cancel()
                done = []

            for item in done:
                if isinstance(item, ScanResult):
                    results.append(item)
                elif isinstance(item, Exception):
                    logger.debug("Platform task raised: %s", item)

        report.results = sorted(results, key=lambda r: r.platform.lower())
        report.finalize()
        return report

    async def scan_stream(
        self, username: str
    ) -> AsyncIterator[tuple[ScanResult, int, int]]:
        """Yield results as they complete."""
        semaphore = asyncio.Semaphore(self.config.concurrency)
        total = len(self.platforms)
        queue: asyncio.Queue[ScanResult | None] = asyncio.Queue()
        completed = 0

        async def _check(platform: Platform) -> None:
            nonlocal completed
            if self._cancelled:
                return
            async with semaphore:
                if self._cancelled:
                    return
                async with httpx.AsyncClient(
                    headers={"User-Agent": self.config.user_agent},
                    follow_redirects=False,
                ) as client:
                    result = await check_platform(
                        platform, username, client, self.rate_limiter, self.config
                    )
                    completed += 1
                    await queue.put(result)

        tasks = [asyncio.create_task(_check(p)) for p in self.platforms]

        yielded = 0
        while yielded < total and not self._cancelled:
            result = await queue.get()
            if result is not None:
                yielded += 1
                yield result, yielded, total

        for t in tasks:
            if not t.done():
                t.cancel()
