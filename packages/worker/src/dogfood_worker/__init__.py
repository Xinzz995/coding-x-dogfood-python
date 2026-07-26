"""Worker fixture behavior."""

from collections.abc import Sequence


def next_job(jobs: Sequence[str]) -> str | None:
    """Return the next queued job without mutating the input sequence."""
    return jobs[0] if jobs else None
