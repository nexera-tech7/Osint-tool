"""HTML report exporter."""

from __future__ import annotations

from html import escape
from pathlib import Path

from uscan.scanner.models import ScanReport, ScanStatus


_STATUS_COLORS = {
    "FOUND": "#22c55e",
    "NOT_FOUND": "#6b7280",
    "UNKNOWN": "#eab308",
    "RATE_LIMITED": "#f59e0b",
    "BLOCKED": "#f59e0b",
    "ERROR": "#ef4444",
}


class HTMLExporter:
    @staticmethod
    def export(report: ScanReport, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        rows = ""
        for r in report.results:
            color = _STATUS_COLORS.get(r.status.value, "#6b7280")
            if r.profile_url:
                safe_url = escape(r.profile_url, quote=True)
                url_cell = f'<a href="{safe_url}" target="_blank" rel="noopener">{safe_url}</a>'
            else:
                url_cell = "—"
            rows += f"""<tr>
                <td>{escape(r.platform)}</td>
                <td>{escape(r.category.value)}</td>
                <td style="color:{color};font-weight:600">{escape(r.status.value)}</td>
                <td>{escape(r.confidence.value) if r.status == ScanStatus.FOUND else '—'}</td>
                <td>{url_cell}</td>
            </tr>\n"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>USCAN Report — {escape(report.username)}</title>
<style>
:root {{
    --bg: #0a0a0a;
    --surface: #111111;
    --border: #1a1a1a;
    --text: #e5e5e5;
    --dim: #6b7280;
    --accent: #dc2626;
    --accent-dim: #7f1d1d;
    --found: #22c55e;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--text); font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace; }}
.container {{ max-width: 960px; margin: 0 auto; padding: 2rem 1rem; }}
header {{ text-align: center; margin-bottom: 2rem; border-bottom: 1px solid var(--accent-dim); padding-bottom: 2rem; }}
h1 {{ color: var(--accent); font-size: 2rem; letter-spacing: 0.3em; margin-bottom: 0.25rem; }}
.subtitle {{ color: var(--dim); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.2em; }}
.meta {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 2rem 0; }}
.meta-item {{ background: var(--surface); padding: 1rem; border: 1px solid var(--border); border-radius: 4px; }}
.meta-label {{ color: var(--dim); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; }}
.meta-value {{ color: var(--text); font-size: 1.4rem; font-weight: 700; margin-top: 0.25rem; }}
.meta-value.found {{ color: var(--found); }}
.meta-value.error {{ color: var(--accent); }}
table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 0.85rem; }}
th {{ background: var(--surface); color: var(--accent); text-align: left; padding: 0.75rem; border-bottom: 2px solid var(--accent-dim); text-transform: uppercase; font-size: 0.7rem; letter-spacing: 0.1em; }}
td {{ padding: 0.6rem 0.75rem; border-bottom: 1px solid var(--border); }}
tr:hover {{ background: var(--surface); }}
a {{ color: #60a5fa; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
footer {{ text-align: center; color: var(--dim); font-size: 0.75rem; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--border); }}
</style>
</head>
<body>
<div class="container">
    <header>
        <h1>USCAN</h1>
        <div class="subtitle">Username Intelligence Report</div>
    </header>

    <div class="meta">
        <div class="meta-item">
            <div class="meta-label">Target</div>
            <div class="meta-value">{escape(report.username)}</div>
        </div>
        <div class="meta-item">
            <div class="meta-label">Platforms</div>
            <div class="meta-value">{report.platforms_checked}</div>
        </div>
        <div class="meta-item">
            <div class="meta-label">Found</div>
            <div class="meta-value found">{report.summary.found}</div>
        </div>
        <div class="meta-item">
            <div class="meta-label">Not Found</div>
            <div class="meta-value">{report.summary.not_found}</div>
        </div>
        <div class="meta-item">
            <div class="meta-label">Unknown</div>
            <div class="meta-value">{report.summary.unknown}</div>
        </div>
        <div class="meta-item">
            <div class="meta-label">Errors</div>
            <div class="meta-value error">{report.summary.errors}</div>
        </div>
        <div class="meta-item">
            <div class="meta-label">Duration</div>
            <div class="meta-value">{report.duration_seconds}s</div>
        </div>
        <div class="meta-item">
            <div class="meta-label">Date</div>
            <div class="meta-value" style="font-size:0.9rem">{report.started_at.strftime('%Y-%m-%d')}</div>
        </div>
    </div>

    <h2 style="color:var(--accent);font-size:1rem;margin:2rem 0 0.5rem;letter-spacing:0.1em">RESULTS</h2>
    <table>
        <thead>
            <tr>
                <th>Platform</th>
                <th>Category</th>
                <th>Status</th>
                <th>Confidence</th>
                <th>Profile URL</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>

    <footer>
        Generated by USCAN v{report.version} &middot; {report.started_at.strftime('%Y-%m-%d %H:%M:%S UTC')}
    </footer>
</div>
</body>
</html>"""

        output_path.write_text(html, encoding="utf-8")
        return output_path
