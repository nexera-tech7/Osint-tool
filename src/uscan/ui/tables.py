"""Result table rendering."""

from __future__ import annotations

from rich.table import Table

from uscan.scanner.models import ScanReport, ScanResult, ScanStatus
from uscan.ui.theme import STATUS_SYMBOLS, STATUS_STYLES, CONFIDENCE_STYLES


def build_results_table(
    report: ScanReport,
    *,
    only_found: bool = False,
) -> Table:
    table = Table(
        title=None,
        border_style="dim red",
        header_style="bold bright_red",
        show_lines=False,
        padding=(0, 1),
    )
    table.add_column("", width=2)
    table.add_column("PLATFORM", min_width=18)
    table.add_column("STATUS", min_width=12)
    table.add_column("CONFIDENCE", min_width=10)
    table.add_column("PROFILE URL", min_width=20)

    results = report.results
    if only_found:
        results = [r for r in results if r.status == ScanStatus.FOUND]

    for r in results:
        symbol = STATUS_SYMBOLS.get(r.status.value, " ")
        status_style = STATUS_STYLES.get(r.status.value, "")
        conf_style = CONFIDENCE_STYLES.get(r.confidence.value, "dim")

        url_display = r.profile_url or "—"
        if len(url_display) > 50:
            url_display = url_display[:47] + "..."

        table.add_row(
            symbol,
            f"[uscan.platform]{r.platform}[/]",
            f"[{status_style}]{r.status.value}[/]",
            f"[{conf_style}]{r.confidence.value if r.status == ScanStatus.FOUND else '—'}[/]",
            f"[uscan.url]{url_display}[/]" if r.profile_url else "[dim]—[/]",
        )

    return table


def build_summary_table(report: ScanReport) -> Table:
    table = Table(
        show_header=False,
        border_style="dim red",
        padding=(0, 2),
        min_width=40,
    )
    table.add_column("Label", style="uscan.stat_label")
    table.add_column("Value", style="uscan.stat_value", justify="right")

    table.add_row("Target", f"[bold]{report.username}[/]")
    table.add_row("Platforms Checked", str(report.platforms_checked))
    table.add_row("[uscan.found]Found[/]", f"[uscan.found]{report.summary.found}[/]")
    table.add_row("Not Found", str(report.summary.not_found))
    table.add_row("[uscan.unknown]Unknown[/]", f"[uscan.unknown]{report.summary.unknown}[/]")
    if report.summary.errors:
        table.add_row("[uscan.error]Errors[/]", f"[uscan.error]{report.summary.errors}[/]")
    if report.summary.rate_limited:
        table.add_row("[uscan.rate_limited]Rate Limited[/]", f"[uscan.rate_limited]{report.summary.rate_limited}[/]")
    if report.summary.blocked:
        table.add_row("[uscan.blocked]Blocked[/]", f"[uscan.blocked]{report.summary.blocked}[/]")
    if report.duration_seconds is not None:
        table.add_row("Duration", f"{report.duration_seconds}s")

    return table


def build_platform_list_table(platforms: list[tuple[str, str, str]]) -> Table:
    """Build a table listing platforms. Each tuple: (name, category, url_pattern)."""
    table = Table(
        title="[bold bright_red]Supported Platforms[/]",
        border_style="dim red",
        header_style="bold bright_red",
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Platform", min_width=20)
    table.add_column("Category", min_width=12)
    table.add_column("URL Pattern", min_width=30)

    for i, (name, category, url) in enumerate(platforms, 1):
        table.add_row(str(i), name, category, f"[dim]{url}[/]")

    return table
