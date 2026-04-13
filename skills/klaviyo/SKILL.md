---
name: klaviyo
description: |
  Klaviyo API integration with managed OAuth. Access profiles, lists, segments, campaigns, flows, events, metrics, templates, catalogs, and webhooks. Use this skill when users want to manage email marketing, customer data, or integrate with Klaviyo workflows. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Klaviyo

Access the Klaviyo API with managed OAuth authentication. Manage profiles, lists, segments, campaigns, flows, events, metrics, templates, catalogs, and webhooks for email marketing and customer engagement.

## Quick Start

```bash
# List profiles
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/klaviyo/api/profiles')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('revision', '2026-01-15')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/klaviyo/{native-api-path}
```

Replace `{native-api-path}` with the actual Klaviyo API endpoint path. The gateway proxies requests to `a.klaviyo.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## API Versioning

Klaviyo uses date-based API versioning. Include the `revision` header in all requests:

```
revision: 2026-01-15
```

## Connection Management

Manage your Klaviyo OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=klaviyo&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'klaviyo'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'

## API Reference

详细 API 文档请参阅 [references/api-reference.md](references/api-reference.md)
