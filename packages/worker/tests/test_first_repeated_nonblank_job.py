import pytest

from dogfood_worker import first_repeated_nonblank_job


def test_first_repeated_nonblank_job_returns_first_job_to_repeat() -> None:
    jobs = ["build", "deploy", "deploy", "build"]
    original_jobs = jobs.copy()

    assert first_repeated_nonblank_job(jobs) == "deploy"
    assert jobs == original_jobs


def test_first_repeated_nonblank_job_reuses_nonblank_normalization() -> None:
    jobs = ("  build  ", "", "\tdeploy", " deploy\n", "build")

    assert first_repeated_nonblank_job(jobs) == "deploy"
    assert jobs == ("  build  ", "", "\tdeploy", " deploy\n", "build")


@pytest.mark.parametrize(
    "jobs",
    [
        [],
        ["", "   ", "\t", "\n"],
        ["build", "deploy", "test"],
        ("  build  ", "deploy", "test"),
    ],
)
def test_first_repeated_nonblank_job_returns_none_without_a_repeated_job(
    jobs: list[str] | tuple[str, ...],
) -> None:
    assert first_repeated_nonblank_job(jobs) is None
