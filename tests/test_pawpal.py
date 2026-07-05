from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_add_pet_increases_count():
    owner = Owner(name="Andre")
    owner.add_pet(Pet(name="Rex", species="dog"))
    assert len(owner.pets) == 1


def test_get_all_tasks_returns_pet_task_pairs_across_pets():
    owner = Owner(name="Andre")
    dog = Pet(name="Rex", species="dog")
    cat = Pet(name="Milo", species="cat")
    dog_task = make_task(title="Walk")
    cat_task = make_task(title="Feed")
    dog.add_task(dog_task)
    cat.add_task(cat_task)
    owner.add_pet(dog)
    owner.add_pet(cat)

    pairs = owner.get_all_tasks()

    assert pairs == [(dog, dog_task), (cat, cat_task)]


def test_task_str_is_readable():
    task = make_task(title="Walk", category="walk", time="09:00", priority="high")
    assert str(task) == "09:00 — Walk (walk, high)"


def test_generate_daily_schedule_returns_schedule_and_conflicts():
    owner = Owner(name="Andre")
    pet = Pet(name="Rex", species="dog")
    pet.add_task(make_task())
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    schedule, conflicts = scheduler.generate_daily_schedule()

    assert schedule == owner.get_all_tasks()
    assert conflicts == []
