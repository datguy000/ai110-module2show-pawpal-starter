"""PawPal+ core object model: Task, Pet, Owner, Scheduler.

Skeleton only (Phase 1, Step 4) — attributes and method stubs, no logic.
"""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    title: str
    category: str
    date: date
    time: str
    duration_minutes: int
    priority: str
    frequency: str
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return this pet's list of tasks."""
        pass


class Owner:
    def __init__(self, name: str):
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        pass

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs for every task across all pets."""
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by date, then by time."""
        pass

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> list[Task]:
        """Filter tasks by pet name and/or completion status."""
        pass

    def detect_conflicts(self, tasks: list[Task]) -> list:
        """Detect overlapping time windows across all pets' tasks."""
        pass

    def generate_daily_schedule(self) -> list[Task]:
        """Build the day's schedule by combining sorting, filtering, and conflict checks."""
        pass
