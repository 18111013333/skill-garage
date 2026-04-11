---
name: Playwright (Automation + MCP + Scraper)
slug: playwright
version: 1.0.3
homepage: https://clawic.com/skills/playwright
description: "Browser automation via Playwright MCP. Navigate websites, click elements, fill forms, take screenshots, extract data, and debug real browser workflows. Use when (1) you need a real browser, not static fetch; (2) the task involves Playwright MCP, browser tools, Playwright tests, scripts, or JS-rendered pages; (3) the user wants navigation, forms, screenshots, PDFs, downloads, or browser-driven extraction turned into a reliable outcome."
changelog: Clarified the MCP-first browser automation flow and improved quick-start guidance for forms, screenshots, and extraction.
metadata: {"clawdbot":{"emoji":"P","requires":{"bins":["node","npx"]},"os":["linux","darwin","win32"],"install":[{"id":"npm-playwright","kind":"npm","package":"playwright","bins":["playwright"],"label":"Install Playwright"},{"id":"npm-playwright-mcp","kind":"npm","package":"@playwright/mcp","bins":["playwright-mcp"],"label":"Install Playwright MCP (optional)"}]}}
---

## When to Use

Use this skill for real browser tasks: JS-rendered pages, multi-step forms, screenshots or PDFs, UI debugging, Playwright test authoring, MCP-driven browser control, and structured extraction from rendered pages.

Prefer it when static fetch is insufficient or when the task depends on browser events, visible DOM state, authentication context, uploads or downloads, or user-facing rendering.

If the user mainly wants the agent to drive a browser with simple actions like navigate, click, fill, screenshot, download, or extract, treat MCP as a first-class path.

Use direct Playwright for scripts and tests. Use MCP when browser tools are already in the loop, the user explicitly wants MCP, or the fastest path is browser actions rather than writing new automation code.

Primary fit is repo-owned browser work: tests, debugging, repros, screenshots, and deterministic automation. Treat rendered-page extraction as a secondary use case, not the default identity.

## Architecture

This skill is instruction-only. It does not create local memory, setup folders, or persistent profiles by default.

Load only the smallest reference file needed for the task. Keep auth state temporary unless the repository already standardizes it and the user explicitly wants browser-session reuse.

## Quick Start

### MCP browser path
```bash
npx @playwright/mcp --headless
```

Use this path when the agent already has browser tools available or the user wants browser automation without writing new Playwright code.

### Common MCP actions

Typical Playwright MCP tool actions include:
- `browser_navigate` for opening a page
- `browser_click` and `browser_press` for interaction
- `browser_type` and `browser_select_option` for forms
- `browser_snapshot` and `browser_evaluate` for inspection and extraction
- `browser_choose_file` for uploads
- screenshot, PDF, trace, and download capture through the active browser workflow

### Common browser outcomes

| Goal | Typical MCP-style action |
|------|--------------------------|
| Open and inspect a site | navigate, wait, inspect, screenshot |
| Complete a form | navigate, click, fill, select, submit |
| Capture evidence | screenshot, PDF, download, trace |
| Pull structured page data | navigate, wait for rendered state, extract |
| Reproduce a UI bug | headed run, trace, console or network inspection |

### Existing test suite
```bash
npx playwright test
npx playwright test --headed
npx playwright test --trace on
```

### Bootstrap selectors and flows
```bash
npx playwright codegen https://example.com
```

### Direct script path
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://example.com');
  await page.screenshot({ path: 'page.png', fullPage: true });
  await browser.close();
})();
```

## Quick Reference

| Topic | File |
|------|------|
| Selector strategy and frame handling | `selectors.md` |
| Failure analysis, traces, logs, and headed runs | `debugging.md` |
| Test architecture, mocks, auth, and assertions | `testing.md` |
| CI defaults, retries, workers, and failure artifacts | `ci-cd.md` |
| Rendered-page extraction, pagination, and respectful throttling | `scraping.md` |

## Approach Selection

| Situation | Best path | Why |
|----------|-----------|-----|
| Static HTML or a simple HTTP response is enough | Use a cheaper fetch path first | Faster, cheaper, less brittle |
| You need a reliable first draft of selectors or flows | Start with `codegen` or a headed exploratory run | Faster than guessing selectors from source or stale DOM |
| Local app, staging app, or repo-owned E2E suite | Use `@playwright/test` | Best fit for repeatable tests and assertions |
| One-off browser automation, screenshots, downloads, or rendered extraction | Use direct Playwright API | Simple, explicit, and easy to debug in code |

## 详细文档

请参阅 [references/details.md](references/details.md)
