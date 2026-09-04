"""Tests for mock/demo mode."""

import pytest
from uscan.mock import generate_mock_result, generate_mock_report
from uscan.platforms.registry import get_default_registry
from uscan.scanner.models import ScanStatus


class TestMockMode:
    def test_mock_result_deterministic(self):
        registry = get_default_registry()
        p = registry.get("github")
        r1 = generate_mock_result("inter", p)
        r2 = generate_mock_result("inter", p)
        assert r1.status == r2.status

    def test_mock_report_has_results(self):
        registry = get_default_registry()
        platforms = registry.all()
        report = generate_mock_report("demo_user", platforms)
        assert len(report.results) == len(platforms)
        assert report.summary.total == len(platforms)

    def test_mock_report_has_found(self):
        registry = get_default_registry()
        platforms = registry.all()
        report = generate_mock_report("demo_user", platforms)
        assert report.summary.found > 0

    def test_mock_report_finalized(self):
        registry = get_default_registry()
        platforms = registry.all()
        report = generate_mock_report("demo_user", platforms)
        assert report.completed_at is not None
        assert report.duration_seconds is not None

    def test_found_results_have_urls(self):
        registry = get_default_registry()
        platforms = registry.all()
        report = generate_mock_report("testuser", platforms)
        for r in report.results:
            if r.status == ScanStatus.FOUND:
                assert r.profile_url is not None
                assert "testuser" in r.profile_url
