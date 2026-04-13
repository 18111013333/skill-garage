### Source Options
- `memory` — MEMORY.md + memory/*.md files
- `sessions` — Past conversation transcripts
- `both` — Full context (recommended)

## Daily Log Format

Create `memory/logs/YYYY-MM-DD.md` daily:

```markdown
# YYYY-MM-DD — Daily Log

## [Time] — [Event/Task]
- What happened
- Decisions made
- Follow-ups needed

## [Time] — [Another Event]
- Details
```

## Agent Instructions (AGENTS.md)

Add to your AGENTS.md for agent behavior:

```markdown
## Memory Recall
Before answering questions about prior work, decisions, dates, people, preferences, or todos:
1. Run memory_search with relevant query
2. Use memory_get to pull specific lines if needed
3. If low confidence after search, say you checked
```

## Troubleshooting

### Memory search not working?
1. Check `memorySearch.enabled: true` in config
2. Verify MEMORY.md exists in workspace root
3. Restart gateway: `clawdbot gateway restart`

### Results not relevant?
- Lower `minScore` to `0.2` for more results
- Increase `maxResults` to `30`
- Check that memory files have meaningful content

### Provider errors?
- Voyage: Set `VOYAGE_API_KEY` in environment
- OpenAI: Set `OPENAI_API_KEY` in environment
- Use `local` provider if no API keys available

## Verification

Test memory is working:

```
User: "What do you remember about [past topic]?"
Agent: [Should search memory and return relevant context]
```

If agent has no memory, config isn't applied. Restart gateway.

## Full Config Example

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "voyage",
    "sources": ["memory", "sessions"],
    "indexMode": "hot",
    "minScore": 0.3,
    "maxResults": 20
  },
  "workspace": "/path/to/your/workspace"
}
```

## Why This Matters

Without memory:
- Agent forgets everything between sessions
- Repeats questions, loses context
- No continuity on projects

With memory:
- Recalls past conversations
- Knows your preferences
- Tracks project history
- Builds relationship over time

Goldfish → Elephant. 🐘
