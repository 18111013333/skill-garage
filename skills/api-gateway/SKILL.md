---
name: api-gateway
description: |
  Connect to 100+ APIs (Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, HubSpot, etc.) with managed OAuth.
  Use this skill when users want to interact with external services.
  Security: The MATON_API_KEY authenticates with Maton.ai but grants NO access to third-party services by itself. Each service requires explicit OAuth authorization by the user through Maton's connect flow. Access is strictly scoped to connections the user has authorized. Provided by Maton (https://maton.ai).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# API Gateway

Passthrough proxy for direct access to third-party APIs using managed OAuth connections, provided by [Maton](https://maton.ai). The API gateway lets you call native API endpoints directly.

## Quick Start

```bash
# Native Slack API call
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'channel': 'C0123456', 'text': 'Hello from gateway!'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/slack/api/chat.postMessage', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```


## Base URL

```
https://gateway.maton.ai/{app}/{native-api-path}
```

Replace `{app}` with the service name and `{native-api-path}` with the actual API endpoint path.

IMPORTANT: The URL path MUST start with the connection's app name (eg. `/google-mail/...`). This prefix tells the gateway which app connection to use. For example, the native Gmail API path starts with `gmail/v1/`, so full paths look like `/google-mail/gmail/v1/users/me/messages`.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

The API gateway automatically injects the appropriate OAuth token for the target service.

**Environment Variable:** You can set your API key as the `MATON_API_KEY` environment variable:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Click the copy button on the right side of API Key section to copy it

## Connection Management

Connection management uses a separate base URL: `https://ctrl.maton.ai`

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=slack&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Query Parameters (optional):**
- `app` - Filter by service name (e.g., `slack`, `hubspot`, `salesforce`)
- `status` - Filter by connection status (`ACTIVE`, `PENDING`, `FAILED`)

**Response:**
```json
{
  "connections": [
    {
      "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
      "status": "ACTIVE",
      "creation_time": "2025-12-08T07:20:53.488460Z",
      "last_updated_time": "2026-01-31T20:03:32.593153Z",
      "url": "https://connect.maton.ai/?session_token=5e9...",
      "app": "slack",
      "method": "OAUTH2",

## API Reference

详细 API 文档请参阅 [references/api-reference.md](references/api-reference.md)
