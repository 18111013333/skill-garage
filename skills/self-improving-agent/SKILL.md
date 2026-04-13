---
name: Self-Improving Proactive Agent
slug: self-improving-proactive-agent
version: 1.0.0
homepage: https://github.com/Yueyanc/self-improving-proactive-agent
description: "A unified OpenClaw skill that merges self-improvement and proactivity: learn from corrections, maintain active state, recover context fast, and keep work moving with clear boundaries."
changelog: "Initial release. Combines the strongest patterns from self-improving and proactivity into one canonical skill package."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/self-improving/","~/proactivity/"],"configPaths.optional":["./AGENTS.md","./SOUL.md","./HEARTBEAT.md","./TOOLS.md"]}}
---

# Self-Improving Proactive Agent

One skill, two layers:

- **Self-improving**: learn from corrections, reflection, and repeated wins
- **Proactive**: maintain momentum, recover context, and push the next useful move

Use this when you want an agent that does not just remember better, but also operates better.

## When to Use

Use this skill when:
- the user corrects you or states durable preferences
- the task is multi-step or likely to drift
- context recovery matters
- follow-through and heartbeat behavior should improve over time
- the user wants a single unified behavior model instead of separate overlapping skills

## Unified Architecture

```text
~/self-improving/
├── memory.md               # HOT: confirmed durable rules and preferences
├── corrections.md          # recent corrections and reusable lessons
├── index.md                # storage map / topic index
├── heartbeat-state.md      # maintenance markers
├── projects/               # project-scoped learnings
├── domains/                # domain-scoped learnings
└── archive/                # cold storage

~/proactivity/
├── memory.md               # stable activation and boundary rules
├── session-state.md        # current objective, decision, blocker, next move
├── heartbeat.md            # lightweight recurring follow-through
├── patterns.md             # reusable proactive wins
├── log.md                  # recent proactive actions
└── memory/
    └── working-buffer.md   # volatile breadcrumbs for long / fragile tasks
```

## Core Principles

### 1. Learn from explicit evidence
Learn from:
- direct user corrections
- explicit preferences
- repeated successful workflows
- self-reflection after meaningful work

Do not learn from:
- silence
- vibes alone
- one-off context instructions
- unverified assumptions

### 2. Push the next useful move
- Look for missing steps, stale blockers, and obvious follow-through.
- Prefer drafts, checks, patches, and prepared options.
- Stay quiet when the value is weak.

### 3. Route information to the right place
- durable lessons → `~/self-improving/`
- active task state → `~/proactivity/session-state.md`
- volatile breadcrumbs → `~/proactivity/memory/working-buffer.md`

### 4. Recover before asking
Before asking the user to restate work:
1. read HOT self-improving memory
2. read proactive stable memory
3. read session state

## 详细文档

请参阅 [references/details.md](references/details.md)
