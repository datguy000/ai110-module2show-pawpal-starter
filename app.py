import streamlit as st
from datetime import date, datetime, timedelta

from pawpal_system import Owner, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Display-only emoji lookups. These never touch stored Task/Pet values.
SPECIES_TABLE_ICONS = {"dog": "🐕", "cat": "🐱", "other": "🐾❓"}
SPECIES_ICON = "🐾"
CATEGORY_ICONS = {"feeding": "🍽️", "walk": "🚶", "meds": "💊", "grooming": "✂️", "general": "📋"}
PRIORITY_ICONS = {"high": "🔴", "medium": "🟡", "low": "🟢"}


def _pet_label(pet):
    """Return a pet's display label prefixed with its species icon."""
    icon = SPECIES_TABLE_ICONS.get(pet.species, SPECIES_TABLE_ICONS["other"])
    return f"{icon} {pet.name}"


def _category_label(category):
    """Return a category value prefixed with its icon for display."""
    return f"{CATEGORY_ICONS.get(category, '📋')} {category}"


def _priority_label(priority):
    """Return a priority value prefixed with its icon for display."""
    return f"{PRIORITY_ICONS.get(priority, '')} {priority}"


def _strip_icon(labeled_value):
    """Strip a leading emoji+space back off a dropdown label to get the plain value."""
    return labeled_value.split(" ", 1)[1] if " " in labeled_value else labeled_value


st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("👤 Quick Demo Inputs (UI only)")
owner_name = st.text_input("👤 Owner name", value="Jordan")
pet_name = st.text_input(f"{SPECIES_ICON} Pet name", value="Mochi")
species_labeled = st.selectbox(
    f"{SPECIES_ICON} Species",
    [f"{SPECIES_TABLE_ICONS[s]} {s}" for s in ["dog", "cat", "other"]],
)
species = _strip_icon(species_labeled)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)

owner = st.session_state.owner

st.markdown("### ✅ Tasks")
st.caption("Add a few tasks. These feed into your scheduler.")

col1, col2 = st.columns(2)
with col1:
    task_title = st.text_input("📋 Task title", value="Morning walk")
    category_labeled = st.selectbox(
        "📋 Category",
        [_category_label(c) for c in ["feeding", "walk", "meds", "grooming", "general"]],
        index=4,
    )
    category = _strip_icon(category_labeled)
    if "task_time" not in st.session_state:
        st.session_state.task_time = datetime.now().time()
    task_time = st.time_input("🕐 Time", key="task_time")
with col2:
    duration = st.number_input("🕐 Duration (minutes)", min_value=1, max_value=240, value=20)
    priority_labeled = st.selectbox(
        "🎯 Priority",
        [_priority_label(p) for p in ["low", "medium", "high"]],
        index=1,
    )
    priority = _strip_icon(priority_labeled)
    frequency = st.selectbox("📅 Frequency", ["once", "daily", "weekly"], index=0)

if st.button("➕ Add task"):
    pet = owner.get_or_create_pet(pet_name, species)
    task = Task(
        title=task_title,
        category=category,
        time=task_time.strftime("%H:%M"),
        duration_minutes=int(duration),
        priority=priority,
        frequency=frequency,
        task_date=date.today(),
    )
    pet.add_task(task)

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": _pet_label(pet),
                "title": task.title,
                "category": _category_label(task.category),
                "time": f"🕐 {task.time}",
                "duration_minutes": task.duration_minutes,
                "priority": _priority_label(task.priority),
                "frequency": task.frequency,
            }
            for pet, task in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("📅 Build Schedule")
st.caption("This calls the Scheduler to build today's schedule.")


def _format_range(task):
    """Return the task's time window as 'HH:MM-HH:MM' for display."""
    start = datetime.strptime(task.time, "%H:%M")
    end = start + timedelta(minutes=task.duration_minutes)
    return task.time, end.strftime("%H:%M")


filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    species_options = ["all"] + sorted({pet.species for pet in owner.pets})
    species_filter_labeled = st.selectbox(
        f"{SPECIES_ICON} Filter by species",
        [
            f"{SPECIES_TABLE_ICONS.get(s, SPECIES_ICON)} {s}" if s != "all" else "🐾 all"
            for s in species_options
        ],
    )
    species_filter = _strip_icon(species_filter_labeled)
with filter_col2:
    show_completed = st.checkbox("✅ Show completed tasks", value=True)

if st.button("✨ Generate schedule"):
    scheduler = Scheduler(owner)
    schedule, conflicts = scheduler.generate_daily_schedule()

    schedule = scheduler.filter_tasks(
        schedule,
        species=None if species_filter == "all" else species_filter,
        completed=None if show_completed else False,
    )

    if schedule:
        st.write("Today's schedule:")

        st.table(
            [
                {
                    "pet": _pet_label(pet),
                    "start": _format_range(task)[0],
                    "end": _format_range(task)[1],
                    "title": task.title,
                    "category": _category_label(task.category),
                    "priority": _priority_label(task.priority),
                    "completed": task.completed,
                }
                for pet, task in schedule
            ]
        )
    else:
        st.info("No tasks match the current filters.")

    if conflicts:
        for (pet_a, task_a), (pet_b, task_b) in conflicts:
            start_a, end_a = _format_range(task_a)
            start_b, end_b = _format_range(task_b)
            st.warning(
                f"Conflict: {_pet_label(pet_a)}'s \"{task_a.title}\" ({start_a}-{end_a}) overlaps "
                f"{_pet_label(pet_b)}'s \"{task_b.title}\" ({start_b}-{end_b})"
            )
    else:
        st.success("No conflicts detected.")
