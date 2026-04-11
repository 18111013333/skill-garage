---
name: Screenshot
slug: screenshot
version: 1.0.1
homepage: https://clawic.com/skills/screenshot
description: "Capture, inspect, and compare screenshots of screens, windows, regions, web pages, simulators, and CI runs with the right tool, wait strategy, viewport, and output format. Use when (1) you need screenshots for debugging, QA, docs, bug reports, or visual review; (2) desktop, browser, simulator, or headless capture is involved; (3) stable screenshots require fixed viewport, settling, masking, or animation control."
changelog: "Improved screenshot guidance with stronger browser, simulator, CI, and visual-stability rules while keeping the skill compact."
metadata: {"clawdbot":{"emoji":"📸","os":["linux","darwin","win32"]}}
---

## When to Use

Use when the task needs a screenshot of a desktop app, browser page, simulator, region, window, or full screen, especially for debugging, QA, documentation, release notes, bug reports, visual review, or before/after comparison.

This skill is about taking the right screenshot reliably, not about editing images after the fact.

## Tool Choice

| Context | Best default | Why |
|---------|--------------|-----|
| macOS desktop or window | `screencapture` | Built-in, reliable, supports silent, interactive, region, and window capture |
| iOS Simulator | `xcrun simctl io booted screenshot` | More reliable than generic desktop capture for simulator output |
| Linux Wayland | `grim` + `slurp` | X11 tools often fail or behave oddly on Wayland |
| Linux X11 / headless CI | `scrot` or browser-native capture | Works in minimal or virtual-display environments |
| Windows desktop capture | `nircmd savescreenshot` or Pillow `ImageGrab` | Easier than verbose PowerShell screen APIs |
| Web page or web app | Playwright | Best for stable viewport, element, full-page, masked, and regression screenshots |
| Visual diff / screenshot tests | Playwright with fixed viewport | Better control over animations, caret, masks, and reproducibility |

Default to the most native capture path first. Move to browser-native tooling when determinism, masking, element capture, or visual regression matters more than convenience.

## Core Rules

### 1. Pick the capture path by artifact, not by habit

- Desktop UI screenshots usually want OS-native tools.
- Web pages and web apps usually want browser-native capture, not a desktop screenshot of the browser window.
- Simulator screenshots should come from the simulator tooling when possible.
- Use region, window, or element capture when the point is local; use full screen or full page only when the full context matters.

### 2. Stabilize the target before capturing

- Dynamic pages should settle before capture: wait for network idle or the specific element that matters, then give fonts and transitions a brief moment to finish.
- Do not take the screenshot before the real rendered state exists.
- For browser capture, prefer explicit readiness over blind sleeps when possible.
- If the page never truly goes idle, wait for the exact UI state you need instead of chasing perfect stillness.

### 3. Freeze viewport, scale, zoom, and theme for reproducibility

- Screenshot comparisons are meaningless if viewport, zoom level, theme, or device scale changed.
- For browser captures, fix the viewport before taking baselines or before/after images.
- Retina and HiDPI displays can produce more pixels than expected; decide whether you want physical pixels or CSS-scale output and keep that choice consistent.
- If dark/light mode matters, capture both intentionally instead of mixing them accidentally.

### 4. Capture the smallest useful scope

- Element, region, or window screenshots are usually better than noisy full-screen captures.
- Full-page screenshots are useful for audits and archives, but long pages become hard to read and compare.
- For browser work, element screenshots or clipped regions usually produce cleaner diffs than full-page output.
- If the screenshot is evidence, keep enough surrounding context that the user can understand what they are looking at.

### 5. Remove noise before you capture

- Hide or avoid unstable UI when it is not the subject: cursors, carets, toasts, chat widgets, notifications, loading spinners, timestamps, and randomized content.
- Mask or avoid secrets, personal data, tokens, and internal URLs before capture.
- For Playwright-style browser capture, features like disabled animations, hidden carets, and masking are worth using when visual stability matters.
- If the noise is the bug, keep it; otherwise remove it.

### 6. Use the right output format

- PNG is the default for screenshots, UI, code, terminals, and text-heavy captures.
- JPEG is for photographic content, not normal screenshots.
- WebP is fine for sharing or storage when compatibility is acceptable, but do not default to it if the consumer expects plain PNG files.
- Avoid recompressing screenshots through JPEG pipelines unless the user explicitly wants smaller lossy output.

### 7. Make automation and CI captures debuggable

- On failures, save a screenshot immediately before retrying or moving on.
- Use stable filenames for baselines and timestamps for ad hoc or batch captures.
- In CI, identical viewport and deterministic state matter more than raw screenshot volume.
- Headless runs should prefer browser-native screenshots over trying to screen-grab the host display.

## 详细文档

请参阅 [references/details.md](references/details.md)
