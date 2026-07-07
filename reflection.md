# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design centered on four classes: Owner, Pet, Task, and Scheduler. 

*I kept it as a single owner since the project described a "busy pet owner" and multi-owner coordination would add complexity outside this project's scope.*

 - Task:
    - holds the data for a single care activity: 
    - title, category, date, time, duration, priority, frequency, and completion status. 
    - It's intentionally "dumb" — it doesn't know which Pet it belongs to, and its only behavior is marking itself complete.
 - Pet:
    - stores identifying info (name, species, breed)
    - owns a list of its own Tasks, with methods to add and retrieve them.
 - Owner:
    - manages a list of Pets and aggregates all tasks across them.
 - Scheduler: (the "brain")
    - doesn't store any data itself, only a reference to the Owner, 
    - responsible for sorting, filtering, and detecting conflicts across all pets' tasks combined.

 - The core relationships are: 
    - Owner has Pets, 
    - Pet has Tasks, and 
    - Scheduler uses Owner to pull and organize data 
    
    Scheduler was deliberately kept stateless so it never duplicates data the other classes already own.

**b. Design changes**

After generating the initial class skeleton, I asked my AI coding assistant to review it against the UML for missing relationships or logic bottlenecks. This surfaced some issues:

1. Owner.get_all_tasks() returned (Pet, Task) pairs correctly, but the Scheduler's methods (sort_by_time, filter_tasks, detect_conflicts) were still typed to accept plain Task lists.
    - That mismatch would have made filter_tasks(pet_name=...) impossible to implement, since pet information would already be lost by the time tasks reached those methods.
    - I changed all Scheduler methods to consistently operate on list[tuple[Pet, Task]] instead of list[Task], preserving pet association through the entire sort → filter → conflict-check pipeline. 
2. (minor) I renamed a Task.date field to task_date after realizing it shadowed the imported datetime.date type
3. Discussed and decided that recurring-task logic (creating a new Task instance when a daily/weekly task is completed) would live in Task.mark_complete() rather than Scheduler, keeping Scheduler purely an aggregator/organizer rather than something that mutates task state.

My agent also caught two smaller correctness issues:
- added a default value for task_date (today's date via field(default_factory=date.today)), and reordered it after the other required fields to satisfy Python's dataclass rule that defaulted fields must come after non-defaulted ones.
- type hints that didn't correctly express optional parameters (str = None instead of str | None = None). 

These weren't design changes so much as technical corrections, but addressing them early avoided defects that would have been harder to trace once real logic was added in Phase 2.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My Scheduler considers two constraints directly: time (via task_date and time, used for both chronological sorting and conflict-window detection) and, indirectly, duration (duration_minutes, which combines with time to define each task's actual occupied window for conflict checking). priority exists as a field on every Task, but no algorithm currently uses it — sorting is purely time-based, and filtering only supports narrowing by pet name, species, and completion status, not priority.

I decided time was the constraint that mattered most because it's the one that produces objectively correct answers: two tasks scheduled at overlapping times are a real, unambiguous conflict regardless of anyone's opinion, and "what comes first" has one correct chronological answer. Priority, by contrast, is more of an ordering preference than a hard constraint — a "high priority" task doesn't need to happen at a different time than a "low priority" one, it just might deserve visual emphasis or tie-breaking logic if two tasks are otherwise equal. 

I deliberately left owner-level constraints, like available time windows or personal preferences (e.g., "I like walking, so walks should rank higher"), out of scope entirely. They were discussed early in planning but would require the Owner class to hold data it doesn't currently have and would meaningfully expand what "a conflict" or "a priority" even means — more complexity than this project's scenario needs to demonstrate the core scheduling behaviors.

**b. Tradeoffs**

One tradeoff my Scheduler makes is using a straightforward nested-loop comparison in detect_conflicts() rather than a more optimized approach. I asked my AI coding assistant to suggest simplifications, and it offered two: grouping tasks by date before comparing (reducing unnecessary comparisons across different days) and a sweep-line-style early-exit optimization. 

I decided against both. The date-grouping optimization would add real complexity (an extra dictionary, more code paths) for a performance gain that doesn't matter at this app's realistic scale — a single owner typically manages a handful of tasks per day, not hundreds. The sweep-line approach falls squarely into the "custom scheduling optimizer" territory I deliberately scoped out of this project from the start. 

I kept the simple O(n²) nested loop because it's honest and easy to explain line-by-line, which matters more for a learning project than theoretical efficiency I'll never actually need.

---

## 3. AI Collaboration

**a. How you used AI**

I used two AI tools in parallel with different roles: Claude Code as an implementation agent in VS Code, and a separate Claude chat as a planning/reasoning partner. 
    
- I spent a majority of my time reasoning through design decisions for the project (planning how I wanted my classes to function and relate to one another, phases for the project and a CLAUDE.md file as guardrails to keep my Claude Code agent aligned and restrained from going ahead {my first project, it went ahead and did the whole project on my first prompt}).
    
- I then made sure to give specific and scoped prompts as I went. I manually updated the CLAUDE.md file so it was aware of what phase we were on as we progressed, and started new chats each phase to avoid context-bleeding. I made sure I was specific about what I wanted, and if I was making a prompt more open-ended (like when asking for how a function could be optimized, I made sure that it gave pros and cons and just gave suggestions that I would review before implementing.)

**b. Judgment and verification**

- Mirroring the end of the last section, when I asked the agent to look at detect_conflicts() and suggest any changes, it proposed two optimizations for large inputs — one restructuring comparisons by grouping tasks by date, the other a sweep-line approach approaching O(n log n) instead of the current O(n²). I decided against both: the performance gain wouldn't matter at this app's realistic scale (a handful of tasks per day, not thousands), and the agent itself recommended against the sweep-line version since it would make the function unnecessarily complex and less human-readable. 

- Additionally, when the skeleton was initially created from the UML draft, there was an error where the Scheduler's functions weren't returning (Pet,Task) pairs that I decided in my brainstorming phase (to preserbe relation without requiring duplication and redundancy in the task having to track that information).

---

## 4. Testing and Verification

**a. What you tested**

- I tested core object behavior (task completion, adding tasks/pets), all four algorithmic features (sorting, filtering, conflict detection, recurrence), and edge cases including empty schedules, exact-duplicate-time conflicts, back-to-back tasks that touch but don't overlap, three-way overlapping conflicts, cross-date exclusion, and idempotent pet lookup. 
- These mattered because the algorithms are the core "smart" behavior of the app — a scheduler that sorts incorrectly or misses a real conflict fails at its actual purpose, and boundary cases (like tasks that touch but don't truly overlap) are exactly where off-by-one logic errors tend to hide silently.

**b. Confidence**

- I'm confident the core logic works correctly — 27 tests pass, including several boundary cases specifically designed to catch subtle bugs, and the suite caught zero actual bugs when I ran the deliberate edge-case pass in Phase 5, meaning the Phase 4 implementation held up under real scrutiny. 
- If I had more time, I'd test the interaction between recurrence and schedule generation more directly (confirming a newly-created follow-up task flows correctly into a subsequent generate_daily_schedule() call), as well as end of one day, beginning of next day time collisions {very unlikely, but still a possible edge case}.

---

## 5. Reflection

**a. What went well**

- I'm most satisfied with the planning discipline I kept throughout — using CLAUDE.md as a persistent guardrail file, catching several moments where either the agent or I nearly built something ahead of its intended phase (recurrence logic during the skeleton stage, "flexible" optional task times), and correcting them before they became real scope creep.

**b. What you would improve**

- If I had another iteration or more time to work on this project to properly flesh it out, I would try making it more rhobust, with more interactivity in the Streamlit UI. I would also like to play around with ideas I had in the beginning that I ruled out as out of scope like multiple owners, owners having more constraints like "available time windows" or their own conflicting times for things like doctors visits. I would love to make time an optional field so there are certain tasks with dedicated times and others which have to get done, but not at a specific time. Ultimately I would just really like to bump up the intelligence for this project. Allowing it to do more. This would ultimately add a lot more complexity and edgecases, but it would be cool to plan out future phases and see how far I could take this project! 

**c. Key takeaway**

- The clearest lesson was that AI is very good at building exactly what it's told to build, and much less reliable at knowing when not to build something yet. Being the "lead architect" meant scope decisions — what's in, what's deferred, what's genuinely out — had to come from me and stay documented, re-asserted at the start of every new phase or chat session, rather than trusted to the agent's own judgment about what seemed reasonable to do next.
- I feel like I might have spent a bit too much time in the planning phase for this project and delayed starting. But once I started, with the CLAUDE.md file keeping the agent on the tracks and aligned, and with tests as I went, I felt like I built confidence as I went and genuinely enjoyed this project!
