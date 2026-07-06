from datetime import date, timedelta

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
    assert str(task) == "09:00 - Walk (walk, high)"


def test_generate_daily_schedule_returns_schedule_and_conflicts():
    owner = Owner(name="Andre")
    pet = Pet(name="Rex", species="dog")
    pet.add_task(make_task())
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    schedule, conflicts = scheduler.generate_daily_schedule()

    assert schedule == owner.get_all_tasks()
    assert conflicts == []


def test_sort_by_time_orders_tasks_chronologically():
    owner = Owner(name="Andre")
    pet = Pet(name="Rex", species="dog")
    late = make_task(title="Dinner", time="18:00")
    early = make_task(title="Breakfast", time="08:00")
    mid = make_task(title="Walk", time="12:00")
    pet.add_task(late)
    pet.add_task(early)
    pet.add_task(mid)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    sorted_pairs = scheduler.sort_by_time(owner.get_all_tasks())

    assert [task.title for _, task in sorted_pairs] == ["Breakfast", "Walk", "Dinner"]


def test_sort_by_time_orders_by_date_then_time():
    owner = Owner(name="Andre")
    pet = Pet(name="Rex", species="dog")
    tomorrow = make_task(title="Tomorrow", time="07:00", task_date=date.today() + timedelta(days=1))
    today = make_task(title="Today", time="20:00", task_date=date.today())
    pet.add_task(tomorrow)
    pet.add_task(today)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    sorted_pairs = scheduler.sort_by_time(owner.get_all_tasks())

    assert [task.title for _, task in sorted_pairs] == ["Today", "Tomorrow"]


def test_detect_conflicts_flags_overlapping_same_time_tasks():
    owner = Owner(name="Andre")
    dog = Pet(name="Rex", species="dog")
    cat = Pet(name="Milo", species="cat")
    dog_task = make_task(title="Walk", time="08:00", duration_minutes=30)
    cat_task = make_task(title="Groom", time="08:15", duration_minutes=20)
    dog.add_task(dog_task)
    cat.add_task(cat_task)
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    assert len(conflicts) == 1
    conflicting_titles = {conflicts[0][0][1].title, conflicts[0][1][1].title}
    assert conflicting_titles == {"Walk", "Groom"}


def test_detect_conflicts_ignores_non_overlapping_tasks():
    owner = Owner(name="Andre")
    pet = Pet(name="Rex", species="dog")
    task_a = make_task(title="Walk", time="08:00", duration_minutes=30)
    task_b = make_task(title="Feed", time="09:00", duration_minutes=15)
    pet.add_task(task_a)
    pet.add_task(task_b)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    assert conflicts == []


def test_mark_complete_daily_task_creates_follow_up_one_day_later():
    task = make_task(frequency="daily", task_date=date(2026, 7, 5))

    follow_up = task.mark_complete()

    assert follow_up is not None
    assert follow_up.task_date == date(2026, 7, 6)
    assert follow_up.completed is False


def test_mark_complete_weekly_task_creates_follow_up_seven_days_later():
    task = make_task(frequency="weekly", task_date=date(2026, 7, 5))

    follow_up = task.mark_complete()

    assert follow_up is not None
    assert follow_up.task_date == date(2026, 7, 12)


def test_mark_complete_once_task_produces_no_follow_up():
    task = make_task(frequency="once")

    follow_up = task.mark_complete()

    assert follow_up is None


def test_filter_tasks_by_pet_name():
    owner = Owner(name="Andre")
    dog = Pet(name="Rex", species="dog")
    cat = Pet(name="Milo", species="cat")
    dog.add_task(make_task(title="Walk"))
    cat.add_task(make_task(title="Feed"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner)

    result = scheduler.filter_tasks(owner.get_all_tasks(), pet_name="Rex")

    assert [task.title for _, task in result] == ["Walk"]


def test_filter_tasks_by_completed_status():
    owner = Owner(name="Andre")
    pet = Pet(name="Rex", species="dog")
    done_task = make_task(title="Walk")
    done_task.mark_complete()
    pending_task = make_task(title="Feed")
    pet.add_task(done_task)
    pet.add_task(pending_task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    result = scheduler.filter_tasks(owner.get_all_tasks(), completed=True)

    assert [task.title for _, task in result] == ["Walk"]


def test_filter_tasks_by_pet_name_and_species_combination():
    owner = Owner(name="Andre")
    dog_rex = Pet(name="Rex", species="dog")
    cat_rex = Pet(name="Rex", species="cat")
    dog_rex.add_task(make_task(title="Walk"))
    cat_rex.add_task(make_task(title="Groom"))
    owner.add_pet(dog_rex)
    owner.add_pet(cat_rex)
    scheduler = Scheduler(owner)

    result = scheduler.filter_tasks(owner.get_all_tasks(), pet_name="Rex", species="cat")

    assert [task.title for _, task in result] == ["Groom"]


def test_generate_daily_schedule_with_no_pets_returns_empty_schedule_and_conflicts():
    owner = Owner(name="Andre")
    scheduler = Scheduler(owner)

    schedule, conflicts = scheduler.generate_daily_schedule()

    assert schedule == []
    assert conflicts == []


def test_detect_conflicts_flags_identical_time_and_duration_tasks():
    owner = Owner(name="Andre")
    dog = Pet(name="Rex", species="dog")
    cat = Pet(name="Milo", species="cat")
    dog_task = make_task(title="Walk", time="08:00", duration_minutes=30)
    cat_task = make_task(title="Groom", time="08:00", duration_minutes=30)
    dog.add_task(dog_task)
    cat.add_task(cat_task)
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    assert len(conflicts) == 1
    conflicting_titles = {conflicts[0][0][1].title, conflicts[0][1][1].title}
    assert conflicting_titles == {"Walk", "Groom"}


def test_detect_conflicts_reports_all_pairs_among_three_mutually_overlapping_tasks():
    owner = Owner(name="Andre")
    pet = Pet(name="Rex", species="dog")
    task_a = make_task(title="A", time="08:00", duration_minutes=60)
    task_b = make_task(title="B", time="08:15", duration_minutes=60)
    task_c = make_task(title="C", time="08:30", duration_minutes=60)
    pet.add_task(task_a)
    pet.add_task(task_b)
    pet.add_task(task_c)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    conflicting_pairs = {
        frozenset({pair[0][1].title, pair[1][1].title}) for pair in conflicts
    }
    assert conflicting_pairs == {
        frozenset({"A", "B"}),
        frozenset({"A", "C"}),
        frozenset({"B", "C"}),
    }


def test_schedule_with_all_tasks_completed():
    owner = Owner(name="Andre")
    pet = Pet(name="Rex", species="dog")
    task_a = make_task(title="Walk", time="08:00")
    task_b = make_task(title="Feed", time="09:00")
    task_a.mark_complete()
    task_b.mark_complete()
    pet.add_task(task_a)
    pet.add_task(task_b)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    schedule, conflicts = scheduler.generate_daily_schedule()
    completed_only = scheduler.filter_tasks(owner.get_all_tasks(), completed=True)

    assert [task.title for _, task in schedule] == ["Walk", "Feed"]
    assert conflicts == []
    assert [task.title for _, task in completed_only] == ["Walk", "Feed"]


def test_detect_conflicts_ignores_back_to_back_tasks():
    owner = Owner(name="Andre")
    pet = Pet(name="Rex", species="dog")
    task_a = make_task(title="Walk", time="08:00", duration_minutes=30)
    task_b = make_task(title="Feed", time="08:30", duration_minutes=15)
    pet.add_task(task_a)
    pet.add_task(task_b)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    assert conflicts == []


def test_detect_conflicts_ignores_identical_time_on_different_dates():
    owner = Owner(name="Andre")
    dog = Pet(name="Rex", species="dog")
    cat = Pet(name="Milo", species="cat")
    dog_task = make_task(title="Walk", time="08:00", duration_minutes=30, task_date=date(2026, 7, 5))
    cat_task = make_task(title="Groom", time="08:00", duration_minutes=30, task_date=date(2026, 7, 6))
    dog.add_task(dog_task)
    cat.add_task(cat_task)
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    assert conflicts == []


def test_filter_tasks_by_nonexistent_pet_name_returns_empty():
    owner = Owner(name="Andre")
    pet = Pet(name="Rex", species="dog")
    pet.add_task(make_task(title="Walk"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    result = scheduler.filter_tasks(owner.get_all_tasks(), pet_name="Ghost")

    assert result == []


def test_filter_tasks_by_nonexistent_species_returns_empty():
    owner = Owner(name="Andre")
    pet = Pet(name="Rex", species="dog")
    pet.add_task(make_task(title="Walk"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    result = scheduler.filter_tasks(owner.get_all_tasks(), species="bird")

    assert result == []


def test_get_or_create_pet_returns_same_pet_and_does_not_duplicate():
    owner = Owner(name="Andre")

    first = owner.get_or_create_pet("Rex", "dog")
    second = owner.get_or_create_pet("Rex", "dog")

    assert first is second
    assert len(owner.pets) == 1
