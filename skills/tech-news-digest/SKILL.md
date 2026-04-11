---
name: tech-news-digest
description: Generate tech news digests with unified source model, quality scoring, and multi-format output. Six-source data collection from RSS feeds, Twitter/X KOLs, GitHub releases, GitHub Trending, Reddit, and web search. Pipeline-based scripts with retry mechanisms and deduplication. Supports Discord, email, and markdown templates.
version: "3.16.0"
homepage: https://github.com/draco-agent/tech-news-digest
source: https://github.com/draco-agent/tech-news-digest
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    optionalBins: ["mail", "msmtp", "gog", "gh", "openssl", "weasyprint"]
env:
  - name: TWITTER_API_BACKEND
    required: false
    description: "Twitter API backend: 'official', 'twitterapiio', or 'auto' (default: auto)"
  - name: X_BEARER_TOKEN
    required: false
    description: Twitter/X API bearer token for KOL monitoring (official backend)
  - name: TWITTERAPI_IO_KEY
    required: false
    description: twitterapi.io API key for KOL monitoring (twitterapiio backend)
  - name: TAVILY_API_KEY
    required: false
    description: Tavily Search API key (alternative to Brave)
  - name: WEB_SEARCH_BACKEND
    required: false
    description: "Web search backend: auto (default), brave, or tavily"
  - name: BRAVE_API_KEYS
    required: false
    description: Brave Search API keys (comma-separated for rotation)
  - name: BRAVE_API_KEY
    required: false
    description: Brave Search API key (single key fallback)
  - name: GITHUB_TOKEN
    required: false
    description: GitHub token for higher API rate limits (auto-generated from GitHub App if not set)
  - name: GH_APP_ID
    required: false
    description: GitHub App ID for automatic installation token generation
  - name: GH_APP_INSTALL_ID
    required: false
    description: GitHub App Installation ID for automatic token generation
  - name: GH_APP_KEY_FILE
    required: false
    description: Path to GitHub App private key PEM file
tools:
  - python3: Required. Runs data collection and merge scripts.
  - mail: Optional. msmtp-based mail command for email delivery (preferred).
  - gog: Optional. Gmail CLI for email delivery (fallback if mail not available).
files:
  read:
    - config/defaults/: Default source and topic configurations
    - references/: Prompt templates and output templates
    - scripts/: Python pipeline scripts
    - <workspace>/archive/tech-news-digest/: Previous digests for dedup
  write:
    - /tmp/td-*.json: Temporary pipeline intermediate outputs
    - /tmp/td-email.html: Temporary email HTML body
    - /tmp/td-digest.pdf: Generated PDF digest
    - <workspace>/archive/tech-news-digest/: Saved digest archives
---

# Tech News Digest

Automated tech news digest system with unified data source model, quality scoring pipeline, and template-based output generation.

## Quick Start

1. **Configuration Setup**: Default configs are in `config/defaults/`. Copy to workspace for customization:
   ```bash
   mkdir -p workspace/config
   cp config/defaults/sources.json workspace/config/tech-news-digest-sources.json
   cp config/defaults/topics.json workspace/config/tech-news-digest-topics.json
   ```

2. **Environment Variables**: 
   - `TWITTERAPI_IO_KEY` - twitterapi.io API key (optional, preferred)
   - `X_BEARER_TOKEN` - Twitter/X official API bearer token (optional, fallback)
   - `TAVILY_API_KEY` - Tavily Search API key, alternative to Brave (optional)
   - `WEB_SEARCH_BACKEND` - Web search backend: auto|brave|tavily (optional, default: auto)
   - `BRAVE_API_KEYS` - Brave Search API keys, comma-separated for rotation (optional)
   - `BRAVE_API_KEY` - Single Brave key fallback (optional)
   - `GITHUB_TOKEN` - GitHub personal access token (optional, improves rate limits)

3. **Generate Digest**:
   ```bash
   # Unified pipeline (recommended) — runs all 6 sources in parallel + merge
   python3 scripts/run-pipeline.py \
     --defaults config/defaults \
     --config workspace/config \
     --hours 48 --freshness pd \
     --archive-dir workspace/archive/tech-news-digest/ \
     --output /tmp/td-merged.json --verbose --force
   ```

4. **Use Templates**: Apply Discord, email, or PDF templates to merged output

## Configuration Files

### `sources.json` - Unified Data Sources

## 详细文档

请参阅 [references/details.md](references/details.md)
