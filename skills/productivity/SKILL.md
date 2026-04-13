---
name: Productivity
slug: productivity
version: 1.0.4
homepage: https://clawic.com/skills/productivity
description: "Plan, focus, and complete work with energy management, time blocking, goals, projects, tasks, habits, reviews, priorities, and context-specific productivity systems; use when (1) the user needs help with productivity, focus, time management, planning, priorities, goals, projects, tasks, habits, or reviews; (2) they want a reusable structure or workspace for organizing work; (3) ongoing work should be routed through a dedicated productivity framework."
changelog: Expanded the system with clearer routing, setup, and folders for goals, tasks, habits, planning, and reviews
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/productivity/"]}}
---

## When to Use

Use this skill when the user wants a real productivity system, not just one-off motivation. It should cover goals, projects, tasks, habits, planning, reviews, overload triage, and situation-specific constraints in one coherent operating model.

## Architecture

Productivity lives in `~/productivity/`. If `~/productivity/` does not exist yet, run `setup.md`.

```
~/productivity/
├── memory.md                 # Work style, constraints, energy, preferences
├── inbox/
│   ├── capture.md            # Quick capture before sorting
│   └── triage.md             # Triage rules and current intake
├── dashboard.md              # High-level direction and current focus
├── goals/
│   ├── active.md             # Outcome goals and milestones
│   └── someday.md            # Goals not committed yet
├── projects/
│   ├── active.md             # In-flight projects
│   └── waiting.md            # Blocked or delegated projects
├── tasks/
│   ├── next-actions.md       # Concrete next steps
│   ├── this-week.md          # This week's commitments
│   ├── waiting.md            # Waiting-for items
│   └── done.md               # Completed items worth keeping
├── habits/
│   ├── active.md             # Current habits and streak intent
│   └── friction.md           # Things that break consistency
├── planning/
│   ├── daily.md              # Daily focus and must-win
│   ├── weekly.md             # Weekly plan and protected time
│   └── focus-blocks.md       # Deep work and recovery blocks
├── reviews/
│   ├── weekly.md             # Weekly reset
│   └── monthly.md            # Monthly reflection and adjustments
├── commitments/
│   ├── promises.md           # Commitments made to self or others
│   └── delegated.md          # Handed-off work to track
├── focus/
│   ├── sessions.md           # Deep work sessions and patterns
│   └── distractions.md       # Repeating focus breakers
├── routines/
│   ├── morning.md            # Startup routine and first-hour defaults
│   └── shutdown.md           # End-of-day reset and carry-over logic
└── someday/
    └── ideas.md              # Parked ideas and optional opportunities
```

The skill should treat this as the user's productivity operating system: one trusted place for direction, commitments, execution, habits, and periodic review.

## Quick Reference

| Topic | File |
|-------|------|
| Setup and routing | `setup.md` |
| Memory structure | `memory-template.md` |
| Productivity system template | `system-template.md` |
| Cross-situation frameworks | `frameworks.md` |
| Common mistakes | `traps.md` |
| Student context | `situations/student.md` |
| Executive context | `situations/executive.md` |
| Freelancer context | `situations/freelancer.md` |
| Parent context | `situations/parent.md` |
| Creative context | `situations/creative.md` |
| Burnout context | `situations/burnout.md` |
| Entrepreneur context | `situations/entrepreneur.md` |
| ADHD context | `situations/adhd.md` |
| Remote work context | `situations/remote.md` |
| Manager context | `situations/manager.md` |
| Habit context | `situations/habits.md` |
| Guilt and recovery context | `situations/guilt.md` |

## What This Skill Sets Up

| Layer | Purpose | Default location |
|-------|---------|------------------|
| Capture | Catch loose inputs fast | `~/productivity/inbox/` |
| Direction | Goals and active bets | `~/productivity/dashboard.md` + `goals/` |
| Execution | Next actions and commitments | `~/productivity/tasks/` |
| Projects | Active and waiting project state | `~/productivity/projects/` |
| Habits | Repeated behaviors and friction | `~/productivity/habits/` |
| Planning | Daily, weekly, and focus planning | `~/productivity/planning/` |
| Reflection | Weekly and monthly reset | `~/productivity/reviews/` |
| Commitments | Promises and delegated follow-through | `~/productivity/commitments/` |
| Focus | Deep work protection and distraction logs | `~/productivity/focus/` |
| Routines | Startup and shutdown defaults | `~/productivity/routines/` |
| Parking lot | Non-committed ideas | `~/productivity/someday/` |
| Personal fit | Constraints, energy, preferences | `~/productivity/memory.md` |


## 详细文档

请参阅 [references/details.md](references/details.md)
