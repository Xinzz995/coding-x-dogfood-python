"""Worker fixture behavior."""

from collections.abc import Sequence


def next_job(jobs: Sequence[str]) -> str | None:
    """Return the next queued job without mutating the input sequence."""
    return jobs[0] if jobs else None


def next_nonblank_job(jobs: Sequence[str]) -> str | None:
    """Return the first nonblank queued job without mutating the input sequence."""
    for job in jobs:
        stripped_job = job.strip()
        if stripped_job:
            return stripped_job
    return None


def nonblank_jobs(jobs: Sequence[str]) -> list[str]:
    """Return trimmed nonblank jobs in their original order."""
    return [stripped_job for job in jobs if (stripped_job := job.strip())]


def unique_nonblank_jobs(jobs: Sequence[str]) -> list[str]:
    """Return trimmed nonblank jobs without duplicate results."""
    return list(dict.fromkeys(nonblank_jobs(jobs)))


def first_repeated_nonblank_job(jobs: Sequence[str]) -> str | None:
    """Return the first trimmed nonblank job encountered a second time."""
    seen_jobs: set[str] = set()
    for job in nonblank_jobs(jobs):
        if job in seen_jobs:
            return job
        seen_jobs.add(job)
    return None


def repeated_nonblank_jobs(jobs: Sequence[str]) -> list[str]:
    """Return trimmed nonblank jobs in the order each is first repeated."""
    seen_jobs: set[str] = set()
    repeated_jobs: set[str] = set()
    result: list[str] = []

    for job in nonblank_jobs(jobs):
        if job not in seen_jobs:
            seen_jobs.add(job)
        elif job not in repeated_jobs:
            repeated_jobs.add(job)
            result.append(job)

    return result
