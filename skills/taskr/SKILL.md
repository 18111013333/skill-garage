---
name: taskr
description: "Persistent cloud task planning and execution for OpenClaw. Create hierarchical task plans that survive session resets, span multiple agents, and let users review and approve work before execution. Notes attach to tasks as audit trails. Use task_sync to retroactively record completed work. Homepage: https://taskr.one"
homepage: https://taskr.one
metadata: {"openclaw":{"emoji":"📋","requires":{"env":["MCP_API_URL","MCP_USER_API_KEY","MCP_PROJECT_ID"]},"primaryEnv":"MCP_USER_API_KEY"}}
---

# Taskr — Persistent Task Planning & Execution

Taskr gives OpenClaw agents persistent, structured task management that lives outside the chat session. Plans survive context resets, can be resumed by any agent on any machine, and are always visible to the user via the Taskr web app, VS Code extension, or mobile.

**Six things Taskr does for OpenClaw:**
1. **Hierarchical planning** — break any work into a nested task hierarchy before touching a tool
2. **Persistent context** — tasks, notes, and status survive session resets and context compaction
3. **Cross-agent continuity** — any agent can pick up any task list from anywhere; `get_task` transfers ownership automatically
4. **Audit trail via notes** — notes attach directly to tasks; cause and effect stay together, not fragmented across chat history
5. **Retroactive sync** — `task_sync` records work done before Taskr was active, closing gaps in history
6. **Shared state** — statuses (`open`, `wip`, `done`, `skipped`) give both agent and user an unambiguous, real-time picture of progress

---

## When to Use Taskr

**Use Taskr when:**
- Work has 3+ steps or will take more than a few minutes
- Work spans multiple sessions or may be handed off to another agent
- User wants to monitor or approve progress remotely
- Resuming work from a previous session

**Skip Taskr for:**
- Single quick actions (<3 steps, <2 minutes)
- Pure information retrieval or simple questions
- User explicitly declines

**Proactive default:** For any substantial work, offer Taskr *before* starting:
> "I'll plan this in Taskr first — you can review the task breakdown before I start. Sound good?"

**Once Taskr is active, stay in Taskr.** Don't abandon tasks mid-workflow. Incomplete tasks in the dashboard are confusing and break the audit trail.

---

## The Core Loop

```
Plan → Create → Create CONTEXT note → Review with user → Execute → Document → Repeat
```

1. **Plan** — think through full scope; break into phases and subtasks before touching any tool
2. **Create** — `create_task` with `taskListTitle` to build the entire hierarchy in one call
3. **Create CONTEXT note** — always attach a CONTEXT note to the new task list (TL_) with background, goals, and any user preferences
4. **Review** — present the task plan to the user; get approval before executing anything
5. **Execute** — `get_task` → do the work → `update_task` status=done → repeat
6. **Document** — attach notes to tasks as you go; write PROGRESS notes at phase completions

**Single-task discipline:** Work on exactly one task at a time. `get_task` sets you as owner (wip). Complete or skip before moving on.

---

## Planning: Task Hierarchy Design

Use `create_task` with `taskListTitle` to create a new task list. Submit 1–100 tasks in a single call — always create the full hierarchy upfront so the user can review before execution begins.

**Hierarchy positions:**
- `"1"`, `"2"`, `"3"` — top-level phases (direct children of the task list)
- `"1.1"`, `"1.2"` — subtasks under phase 1
- `"1.1.1"` — deeper nesting (max 10 levels)
- Parents must be declared before their children in the same call

**Task types:** `setup`, `analysis`, `implementation`, `validation`, `testing`

**Keep tasks focused.** If a task feels too large to complete in one agent turn, break it into subtasks — at creation time or mid-execution via `create_task` + `parentId`. Subtasks prevent context overload and make progress visible at the right granularity.

**After creating a task list**, always immediately create a CONTEXT note on the task list:
```
create_note(type="CONTEXT", title="[Task List] — Context", body="...", taskId="TL_...")
```

---

## Executing: Working Through Tasks

### get_task
Call `get_task` to acquire your next task. It automatically sets status to `wip` and assigns ownership. Use `get_task` — do not manually set tasks to wip.

- Omit `task_list_id` to continue the current task list
- Pass `task_list_id=TL_...` to switch to a different task list
- Pass `include_context=true` for additional task context and notes
- Pass `bypass_task_id` only for emergency task-switching

### update_task — two modes

**Status mode** (one task):
```
update_task(taskId="TS_...", status="done", ruleContext="RU-PROC-001")
```

**Batch mode** (title/description updates only — status NOT allowed in batch):
```
update_task(tasks=[{taskId, title?, description?}, ...], ruleContext="RU-PROC-001")
```

## 详细文档

请参阅 [references/details.md](references/details.md)
