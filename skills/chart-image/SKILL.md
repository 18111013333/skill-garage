---
name: chart-image
description: Generate publication-quality chart images from data. Supports line, bar, area, point, candlestick, pie/donut, heatmap, multi-series, and stacked charts. Use when visualizing data, creating graphs, plotting time series, or generating chart images for reports/alerts. Designed for Fly.io/VPS deployments - no native compilation, no Puppeteer, no browser required. Pure Node.js with prebuilt binaries.
---

# Chart Image Generator

Generate PNG chart images from data using Vega-Lite. Perfect for headless server environments.

## Why This Skill?

**Built for Fly.io / VPS / Docker deployments:**
- ✅ **No native compilation** - Uses Sharp with prebuilt binaries (unlike `canvas` which requires build tools)
- ✅ **No Puppeteer/browser** - Pure Node.js, no Chrome download, no headless browser overhead
- ✅ **Lightweight** - ~15MB total dependencies vs 400MB+ for Puppeteer-based solutions
- ✅ **Fast cold starts** - No browser spinup delay, generates charts in <500ms
- ✅ **Works offline** - No external API calls (unlike QuickChart.io)

## Setup (one-time)

```bash
cd /data/clawd/skills/chart-image/scripts && npm install
```

## Quick Usage

```bash
node /data/clawd/skills/chart-image/scripts/chart.mjs \
  --type line \
  --data '[{"x":"10:00","y":25},{"x":"10:30","y":27},{"x":"11:00","y":31}]' \
  --title "Price Over Time" \
  --output chart.png
```

## Chart Types

### Line Chart (default)
```bash
node chart.mjs --type line --data '[{"x":"A","y":10},{"x":"B","y":15}]' --output line.png
```

### Bar Chart
```bash
node chart.mjs --type bar --data '[{"x":"A","y":10},{"x":"B","y":15}]' --output bar.png
```

### Area Chart
```bash
node chart.mjs --type area --data '[{"x":"A","y":10},{"x":"B","y":15}]' --output area.png
```

### Pie / Donut Chart
```bash
# Pie
node chart.mjs --type pie --data '[{"category":"A","value":30},{"category":"B","value":70}]' \
  --category-field category --y-field value --output pie.png

# Donut (with hole)
node chart.mjs --type donut --data '[{"category":"A","value":30},{"category":"B","value":70}]' \
  --category-field category --y-field value --output donut.png
```

### Candlestick Chart (OHLC)
```bash
node chart.mjs --type candlestick \
  --data '[{"x":"Mon","open":100,"high":110,"low":95,"close":105}]' \
  --open-field open --high-field high --low-field low --close-field close \
  --title "Stock Price" --output candle.png
```

### Heatmap
```bash
node chart.mjs --type heatmap \
  --data '[{"x":"Mon","y":"Week1","value":5},{"x":"Tue","y":"Week1","value":8}]' \
  --color-value-field value --color-scheme viridis \
  --title "Activity Heatmap" --output heatmap.png
```

### Multi-Series Line Chart
Compare multiple trends on one chart:
```bash
node chart.mjs --type line --series-field "market" \
  --data '[{"x":"Jan","y":10,"market":"A"},{"x":"Jan","y":15,"market":"B"}]' \
  --title "Comparison" --output multi.png
```

### Stacked Bar Chart
```bash
node chart.mjs --type bar --stacked --color-field "category" \
  --data '[{"x":"Mon","y":10,"category":"Work"},{"x":"Mon","y":5,"category":"Personal"}]' \
  --title "Hours by Category" --output stacked.png
```

### Volume Overlay (Dual Y-axis)
Price line with volume bars:
```bash
node chart.mjs --type line --volume-field volume \
  --data '[{"x":"10:00","y":100,"volume":5000},{"x":"11:00","y":105,"volume":3000}]' \
  --title "Price + Volume" --output volume.png
```

## 详细文档

请参阅 [references/details.md](references/details.md)
