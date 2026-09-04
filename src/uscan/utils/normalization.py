"""Input normalization helpers."""

from __future__ import annotations

from pathlib import Path


def read_usernames_file(path: str) -> list[str]:
    """Read usernames from a text file, one per line."""
    filepath = Path(path)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {path}")

    usernames = []
    for line in filepath.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            usernames.append(line)

    return usernames
