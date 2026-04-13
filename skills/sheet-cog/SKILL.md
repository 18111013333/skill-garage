---
name: sheet-cog
description: "AI spreadsheet and Excel generation powered by CellCog. Create financial models, budget templates, data trackers, projections, pivot tables, and complex formulas — XLSX output with full Python access. Data manipulation, analysis, charts, and professional formatting. Engineering-grade spreadsheets."
metadata:
  openclaw:
    emoji: "📋"
    os: [darwin, linux, windows]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---

# Sheet Cog - Built by the Agent That Builds CellCog

**CellCog is built by its own Coding Agent. That same agent builds your spreadsheets.**

Full Python access, complex data manipulation, formulas, pivot tables, and financial models — powered by the engineering brain that develops an entire AI platform daily. Not a template filler. A programmer that understands your data and builds exactly what you need.

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

## What Spreadsheets You Can Create

### Financial Models

Professional financial analysis and projections:

- **Startup Financial Model**: "Create a 3-year financial model for a SaaS startup including revenue projections, expenses, and cash flow"
- **DCF Model**: "Build a discounted cash flow model for valuing a company"
- **Investment Analysis**: "Create a real estate investment analysis spreadsheet with ROI calculations"
- **Revenue Model**: "Build a revenue forecasting model with multiple scenarios (base, optimistic, pessimistic)"
- **Unit Economics**: "Create a unit economics spreadsheet showing CAC, LTV, payback period"

### Budget Templates

Personal and business budgets:

- **Personal Budget**: "Create a monthly personal budget tracker with income, fixed expenses, variable expenses, and savings goals"
- **Household Budget**: "Build a family budget spreadsheet with categories for housing, food, transportation, etc."
- **Project Budget**: "Create a project budget template with phases, resources, and variance tracking"
- **Marketing Budget**: "Build a marketing budget spreadsheet with channels, planned vs actual, and ROI tracking"
- **Event Budget**: "Create a wedding budget spreadsheet with vendor categories and payment tracking"

### Data Trackers

Organized tracking for any data:

- **Fitness Tracker**: "Create a workout log spreadsheet with exercises, sets, reps, weights, and progress charts"

## 详细文档

请参阅 [references/details.md](references/details.md)
