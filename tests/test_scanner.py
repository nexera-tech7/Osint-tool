"""Tests for scanner engine and classifier."""

import pytest
from uscan.scanner.models import (
    ScanStatus, Confidence, ScanResult, ScanSummary, ScanReport, PlatformCategory,
)
from uscan.scanner.classifier import ResponseClassifier


class TestResponseClassifier:
    def test_404_is_not_found(self):
        status, conf = ResponseClassifier.classify(404)
        assert status == ScanStatus.NOT_FOUND
        assert conf == Confidence.HIGH

    def test_429_is_rate_limited(self):
        status, conf = ResponseClassifier.classify(429)
        assert status == ScanStatus.RATE_LIMITED

    def test_403_is_blocked(self):
        status, conf = ResponseClassifier.classify(403)
        assert status == ScanStatus.BLOCKED

    def test_500_is_error(self):
        status, _ = ResponseClassifier.classify(500)
        assert status == ScanStatus.ERROR

    def test_200_with_not_found_indicator(self):
        status, conf = ResponseClassifier.classify(
            200,
            "Sorry, this page isn't available",
            not_found_indicators=["Sorry, this page isn't available"],
        )
        assert status == ScanStatus.NOT_FOUND
        assert conf == Confidence.HIGH

    def test_200_with_found_indicators(self):
        status, conf = ResponseClassifier.classify(
            200,
            '<div class="profilePage"><img src="avatar.jpg"></div>',
            found_indicators=["profilePage", "avatar"],
        )
        assert status == ScanStatus.FOUND
        assert conf == Confidence.HIGH

    def test_200_with_one_found_indicator(self):
        status, conf = ResponseClassifier.classify(
            200,
            '<div class="profilePage"></div>',
            found_indicators=["profilePage", "avatar"],
        )
        assert status == ScanStatus.FOUND
        assert conf == Confidence.MEDIUM

    def test_200_no_indicators(self):
        status, conf = ResponseClassifier.classify(200, "some page content")
        assert status == ScanStatus.FOUND
        assert conf == Confidence.LOW

    def test_none_status(self):
        status, _ = ResponseClassifier.classify(None)
        assert status == ScanStatus.ERROR

    def test_redirect(self):
        status, _ = ResponseClassifier.classify(302)
        assert status == ScanStatus.UNKNOWN


class TestScanSummary:
    def test_from_results(self):
        from datetime import datetime, timezone
        results = [
            ScanResult(username="test", platform="A", category=PlatformCategory.SOCIAL, status=ScanStatus.FOUND),
            ScanResult(username="test", platform="B", category=PlatformCategory.SOCIAL, status=ScanStatus.FOUND),
            ScanResult(username="test", platform="C", category=PlatformCategory.SOCIAL, status=ScanStatus.NOT_FOUND),
            ScanResult(username="test", platform="D", category=PlatformCategory.SOCIAL, status=ScanStatus.ERROR),
        ]
        summary = ScanSummary.from_results(results)
        assert summary.found == 2
        assert summary.not_found == 1
        assert summary.errors == 1
        assert summary.total == 4


class TestScanReport:
    def test_finalize(self):
        report = ScanReport(username="test")
        report.results = [
            ScanResult(username="test", platform="A", category=PlatformCategory.SOCIAL, status=ScanStatus.FOUND),
            ScanResult(username="test", platform="B", category=PlatformCategory.SOCIAL, status=ScanStatus.NOT_FOUND),
        ]
        report.finalize()
        assert report.platforms_checked == 2
        assert report.summary.found == 1
        assert report.completed_at is not None
        assert report.duration_seconds is not None

    def test_to_dict(self):
        report = ScanReport(username="test")
        report.results = [
            ScanResult(username="test", platform="A", category=PlatformCategory.SOCIAL, status=ScanStatus.FOUND, profile_url="https://example.com/test"),
        ]
        report.finalize()
        d = report.to_dict()
        assert d["tool"] == "USCAN"
        assert d["target"]["username"] == "test"
        assert len(d["results"]) == 1
        assert d["results"][0]["status"] == "FOUND"
