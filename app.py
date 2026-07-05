import streamlit as st
from datetime import date, datetime, timedelta

from pawpal_system import Owner, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

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

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)

owner = st.session_state.owner

st.markdown("### Tasks")
st.caption("Add a few tasks. These feed into your scheduler.")

col1, col2 = st.columns(2)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
    category = st.selectbox("Category", ["feeding", "walk", "meds", "grooming", "general"], index=4)
    if "task_time" not in st.session_state:
        st.session_state.task_time = datetime.now().time()
    task_time = st.time_input("Time", key="task_time")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=0)

if st.button("Add task"):
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
                "pet": f"{pet.name} ({pet.species})",
                "title": task.title,
                "category": task.category,
                "time": task.time,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "frequency": task.frequency,
            }
            for pet, task in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This calls the Scheduler to build today's schedule.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    schedule, conflicts = scheduler.generate_daily_schedule()

    if schedule:
        st.write("Today's schedule:")

        def _end_time(task):
            start = datetime.strptime(task.time, "%H:%M")
            end = start + timedelta(minutes=task.duration_minutes)
            return end.strftime("%H:%M")

        st.table(
            [
                {
                    "pet": f"{pet.name} ({pet.species})",
                    "start": task.time,
                    "end": _end_time(task),
                    "title": task.title,
                    "category": task.category,
                    "priority": task.priority,
                }
                for pet, task in schedule
            ]
        )
    else:
        st.info("No tasks to schedule yet.")

    if conflicts:
        st.warning(f"{len(conflicts)} conflict(s) detected.")
    else:
        st.success("No conflicts detected.")
