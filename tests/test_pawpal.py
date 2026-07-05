from pawpal_system import Pet, Task


def make_task(**overrides):
    defaults = dict(
        title="Feed",
        category="feeding",
        time="08:00",
        duration_minutes=15,
        priority="medium",
        frequency="once",
    )
    defaults.update(overrides)
    return Task(**defaults)


def test_mark_complete_sets_completed_true():
    task = make_task()
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Rex", species="dog")
    pet.add_task(make_task())
    assert len(pet.get_tasks()) == 1


def test_get_tasks_returns_pets_tasks():
    pet = Pet(name="Rex", species="dog")
    task = make_task()
    pet.add_task(task)
    assert pet.get_tasks() == [task]


def test_complete_task_marks_completed_and_does_not_duplicate_once_task():
    pet = Pet(name="Rex", species="dog")
    task = make_task(frequency="once")
    pet.add_task(task)
    pet.complete_task(task)
    assert task.completed is True
    assert len(pet.get_tasks()) == 1
