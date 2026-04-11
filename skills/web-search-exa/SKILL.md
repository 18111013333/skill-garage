---
name: web-search-exa
description: "Neural web search, content extraction, company and people research, code search, and deep research via the Exa MCP server. Use when you need to: (1) search the web with semantic understanding — not just keywords, (2) find research papers, news, tweets, companies, or people, (3) extract clean content from URLs, (4) find semantically similar pages to a known URL, (5) get code examples and documentation, (6) run deep multi-step research with a report, (7) get a quick synthesized answer with citations. NOT for: local file operations, non-web tasks, or anything that doesn't involve web search or content retrieval."
---

# Exa — Neural Web Search & Research

Exa is a neural search engine. Unlike keyword-based search, it understands meaning — you describe the page you're looking for and it finds it. Returns clean, LLM-ready content with no scraping needed.

**MCP server:** `https://mcp.exa.ai/mcp`
**Free tier:** generous rate limits, no key needed for basic tools
**API key:** [dashboard.exa.ai/api-keys](https://dashboard.exa.ai/api-keys) — unlocks higher limits + all tools
**Docs:** [exa.ai/docs](https://exa.ai/docs)
**GitHub:** [github.com/exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server)

## Setup

Add the MCP server to your agent config:

```bash
# OpenClaw
openclaw mcp add exa --url "https://mcp.exa.ai/mcp"
```

Or in any MCP config JSON:
```json
{
  "mcpServers": {
    "exa": {
      "url": "https://mcp.exa.ai/mcp"
    }
  }
}
```

To unlock all tools and remove rate limits, append your API key:
```
https://mcp.exa.ai/mcp?exaApiKey=YOUR_EXA_KEY
```

To enable specific optional tools:
```
https://mcp.exa.ai/mcp?exaApiKey=YOUR_KEY&tools=web_search_exa,web_search_advanced_exa,people_search_exa,crawling_exa,company_research_exa,get_code_context_exa,deep_researcher_start,deep_researcher_check,deep_search_exa
```

---

## Tool Reference

### Default tools (available without API key)

| Tool | What it does |
|------|-------------|
| `web_search_exa` | General-purpose web search — clean content, fast |
| `get_code_context_exa` | Code examples + docs from GitHub, Stack Overflow, official docs |
| `company_research_exa` | Company overview, news, funding, competitors |

### Optional tools (enable via `tools` param, need API key for some)

| Tool | What it does |
|------|-------------|
| `web_search_advanced_exa` | Full-control search: domain filters, date ranges, categories, content modes |
| `crawling_exa` | Extract full page content from a known URL — handles JS, PDFs, complex layouts |
| `people_search_exa` | Find LinkedIn profiles, professional backgrounds, experts |
| `deep_researcher_start` | Kick off an async multi-step research agent → detailed report |
| `deep_researcher_check` | Poll status / retrieve results from deep research |
| `deep_search_exa` | Single-call deep search with synthesized answer + citations (needs API key) |

---

## web_search_exa

Fast general search. Describe what you're looking for in natural language.

**Parameters:**
- `query` (string, required) — describe the page you want to find
- `numResults` (int) — number of results, default 10
- `type` — `auto` (best quality), `fast` (lower latency), `deep` (multi-step reasoning)
- `livecrawl` — `fallback` (default) or `preferred` (always fetch fresh)
- `contextMaxCharacters` (int) — cap the returned content size

```
web_search_exa {
  "query": "blog posts about using vector databases for recommendation systems",
  "numResults": 8
}
```

```
web_search_exa {
  "query": "latest OpenAI announcements March 2026",
  "numResults": 5,
  "type": "fast"
}
```

---

## web_search_advanced_exa


## 详细文档

请参阅 [references/details.md](references/details.md)
