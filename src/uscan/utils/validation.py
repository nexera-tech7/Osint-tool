"""Username validation utilities."""

from __future__ import annotations

import re
import unicodedata


GENERAL_USERNAME_RE = re.compile(r"^[a-zA-Z0-9._@-]+$")
MIN_LENGTH = 1
MAX_LENGTH = 64


def validate_username(username: str) -> tuple[bool, str]:
    """Validate a username. Returns (is_valid, error_message)."""
    if not username:
        return False, "Username cannot be empty"

    if len(username) < MIN_LENGTH:
        return False, f"Username too short (min {MIN_LENGTH} characters)"

    if len(username) > MAX_LENGTH:
        return False, f"Username too long (max {MAX_LENGTH} characters)"

    if not GENERAL_USERNAME_RE.match(username):
        bad = [c for c in username if not GENERAL_USERNAME_RE.match(c)]
        return False, f"Invalid characters: {', '.join(repr(c) for c in bad[:5])}"

    return True, ""


def normalize_username(raw: str) -> str:
    """Normalize a raw username input."""
    username = raw.strip()
    username = unicodedata.normalize("NFKC", username)
    username = username.lstrip("@")
    return username


def generate_variants(username: str) -> list[str]:
    """Generate reasonable username variants."""
    variants = [username]
    seen = {username}

    candidates = [
        f"_{username}",
        f"{username}_",
        f"{username}123",
        f"{username}1",
        f"{username}_",
        username.replace(".", "_"),
        username.replace("_", "."),
        username.replace("-", "_"),
        username.lower(),
    ]

    for c in candidates:
        if c and c not in seen and GENERAL_USERNAME_RE.match(c):
            variants.append(c)
            seen.add(c)

    return variants[:8]
