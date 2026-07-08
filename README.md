# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule                                                            
Rex: 08:00 - Morning Walk (walk, high)
Milo: 08:15 - Nail Trim (grooming, low)
Milo: 12:30 - Vet Checkup (meds, high)
Rex: 18:00 - Dinner (feeding, medium)

Conflicts
Rex: 08:00-08:30 Morning Walk  <->  Milo: 08:15-08:35 Nail Trim
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

This suite includes 27 tests covering core object behavior (task creation, completion, adding tasks/pets), all four algorithmic features (sorting by time, filtering by pet/species/completion status, conflict detection, and recurring task generation), and edge cases including empty schedules, boundary-exact conflicts (identical time/duration, back-to-back tasks that touch but don't overlap), multi-way overlapping conflicts, and idempotent pet lookup via `get_or_create_pet`.

Sample test output:

```
============================================================ test session starts =============================================================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\costa\CodePath\Summer 2026\AI110\Week4 Project\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 27 items                                                                                                                            

tests\test_pawpal.py ...........................                                                                                        [100%]

============================================================= 27 passed in 0.05s =============================================================
```

**Confidence Level: ⭐⭐⭐⭐☆ (4/5)**

The core logic — sorting, filtering, conflict detection, and recurrence — is thoroughly tested, including boundary cases that are easy to get subtly wrong. I'm slightly short of 5 stars because a few interaction scenarios remain untested for time reasons (e.g., a newly-generated recurring task flowing correctly into a subsequent schedule generation), and the Streamlit UI layer itself isn't covered by automated tests, only manual verification.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time` | Sorts (pet, task) pairs by `task_date`, then by `time` |
| Filtering | `Scheduler.filter_tasks` | Narrows (pet, task) pairs by `pet_name`, `species`, and/or `completed`, AND-combined |
| Conflict handling | `Scheduler.detect_conflicts` | Flags any two tasks (across all pets) whose `[time, time + duration_minutes)` windows overlap on the same date |
| Recurring tasks | `Task.mark_complete` | Completing a `"daily"`/`"weekly"` task returns a new follow-up Task dated +1/+7 days; `"once"` tasks return `None` |

## ✨ Features
- **Multi-pet task tracking** — one Owner manages any number of Pets, each with their own task list
- **Sorting** — `Scheduler.sort_by_time()` orders all tasks chronologically by date, then time
- **Filtering** — `Scheduler.filter_tasks()` narrows tasks by pet name, species, and/or completion status
- **Conflict detection** — `Scheduler.detect_conflicts()` flags overlapping task time windows across all pets, with clear same-name/species disambiguation in warnings
- **Recurring tasks** — completing a daily or weekly task automatically generates the next occurrence via `Task.mark_complete()`
- **Interactive UI** — Streamlit app for adding pets/tasks and generating a live daily schedule, with species and completion-status filters

## 📸 Demo Walkthrough

1. Enter an owner name, then a pet's name and species in the "Quick Demo Inputs" section.
2. Fill out the Add Task form (title, category, duration, priority, time, frequency) and click **Add task**. Repeat for multiple pets by changing the pet name/species fields between additions — each unique name+species pair is tracked as its own pet.
3. The "Current tasks" table shows every task added so far, with a pet column (name and species) so same-named pets stay distinguishable.
4. Click **Generate schedule** to run the Scheduler: tasks are sorted chronologically, optionally filtered by species or completion status using the controls above the button, and checked for time conflicts.
5. If two tasks overlap in time, a warning names both pets, both task titles, and the overlapping time windows. If no conflicts exist, a success message confirms it.

Sample CLI output (from running `python main.py`):
```
Today's Schedule
Rex: 08:00 - Morning Walk (walk, high)
Milo: 08:15 - Nail Trim (grooming, low)
Milo: 12:30 - Vet Checkup (meds, high)
Rex: 18:00 - Dinner (feeding, medium)

Conflicts
Rex: 08:00-08:30 Morning Walk  <->  Milo: 08:15-08:35 Nail Trim
```

## 🌟 Stretch Features

### 🌟 Stretch 3: Advanced Priority Scheduling
Scheduler.sort_by_priority_then_time() provides a triage-style view of the day's tasks — ordered by priority first (High → Medium → Low), with time only breaking ties within each tier. This differs intentionally from the chronological "Today's Schedule" view: a high-priority task later in the day will still outrank a low-priority task earlier in the day.

```
Today's Schedule (chronological)
Rex: 08:00 - Morning Walk (walk, high)
Milo: 08:15 - Nail Trim (grooming, low)
Milo: 12:30 - Vet Checkup (meds, high)
Rex: 18:00 - Dinner (feeding, medium)

Priority View (triage)
Rex: 08:00 - Morning Walk (walk, high)
Milo: 12:30 - Vet Checkup (meds, high)
Rex: 18:00 - Dinner (feeding, medium)
Milo: 08:15 - Nail Trim (grooming, low)
```

Notice Milo's 08:15 Nail Trim (low priority) drops from second to last in the priority view, despite being early in the day — proving priority genuinely takes precedence over time, not just breaking ties.