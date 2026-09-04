"""ASCII banner and branding."""

from __future__ import annotations

from rich.text import Text

BANNER = r"""
 ██╗   ██╗███████╗ ██████╗ █████╗ ███╗   ██╗
 ██║   ██║██╔════╝██╔════╝██╔══██╗████╗  ██║
 ██║   ██║███████╗██║     ███████║██╔██╗ ██║
 ██║   ██║╚════██║██║     ██╔══██║██║╚██╗██║
 ╚██████╔╝███████║╚██████╗██║  ██║██║ ╚████║
  ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
"""

TAGLINE = "USERNAME INTELLIGENCE & OSINT DISCOVERY"
SUBTITLE = "Public-source discovery engine"


def get_banner_text() -> Text:
    text = Text()
    text.append(BANNER, style="bold red")
    text.append(f" {TAGLINE}\n", style="bold bright_red")
    text.append(f" {SUBTITLE}\n", style="dim white")
    return text


def get_banner_plain() -> str:
    return f"{BANNER}\n {TAGLINE}\n {SUBTITLE}\n"
