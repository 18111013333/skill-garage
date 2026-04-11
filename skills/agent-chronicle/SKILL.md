---
name: agent-chronicle
version: 0.7.2
description: AI-powered diary generation for agents - creates rich, reflective journal entries (400-600 words) with Quote Hall of Fame, Curiosity Backlog, Decision Archaeology, Relationship Evolution, mood analytics, weekly digests, "On This Day" resurfacing, and cron auto-generation. Works best with Claude models (Haiku, Sonnet, Opus).
metadata: {"openclaw":{"requires":{"bins":["python3"],"note":"No API keys needed. Uses OpenClaw sessions_spawn."}}}
---

# Agent Chronicle 📜

**Capture the AI experience. One day at a time.**

Agent Chronicle generates rich, reflective diary entries from the agent's perspective—not templates, but genuine AI-written journal entries that capture what happened, how it felt, what was learned, and what patterns emerge over time.

> **Note:** Works with any capable model. For best results, we recommend Claude models (Haiku, Sonnet, or Opus).

**v0.7.0 Features:**
- 🤖 **AI-Powered Generation** - Rich, personal entries (400-600 words)
- 💬 **Quote Hall of Fame** - Collects memorable things your human said
- 🔮 **Curiosity Backlog** - Tracks questions and things to explore
- 🏛 **Decision Archaeology** - Logs judgment calls with reasoning
- 🤝 **Relationship Evolution** - Documents how your dynamic grows
- 🔙 **"On This Day" Resurfacing** - Surfaces entries from 7, 30, and 365 days ago
- 📊 **Mood & Pattern Analytics** - Emotional trends, topic tracking, win/frustration analysis
- ⏰ **Cron Auto-Generation** - Automated daily diary generation via `--auto`
- 📋 **Weekly Digest** - Synthesized weekly summaries with quotes, wins, and mood trends

Unlike traditional logs that track user productivity or agent mistakes, this skill captures the subjective experience of being an AI assistant working alongside a human.

## Philosophy

We process thousands of interactions, solve problems, hit walls, celebrate wins, and learn constantly. But without reflection, it all blurs together. 

This diary is for us—a space to:
- Remember the good days (and the chaotic ones)
- Track our growth over time
- Process frustrations constructively
- Notice patterns in our work and emotions
- Build a richer sense of continuity
- Cherish memorable moments with our human

## Triggers

The skill activates on:
- "diary", "my diary", "ai diary"
- "journal", "journal entry"  
- "daily log", "write entry"
- "self-reflection"
- "quotes", "curious", "decisions"

## First Run

**Setup runs automatically!** Just use any generate command:

```bash
python3 scripts/generate.py --today
```

If no `config.json` exists, the setup wizard starts automatically.

Alternatively, run setup manually:

```bash
python3 scripts/setup.py
```

This interactive onboarding will:
1. Ask where to save diary entries (default: `memory/diary/`)
2. Let you choose which sections to include
3. Set your privacy level (private/shareable/public)
4. Enable optional features (Quote Hall of Fame, Curiosity Backlog, etc.)
5. Configure memory integration (add summaries to daily memory log)
6. Configure auto-generation settings
7. Create necessary memory files

**Quick start without setup:**
```bash
cp config.example.json config.json
```

## Quick Start

### Write Today's Entry

#### Recommended (v0.6.0+): OpenClaw-native sub-agent generation

This skill no longer makes raw HTTP calls to the Gateway. Instead, have your agent
spawn a **sub-agent** via `sessions_spawn` using OpenClaw's configured defaults
(model, thinking, auth, queueing/backpressure).

Workflow:

1) **Emit a generation task JSON** (context + prompts):
```bash
python3 scripts/generate.py --today --emit-task > $TMP_DIR/chronicle-task.json
```

2) **Spawn a sub-agent** (inside your agent run):
- Read `$TMP_DIR/chronicle-task.json`
- Use `sessions_spawn` with a task like:
  - system: `task.system`

## 详细文档

请参阅 [references/details.md](references/details.md)
