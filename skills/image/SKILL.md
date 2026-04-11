---
name: image-cog
description: "AI image generation and photo editing powered by CellCog. Text-to-image, image-to-image, consistent characters, product photography, reference-based generation, style transfer, sets of images, social media visuals. Professional image creation with multiple AI models."
metadata:
  openclaw:
    emoji: "🎨"
    os: [darwin, linux, windows]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---

# Image Cog - AI Image Generation Powered by CellCog

Create professional images with AI - from single images to consistent character sets to product photography.

---

## Prerequisites

This skill requires the `cellcog` skill for SDK setup and API calls.

```bash
clawhub install cellcog
```

**Read the cellcog skill first** for SDK setup. This skill shows you what's possible.

**OpenClaw agents (fire-and-forget — recommended for long tasks):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",  # OpenClaw only
    task_label="my-task",
    chat_mode="agent",  # See cellcog skill for all modes
)
```

**All other agents (blocks until done):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
)
```

See the **cellcog** mothership skill for complete SDK API reference — delivery modes, timeouts, file handling, and more.

---

## What Models Do We Use

| Model | Provider | Primary Use |
|-------|----------|-------------|
| **Nano Banana 2** (Gemini 3.1 Flash Image) | Google | Default image generation — photorealistic scenes, complex compositions, text rendering, multi-turn character consistency |
| **GPT Image 1.5** | OpenAI | Transparent background images — logos, stickers, product cutouts, overlay graphics |
| **Recraft** | Recraft AI | Scalable vector illustrations (SVG) and icon generation |

**Nano Banana 2** is the default model for all image generation. CellCog's agents intelligently route to other models when the task calls for it — for example, transparent PNGs are automatically handled by GPT Image 1.5, and vector/icon requests go to Recraft. If you'd prefer a specific model, just mention it in your prompt (e.g., *"use ChatGPT/OpenAI image generation"*).

## What Images You Can Create

### Single Image Creation

Generate any image from a text description:

- **Scenes**: "A cozy coffee shop interior with morning light streaming through windows"
- **Portraits**: "Professional headshot of a confident woman in business attire"
- **Products**: "Minimalist product shot of a white sneaker on a marble surface"
- **Abstract**: "Geometric abstract art in navy and gold"
- **Nature**: "Misty mountain landscape at sunrise with a lone hiker"

### Image Editing

Transform existing images:

- **Style Transfer**: "Transform this photo into a watercolor painting"
- **Background Removal**: "Remove the background and place on a clean white backdrop"
- **Enhancement**: "Enhance the colors and add dramatic lighting"

## 详细文档

请参阅 [references/details.md](references/details.md)
