# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Prompt Comparison (SF11)

### Prompt used (identical across all models):

> "I'm building a Python scheduling app where users create tasks (each with a category, priority, and duration) for a daily planner. I'm deciding whether a task's time field should be required (every task must have a specific clock time, like '14:30') or optional (a user could add a task like 'walk the dog' without picking a specific time, to be done 'sometime that day'). The app needs to support sorting tasks chronologically and detecting time conflicts between overlapping tasks. Which approach would you recommend, and how would each choice affect the sorting and conflict-detection logic? What edge cases should I watch out for either way?"

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | Claude | ChatGPT |
| **Response summary** | Recommended optional time, modeled as start_time: Optional[time]. Split sorting into scheduled (by time) and unscheduled (by priority) groups. Conflict detection only compares scheduled tasks; warned explicitly against faking a sort key like time.min for untimed tasks. Provided full code for sorting and conflict detection, plus a long list of edge cases (midnight-crossing, zero-duration, timezone/DST). | Recommended optional time, using explicit ScheduledTask/UnscheduledTask framing (conceptually, though the code model used a single Task with start_time: time | None). Same scheduled/unscheduled split for sorting and conflicts. Suggested surfacing unscheduled tasks under an "Anytime today" section, and proposed a capacity-based warning ("total unscheduled duration exceeds remaining free time") as an alternative to clock-time conflicts for untimed tasks. |
| **What was useful** | The explicit warning against sentinel/fake sort keys was the most concrete, actionable piece of advice — a real bug I would likely have hit if I'd chosen optional time without this callout. The edge-case list (back-to-back not conflicting, midnight-crossing) was thorough and directly applicable to logic I'd already built. | The "capacity conflict" idea (total unscheduled duration vs. remaining free time) was a genuinely novel suggestion neither Claude nor Perplexity raised — a reasonable way to keep untimed tasks useful without forcing them into clock-time conflict logic. |
| **Problems noticed** | Reasoned entirely from a generic best-practice standpoint, with no awareness of project-specific constraints (a graded assignment with a fixed rubric requirement and firm deadline). The added implementation surface (two task states, conditional conflict logic, sentinel handling) is real complexity that a from-scratch decision needs to weigh against project scope, which the response couldn't account for. | Same generic-best-practice blind spot as Claude. The capacity-conflict idea, while interesting, would have added an entirely new algorithmic feature beyond what the project's rubric asks for — scope the response had no way to know about. |
| **Decision** | Rejected — despite good technical reasoning, the added complexity (two-state task model, conditional sort/conflict logic) wasn't worth it for this project's scope and timeline. | Rejected, same core reasoning — though the capacity-conflict idea was noted as a genuinely interesting concept for a possible future iteration. |

**Which approach did you use in your final implementation and why?**

I kept time as a required field on Task, overriding what all three models I consulted (Claude, ChatGPT, and Perplexity) independently recommended. All three converged on the same advice — model time as optional, split tasks into scheduled/unscheduled groups, and handle sorting and conflict detection conditionally. That's sound general advice for a production daily-planner app optimizing for end-user flexibility.

But my actual constraints were different: this is a class project graded against a specific rubric that explicitly requires a "due time or date" on Task, built under a firm deadline, with a CLAUDE.md guardrail file specifically designed to prevent scope creep beyond what each phase actually required. Adding optional time would have meant a genuinely more complex data model (two task states instead of one), more complex sorting (a two-stage sort with None handling), and conditional conflict detection — real implementation cost for a UX flexibility benefit the project's scenario didn't actually call for. Required time keeps sorting and conflict detection simple and directly testable, which mattered more for this project's goals than the theoretical flexibility of an optional field. This was a case where the technically "better" generic advice wasn't the right advice for the specific problem I was solving.
