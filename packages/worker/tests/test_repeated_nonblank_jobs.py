from dogfood_worker import repeated_nonblank_jobs


def test_repeated_nonblank_jobs_follows_second_occurrence_order() -> None:
    jobs = [" build ", "deploy", "build", " deploy\n", "build", "test"]
    original_jobs = jobs.copy()

    assert repeated_nonblank_jobs(jobs) == ["build", "deploy"]
    assert jobs == original_jobs


def test_repeated_nonblank_jobs_reuses_nonblank_normalization() -> None:
    jobs = ("", " build ", "\t", "build\n", " deploy", "deploy ", "build")

    assert repeated_nonblank_jobs(jobs) == ["build", "deploy"]
    assert jobs == ("", " build ", "\t", "build\n", " deploy", "deploy ", "build")


def test_repeated_nonblank_jobs_returns_empty_without_repeats() -> None:
    assert repeated_nonblank_jobs([]) == []
    assert repeated_nonblank_jobs(["", "   ", "\t", "\n"]) == []
    assert repeated_nonblank_jobs(["build", "deploy", "test"]) == []
