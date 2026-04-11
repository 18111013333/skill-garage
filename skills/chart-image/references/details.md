
### Sparkline (mini inline chart)
```bash
node chart.mjs --sparkline --data '[{"x":"1","y":10},{"x":"2","y":15}]' --output spark.png
```
Sparklines are 80x20 by default, transparent, no axes.

## Options Reference

### Basic Options
| Option | Description | Default |
|--------|-------------|---------|
| `--type` | Chart type: line, bar, area, point, pie, donut, candlestick, heatmap | line |
| `--data` | JSON array of data points | - |
| `--output` | Output file path | chart.png |
| `--title` | Chart title | - |
| `--width` | Width in pixels | 600 |
| `--height` | Height in pixels | 300 |

### Axis Options
| Option | Description | Default |
|--------|-------------|---------|
| `--x-field` | Field name for X axis | x |
| `--y-field` | Field name for Y axis | y |
| `--x-title` | X axis label | field name |
| `--y-title` | Y axis label | field name |
| `--x-type` | X axis type: ordinal, temporal, quantitative | ordinal |
| `--x-format` | Temporal X axis label format (d3-time-format, e.g. `%b %d`, `%H:%M`) | auto |
| `--x-sort` | X axis order: ascending, descending, or none (preserve input order) | auto |
| `--series-order CSV` | Explicit series/category order for multi-series and stacked legends (e.g. `Critical,High,Medium`) | data order |
| `--x-label-limit PX` | Max pixel width for X axis labels before Vega truncates them | auto |
| `--y-label-limit PX` | Max pixel width for Y axis labels before Vega truncates them | auto |
| `--x-ticks N` | Target X-axis tick count for dense or sparse charts | auto |
| `--y-ticks N` | Target primary/left Y-axis tick count for dense or sparse charts | auto |
| `--y2-ticks N` | Target secondary/right Y-axis tick count for dual-axis and volume charts | auto |
| `--y-domain` | Y scale as "min,max" | auto |
| `--y-pad` | Add vertical padding as a fraction of range (e.g. `0.1` = 10%) | 0 |

### Visual Options
| Option | Description | Default |
|--------|-------------|---------|
| `--color` | Line/bar color | #e63946 |
| `--dark` | Dark mode theme | false |
| `--svg` | Output SVG instead of PNG | false |
| `--font-family` | CSS font-family string for chart text/legend/title theming | Helvetica, Arial, sans-serif |

**Font examples:** `"Inter, Helvetica, Arial, sans-serif"`, `"Georgia, serif"`, `"JetBrains Mono, Consolas, monospace"`
| `--no-points` | Hide point markers on line charts | false |
| `--line-width N` | Set line thickness in pixels for line charts | 2 |
| `--point-size N` | Set point marker size for line/point charts | 60 |
| `--bar-radius N` | Round bar corners in pixels for bar-based charts | 0 |
| `--color-scheme` | Vega color scheme (category10, viridis, etc.) | - |
| `--legend-columns N` | Wrap legend entries into N columns for crowded multi-series/pie charts | auto |
| `--legend-label-limit PX` | Max pixel width for legend labels before Vega truncates them | auto |

### Alert/Monitor Options
| Option | Description | Default |
|--------|-------------|---------|
| `--show-change` | Show +/-% change annotation at last point | false |
| `--focus-change` | Zoom Y-axis to 2x data range | false |
| `--focus-recent N` | Show only last N data points | all |
| `--show-values` | Label min/max peak points | false |
| `--last-value` | Label the final data point value | false |

### Multi-Series/Stacked Options
| Option | Description | Default |
|--------|-------------|---------|
| `--series-field` | Field for multi-series line charts | - |
| `--stacked` | Enable stacked bar mode | false |
| `--color-field` | Field for stack/color categories | - |

### Candlestick Options
| Option | Description | Default |
|--------|-------------|---------|
| `--open-field` | OHLC open field | open |
| `--high-field` | OHLC high field | high |
| `--low-field` | OHLC low field | low |
| `--close-field` | OHLC close field | close |

### Pie/Donut Options
| Option | Description | Default |
|--------|-------------|---------|
| `--category-field` | Field for pie slice categories | x |
| `--donut` | Render as donut (with center hole) | false |

### Heatmap Options
| Option | Description | Default |
|--------|-------------|---------|
| `--color-value-field` | Field for heatmap intensity | value |
| `--y-category-field` | Y axis category field | y |

### Dual-Axis Options (General)
| Option | Description | Default |
|--------|-------------|---------|
| `--y2-field` | Second Y axis field (independent right axis) | - |
| `--y2-title` | Title for second Y axis | field name |
| `--y2-color` | Color for second series | #60a5fa (dark) / #2563eb (light) |
| `--y2-type` | Chart type for second axis: line, bar, area | line |
| `--y2-format` | Right-axis format: percent, dollar, compact, integer, decimal4, or d3-format string | auto |

**Example:** Revenue bars (left) + Churn area (right):
```bash
node chart.mjs \
  --data '[{"month":"Jan","revenue":12000,"churn":4.2},...]' \
  --x-field month --y-field revenue --type bar \
  --y2-field churn --y2-type area --y2-color "#60a5fa" --y2-format ".1f" \
  --y-title "Revenue ($)" --y2-title "Churn (%)" \
  --x-sort none --dark --title "Revenue vs Churn"
```

### Volume Overlay Options (Candlestick)
| Option | Description | Default |
|--------|-------------|---------|
| `--volume-field` | Field for volume bars (enables dual-axis) | - |
| `--volume-color` | Color for volume bars | #4a5568 |

### Formatting Options
| Option | Description | Default |
|--------|-------------|---------|
| `--y-format` | Y axis format: percent, dollar, compact, decimal4, integer, scientific, or d3-format string | auto |
| `--subtitle` | Subtitle text below chart title | - |
| `--hline` | Horizontal reference line: "value" or "value,color" or "value,color,label" (repeatable) | - |

### Annotation Options
| Option | Description | Default |
|--------|-------------|---------|
| `--annotation` | Static text annotation | - |
| `--annotations` | JSON array of event markers | - |

## Alert-Style Chart (recommended for monitors)

```bash
node chart.mjs --type line --data '[...]' \
  --title "Iran Strike Odds (48h)" \
  --show-change --focus-change --show-values --dark \
  --output alert.png
```

For recent action only:
```bash
node chart.mjs --type line --data '[hourly data...]' \
  --focus-recent 4 --show-change --focus-change --dark \
  --output recent.png
```

## Timeline Annotations

Mark events on the chart:
```bash
node chart.mjs --type line --data '[...]' \
  --annotations '[{"x":"14:00","label":"News broke"},{"x":"16:30","label":"Press conf"}]' \
  --output annotated.png
```

## Temporal X-Axis

For proper time series with date gaps:
```bash
node chart.mjs --type line --x-type temporal \
  --data '[{"x":"2026-01-01","y":10},{"x":"2026-01-15","y":20}]' \
  --output temporal.png
```

Use `--x-type temporal` when X values are ISO dates and you want spacing to reflect actual time gaps (not evenly spaced).

## Y-Axis Formatting

Format axis values for readability:
```bash
# Dollar amounts
node chart.mjs --data '[...]' --y-format dollar --output revenue.png
# → $1,234.56

# Percentages (values as decimals 0-1)
node chart.mjs --data '[...]' --y-format percent --output rates.png
# → 45.2%

# Compact large numbers
node chart.mjs --data '[...]' --y-format compact --output users.png
# → 1.2K, 3.4M

# Crypto prices (4 decimal places)
node chart.mjs --data '[...]' --y-format decimal4 --output molt.png
# → 0.0004

# Custom d3-format string
node chart.mjs --data '[...]' --y-format ',.3f' --output custom.png
```

Available shortcuts: `percent`, `dollar`/`usd`, `compact`, `integer`, `decimal2`, `decimal4`, `scientific`

## Chart Subtitle

Add context below the title:
```bash
node chart.mjs --title "MOLT Price" --subtitle "20,668 MOLT held" --data '[...]' --output molt.png
```

## Theme Selection

Use `--dark` for dark mode. Auto-select based on time:
- **Night (20:00-07:00 local)**: `--dark`
- **Day (07:00-20:00 local)**: light mode (default)

## Social Size Presets

Use `--output-size` when the chart is meant for a specific surface:

```bash
# Bluesky / OG-style landscape post
node chart.mjs --type line --data '[...]' --output-size bluesky --output bluesky-chart.png

# Instagram / Threads portrait post
node chart.mjs --type line --data '[...]' --output-size portrait --output portrait-chart.png
```

Available presets include `twitter`, `discord`, `slack`, `linkedin`, `bluesky` (`bsky` alias), `youtube`, `instagram`, `portrait`, `story`, `thumbnail`, `wide`, and `square`.

## Piping Data

```bash
echo '[{"x":"A","y":1},{"x":"B","y":2}]' | node chart.mjs --output out.png
```

## Custom Vega-Lite Spec

For advanced charts:
```bash
node chart.mjs --spec my-spec.json --output custom.png
```

## ⚠️ IMPORTANT: Always Send the Image!

After generating a chart, **always send it back to the user's channel**.
Don't just save to a file and describe it — the whole point is the visual.

```bash
# 1. Generate the chart
node chart.mjs --type line --data '...' --output /data/clawd/tmp/my-chart.png

# 2. Send it! Use message tool with filePath:
#    action=send, target=<channel_id>, filePath=/data/clawd/tmp/my-chart.png
```

**Tips:**
- Save to `/data/clawd/tmp/` (persistent) not `/tmp/` (may get cleaned)
- Use `action=send` with `filePath` — `thread-reply` does NOT support file attachments
- Include a brief caption in the message text
- Auto-use `--dark` between 20:00-07:00 Israel time

---
*Updated: 2026-03-27 - Added `--y2-ticks` so dual-axis + volume-overlay charts can tune the right-axis tick density independently; version bumped to 2.6.22*
