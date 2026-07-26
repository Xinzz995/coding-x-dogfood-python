"""API fixture behavior."""


def normalize_name(name: str) -> str:
    """Return a stable display name for an API caller."""
    normalized = name.strip()
    return normalized or "anonymous"
