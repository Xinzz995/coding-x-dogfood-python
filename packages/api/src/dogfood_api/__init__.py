"""API fixture behavior."""

from collections.abc import Sequence


def normalize_name(name: str) -> str:
    """Return a stable display name for an API caller."""
    normalized = name.strip()
    return normalized or "anonymous"


def normalize_names(names: Sequence[str]) -> list[str]:
    """Return normalized display names in input order."""
    return [normalize_name(name) for name in names]


def normalize_unique_names(names: Sequence[str]) -> list[str]:
    """Return normalized display names without duplicate results."""
    return list(dict.fromkeys(normalize_names(names)))
