"""Tests for export engines."""

import json
import csv
import pytest
from pathlib import Path
from datetime import datetime, timezone

from uscan.scanner.models import (
    ScanReport, ScanResult, ScanStatus, Confidence, PlatformCategory,
)
from uscan.exporters.json_exporter import JSONExporter
from uscan.exporters.txt_exporter import TXTExporter
from uscan.exporters.csv_exporter import CSVExporter
from uscan.exporters.html_exporter import HTMLExporter


def _sample_report() -> ScanReport:
    report = ScanReport(username="testuser")
    report.results = [
        ScanResult(
            username="testuser",
            platform="GitHub",
            category=PlatformCategory.DEVELOPER,
            status=ScanStatus.FOUND,
            profile_url="https://github.com/testuser",
            confidence=Confidence.HIGH,
            http_status=200,
            response_time_ms=142.5,
        ),
        ScanResult(
            username="testuser",
            platform="Instagram",
            category=PlatformCategory.SOCIAL,
            status=ScanStatus.NOT_FOUND,
            confidence=Confidence.NONE,
            http_status=404,
            response_time_ms=230.1,
        ),
        ScanResult(
            username="testuser",
            platform="LinkedIn",
            category=PlatformCategory.PROFESSIONAL,
            status=ScanStatus.ERROR,
            confidence=Confidence.NONE,
            error="timeout",
        ),
    ]
    report.finalize()
    return report


class TestJSONExporter:
    def test_export_creates_file(self, tmp_path):
        report = _sample_report()
        out = tmp_path / "test.json"
        JSONExporter.export(report, out)
        assert out.exists()

    def test_export_valid_json(self, tmp_path):
        report = _sample_report()
        out = tmp_path / "test.json"
        JSONExporter.export(report, out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["tool"] == "USCAN"
        assert data["target"]["username"] == "testuser"
        assert len(data["results"]) == 3

    def test_export_summary(self, tmp_path):
        report = _sample_report()
        out = tmp_path / "test.json"
        JSONExporter.export(report, out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["summary"]["found"] == 1
        assert data["summary"]["not_found"] == 1
        assert data["summary"]["errors"] == 1


class TestTXTExporter:
    def test_export_creates_file(self, tmp_path):
        report = _sample_report()
        out = tmp_path / "test.txt"
        TXTExporter.export(report, out)
        assert out.exists()

    def test_export_contains_username(self, tmp_path):
        report = _sample_report()
        out = tmp_path / "test.txt"
        TXTExporter.export(report, out)
        content = out.read_text(encoding="utf-8")
        assert "testuser" in content

    def test_export_contains_found_url(self, tmp_path):
        report = _sample_report()
        out = tmp_path / "test.txt"
        TXTExporter.export(report, out)
        content = out.read_text(encoding="utf-8")
        assert "https://github.com/testuser" in content


class TestCSVExporter:
    def test_export_creates_file(self, tmp_path):
        report = _sample_report()
        out = tmp_path / "test.csv"
        CSVExporter.export(report, out)
        assert out.exists()

    def test_export_has_header(self, tmp_path):
        report = _sample_report()
        out = tmp_path / "test.csv"
        CSVExporter.export(report, out)
        with out.open(encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            assert "platform" in header
            assert "status" in header

    def test_export_row_count(self, tmp_path):
        report = _sample_report()
        out = tmp_path / "test.csv"
        CSVExporter.export(report, out)
        with out.open(encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 4  # header + 3 results


class TestHTMLExporter:
    def test_export_creates_file(self, tmp_path):
        report = _sample_report()
        out = tmp_path / "test.html"
        HTMLExporter.export(report, out)
        assert out.exists()

    def test_export_valid_html(self, tmp_path):
        report = _sample_report()
        out = tmp_path / "test.html"
        HTMLExporter.export(report, out)
        content = out.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content
        assert "USCAN" in content
        assert "testuser" in content

    def test_export_contains_links(self, tmp_path):
        report = _sample_report()
        out = tmp_path / "test.html"
        HTMLExporter.export(report, out)
        content = out.read_text(encoding="utf-8")
        assert "https://github.com/testuser" in content
