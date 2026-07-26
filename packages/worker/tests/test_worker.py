from dogfood_worker import next_job


def test_next_job_returns_first_item() -> None:
    assert next_job(["build", "deploy"]) == "build"


def test_next_job_handles_empty_queue() -> None:
    assert next_job([]) is None
