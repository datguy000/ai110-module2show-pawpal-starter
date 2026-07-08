"""PawPal+ core object model: Task, Pet, Owner, Scheduler.

Skeleton only (Phase 1, Step 4) — attributes and method stubs, no logic.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta


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

    def mark_complete(self) -> "Task | None":
        """Mark this task as completed and return a follow-up task if it recurs."""
        self.completed = True
        if self.frequency == "daily":
            delta = timedelta(days=1)
        elif self.frequency == "weekly":
            delta = timedelta(days=7)
        else:
            return None
        return Task(
            title=self.title,
            category=self.category,
            time=self.time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            task_date=self.task_date + delta,
            completed=False,
        )

    def __str__(self) -> str:
        """Return a readable one-line summary of this task."""
        return f"{self.time} - {self.title} ({self.category}, {self.priority})"


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

    def get_or_create_pet(self, name: str, species: str) -> Pet:
        """Return the existing pet matching name and species, or create and add a new one."""
        for pet in self.pets:
            if pet.name == name and pet.species == species:
                return pet
        pet = Pet(name=name, species=species)
        self.add_pet(pet)
        return pet


def _time_to_minutes(time_str: str) -> int:
    """Convert an 'HH:MM' string to minutes since midnight."""
    hours, minutes = time_str.split(":")
    return int(hours) * 60 + int(minutes)


def _minutes_to_time(minutes: int) -> str:
    """Convert minutes since midnight to a zero-padded 'HH:MM' string."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


SEARCH_DAY_START = "06:00"
SEARCH_DAY_END = "22:00"
SLOT_STEP_MINUTES = 15


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner

    def sort_by_time(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Sort (pet, task) pairs by task_date, then by time."""
        return sorted(tasks, key=lambda pair: (pair[1].task_date, pair[1].time))

    def filter_tasks(
        self,
        tasks: list[tuple[Pet, Task]],
        pet_name: str | None = None,
        species: str | None = None,
        completed: bool | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Filter (pet, task) pairs by pet name, species, and/or completion status."""
        result = tasks
        if pet_name is not None:
            result = [pair for pair in result if pair[0].name == pet_name]
        if species is not None:
            result = [pair for pair in result if pair[0].species == species]
        if completed is not None:
            result = [pair for pair in result if pair[1].completed == completed]
        return result

    def detect_conflicts(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[tuple[Pet, Task], tuple[Pet, Task]]]:
        """Detect overlapping time windows across all pets' tasks; returns pairs of conflicting (Pet, Task) entries."""
        conflicts = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                task_a = tasks[i][1]
                task_b = tasks[j][1]
                if task_a.task_date != task_b.task_date:
                    continue
                start_a = _time_to_minutes(task_a.time)
                end_a = start_a + task_a.duration_minutes
                start_b = _time_to_minutes(task_b.time)
                end_b = start_b + task_b.duration_minutes
                if start_a < end_b and start_b < end_a:
                    conflicts.append((tasks[i], tasks[j]))
        return conflicts

    def sort_by_priority_then_time(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Sort (pet, task) pairs by priority (high, medium, low), then by time within each tier."""
        priority_weight = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            tasks,
            key=lambda pair: (priority_weight[pair[1].priority], pair[1].task_date, pair[1].time),
        )

    def find_next_available_slot(
        self,
        tasks: list[tuple[Pet, Task]],
        duration_minutes: int,
        after_time: str | None = None,
    ) -> str | None:
        """Find the next 'HH:MM' start time (within 06:00-22:00) fitting duration_minutes with no conflicts."""
        busy_windows = [
            (_time_to_minutes(task.time), _time_to_minutes(task.time) + task.duration_minutes)
            for _, task in tasks
        ]
        day_start = _time_to_minutes(SEARCH_DAY_START)
        day_end = _time_to_minutes(SEARCH_DAY_END)
        earliest = max(day_start, _time_to_minutes(after_time)) if after_time else day_start

        candidate = earliest
        while candidate + duration_minutes <= day_end:
            candidate_end = candidate + duration_minutes
            if not any(candidate < busy_end and busy_start < candidate_end for busy_start, busy_end in busy_windows):
                return _minutes_to_time(candidate)
            candidate += SLOT_STEP_MINUTES

        return None

    def generate_daily_schedule(self) -> tuple[list[tuple[Pet, Task]], list]:
        """Build the day's schedule by combining sorting, filtering, and conflict checks."""
        all_tasks = self.owner.get_all_tasks()
        sorted_tasks = self.sort_by_time(all_tasks)
        schedule = self.filter_tasks(sorted_tasks)
        conflicts = self.detect_conflicts(schedule)
        return schedule, conflicts
