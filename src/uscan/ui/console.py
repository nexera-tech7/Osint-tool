"""Main console UI controller."""

from __future__ import annotations

import sys
from datetime import datetime

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from uscan import __version__
from uscan.banner import get_banner_text, get_banner_plain
from uscan.scanner.models import ScanReport, ScanResult, ScanStatus
from uscan.ui.theme import USCAN_THEME, STATUS_SYMBOLS, STATUS_STYLES
from uscan.ui.tables import build_results_table, build_summary_table, build_platform_list_table
from uscan.ui.progress import ScanProgress


class USCANConsole:
    """High-level terminal UI for USCAN."""

    def __init__(self, *, color: bool = True, quiet: bool = False) -> None:
        self.quiet = quiet
        force_terminal = None if sys.stdout.isatty() else False

        if sys.platform == "win32" and sys.stdout.isatty():
            try:
                sys.stdout.reconfigure(encoding="utf-8")
            except Exception:
                pass

        self.console = Console(
            theme=USCAN_THEME,
            force_terminal=force_terminal,
            no_color=not color,
            force_jupyter=False,
        )
        self._is_tty = sys.stdout.isatty()

    def print_banner(self) -> None:
        if self.quiet:
            return
        self.console.print(get_banner_text())
        self.console.print(
            f" [dim]v{__version__}[/]",
            highlight=False,
        )
        self.console.print()

    def print_scan_header(
        self,
        username: str,
        platform_count: int,
        concurrency: int,
        timeout: float,
    ) -> None:
        if self.quiet:
            return
        self.console.print("[uscan.separator]" + "━" * 60 + "[/]")
        self.console.print(f" [uscan.label]Target       [/] [uscan.value]{username}[/]")
        self.console.print(f" [uscan.label]Started      [/] [uscan.value]{datetime.now().strftime('%H:%M:%S')}[/]")
        self.console.print(f" [uscan.label]Platforms    [/] [uscan.value]{platform_count}[/]")
        self.console.print(f" [uscan.label]Workers      [/] [uscan.value]{concurrency}[/]")
        self.console.print(f" [uscan.label]Timeout      [/] [uscan.value]{timeout}s[/]")
        self.console.print("[uscan.separator]" + "━" * 60 + "[/]")
        self.console.print()

    def print_result_line(self, result: ScanResult, index: int, total: int) -> None:
        if self.quiet:
            return
        symbol = STATUS_SYMBOLS.get(result.status.value, " ")
        style = STATUS_STYLES.get(result.status.value, "")
        pad = len(str(total))
        idx = str(index).rjust(pad, "0")
        self.console.print(
            f" [dim][{idx}/{total}][/] {symbol} {result.platform:<22} [{style}]{result.status.value}[/]"
        )

    def print_results(self, report: ScanReport, *, only_found: bool = False) -> None:
        self.console.print()
        self.console.print("[uscan.separator]" + "━" * 60 + "[/]")
        self.console.print()
        self.console.print(build_results_table(report, only_found=only_found))

    def print_summary(self, report: ScanReport) -> None:
        self.console.print()
        self.console.print("[uscan.separator]" + "━" * 60 + "[/]")
        self.console.print(
            " [uscan.header]SCAN COMPLETE[/]",
        )
        self.console.print()
        self.console.print(build_summary_table(report))

    def print_export_paths(self, paths: list[str]) -> None:
        if not paths:
            return
        self.console.print()
        self.console.print(" [uscan.label]Reports:[/]")
        for p in paths:
            self.console.print(f"   [uscan.url]{p}[/]")

    def print_platform_list(self, platforms: list[tuple[str, str, str]]) -> None:
        self.console.print(build_platform_list_table(platforms))
        self.console.print(f"\n [uscan.stat_label]Total:[/] [uscan.stat_value]{len(platforms)} platforms[/]")

    def print_error(self, message: str) -> None:
        self.console.print(f" [uscan.error]Error:[/] {message}")

    def print_warning(self, message: str) -> None:
        self.console.print(f" [uscan.warning]Warning:[/] {message}")

    def print_info(self, message: str) -> None:
        if not self.quiet:
            self.console.print(f" [uscan.info]Info:[/] {message}")

    def create_progress(self, total: int) -> ScanProgress:
        return ScanProgress(total, self.console)

    def live_context(self) -> Live:
        return Live(console=self.console, refresh_per_second=8)
