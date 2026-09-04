"""USCAN color theme and styling constants."""

from rich.theme import Theme

USCAN_THEME = Theme({
    "uscan.brand": "bold red",
    "uscan.header": "bold bright_red",
    "uscan.separator": "dim red",
    "uscan.label": "dim white",
    "uscan.value": "bold white",
    "uscan.found": "bold bright_green",
    "uscan.not_found": "dim",
    "uscan.unknown": "yellow",
    "uscan.error": "bold red",
    "uscan.rate_limited": "yellow",
    "uscan.blocked": "bold yellow",
    "uscan.high": "bold bright_green",
    "uscan.medium": "green",
    "uscan.low": "dim yellow",
    "uscan.url": "underline cyan",
    "uscan.platform": "white",
    "uscan.counter": "bold bright_red",
    "uscan.stat_label": "dim white",
    "uscan.stat_value": "bold white",
    "uscan.success": "bold green",
    "uscan.warning": "bold yellow",
    "uscan.info": "bold blue",
})

STATUS_SYMBOLS = {
    "FOUND": "[uscan.found]✓[/]",
    "NOT_FOUND": "[uscan.not_found]✗[/]",
    "UNKNOWN": "[uscan.unknown]?[/]",
    "RATE_LIMITED": "[uscan.rate_limited]![/]",
    "BLOCKED": "[uscan.blocked]⊘[/]",
    "ERROR": "[uscan.error]✖[/]",
}

STATUS_STYLES = {
    "FOUND": "uscan.found",
    "NOT_FOUND": "uscan.not_found",
    "UNKNOWN": "uscan.unknown",
    "RATE_LIMITED": "uscan.rate_limited",
    "BLOCKED": "uscan.blocked",
    "ERROR": "uscan.error",
}

CONFIDENCE_STYLES = {
    "HIGH": "uscan.high",
    "MEDIUM": "uscan.medium",
    "LOW": "uscan.low",
    "NONE": "dim",
}
