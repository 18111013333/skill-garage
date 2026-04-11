---
name: audio-cog
description: "AI audio generation and text-to-speech powered by CellCog. Three voice providers (OpenAI, ElevenLabs, MiniMax), voice cloning, avatar voices, sound effects generation, music creation up to 10 minutes. Professional voiceover, narration, and audio production with AI."
metadata:
  openclaw:
    emoji: "🎵"
    os: [darwin, linux, windows]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---

# Audio Cog - AI Audio Generation Powered by CellCog

Create professional audio with AI — voiceovers, music, sound effects, and personalized avatar voices.

CellCog provides **three voice providers**, each with different strengths. Choose based on your needs:

| Scenario | Provider | Why |
|----------|----------|-----|
| Standard narration/voiceover | OpenAI | Best voice style control, consistent quality |
| Emotional/dramatic delivery | ElevenLabs | Richest emotional range, supports emotion tags |
| Cloned voice (avatar) | MiniMax | Only provider with voice cloning support |
| Character voice with specific accent | ElevenLabs | 100+ diverse pre-made voices |
| Fine pitch/speed/volume control | MiniMax | Granular voice settings |

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

## Voice Providers

### OpenAI (Default)

Best for standard narration, voiceovers, and single-speaker content with precise delivery control.

**Key strength**: Natural-language style instructions — describe the accent, tone, pacing, and emotion you want.

**8 built-in voices:**

| Voice | Gender | Characteristics |
|-------|--------|----------------|
| **cedar** | Male | Warm, resonant, authoritative, trustworthy |
| **marin** | Female | Bright, articulate, emotionally agile, professional |
| **ballad** | Male | Smooth, melodic, musical quality |
| **coral** | Female | Vibrant, lively, dynamic, spirited |
| **echo** | Male | Calm, measured, thoughtful, deliberate |
| **sage** | Female | Wise, contemplative, reflective |
| **shimmer** | Female | Soft, gentle, soothing, approachable |

## 详细文档

请参阅 [references/details.md](references/details.md)
