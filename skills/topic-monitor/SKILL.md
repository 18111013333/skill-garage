---
name: topic-monitor
version: 1.5.2
description: Monitor topics of interest and proactively alert when important developments occur. Use when the user wants automated monitoring of specific subjects like product releases, news topics, technology updates, RSS/Atom feeds, or GitHub releases. Supports scheduled web search plus feed polling, boolean topic filters, AI importance scoring with sentiment tracking, smart alerts vs weekly digests, and memory-aware contextual summaries.
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":{"TOPIC_MONITOR_TELEGRAM_ID":"optional - Telegram chat ID for alerts","TOPIC_MONITOR_DATA_DIR":"optional - defaults to .data/ in skill dir","WEB_SEARCH_PLUS_PATH":"optional - defaults to relative path"},"note":"All env vars optional. Defaults work out of the box."}}}
---

# Topic Monitor

Monitor topics continuously and alert only when something looks relevant.

## What’s new in v1.5.0

- **RSS/Atom feed monitoring** as a first-class source via `feeds`
- **GitHub release monitoring** via `github_repos` → `https://github.com/{owner}/{repo}/releases.atom`
- **Feed auto-discovery** from normal URLs
- **OPML import** for feed lists
- **Advanced filters** with `required_keywords` and `exclude_keywords`
- **Sentiment analysis** on findings: `positive`, `negative`, `neutral`, `mixed`
- **Sentiment shift alerts** with `alert_on_sentiment_shift`

## Quick start

```bash
python3 scripts/quick.py "AI Model Releases"
python3 scripts/quick.py "OpenClaw Releases" --github-repos "openclaw/openclaw"
python3 scripts/quick.py "Security Advisories" --feeds "https://example.com/security.xml"
```

Then test it:

```bash
python3 scripts/monitor.py --dry-run --verbose
```

## Core model

Each topic can mix multiple sources:

- **Web search** via `query`
- **RSS/Atom feeds** via `feeds`
- **GitHub releases** via `github_repos`

All collected results flow into the same pipeline:

1. gather results
2. deduplicate
3. apply advanced filters
4. score importance
5. classify sentiment
6. alert immediately or save for digest
7. track state and sentiment history

## Topic config

Each topic supports these keys:

- `id`
- `name`
- `query`
- `keywords`
- `feeds`
- `github_repos`
- `required_keywords`
- `exclude_keywords`
- `frequency` → `hourly|daily|weekly`
- `importance_threshold` → `high|medium|low`
- `channels`
- `context`
- `alert_on`
- `alert_on_sentiment_shift`
- `ignore_sources`
- `boost_sources`

### Example config

```json
{
  "topics": [
    {

## 详细文档

请参阅 [references/details.md](references/details.md)
