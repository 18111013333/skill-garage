---
name: story-cog
description: "AI creative writing and storytelling powered by CellCog. Write novels, short stories, screenplays, fan fiction, poetry. World building, character development, narrative design. Fiction writing for fantasy, sci-fi, mystery, romance, horror, literary fiction. AI story writer and writing assistant."
metadata:
  openclaw:
    emoji: "📖"
    os: [darwin, linux, windows]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---

# Story Cog - Storytelling Powered by CellCog

Create compelling stories with AI - from short fiction to novels to screenplays to immersive worlds.

---

## Prerequisites

This skill requires the `cellcog` skill for SDK setup and API calls.

```bash
clawhub install cellcog
```

**Read the cellcog skill first** for SDK setup. This skill shows you what's possible.

**OpenClaw agents (fire-and-forget — recommended for long tasks):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",  # OpenClaw only
    task_label="my-task",
    chat_mode="agent",  # See cellcog skill for all modes
)
```

**All other agents (blocks until done):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
)
```

See the **cellcog** mothership skill for complete SDK API reference — delivery modes, timeouts, file handling, and more.

---

## What Stories You Can Create

### Short Fiction

Complete short stories:

- **Flash Fiction**: "Write a 500-word horror story that ends with a twist"
- **Short Stories**: "Create a 3,000-word sci-fi story about first contact"
- **Micro Fiction**: "Write a complete story in exactly 100 words"
- **Anthology Pieces**: "Create a short story for a cyberpunk anthology"

**Example prompt:**
> "Write a 2,000-word short story:
> 
> Genre: Magical realism
> Setting: A small Japanese village with a mysterious tea shop
> Theme: Grief and healing
> 
> The protagonist discovers that the tea shop owner can brew memories into tea.
> 
> Tone: Melancholic but hopeful. Studio Ghibli meets Haruki Murakami."

### Novel Development

Long-form fiction support:

- **Novel Outlines**: "Create a detailed outline for a fantasy trilogy"
- **Chapter Drafts**: "Write Chapter 1 of my mystery novel"
- **Character Arcs**: "Develop the protagonist's arc across a 3-act structure"

## 详细文档

请参阅 [references/details.md](references/details.md)
