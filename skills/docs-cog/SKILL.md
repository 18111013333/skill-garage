---
name: docs-cog
description: "AI document generation powered by CellCog — PDF by default, native DOCX when you need it. Create resumes, contracts, reports, proposals, invoices, certificates, NDAs, letters, brochures, and any professional document. Beautiful design with accurate, researched content. #1 on DeepResearch Bench (Apr 2026)."
metadata:
  openclaw:
    emoji: "📄"
    os: [darwin, linux, windows]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---

# Docs Cog - Professional Documents Powered by CellCog

**Deep reasoning. Accurate data. Beautiful design.** The three things every great document needs — and most AI gets wrong.

CellCog gets them right: **#1 on DeepResearch Bench (Apr 2026)** for deep reasoning, **SOTA search models** for factually grounded content, and **state-of-the-art document generation** — PDF or native DOCX, both rivaling professional design studios. Resumes, contracts, reports, proposals — delivered in minutes, looking like they took days.

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

## Output Formats

CellCog generates professional documents in multiple formats:

### PDF (Default for Ambiguous Requests)

When you say "create a report" or "make a document" without specifying a format, CellCog generates PDF — perfect typography, layouts, and design with full creative control.

### DOCX (First-Class Support)

When you explicitly request DOCX ("create a Word document", "make a .docx"), CellCog generates native Word directly — editable, compatible with Microsoft Word and Google Docs, great for collaborative workflows where multiple people contribute.

**Just ask for DOCX and you'll get it.** No need to justify why you want an editable format.

---

## What Documents You Can Create

### Resume & Career Documents

Build your professional story:

- **Resume/CV**: "Create a modern resume for a software engineer with 5 years of experience"
- **Cover Letter**: "Write a compelling cover letter for a product manager position at Google"
- **LinkedIn Summary**: "Create a professional LinkedIn summary that highlights my transition from finance to tech"
- **Portfolio**: "Build a portfolio document showcasing my UX design projects"


## 详细文档

请参阅 [references/details.md](references/details.md)
