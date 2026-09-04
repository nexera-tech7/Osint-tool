"""JSON report exporter."""

from __future__ import annotations

import json
from pathlib import Path

from uscan.scanner.models import ScanReport


class JSONExporter:
    @staticmethod
    def export(report: ScanReport, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = report.to_dict()
        output_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return output_path
