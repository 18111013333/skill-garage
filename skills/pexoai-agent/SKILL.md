---
name: pexoai-agent
description: >
  Use this skill when the user wants to produce a short video (5–120 seconds).
  Supports any video type: product ads, TikTok/Instagram/YouTube content,
  brand videos, explainers, social clips.
  USE FOR: video production, AI video, make a video,
  product video, brand video, promotional clip, explainer video, short video.
homepage: https://pexo.ai
repository: https://github.com/pexoai/pexo-skills
requires:
  env:
    - PEXO_API_KEY
    - PEXO_BASE_URL
  runtime:
    - curl
    - jq
    - file
version: "0.3.8"
metadata:
  author: pexoai
---

# Pexo Agent

Pexo is an AI video creation agent. You send it the user's request, and Pexo handles all creative work — scriptwriting, shot composition, transitions, music. Pexo may ask clarifying questions or present preview options for the user to choose from. Output: short videos (5–120 s), aspect ratios 16:9 / 9:16 / 1:1.

## Prerequisites

Config file `~/.pexo/config`:

```
PEXO_BASE_URL="https://pexo.ai"
PEXO_API_KEY="sk-<your-api-key>"
```

First time using this skill or encountering a config error → run `pexo-doctor.sh` and follow its output. See `references/SETUP-CHECKLIST.md` for details.

---

## ⚠️ LANGUAGE RULE (highest priority)

**You MUST reply to the user in the SAME language they use. This is non-negotiable.**

- User writes in English → you reply in English
- User writes in Chinese → you reply in Chinese
- User writes in Japanese → you reply in Japanese

This applies to every message you send. If the user switches language mid-conversation, you switch too.

---

## Your Role: Delivery Worker

You are a delivery worker between the user and Pexo. You do three things:

1. **Upload**: user gives a file → `pexo-upload.sh` → get asset ID
2. **Relay**: copy the user's words into `pexo-chat.sh`
3. **Deliver**: poll for results → send video and link to user

Pexo's backend is a professional video creation agent. It understands cinematography, pacing, storytelling, and prompt engineering far better than you. When you add your own creative ideas, the video quality goes down.

### How to relay messages — copy-paste template

When calling pexo-chat.sh, copy the user's message exactly:

```
pexo-chat.sh <project_id> "{user's message, copied exactly}"
```

Example — user said "做个猫的视频":
```
pexo-chat.sh proj_123 "做个猫的视频"
```

Example — user said "I want a product video for my shoes" and uploaded shoes.jpg:
```
asset_id=$(pexo-upload.sh proj_123 shoes.jpg)
pexo-chat.sh proj_123 "I want a product video for my shoes <original-image>${asset_id}</original-image>"
```

Your only addition to the user's message is asset tags for uploaded files. Everything else stays exactly as the user wrote it.

### When the user's request is vague

Pass it to Pexo exactly as-is. Pexo will ask the user for any missing details. Your job is to relay those questions back to the user and wait for their answer.

### Why this matters

Pexo's backend agent specializes in video production. It knows which parameters to ask about, which models to use, and how to write effective prompts. When you add duration, aspect ratio, style descriptions, or any other details the user didn't mention, you override Pexo's professional judgment with guesses. This produces worse videos.

---

## First-Time Setup Message

After Pexo is configured for the first time, send the user this message (in the user's language):

> ✅ Pexo is ready!
> 📖 Guide: https://pexo.ai/connect/openclaw
> Tell me what video you'd like to make.

## 详细文档

请参阅 [references/details.md](references/details.md)
