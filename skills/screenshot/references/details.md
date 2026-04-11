
### 8. Validate that the screenshot is actually useful

- Check that the important detail is visible, legible, and not cropped away.
- Verify that secrets are not still visible in tabs, sidebars, URLs, notifications, or test data.
- Before/after comparisons should use the same viewport, zoom, theme, and state.
- A screenshot is bad if it is technically correct but useless for the human who needs it.

## High-Value Patterns

- macOS: `screencapture -x out.png` for silent capture, `-i` for interactive selection, `-R x,y,w,h` for a fixed region.
- iOS Simulator: `xcrun simctl io booted screenshot out.png`
- Linux Wayland: `grim -g "$(slurp)" out.png`
- Playwright page capture: wait for the target state, then use page, element, clipped, or full-page screenshots deliberately.
- Playwright stability features worth remembering: fixed viewport, disabled animations, hidden caret, masks for sensitive regions, and stable theme/media settings.

## Common Traps

- Taking a browser-window screenshot when an element or page screenshot was the real need.
- Capturing before fonts, data, or layout transitions finish.
- Comparing screenshots with different viewport sizes or zoom levels and treating the diff as meaningful.
- Using JPEG for screenshots and blurring text, edges, and code.
- Letting timestamps, cursor blinks, notifications, or random data ruin visual diffs.
- Forgetting that Wayland breaks familiar X11 screenshot tools.
- Sharing screenshots with secrets still visible in tabs, sidebars, URLs, or test accounts.
- Taking full-page captures of huge pages and ending up with unreadable evidence.

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `playwright` — Browser automation, DOM interaction, and web screenshots
- `image` — Post-capture format, cropping, compression, and export decisions
- `image-edit` — Annotation, cleanup, masking, and targeted edits after capture
- `documentation` — Turning screenshots into docs, guides, and release assets
- `video` — When a flow should be recorded instead of reduced to still images

## Feedback

- If useful: `clawhub star screenshot`
- Stay updated: `clawhub sync`
