from pawpal_system import Task


def test_mark_complete_sets_completed_true():
    task = Task(
        title="Feed",
        category="feeding",
        time="08:00",
        duration_minutes=15,
        priority="medium",
        frequency="once",
    )
    task.mark_complete()
    assert task.completed is True
