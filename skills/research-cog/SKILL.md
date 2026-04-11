---
name: research-cog
description: "Deep research agent powered by CellCog. Market research, competitive analysis, investment research, academic research, due diligence, literature reviews with citations. Multi-source synthesis across hundreds of sources. #1 on DeepResearch Bench (Apr 2026)."
author: CellCog
homepage: https://cellcog.ai
metadata:
  openclaw:
    emoji: "🔬"
    os: [darwin, linux, windows]
dependencies: [cellcog]
---

# Research Cog - Deep Research Powered by CellCog

**#1 on DeepResearch Bench (Apr 2026).** Your AI research analyst for comprehensive, citation-backed research on any topic.

Leaderboard: https://huggingface.co/spaces/muset-ai/DeepResearch-Bench-Leaderboard

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

## What You Can Research

### Competitive Analysis

Analyze companies against their competitors with structured insights:

- **Company vs. Competitors**: "Compare Stripe vs Square vs Adyen - market positioning, pricing, features, strengths/weaknesses"
- **SWOT Analysis**: "Create a SWOT analysis for Shopify in the e-commerce platform market"
- **Market Positioning**: "How does Notion position itself against Confluence, Coda, and Obsidian?"
- **Feature Comparison**: "Compare the AI capabilities of Salesforce, HubSpot, and Zoho CRM"

### Market Research

Understand markets, industries, and trends:

- **Industry Analysis**: "Analyze the electric vehicle market in Europe - size, growth, key players, trends"
- **Market Sizing**: "What's the TAM/SAM/SOM for AI-powered customer service tools in North America?"
- **Trend Analysis**: "What are the emerging trends in sustainable packaging for 2026?"
- **Customer Segments**: "Identify and profile the key customer segments for premium pet food"
- **Regulatory Landscape**: "Research FDA regulations for AI-powered medical devices"

### Stock & Investment Analysis

Financial research with data and analysis:

- **Company Fundamentals**: "Analyze NVIDIA's financials - revenue growth, margins, competitive moat"
- **Investment Thesis**: "Build an investment thesis for Microsoft's AI strategy"

## 详细文档

请参阅 [references/details.md](references/details.md)
