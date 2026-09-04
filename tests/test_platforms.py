"""Tests for platform registry and adapters."""

import pytest
from uscan.platforms.registry import get_default_registry, PlatformRegistry
from uscan.platforms.base import Platform
from uscan.platforms.social import Instagram
from uscan.platforms.developer import GitHub


class TestPlatformRegistry:
    def test_default_registry_not_empty(self):
        registry = get_default_registry()
        assert registry.count > 0

    def test_default_registry_has_major_platforms(self):
        registry = get_default_registry()
        for name in ["instagram", "github", "reddit", "x (twitter)", "youtube"]:
            assert registry.get(name) is not None, f"Missing: {name}"

    def test_categories(self):
        registry = get_default_registry()
        cats = registry.categories()
        assert "social" in cats
        assert "developer" in cats
        assert "gaming" in cats

    def test_filter_by_category(self):
        registry = get_default_registry()
        social = registry.by_category("social")
        assert len(social) > 0
        assert all(p.category == "social" for p in social)

    def test_filter_disabled(self):
        registry = get_default_registry()
        total = registry.count
        filtered = registry.filter(disabled=["Instagram"])
        assert len(filtered) == total - 1

    def test_filter_by_name(self):
        registry = get_default_registry()
        filtered = registry.filter(platform_names=["GitHub", "Instagram"])
        assert len(filtered) == 2

    def test_register_custom(self):
        registry = PlatformRegistry()
        p = Platform()
        p.name = "TestPlatform"
        p.category = "other"
        registry.register(p)
        assert registry.count == 1
        assert registry.get("testplatform") is not None


class TestPlatformBase:
    def test_instagram_url(self):
        p = Instagram()
        assert p.build_url("inter") == "https://www.instagram.com/inter/"

    def test_instagram_validate_valid(self):
        p = Instagram()
        assert p.validate_username("inter") is True

    def test_instagram_validate_too_long(self):
        p = Instagram()
        assert p.validate_username("a" * 31) is False

    def test_github_url(self):
        from uscan.platforms.developer import GitHub
        p = GitHub()
        assert p.build_url("torvalds") == "https://github.com/torvalds"

    def test_github_validate_dash(self):
        from uscan.platforms.developer import GitHub
        p = GitHub()
        assert p.validate_username("my-user") is True

    def test_github_validate_leading_dash_rejected(self):
        from uscan.platforms.developer import GitHub
        p = GitHub()
        assert p.validate_username("-myuser") is False

    def test_all_platforms_have_required_fields(self):
        registry = get_default_registry()
        for p in registry.all():
            assert p.name, f"Platform missing name"
            assert p.category, f"{p.name} missing category"
            assert p.url_pattern, f"{p.name} missing url_pattern"
            assert "{username}" in p.url_pattern, f"{p.name} url_pattern missing {{username}}"
