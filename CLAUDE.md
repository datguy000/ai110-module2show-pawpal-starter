# PawPal+ — CLAUDE.md

## Project context
PawPal+ is a CodePath AI110 assignment: a pet care scheduling system built in
Python (OOP) with a thin Streamlit UI. This file is your persistent memory
across sessions — read it fully before doing any work, and update the
Progress Tracker at the end of every session.

The full assignment instructions and rubric live in the human's own notes;
this file summarizes only what's needed to build correctly and to stay in
scope. When in doubt, ask before assuming.

## Hard scope boundaries — do NOT do these unless explicitly asked
- No authentication, login, or user accounts.
- No database (SQLite/Postgres/etc). Data lives in memory; persistence via
  JSON is a stretch feature only, not default behavior.
- No multi-owner support. There is exactly one Owner in this system.
- No task dependency/ordering logic (e.g. "walk before feeding"). Tasks are
  independent except for time/date.
- Do not build a full custom scheduling optimizer (bin-packing, auto time
  assignment based on available minutes). Tasks have an explicit, required
  `time` — the Scheduler organizes given times, it does not invent them.
- Do not jump ahead to a future phase's work without being asked, even if it
  seems efficient to "just do it now while I'm in this file."
- Do not refactor or rewrite files outside the current phase's scope.
- If a request seems to require touching files/logic outside current scope,
  STOP and ask before proceeding.

## Core object design (matches diagrams/uml_draft.mmd)

### Task
- `title: str`
- `category: str` — e.g. "feeding", "walk", "meds", "grooming"
- `date: date` — defaults to today
- `time: str` — REQUIRED, 24-hour "HH:MM" format (e.g. "16:45"), zero-padded
- `duration_minutes: int`
- `priority: str` — one of exactly: `"low"`, `"medium"`, `"high"`
  (must match existing app.py dropdown values exactly — lowercase)
- `frequency: str` — one of exactly: `"once"`, `"daily"`, `"weekly"`
- `completed: bool = False`
- Method: `mark_complete()`

### Pet
- `name: str`
- `species: str`
- `breed: str = ""` (optional, cosmetic)
- `tasks: list[Task]`
- Methods: `add_task(task)`, `get_tasks()`

### Owner
- `name: str`
- `pets: list[Pet]`
- Methods: `add_pet(pet)`, `get_all_tasks()` — returns `(pet, task)` pairs,
  NOT bare Task objects, so the pet a task belongs to is always available
  without Task needing a back-reference to Pet.

### Scheduler
- Holds a reference to `owner`. Does NOT store pets itself.
- `sort_by_time(tasks)` — sort by `date` then `time`
- `filter_tasks(pet_name=None, completed=None)` — filter by pet and/or status
- `detect_conflicts(tasks)` — checks for overlapping `time` +
  `duration_minutes` windows, ACROSS ALL PETS COMBINED (the owner has one
  schedule; two different pets' tasks at the same time still conflict).
  Return a warning/list of conflicts — never raise/crash on a conflict.
- Recurrence: when a `"daily"` or `"weekly"` task is completed, generate a
  new Task with `date` advanced via `timedelta` (+1 day or +7 days). This can
  live on Scheduler or Task — pick one and be consistent.
- `generate_daily_schedule()` — orchestrates the above into the final
  schedule shown in CLI and UI.

Use Python `@dataclass` for Task and Pet, per the assignment's instruction.

## Phase-by-phase plan
Work one phase at a time. Do not start the next phase's work until the
current phase's checkpoint is confirmed complete by the human.

- [x] Phase 1, Step 1: Identify 3 core user actions (done in reflection.md)
- [x] Phase 1, Step 3: UML draft (diagrams/uml_draft.mmd — done)
- [x] Phase 1, Step 4: Generate class skeletons (names/attributes/method
      stubs only, no logic) in pawpal_system.py, using dataclasses for
      Task and Pet. Commit as its own step.
- [x] Phase 1, Step 5: Review skeleton against UML for gaps; report findings
      to human before making changes.
- [x] Phase 2: Full implementation of all 4 classes' logic. Then main.py
      demo script (1 Owner, 2+ Pets, 3+ Tasks, printed "Today's Schedule").
      Then tests/test_pawpal.py with 2 basic tests (mark_complete, add_task
      increases count). Add 1-line docstrings to all methods.
- [x] Phase 3: Wire app.py to real Owner/Pet/Task objects via
      st.session_state (app.py already has a placeholder session_state
      pattern for a plain dict-based task list — replace it with real
      objects, don't rebuild the UI from scratch).
- [x] Phase 4: Algorithmic layer — sort_by_time, filter_tasks, recurrence,
      detect_conflicts. Update main.py to demonstrate each. Update README's
      "Smarter Scheduling" table.
- [x] Phase 5: Testing pass — add sorting correctness, recurrence, and
      conflict detection tests. Get full pytest suite green.
- [ ] Phase 6: UI polish (surface sort/filter/conflict results with
      st.success/st.warning/st.table), diagrams/uml_final.mmd, README
      polish, reflection.md final sections.

## Working style
- Keep changes scoped to what the current phase step asks for. Small,
  reviewable diffs over large rewrites.
- Prefer readable, simple code over "clever" one-liners — this is a
  learning project; the human wants to be able to explain every line.
- Add a short docstring to every method as you write it (not as a separate
  cleanup pass later), one line, describing what it does.
- When asked to review/critique code (skeleton review, algorithm
  simplification, etc.), give a real critique — don't just rubber-stamp
  what's already there.
- If two implementation approaches are reasonably different (e.g. "Pythonic
  but less readable" vs "more verbose but clearer"), present the tradeoff
  rather than silently picking one.
- Commit messages: use conventional commit prefixes (feat/fix/docs/
  chore/test/refactor) matched honestly to what changed — don't default
  everything to "chore".

## Notes for stretch features (only if explicitly requested — do not build these preemptively)
- Advanced algorithmic capability (next-available-slot, weighted
  prioritization, etc.) — requires an "Agent Workflow" entry in
  ai_interactions.md documenting files touched, task requested, what was
  completed, manual corrections made.
- JSON persistence (save_to_json/load_from_json on pawpal_system.py).
- Priority-first sorting (priority, then time) — quick, since `priority`
  already exists as a field.
- CLI/UI formatting polish (emojis, color, tabulate).