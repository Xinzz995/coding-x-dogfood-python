from dogfood_worker import (
    last_nonblank_job,
    next_job,
    next_nonblank_job,
    nonblank_jobs,
    unique_nonblank_jobs,
)


def test_next_job_returns_first_item() -> None:
    assert next_job(["build", "deploy"]) == "build"


def test_next_job_handles_empty_queue() -> None:
    assert next_job([]) is None


def test_next_job_keeps_blank_first_item() -> None:
    assert next_job(["   ", "build"]) == "   "


def test_next_nonblank_job_strips_and_preserves_input() -> None:
    jobs = ["   ", "  build  ", "deploy"]
    original_jobs = jobs.copy()

    assert next_nonblank_job(jobs) == "build"
    assert jobs == original_jobs


def test_next_nonblank_job_handles_no_available_job() -> None:
    assert next_nonblank_job([]) is None
    assert next_nonblank_job(["   ", "\t"]) is None


def test_nonblank_jobs_filters_trims_preserves_order_and_input() -> None:
    jobs = ["  build  ", "", "\tdeploy\n", "   ", "test"]
    original_jobs = jobs.copy()

    assert nonblank_jobs(jobs) == ["build", "deploy", "test"]
    assert jobs == original_jobs


def test_nonblank_jobs_accepts_an_immutable_sequence() -> None:
    jobs = ("  build  ", "", "deploy")

    assert nonblank_jobs(jobs) == ["build", "deploy"]
    assert jobs == ("  build  ", "", "deploy")


def test_nonblank_jobs_handles_empty_input() -> None:
    assert nonblank_jobs([]) == []


def test_nonblank_jobs_handles_all_blank_input() -> None:
    assert nonblank_jobs(["", "   ", "\t", "\n"]) == []


def test_unique_nonblank_jobs_normalizes_deduplicates_and_preserves_input() -> None:
    jobs = ["  build  ", "", "deploy", "build", "  deploy\n", "test"]
    original_jobs = jobs.copy()

    assert unique_nonblank_jobs(jobs) == ["build", "deploy", "test"]
    assert jobs == original_jobs


def test_unique_nonblank_jobs_handles_empty_and_all_blank_input() -> None:
    assert unique_nonblank_jobs([]) == []
    assert unique_nonblank_jobs(["", "   ", "\t", "\n"]) == []


def test_last_nonblank_job_returns_trimmed_last_match_without_mutating_input() -> None:
    jobs = ["  build  ", "", " deploy ", "\t", "  test  ", "   "]
    original_jobs = jobs.copy()

    assert last_nonblank_job(jobs) == "test"
    assert jobs == original_jobs


def test_last_nonblank_job_accepts_an_immutable_sequence() -> None:
    jobs = ("  build  ", "", " deploy ")

    assert last_nonblank_job(jobs) == "deploy"
    assert jobs == ("  build  ", "", " deploy ")


def test_last_nonblank_job_handles_empty_and_all_blank_input() -> None:
    assert last_nonblank_job([]) is None
    assert last_nonblank_job(["", "   ", "\t", "\n"]) is None
