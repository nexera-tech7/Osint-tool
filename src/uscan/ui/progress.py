"""Live progress display during scanning."""

from __future__ import annotations

from typing import Any

from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, MofNCompleteColumn
from rich.table import Table
from rich.text import Text

from uscan.scanner.models import ScanResult, ScanStatus
from uscan.ui.theme import STATUS_SYMBOLS, STATUS_STYLES


class ScanProgress:
    """Manages the live scanning display."""

    def __init__(self, total: int, console: Any) -> None:
        self.total = total
        self.console = console
        self._results: list[ScanResult] = []
        self._found = 0
        self._not_found = 0
        self._errors = 0

        self.progress = Progress(
            TextColumn("[uscan.header]Scanning[/]"),
            BarColumn(bar_width=40, style="dim red", complete_style="bright_red", finished_style="green"),
            MofNCompleteColumn(),
            TextColumn("•"),
            TimeElapsedColumn(),
            console=console,
        )
        self.task_id = self.progress.add_task("scan", total=total)

    def update(self, result: ScanResult, completed: int, total: int) -> None:
        self._results.append(result)
        match result.status:
            case ScanStatus.FOUND:
                self._found += 1
            case ScanStatus.NOT_FOUND:
                self._not_found += 1
            case ScanStatus.ERROR | ScanStatus.BLOCKED | ScanStatus.RATE_LIMITED:
                self._errors += 1
        self.progress.update(self.task_id, completed=completed)

    def get_display(self) -> Table:
        grid = Table.grid(padding=(0, 0))
        grid.add_row(self.progress)

        counters = Text()
        counters.append(" Found: ", style="dim")
        counters.append(f"{self._found}", style="uscan.found")
        counters.append("  Not Found: ", style="dim")
        counters.append(f"{self._not_found}", style="dim")
        counters.append("  Errors: ", style="dim")
        counters.append(f"{self._errors}", style="uscan.error")
        grid.add_row(counters)

        if self._results:
            last = self._results[-1]
            symbol = STATUS_SYMBOLS.get(last.status.value, " ")
            style = STATUS_STYLES.get(last.status.value, "")
            grid.add_row(Text.from_markup(
                f" {symbol} {last.platform:<20} [{style}]{last.status.value}[/]"
            ))

        return grid
