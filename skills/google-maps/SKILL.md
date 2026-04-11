---
name: google-maps
description: >
  Google Maps integration for OpenClaw with Routes API. Use for: (1) Distance/travel time calculations 
  with traffic prediction, (2) Turn-by-turn directions, (3) Distance matrix between multiple points, 
  (4) Geocoding addresses to coordinates and reverse, (5) Places search and details, (6) Transit 
  planning with arrival times. Supports future departure times, traffic models (pessimistic/optimistic), 
  avoid options (tolls/highways), and multiple travel modes (driving/walking/bicycling/transit).
version: 3.2.0
author: Leo 🦁
tags: [maps, places, location, navigation, google, traffic, directions, geocoding, routes-api]
metadata: {"clawdbot":{"emoji":"🗺️","requires":{"env":["GOOGLE_API_KEY"],"python":["requests"]},"primaryEnv":"GOOGLE_API_KEY","secondaryEnv":["GOOGLE_MAPS_API_KEY"],"optionalEnv":["GOOGLE_MAPS_LANG"],"notes":"Requires the 'requests' Python package (pip install requests). No other external dependencies."}}
allowed-tools: [exec]
---

# Google Maps 🗺️

Google Maps integration powered by the Routes API.

## Requirements

- `GOOGLE_API_KEY` environment variable
- Enable in Google Cloud Console: Routes API, Places API, Geocoding API
- Python package: `requests` (`pip install requests`)

## Configuration

| Env Variable | Default | Description |
|--------------|---------|-------------|
| `GOOGLE_API_KEY` | - | Required. Your Google Maps API key |
| `GOOGLE_MAPS_API_KEY` | - | Alternative to `GOOGLE_API_KEY` (fallback) |
| `GOOGLE_MAPS_LANG` | `en` | Response language (en, he, ja, etc.) |

Set in OpenClaw config:
```json
{
  "env": {
    "GOOGLE_API_KEY": "AIza...",
    "GOOGLE_MAPS_LANG": "en"
  }
}
```

## Script Location

```bash
python3 skills/google-maps/lib/map_helper.py <action> [options]
```

---

## Actions

### distance - Calculate travel time

```bash
python3 skills/google-maps/lib/map_helper.py distance "origin" "destination" [options]
```

**Options:**
| Option | Values | Description |
|--------|--------|-------------|
| `--mode` | driving, walking, bicycling, transit | Travel mode (default: driving) |
| `--depart` | now, +30m, +1h, 14:00, 2026-02-07 08:00 | Departure time |
| `--arrive` | 14:00 | Arrival time (transit only) |
| `--traffic` | best_guess, pessimistic, optimistic | Traffic model |
| `--avoid` | tolls, highways, ferries | Comma-separated |

**Examples:**
```bash
python3 skills/google-maps/lib/map_helper.py distance "New York" "Boston"
python3 skills/google-maps/lib/map_helper.py distance "Los Angeles" "San Francisco" --depart="+1h"
python3 skills/google-maps/lib/map_helper.py distance "Chicago" "Detroit" --depart="08:00" --traffic=pessimistic
python3 skills/google-maps/lib/map_helper.py distance "London" "Manchester" --mode=transit --arrive="09:00"
python3 skills/google-maps/lib/map_helper.py distance "Paris" "Lyon" --avoid=tolls,highways
```

**Response:**
```json
{

## 详细文档

请参阅 [references/details.md](references/details.md)
