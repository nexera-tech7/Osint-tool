"""Platform registry — central catalog of all supported platforms."""

from __future__ import annotations

from uscan.platforms.base import Platform
from uscan.platforms.social import SOCIAL_PLATFORMS
from uscan.platforms.developer import DEVELOPER_PLATFORMS
from uscan.platforms.gaming import GAMING_PLATFORMS
from uscan.platforms.content import CONTENT_PLATFORMS
from uscan.platforms.professional import PROFESSIONAL_PLATFORMS
from uscan.platforms.other import OTHER_PLATFORMS


class PlatformRegistry:
    """Manages the collection of platform adapters."""

    def __init__(self) -> None:
        self._platforms: dict[str, Platform] = {}

    def register(self, platform: Platform) -> None:
        self._platforms[platform.name.lower()] = platform

    def get(self, name: str) -> Platform | None:
        return self._platforms.get(name.lower())

    def all(self) -> list[Platform]:
        return list(self._platforms.values())

    def by_category(self, category: str) -> list[Platform]:
        return [p for p in self._platforms.values() if p.category == category]

    def by_categories(self, categories: list[str]) -> list[Platform]:
        cat_set = set(categories)
        return [p for p in self._platforms.values() if p.category in cat_set]

    def names(self) -> list[str]:
        return sorted(self._platforms.keys())

    def categories(self) -> list[str]:
        return sorted({p.category for p in self._platforms.values()})

    @property
    def count(self) -> int:
        return len(self._platforms)

    def filter(
        self,
        *,
        platform_names: list[str] | None = None,
        categories: list[str] | None = None,
        disabled: list[str] | None = None,
        enabled: list[str] | None = None,
    ) -> list[Platform]:
        platforms = self.all()

        if platform_names:
            name_set = {n.lower() for n in platform_names}
            platforms = [p for p in platforms if p.name.lower() in name_set]

        if categories:
            cat_set = set(categories)
            platforms = [p for p in platforms if p.category in cat_set]

        if enabled:
            enabled_set = {n.lower() for n in enabled}
            platforms = [p for p in platforms if p.name.lower() in enabled_set]

        if disabled:
            disabled_set = {n.lower() for n in disabled}
            platforms = [p for p in platforms if p.name.lower() not in disabled_set]

        return platforms


def get_default_registry() -> PlatformRegistry:
    """Create and return a registry with all built-in platforms."""
    registry = PlatformRegistry()

    all_platform_classes = (
        SOCIAL_PLATFORMS
        + DEVELOPER_PLATFORMS
        + GAMING_PLATFORMS
        + CONTENT_PLATFORMS
        + PROFESSIONAL_PLATFORMS
        + OTHER_PLATFORMS
    )

    for cls in all_platform_classes:
        registry.register(cls())

    return registry
