"""PawPal+ core object model: Task, Pet, Owner, Scheduler.

Skeleton only (Phase 1, Step 4) — attributes and method stubs, no logic.
"""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    title: str
    category: str
    time: str
    duration_minutes: int
    priority: str
    frequency: str
    task_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True
        # TODO (Phase 4): if frequency is 'daily' or 'weekly', build and
        # return a new Task with task_date advanced via timedelta (+1 or +7
        # days). Returns None for 'once' tasks.
        return None


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's list of tasks."""
        return self.tasks

    def complete_task(self, task: Task) -> None:
        """Complete a task and add any resulting recurring follow-up task to this pet's list."""
        follow_up = task.mark_complete()
        # TODO (Phase 4): once Task.mark_complete() returns a follow-up Task
        # for 'daily'/'weekly' frequencies, this will add it automatically.
        if follow_up is not None:
            self.add_task(follow_up)


class Owner:
    def __init__(self, name: str):
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs for every task across all pets."""
        return [(pet, task) for pet in self.pets for task in pet.get_tasks()]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner

    def sort_by_time(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Sort (pet, task) pairs by task_date, then by time."""
        pass

    def filter_tasks(self, pet_name: str | None = None, completed: bool | None = None) -> list[tuple[Pet, Task]]:
        """Filter (pet, task) pairs by pet name and/or completion status."""
        pass

    def detect_conflicts(self, tasks: list[tuple[Pet, Task]]) -> list:
        """Detect overlapping time windows across all pets' tasks."""
        pass

    def generate_daily_schedule(self) -> list[tuple[Pet, Task]]:
        """Build the day's schedule by combining sorting, filtering, and conflict checks."""
        pass
