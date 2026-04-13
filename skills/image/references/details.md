### 5. Treat metadata and orientation as real delivery concerns

- EXIF orientation can make an image look upright in one viewer and rotated in another after export.
- Public web assets usually should strip GPS and unnecessary camera metadata.
- Copyright, author, or provenance metadata may need to be preserved for editorial, legal, or archive use.
- Metadata decisions are part of the workflow, not an afterthought.
- Preserve filenames and output naming conventions when downstream systems map assets by exact names or SKU patterns.
- Do not strip metadata blindly if the workflow depends on authoring info, rights data, timestamps, or orientation.

### 6. Use practical budgets and delivery defaults

- For web work, use budgets as a forcing function, not as decoration.
- A useful default starting point is: hero image under 200 KB, content image under 100 KB, thumbnail under 30 KB, raster icon under 5 KB.
- Reserve layout space with explicit dimensions or aspect ratio when the image ships on the web.
- Do not lazy-load the primary hero or likely LCP image.
- A file that "looks fine locally" is not finished if it breaks CLS, LCP, or responsive delivery in the real page.
- A small file is not automatically good if detail, text legibility, product edges, or gradients collapse.
- If a platform will recompress the image anyway, leave enough headroom that the second compression does not destroy the result.

### 7. Validate against the actual destination

- Platform specs are not interchangeable: web hero, social preview, app store art, marketplace gallery, and print ad all have different constraints.
- Ecommerce images may need background consistency, edge cleanliness, square-safe crops, and zoom-friendly detail.
- Social images need safe composition because feeds crop previews differently across platforms.
- Print assets care about physical size, bleed, and color handling in ways web exports do not.
- If the asset ships on the web, remember the surrounding delivery too: width, height, alt text, and whether the image should carry text at all.
- If the asset will be uploaded to a third-party platform, check the post-upload result because many pipelines resize, strip profiles, flatten metadata, or recompress again.
- If the image carries meaning, validate its accessibility too: alt text strategy, text legibility, decorative vs informative role, and whether the meaning should have stayed in HTML or surrounding copy.

### 8. Batch safely and keep the original reversible

- Work from originals or clean masters, not from already-optimized outputs.
- Batch processing should apply consistent rules, but still spot-check representative files before touching the whole set.
- One wrong crop preset, color conversion, or lossy export can damage an entire batch quickly.
- Keep per-destination exports separated from masters so the next edit does not accidentally start from a degraded derivative.

## Specialized Cases Worth Loading

- Load `branding.md` when the asset is a logo, app icon, favicon, social avatar, badge, or reusable icon set.
- Load `screenshots.md` when the asset is a UI capture, bug report image, tutorial screenshot, release-note image, or device-framed marketing visual.
- Load `accessibility.md` when the image needs alt text, contains embedded text, carries chart/diagram meaning, or may be decorative instead of informative.

## What Good Looks Like

- The chosen format matches the content and the destination, not a blanket preference.
- The exported file keeps the right focal area, text legibility, transparency, and color intent.
- Metadata is preserved or stripped deliberately.
- The file size is efficient without obvious visual damage.
- The asset still works after the actual upload, embed, or platform preview step.
- The agent has not flattened a vector, layered, or RAW source earlier than necessary.
- The asset is still understandable in its real use context, not just visually attractive in isolation.

## Common Traps

- Saving transparent images as JPEG and silently losing the alpha channel.
- Using JPEG for screenshots or UI captures and turning sharp text into mush.
- Shipping a file that matches the requested dimensions but has the wrong aspect ratio or unsafe crop.
- Recompressing the same JPEG multiple times and blaming the tool instead of the workflow.
- Stripping metadata and accidentally breaking orientation, licensing context, or provenance needs.
- Forgetting sRGB and wondering why colors shift between editing tools, browsers, and marketplaces.
- Using SVG where the target platform strips it, rasterizes it badly, or blocks it entirely.
- Assuming AVIF or WebP is safe everywhere when some platforms, email clients, or upload pipelines still normalize back to JPEG or PNG.
- Embedding critical text into images where HTML or native UI text should have carried the meaning.
- Hitting the file-size budget but missing visual quality because the image was resized, cropped, or sharpened badly.
- Rasterizing a logo too early and then fighting blurry exports forever.
- Shipping a screenshot with secrets, personal data, or unstable timestamps still visible.
- Treating alt text, captions, or chart summaries as someone else's problem after the pixels look good.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `image-edit` — Masking, cleanup, inpainting, and targeted visual edits.
- `image-generation` — AI image generation and editing across current model providers.
- `photography` — Capture, color, and print-oriented photo workflows.
- `svg` — Vector graphics workflows when raster files are the wrong output.
- `ecommerce` — Marketplace and product-listing requirements that often constrain image delivery.

## Feedback

- If useful: `clawhub star image`
- Stay updated: `clawhub sync`
