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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
