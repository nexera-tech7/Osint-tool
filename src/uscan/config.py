"""Application configuration with TOML file support."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from dataclasses import dataclass, field


def _config_dir() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "uscan"


def _cache_dir() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home()))
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / "uscan"


@dataclass
class ScanConfig:
    concurrency: int = 10
    timeout: float = 10.0
    retries: int = 2
    retry_delay: float = 1.0
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )


@dataclass
class OutputConfig:
    directory: Path = field(default_factory=lambda: Path("reports"))
    color: bool = True
    verbose: bool = False
    quiet: bool = False


@dataclass
class CacheConfig:
    enabled: bool = False
    directory: Path = field(default_factory=_cache_dir)
    ttl_seconds: int = 3600


@dataclass
class AppConfig:
    scan: ScanConfig = field(default_factory=ScanConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    disabled_platforms: list[str] = field(default_factory=list)
    enabled_platforms: list[str] = field(default_factory=list)

    @classmethod
    def load(cls) -> AppConfig:
        config = cls()
        config_file = _config_dir() / "config.toml"
        if config_file.exists():
            try:
                import tomllib
            except ImportError:
                try:
                    import tomli as tomllib  # type: ignore[no-redef]
                except ImportError:
                    return config
            try:
                with open(config_file, "rb") as f:
                    data = tomllib.load(f)
                if "scan" in data:
                    for k, v in data["scan"].items():
                        if hasattr(config.scan, k):
                            setattr(config.scan, k, v)
                if "output" in data:
                    for k, v in data["output"].items():
                        if k == "directory":
                            config.output.directory = Path(v)
                        elif hasattr(config.output, k):
                            setattr(config.output, k, v)
                if "cache" in data:
                    for k, v in data["cache"].items():
                        if k == "directory":
                            config.cache.directory = Path(v)
                        elif hasattr(config.cache, k):
                            setattr(config.cache, k, v)
                if "platforms" in data:
                    config.disabled_platforms = data["platforms"].get("disabled", [])
                    config.enabled_platforms = data["platforms"].get("enabled", [])
            except Exception:
                pass
        return config
