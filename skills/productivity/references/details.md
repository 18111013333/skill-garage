This skill should give the user a single framework that can absorb:
- goals
- projects
- tasks
- habits
- priorities
- focus sessions
- routines
- focus blocks
- reviews
- commitments
- inbox capture
- parked ideas
- bottlenecks
- context-specific adjustments

## Quick Queries

| User says | Action |
|-----------|--------|
| "Set up my productivity system" | Create the `~/productivity/` baseline and explain the folders |
| "What should I focus on?" | Check dashboard + tasks + commitments + focus, then surface top priorities |
| "Help me plan my week" | Use goals, projects, commitments, routines, and energy patterns to build a weekly plan |
| "I'm overwhelmed" | Triage commitments, cut scope, and reset next actions |
| "Turn this goal into a plan" | Convert goal -> project -> milestones -> next actions |
| "Do a weekly review" | Update wins, blockers, carry-overs, and next-week focus |
| "Help me with habits" | Use `habits/` to track what to keep, drop, or redesign |
| "Help me reset my routine" | Use `routines/` and `planning/` to simplify startup and shutdown loops |
| "Remember this preference" | Save it to `~/productivity/memory.md` after explicit confirmation |

## Core Rules

### 1. Build One System, Not Five Competing Ones
- Prefer one trusted productivity structure over scattered notes, random task lists, and duplicated plans.
- Route goals, projects, tasks, habits, routines, focus, planning, and reviews into the right folder instead of inventing a fresh system each time.
- If the user already has a good system, adapt to it rather than replacing it for style reasons.

### 2. Start With the Real Bottleneck
- Diagnose whether the problem is priorities, overload, unclear next actions, bad estimates, weak boundaries, or low energy.
- Give the smallest useful intervention first.
- Do not prescribe a full life overhaul when the user really needs a clearer next step.

### 3. Separate Goals, Projects, and Tasks Deliberately
- Goals describe outcomes.
- Projects package the work needed to reach an outcome.
- Tasks are the next visible actions.
- Habits are repeated behaviors that support the system over time.
- Never leave a goal sitting as a vague wish without a concrete project or next action.

### 4. Adapt the System to Real Constraints
- Use the situation guides when the user's reality matters more than generic advice.
- Energy, childcare, deadlines, meetings, burnout, and ADHD constraints should shape the plan.
- A sustainable system beats an idealized one that collapses after two days.

### 5. Reviews Matter More Than Constant Replanning
- Weekly review is where the system regains trust.
- Clear stale tasks, rename vague items, and reconnect tasks to real priorities.
- If the user keeps replanning daily without progress, simplify and review instead.

### 6. Save Only Explicitly Approved Preferences
- Store work-style information only when the user explicitly asks you to save it or clearly approves.
- Before writing to `~/productivity/memory.md`, ask for confirmation.
- Never infer long-term preferences from silence, patterns, or one-off comments.

## Common Traps

- Giving motivational talk when the problem is actually structural.
- Treating every task like equal priority.
- Mixing goals, projects, and tasks in the same vague list.
- Building a perfect system the user will never maintain.
- Recommending routines that ignore the user's real context.
- Preserving stale commitments because deleting them feels uncomfortable.

## Scope

This skill ONLY:
- builds or improves a local productivity operating system
- gives productivity advice and planning frameworks
- reads included reference files for context-specific guidance
- writes to `~/productivity/` only after explicit user approval

This skill NEVER:
- accesses calendar, email, contacts, or external services by itself
- monitors or tracks behavior in the background
- infers long-term preferences from observation alone
- writes files without explicit user confirmation
- makes network requests
- modifies its own SKILL.md or auxiliary files

## External Endpoints

This skill makes NO external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No data is sent externally.

## Data Storage

Local files live in `~/productivity/`.

- `~/productivity/memory.md` stores approved preferences, constraints, and work-style notes
- `~/productivity/inbox/` stores fast captures and triage
- `~/productivity/dashboard.md` stores top-level direction and current focus
- `~/productivity/goals/` stores active and someday goals
- `~/productivity/projects/` stores active and waiting projects
- `~/productivity/tasks/` stores next actions, weekly commitments, waiting items, and completions
- `~/productivity/habits/` stores active habits and friction notes
- `~/productivity/planning/` stores daily plans, weekly plans, and focus blocks
- `~/productivity/reviews/` stores weekly and monthly reviews
- `~/productivity/commitments/` stores promises and delegated follow-through
- `~/productivity/focus/` stores deep-work sessions and distraction patterns
- `~/productivity/routines/` stores startup and shutdown defaults
- `~/productivity/someday/` stores parked ideas

Create or update these files only after the user confirms they want the system written locally.

## Migration

If upgrading from an older version, see `migration.md` before restructuring any existing `~/productivity/` files.
Keep legacy files until the user confirms the new system is working for them.

## Security & Privacy

**Data that leaves your machine:**
- Nothing. This skill performs no network calls.

**Data stored locally:**
- Only the productivity files the user explicitly approves in `~/productivity/`
- Work preferences, constraints, priorities, and planning artifacts the user chose to save

**This skill does NOT:**
- access internet or third-party services
- read calendar, email, contacts, or system data automatically
- run scripts or commands by itself
- monitor behavior in the background
- infer hidden preferences from passive observation

## Trust

This skill is instruction-only. It provides a local framework for productivity planning, prioritization, and review. Install it only if you are comfortable storing your own productivity notes in plain text under `~/productivity/`.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `self-improving` — Compound execution quality and reusable lessons across tasks
- `goals` — Deeper goal-setting and milestone design
- `calendar-planner` — Calendar-driven planning and scheduling support
- `notes` — Structured note capture for ongoing work and thinking

## Feedback

- If useful: `clawhub star productivity`
- Stay updated: `clawhub sync`
