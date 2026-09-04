"""Simple file-based scan result cache."""

from __future__ import annotations

import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime, timezone

from uscan.config import CacheConfig


class ScanCache:
    def __init__(self, config: CacheConfig) -> None:
        self.config = config
        self.cache_dir = config.directory / "results"

    def _key(self, username: str, platform: str) -> str:
        raw = f"{username.lower()}:{platform.lower()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def get(self, username: str, platform: str) -> dict | None:
        if not self.config.enabled:
            return None
        path = self._path(self._key(username, platform))
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            cached_at = datetime.fromisoformat(data.get("cached_at", ""))
            if cached_at.tzinfo is None:
                cached_at = cached_at.replace(tzinfo=timezone.utc)
            age = (datetime.now(timezone.utc) - cached_at).total_seconds()
            if age > self.config.ttl_seconds:
                path.unlink(missing_ok=True)
                return None
            return data
        except Exception:
            return None

    def put(self, username: str, platform: str, result: dict) -> None:
        if not self.config.enabled:
            return
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        key = self._key(username, platform)
        data = {**result, "cached_at": datetime.now(timezone.utc).isoformat()}
        self._path(key).write_text(
            json.dumps(data, ensure_ascii=False), encoding="utf-8"
        )

    def clear(self) -> int:
        if not self.cache_dir.exists():
            return 0
        count = sum(1 for _ in self.cache_dir.glob("*.json"))
        shutil.rmtree(self.cache_dir, ignore_errors=True)
        return count
