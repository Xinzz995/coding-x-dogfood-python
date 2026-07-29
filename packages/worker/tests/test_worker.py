from dogfood_worker import next_job, next_nonblank_job, nonblank_jobs


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
