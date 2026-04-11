- `--reference-images`: Comma-separated image URLs for context/character consistency (**Nano Banana only**)
- `--mode`: Midjourney speed: `turbo` (default, ~20-40s), `fast` (~30-60s), `relax` (free but slow)

**exec timeout**: Set at least **120 seconds** for Midjourney and Nano Banana; 30 seconds is sufficient for Flux Schnell.

---

## ⚡ Midjourney Workflow (Sync Mode — No --async)

Always use sync mode (no `--async`). The script waits internally until complete.

```bash
node {baseDir}/generate.js \
  --model midjourney \
  --prompt "<enhanced prompt>" \
  --aspect-ratio 16:9
```

### Understanding Midjourney Output

```json
{
  "success": true,
  "model": "midjourney",
  "jobId": "xxxxxxxx-...",
  "imageUrl": "https://cdn.legnext.ai/temp/....png",
  "imageUrls": [
    "https://cdn.legnext.ai/mj/xxxx_0.png",
    "https://cdn.legnext.ai/mj/xxxx_1.png",
    "https://cdn.legnext.ai/mj/xxxx_2.png",
    "https://cdn.legnext.ai/mj/xxxx_3.png"
  ]
}
```

**CRITICAL — image field meanings:**

| Field | What it is | When to use |
|---|---|---|
| `imageUrl` | A **2×2 grid composite** of all 4 images | Send as **preview** so user can see all options |
| `imageUrls[0]` | Image 1 (top-left) | Send when user wants image 1 |
| `imageUrls[1]` | Image 2 (top-right) | Send when user wants image 2 |
| `imageUrls[2]` | Image 3 (bottom-left) | Send when user wants image 3 |
| `imageUrls[3]` | Image 4 (bottom-right) | Send when user wants image 4 |

**"放大第N张" / "要第N张" / "give me image N" = send `imageUrls[N-1]` directly. Do NOT call generate.js again.**

### Midjourney Interaction Flow

**After generation:**
> 🎨 生成完成！这是 4 张图的预览：
> [预览图](imageUrl)
> 你喜欢哪一张？回复 1、2、3 或 4，我直接发给你高清单图。

**When user picks image N:**
> 这是第 N 张的单独高清图：
> [图片 N](imageUrls[N-1])

---

## 🤖 Nano Banana (Gemini) Workflow

Use for storyboards, character series, and any context-dependent multi-image generation.

### Single image (no reference)
```bash
node {baseDir}/generate.js \
  --model nano-banana \
  --prompt "<detailed scene description>" \
  --aspect-ratio 16:9
```

### With reference images (character/scene consistency)
```bash
node {baseDir}/generate.js \
  --model nano-banana \
  --prompt "<scene description, referencing the character/style from the reference images>" \
  --aspect-ratio 16:9 \
  --reference-images "https://url-of-previous-image-1.png,https://url-of-previous-image-2.png"
```

**How to build a storyboard series:**

1. Generate the **first frame** without reference images (establishes the character/scene)
2. Use the first frame's URL as `--reference-images` for the **second frame**
3. For subsequent frames, use the most recent 1-3 images as references to maintain consistency
4. Keep the character description consistent across all prompts

**Example storyboard workflow:**
```
Frame 1: node generate.js --model nano-banana --prompt "A young girl with red hair, wearing a blue dress, sitting under a magical treehouse in an enchanted forest, warm golden light, storybook illustration style" --aspect-ratio 16:9

Frame 2: node generate.js --model nano-banana --prompt "The same red-haired girl in blue dress climbing the rope ladder up to the treehouse, excited expression, enchanted forest background, same storybook illustration style" --aspect-ratio 16:9 --reference-images "<frame1_url>"

Frame 3: node generate.js --model nano-banana --prompt "Inside the magical treehouse, the red-haired girl discovers a glowing book on a wooden shelf, wonder on her face, warm candlelight, same storybook illustration style" --aspect-ratio 16:9 --reference-images "<frame1_url>,<frame2_url>"
```

### Nano Banana Output
```json
{
  "success": true,
  "model": "nano-banana",
  "images": ["https://v3b.fal.media/files/...png"],
  "imageUrl": "https://v3b.fal.media/files/...png"
}
```
Send `imageUrl` directly to the user (no grid, single image).

---

## Other Models

### Flux Pro / Dev / Schnell
Best for photorealistic standalone images. Output format same as Nano Banana (single `imageUrl`).

```bash
node {baseDir}/generate.js --model flux-pro --prompt "<prompt>" --aspect-ratio 16:9
```

### Ideogram v3
Best for images containing text (logos, posters, signs).

```bash
node {baseDir}/generate.js --model ideogram --prompt "A motivational poster with text 'DREAM BIG' in bold typography, sunset gradient background" --aspect-ratio 3:4
```

### Recraft v3
Best for vector-style, icons, flat design.

```bash
node {baseDir}/generate.js --model recraft --prompt "A minimal flat design app icon, blue gradient, abstract geometric shape" --aspect-ratio 1:1
```

---

## Prompt Enhancement Tips

**For Midjourney**: Add `cinematic lighting`, `ultra detailed`, `--v 7`, `--style raw`. Legnext supports all MJ parameters.

**For Nano Banana**: Use natural language descriptions. Describe the character consistently across frames (hair color, clothing, expression). Mention "same style as reference" or "consistent with previous frame".

**For Flux**: Add `masterpiece`, `highly detailed`, `sharp focus`, `professional photography`, `8k`.

**For Ideogram**: Be explicit about text content, font style, layout, and color scheme.

**For Recraft**: Specify `vector illustration`, `flat design`, `icon style`, `minimal`.

---

## Example Conversations

**User**: "帮我画一只赛博朋克猫"
→ Single artistic image → **Midjourney**
→ Tell user "🎨 正在用 Midjourney 生成，约 30 秒..."
→ Send grid preview, ask which one they want

**User**: "帮我生成一套分镜图，讲述一个女孩在魔法森林的冒险"
→ Multiple frames with story continuity → **Nano Banana**
→ Tell user "🎨 这类有上下文关联的分镜图用 Gemini 生成，能保持角色一致性..."
→ Generate frame by frame, using previous frames as reference images

**User**: "要第2张" / "放大第2张" (after Midjourney generation)
→ Send `imageUrls[1]` directly. No need to call generate.js again.

**User**: "做一个 App 图标，蓝色系扁平风格"
→ Vector/icon → **Recraft**

**User**: "生成一张带有'欢迎光临'文字的门牌图"
→ Text in image → **Ideogram**

**User**: "快速生成个草稿看看效果"
→ Speed priority → **Flux Schnell** (<2s)

**User**: "生成一张产品海报，白色背景，一瓶香水"
→ Photorealistic product → **Flux Pro**

---

## Environment Variables

| Variable | Description |
|---|---|
| `FAL_KEY` | fal.ai API key (for Flux, Nano Banana, Ideogram, Recraft) |
| `LEGNEXT_KEY` | Legnext.ai API key (for Midjourney) |
