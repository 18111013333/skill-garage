---
name: memory-setup
description: Enable and configure Moltbot/Clawdbot memory search for persistent context. Use when setting up memory, fixing "goldfish brain," or helping users configure memorySearch in their config. Covers MEMORY.md, daily logs, and vector search setup.
---

# Memory Setup Skill

Transform your agent from goldfish to elephant. This skill helps configure persistent memory for Moltbot/Clawdbot.

## Quick Setup

### 1. Enable Memory Search in Config

Add to `~/.clawdbot/clawdbot.json` (or `moltbot.json`):

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "voyage",
    "sources": ["memory", "sessions"],
    "indexMode": "hot",
    "minScore": 0.3,
    "maxResults": 20
  }
}
```

### 2. Create Memory Structure

In your workspace, create:

```
workspace/
├── MEMORY.md              # Long-term curated memory
└── memory/
    ├── logs/              # Daily logs (YYYY-MM-DD.md)
    ├── projects/          # Project-specific context
    ├── groups/            # Group chat context
    └── system/            # Preferences, setup notes
```

### 3. Initialize MEMORY.md

Create `MEMORY.md` in workspace root:

```markdown
# MEMORY.md — Long-Term Memory

## About [User Name]
- Key facts, preferences, context

## Active Projects
- Project summaries and status

## Decisions & Lessons
- Important choices made
- Lessons learned

## Preferences
- Communication style
- Tools and workflows
```

## Config Options Explained

| Setting | Purpose | Recommended |
|---------|---------|-------------|
| `enabled` | Turn on memory search | `true` |
| `provider` | Embedding provider | `"voyage"` |
| `sources` | What to index | `["memory", "sessions"]` |
| `indexMode` | When to index | `"hot"` (real-time) |
| `minScore` | Relevance threshold | `0.3` (lower = more results) |
| `maxResults` | Max snippets returned | `20` |

### Provider Options
- `voyage` — Voyage AI embeddings (recommended)
- `openai` — OpenAI embeddings
- `local` — Local embeddings (no API needed)


## 详细文档

请参阅 [references/details.md](references/details.md)
