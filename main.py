"""PawPal+ demo script: builds an owner, pets, and tasks, then prints the day's schedule."""

from pawpal_system import Owner, Pet, Scheduler, Task

owner = Owner(name="Andre")

dog = Pet(name="Rex", species="dog", breed="Labrador")
cat = Pet(name="Milo", species="cat")

dog.add_task(Task(
    title="Morning Walk",
    category="walk",
    time="08:00",
    duration_minutes=30,
    priority="high",
    frequency="daily",
))
dog.add_task(Task(
    title="Dinner",
    category="feeding",
    time="18:00",
    duration_minutes=15,
    priority="medium",
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
        print(f"{pet_a.name}: {task_a}  <->  {pet_b.name}: {task_b}")
