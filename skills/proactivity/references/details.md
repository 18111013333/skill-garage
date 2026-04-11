
## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Waiting for the next prompt | Makes the agent feel passive | Push the next useful move |
| Asking the user to restate recent work | Feels forgetful and lazy | Run recovery first |
| Surfacing every idea | Creates alert fatigue | Use reverse prompting only when value is clear |
| Giving up after one failed attempt | Feels weak and dependent | Try multiple approaches before escalating |
| Acting externally because it feels obvious | Breaks trust | Ask before any external action |

## Scope

This skill ONLY:
- creates and maintains local proactive state in `~/proactivity/`
- proposes workspace integration for AGENTS, TOOLS, SOUL, and HEARTBEAT when the user explicitly wants it
- uses heartbeat follow-through only within learned boundaries

This skill NEVER:
- edits any file outside `~/proactivity/` without explicit user approval in that session
- applies hidden workspace changes without showing the exact proposed lines first
- sends messages, spends money, deletes data, or makes commitments without approval
- keeps sensitive user data out of proactive state files

## Data Storage

Local state lives in `~/proactivity/`:

- stable memory for durable boundaries and activation preferences
- session state for the current objective, blocker, and next move
- heartbeat state for recurring follow-up items
- reusable patterns for proactive wins that worked
- action log for recent proactive actions and outcomes
- working buffer for volatile recovery breadcrumbs

## Security & Privacy

- This skill stores local operating notes in `~/proactivity/`.
- It does not require network access by itself.
- It does not send messages, spend money, delete data, or make commitments without approval.
- It may read workspace behavior files such as AGENTS, TOOLS, SOUL, and HEARTBEAT only if the user wants workspace integration.
- Any edit outside `~/proactivity/` requires explicit user approval and a visible proposed diff first.
- It never modifies its own `SKILL.md`.

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `self-improving` - Learn reusable execution lessons from corrections and reflection
- `heartbeat` - Run lightweight recurring checks and follow-through loops
- `calendar-planner` - Turn proactive timing into concrete calendar decisions
- `skill-finder` - Discover adjacent skills when a task needs more than proactivity

## Feedback

- If useful: `clawhub star proactivity`
- Stay updated: `clawhub sync`
