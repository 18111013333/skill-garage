---
name: image-gen
description: Generate images using multiple AI models — Midjourney (via Legnext.ai), Flux, Nano Banana Pro (Gemini), Ideogram, Recraft, and more via fal.ai. Intelligently routes to the best model based on use case.
homepage: https://legnext.ai
metadata: {"openclaw":{"emoji":"🎨","primaryEnv":"FAL_KEY","requires":{"env":["FAL_KEY","LEGNEXT_KEY"]},"install":[{"id":"node","kind":"node","package":"@fal-ai/client","label":"Install fal.ai client (npm)"}]}}
---

# Image Generation Skill

This skill generates images using the best AI model for each use case. **Model selection is the most important decision** — read the dispatch logic carefully before generating.

---

## 🧠 Intelligent Dispatch Logic

**Always select the model based on the user's actual need, not just the request surface.**

### Decision Tree

```
Does the request involve MULTIPLE images that share characters, scenes, or story continuity?
  ├─ YES → Use NANO BANANA (Gemini)
  │         Reason: Gemini understands context holistically; supports reference_images
  │         for character/scene consistency across a series (storyboard, comic, sequence)
  │
  └─ NO → Is it a SINGLE standalone image?
            ├─ Artistic / cinematic / painterly / highly detailed?
            │   → Use MIDJOURNEY
            │
            ├─ Photorealistic / portrait / product photo?
            │   → Use FLUX PRO
            │
            ├─ Contains TEXT (logo, poster, sign, infographic)?
            │   → Use IDEOGRAM
            │
            ├─ Vector / icon / flat design / brand asset?
            │   → Use RECRAFT
            │
            ├─ Quick draft / fast iteration (speed priority)?
            │   → Use FLUX SCHNELL (<2s)
            │
            └─ General purpose / balanced?
                → Use FLUX DEV
```

### Model Capability Matrix

| Model | ID | Artistic | Photorealism | Text | Context Continuity | Speed | Cost |
|---|---|---|---|---|---|---|---|
| **Midjourney** | `midjourney` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ❌ (no context) | ~30s | ~$0.05 |
| **Nano Banana Pro** | `nano-banana` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ~20s | $0.15 |
| **Flux Pro** | `flux-pro` | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ | ~5s | ~$0.05 |
| **Flux Dev** | `flux-dev` | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ❌ | ~8s | ~$0.03 |
| **Flux Schnell** | `flux-schnell` | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ❌ | <2s | ~$0.003 |
| **Ideogram v3** | `ideogram` | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ~10s | ~$0.08 |
| **Recraft v3** | `recraft` | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ❌ | ~8s | ~$0.04 |
| **SDXL Lightning** | `sdxl` | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ❌ | ~3s | ~$0.01 |

### When to Use Nano Banana (Critical)

Use **Nano Banana** whenever the user's request involves:
- **Storyboard / 分镜图**: Multiple frames that tell a story with the same characters
- **Comic strip / 漫画**: Sequential panels with consistent characters
- **Character series**: Multiple images of the same person/character in different poses or scenes
- **Scene continuation**: "Now show the same girl in the forest" (referencing a previous image)
- **Style consistency**: A set of images that must share the same visual style/world

Nano Banana uses Google's Gemini 3 Pro multimodal architecture, which understands context holistically rather than keyword-matching. It supports up to 14 reference images for maintaining character and scene consistency.

---

## How to Use This Skill

1. **Analyze the request**: Is it a single image or a series? Does it need context continuity?
2. **Select model**: Use the decision tree above.
3. **Enhance the prompt**: Add style, lighting, and quality descriptors appropriate for the model.
4. **Inform the user**: Tell them which model you're using and why, and that generation has started.
5. **Run the script**: Use `exec` tool with sufficient timeout.
6. **Deliver the result**: Send image URL(s) to the user.

---

## Calling the Generation Script

```bash
node {baseDir}/generate.js \
  --model <model_id> \
  --prompt "<enhanced prompt>" \
  [--aspect-ratio <ratio>] \
  [--num-images <1-4>] \
  [--negative-prompt "<negative prompt>"] \
  [--reference-images "<url1,url2,...>"]
```

**Parameters:**
- `--model`: One of `midjourney`, `flux-pro`, `flux-dev`, `flux-schnell`, `sdxl`, `nano-banana`, `ideogram`, `recraft`
- `--prompt`: The image generation prompt (required)
- `--aspect-ratio`: e.g. `16:9`, `1:1`, `9:16`, `4:3`, `3:4` (default: `1:1`)
- `--num-images`: 1-4 (default: `1`; Midjourney always returns 4 regardless)
- `--negative-prompt`: Things to avoid (not supported by Midjourney)

## 详细文档

请参阅 [references/details.md](references/details.md)
