"""PawPal+ demo script: builds an owner, pets, and tasks, then prints the day's schedule."""

from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def _format_range(task):
    """Return the task's time window as 'HH:MM-HH:MM' for conflict display."""
    start = datetime.strptime(task.time, "%H:%M")
    end = start + timedelta(minutes=task.duration_minutes)
    return f"{task.time}-{end.strftime('%H:%M')}"

owner = Owner(name="Andre")

dog = Pet(name="Rex", species="dog", breed="Labrador")
cat = Pet(name="Milo", species="cat")

dog.add_task(Task(
    title="Dinner",
    category="feeding",
    time="18:00",
    duration_minutes=15,
    priority="medium",
    frequency="daily",
))
dog.add_task(Task(
    title="Morning Walk",
    category="walk",
    time="08:00",
    duration_minutes=30,
    priority="high",
    frequency="daily",
))
cat.add_task(Task(
    title="Vet Checkup",
    category="meds",
    time="12:30",
    duration_minutes=45,
    priority="high",
    frequency="once",
))
cat.add_task(Task(
    title="Nail Trim",
    category="grooming",
    time="08:15",
    duration_minutes=20,
    priority="low",
    frequency="once",
))

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner)
schedule, conflicts = scheduler.generate_daily_schedule()

print("Today's Schedule")
for pet, task in schedule:
    print(f"{pet.name}: {task}")

if conflicts:
    print("\nConflicts")
    for (pet_a, task_a), (pet_b, task_b) in conflicts:
        print(
            f"{pet_a.name}: {_format_range(task_a)} {task_a.title}  <->  "
            f"{pet_b.name}: {_format_range(task_b)} {task_b.title}"
        )

priority_view = scheduler.sort_by_priority_then_time(owner.get_all_tasks())

print("\nPriority View")
for pet, task in priority_view:
    print(f"{pet.name}: {task}")
