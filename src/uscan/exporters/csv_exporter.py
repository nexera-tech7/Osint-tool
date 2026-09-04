"""CSV report exporter."""

from __future__ import annotations

import csv
from pathlib import Path

from uscan.scanner.models import ScanReport


class CSVExporter:
    @staticmethod
    def export(report: ScanReport, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "platform", "category", "status", "confidence",
                "profile_url", "http_status", "response_time_ms",
                "checked_at", "error",
            ])
            for r in report.results:
                writer.writerow([
                    r.platform,
                    r.category.value,
                    r.status.value,
                    r.confidence.value,
                    r.profile_url or "",
                    r.http_status or "",
                    r.response_time_ms or "",
                    r.checked_at.isoformat(),
                    r.error or "",
                ])

        return output_path
