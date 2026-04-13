  "distance": "215.2 mi",
  "distance_meters": 346300,
  "duration": "3 hrs 45 mins",
  "duration_seconds": 13500,
  "static_duration": "3 hrs 30 mins",
  "duration_in_traffic": "3 hrs 45 mins"
}
```

---

### directions - Turn-by-turn route

```bash
python3 skills/google-maps/lib/map_helper.py directions "origin" "destination" [options]
```

**Additional options (beyond distance):**
| Option | Description |
|--------|-------------|
| `--alternatives` | Return multiple routes |
| `--waypoints` | Intermediate stops (pipe-separated) |
| `--optimize` | Optimize waypoint order (TSP) |

**Examples:**
```bash
python3 skills/google-maps/lib/map_helper.py directions "New York" "Washington DC"
python3 skills/google-maps/lib/map_helper.py directions "San Francisco" "Los Angeles" --alternatives
python3 skills/google-maps/lib/map_helper.py directions "Miami" "Orlando" --waypoints="Fort Lauderdale|West Palm Beach" --optimize
```

**Response includes:** summary, labels, duration, static_duration, warnings, steps[], optimized_waypoint_order

---

### matrix - Distance matrix

Calculate distances between multiple origins and destinations:

```bash
python3 skills/google-maps/lib/map_helper.py matrix "orig1|orig2" "dest1|dest2"
```

**Example:**
```bash
python3 skills/google-maps/lib/map_helper.py matrix "New York|Boston" "Philadelphia|Washington DC"
```

**Response:**
```json
{
  "origins": ["New York", "Boston"],
  "destinations": ["Philadelphia", "Washington DC"],
  "results": [
    {"origin_index": 0, "destination_index": 0, "distance": "97 mi", "duration": "1 hr 45 mins"},
    {"origin_index": 0, "destination_index": 1, "distance": "225 mi", "duration": "4 hrs 10 mins"}
  ]
}
```

---

### geocode - Address to coordinates

```bash
python3 skills/google-maps/lib/map_helper.py geocode "1600 Amphitheatre Parkway, Mountain View, CA"
python3 skills/google-maps/lib/map_helper.py geocode "10 Downing Street, London"
```

### reverse - Coordinates to address

```bash
python3 skills/google-maps/lib/map_helper.py reverse 40.7128 -74.0060  # New York City
python3 skills/google-maps/lib/map_helper.py reverse 51.5074 -0.1278  # London
```

---

### search - Find places

```bash
python3 skills/google-maps/lib/map_helper.py search "coffee near Times Square"
python3 skills/google-maps/lib/map_helper.py search "pharmacy in San Francisco" --open
```

### details - Place information

```bash
python3 skills/google-maps/lib/map_helper.py details "<place_id>"
```

---

## Traffic Models

| Model | Use Case |
|-------|----------|
| `best_guess` | Default balanced estimate |
| `pessimistic` | Important meetings (worst-case) |
| `optimistic` | Best-case scenario |

---

## Regional Notes

Some features may not be available in all countries:

| Feature | Availability |
|---------|--------------|
| `--fuel-efficient` | US, EU, select countries |
| `--shorter` | Limited availability |
| `--mode=two_wheeler` | Asia, select countries |

Check [Google Maps coverage](https://developers.google.com/maps/coverage) for details.

---

## Multilingual Support

Works with addresses in any language:

```bash
# Hebrew
python3 skills/google-maps/lib/map_helper.py distance "תל אביב" "ירושלים"
python3 skills/google-maps/lib/map_helper.py geocode "דיזנגוף 50, תל אביב"

# Japanese
python3 skills/google-maps/lib/map_helper.py distance "東京" "大阪"

# Arabic
python3 skills/google-maps/lib/map_helper.py distance "دبي" "أبو ظبي"
```

**Language configuration:**

1. Set default via env: `GOOGLE_MAPS_LANG=he` (persists)
2. Override per-request: `--lang=ja`

```bash
# Set Hebrew as default in OpenClaw config
GOOGLE_MAPS_LANG=he

# Override for specific request
python3 skills/google-maps/lib/map_helper.py distance "Tokyo" "Osaka" --lang=ja
```

---

## Help

```bash
python3 skills/google-maps/lib/map_helper.py help
```
