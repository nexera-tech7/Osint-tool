"""USCAN CLI — main entry point."""

from __future__ import annotations

import asyncio
import signal
import sys
import time
from pathlib import Path
from typing import Optional

import typer

from uscan import __version__, __app_name__
from uscan.config import AppConfig
from uscan.ui.console import USCANConsole
from uscan.platforms.registry import get_default_registry
from uscan.scanner.engine import ScanEngine
from uscan.scanner.models import ScanReport, ScanResult
from uscan.utils.validation import validate_username, normalize_username, generate_variants
from uscan.utils.normalization import read_usernames_file
from uscan.utils.logging import setup_logging

app = typer.Typer(
    name="uscan",
    help="USCAN — Username Intelligence & OSINT Discovery Tool",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"USCAN v{__version__}")
        raise typer.Exit()


def _export_report(
    report: ScanReport,
    output_dir: Path,
    output_file: str | None,
    *,
    do_json: bool = False,
    do_txt: bool = False,
    do_csv: bool = False,
    do_html: bool = False,
    do_pdf: bool = False,
) -> list[str]:
    paths: list[str] = []
    base = report.username

    if do_json:
        from uscan.exporters.json_exporter import JSONExporter
        p = Path(output_file) if output_file and output_file.endswith(".json") else output_dir / f"{base}.json"
        JSONExporter.export(report, p)
        paths.append(str(p))

    if do_txt:
        from uscan.exporters.txt_exporter import TXTExporter
        p = Path(output_file) if output_file and output_file.endswith(".txt") else output_dir / f"{base}.txt"
        TXTExporter.export(report, p)
        paths.append(str(p))

    if do_csv:
        from uscan.exporters.csv_exporter import CSVExporter
        p = Path(output_file) if output_file and output_file.endswith(".csv") else output_dir / f"{base}.csv"
        CSVExporter.export(report, p)
        paths.append(str(p))

    if do_html:
        from uscan.exporters.html_exporter import HTMLExporter
        p = Path(output_file) if output_file and output_file.endswith(".html") else output_dir / f"{base}.html"
        HTMLExporter.export(report, p)
        paths.append(str(p))

    if do_pdf:
        from uscan.exporters.pdf_exporter import PDFExporter
        p = Path(output_file) if output_file and output_file.endswith(".pdf") else output_dir / f"{base}.pdf"
        PDFExporter.export(report, p)
        paths.append(str(p))

    return paths


def _run_scan(
    username: str,
    config: AppConfig,
    ui: USCANConsole,
    *,
    platform_filter: str | None = None,
    categories: str | None = None,
    mock: bool = False,
    only_found: bool = False,
    do_json: bool = False,
    do_txt: bool = False,
    do_csv: bool = False,
    do_html: bool = False,
    do_pdf: bool = False,
    output_file: str | None = None,
) -> ScanReport:
    registry = get_default_registry()

    platform_names = [p.strip() for p in platform_filter.split(",")] if platform_filter else None
    category_list = [c.strip() for c in categories.split(",")] if categories else None

    platforms = registry.filter(
        platform_names=platform_names,
        categories=category_list,
        disabled=config.disabled_platforms or None,
        enabled=config.enabled_platforms or None,
    )

    if not platforms:
        ui.print_error("No platforms matched the given filters.")
        raise typer.Exit(1)

    ui.print_scan_header(
        username,
        len(platforms),
        config.scan.concurrency,
        config.scan.timeout,
    )

    if mock:
        from uscan.mock import generate_mock_result

        report = ScanReport(username=username, concurrency=config.scan.concurrency)
        for i, p in enumerate(platforms, 1):
            result = generate_mock_result(username, p)
            report.results.append(result)
            ui.print_result_line(result, i, len(platforms))
            time.sleep(0.02)
        report.finalize()
    else:
        engine = ScanEngine(platforms, config.scan)

        def on_result(result: ScanResult, completed: int, total: int) -> None:
            ui.print_result_line(result, completed, total)

        def handle_sigint(*_: object) -> None:
            engine.cancel()

        prev_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, handle_sigint)

        try:
            report = asyncio.run(engine.scan(username, on_result=on_result))
        finally:
            signal.signal(signal.SIGINT, prev_handler)

    ui.print_results(report, only_found=only_found)
    ui.print_summary(report)

    any_export = do_json or do_txt or do_csv or do_html or do_pdf
    if any_export:
        try:
            paths = _export_report(
                report,
                config.output.directory,
                output_file,
                do_json=do_json,
                do_txt=do_txt,
                do_csv=do_csv,
                do_html=do_html,
                do_pdf=do_pdf,
            )
            ui.print_export_paths(paths)
        except Exception as e:
            ui.print_error(f"Export failed: {e}")

    return report


@app.command(name="scan", hidden=True)
@app.callback(invoke_without_command=True)
def scan_command(
    usernames: Optional[list[str]] = typer.Argument(None, help="Username(s) to scan"),
    version: bool = typer.Option(False, "--version", "-V", callback=_version_callback, is_eager=True, help="Show version"),
    platform: Optional[str] = typer.Option(None, "--platform", "-p", help="Scan specific platform(s), comma-separated"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Scan category (social,developer,gaming,content,professional)"),
    threads: int = typer.Option(10, "--threads", "-t", min=1, max=30, help="Concurrent workers"),
    timeout: float = typer.Option(10.0, "--timeout", help="Request timeout in seconds"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Minimal output"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Debug output"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colors"),
    only_found: bool = typer.Option(False, "--only-found", help="Show only found results"),
    json_export: bool = typer.Option(False, "--json", help="Export JSON report"),
    txt_export: bool = typer.Option(False, "--txt", help="Export TXT report"),
    csv_export: bool = typer.Option(False, "--csv", help="Export CSV report"),
    html_export: bool = typer.Option(False, "--html", help="Export HTML report"),
    pdf_export: bool = typer.Option(False, "--pdf", help="Export PDF report"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    input_file: Optional[str] = typer.Option(None, "--input", "-i", help="Read usernames from file"),
    mock: bool = typer.Option(False, "--mock", help="Run with mock data (no network)"),
    demo: bool = typer.Option(False, "--demo", help="Demo mode with simulated results"),
    variants: bool = typer.Option(False, "--variants", help="Also scan common username variants"),
    platforms_list: bool = typer.Option(False, "--platforms", help="List all supported platforms"),
    cache: bool = typer.Option(False, "--cache", help="Enable result caching"),
    clear_cache: bool = typer.Option(False, "--clear-cache", help="Clear the result cache"),
) -> None:
    """Scan public platforms for a username."""
    setup_logging(verbose)
    config = AppConfig.load()
    config.scan.concurrency = threads
    config.scan.timeout = timeout
    config.output.quiet = quiet
    config.output.verbose = verbose
    config.output.color = not no_color
    config.cache.enabled = cache

    ui = USCANConsole(color=not no_color, quiet=quiet)

    if clear_cache:
        from uscan.cache import ScanCache
        sc = ScanCache(config.cache)
        count = sc.clear()
        ui.print_info(f"Cleared {count} cached entries.")
        raise typer.Exit()

    if platforms_list:
        ui.print_banner()
        registry = get_default_registry()
        items = [
            (p.name, p.category, p.url_pattern)
            for p in sorted(registry.all(), key=lambda x: (x.category, x.name))
        ]
        ui.print_platform_list(items)
        raise typer.Exit()

    if demo:
        usernames = ["demo_user"]
        mock = True

    targets: list[str] = []

    if input_file:
        try:
            targets.extend(read_usernames_file(input_file))
        except FileNotFoundError as e:
            ui.print_error(str(e))
            raise typer.Exit(1)

    if usernames:
        targets.extend(usernames)

    if not targets:
        ui.print_banner()
        ui.print_error("No username provided. Usage: uscan <username>")
        raise typer.Exit(1)

    ui.print_banner()

    for raw_username in targets:
        username = normalize_username(raw_username)
        valid, err = validate_username(username)
        if not valid:
            ui.print_error(f"Invalid username '{raw_username}': {err}")
            continue

        scan_targets = [username]
        if variants:
            scan_targets = generate_variants(username)
            ui.print_info(f"Scanning variants: {', '.join(scan_targets)}")

        for target in scan_targets:
            _run_scan(
                target,
                config,
                ui,
                platform_filter=platform,
                categories=category,
                mock=mock,
                only_found=only_found,
                do_json=json_export,
                do_txt=txt_export,
                do_csv=csv_export,
                do_html=html_export,
                do_pdf=pdf_export,
                output_file=output,
            )

        if len(targets) > 1:
            ui.console.print()


def main() -> None:
    app()
