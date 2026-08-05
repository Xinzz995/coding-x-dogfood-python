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


def normalized_name_counts(names: Sequence[str]) -> dict[str, int]:
    """Return counts of normalized display names in first-seen order."""
    counts: dict[str, int] = {}
    for name in names:
        normalized_name = normalize_name(name)
        counts[normalized_name] = counts.get(normalized_name, 0) + 1
    return counts
