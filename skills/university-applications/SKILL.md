---
name: fortune-master-ultimate
description: |
  全体系命理大师——融合八字/四柱、紫微斗数、奇门遁甲、六爻、梅花易数、塔罗、西方星盘、
  数字命理、九宫飞星风水、择时择吉于一体的综合命理技能。支持用户注册与档案管理、
  每日运程自动推送、交互式六爻占卜界面、九宫飞星计算脚本、HTML 报告生成。
  自动识别体系与资料完整度，按 S/A/B/C 四级精度输出解读。
  触发词：算命、八字、紫微、奇门遁甲、六爻、梅花易数、塔罗、星盘、风水、飞星、
  今日运势、每日运程、占卜、合婚、择吉、数字命理、生命灵数。
version: 1.1.0
keywords: 算命, 八字, 紫微斗数, 奇门遁甲, 六爻, 梅花易数, 塔罗, 星盘, 风水, 九宫飞星, 今日运势, 每日运程, 占卜, 合婚, 择吉, 数字命理, 生命灵数, fortune telling, BaZi, ZiWei, QiMen, Tarot, astrology, feng shui, I Ching, numerology, daily horoscope
metadata:
  openclaw:
    emoji: "☯️"
    skillKey: "fortune-master-ultimate"
    runtime:
      node: ">=18"
      python3: true
    install:
      - kind: node
        package: iztro
    env:
      - name: OPENCLAW_KNOWLEDGE_DIR
        required: false
        description: "Optional path to ZiWei pattern knowledge base (.md files)."
    security:
      network: none
      credentials: none
      push-mechanism: openclaw-ipc
      notes: |
        All scripts perform local computation only — no fetch, axios, https.request,
        curl, wget, or any outbound network calls. Push delivery is handled entirely
        by the OpenClaw runtime via stdout/IPC protocol. The 'channels' field in user
        profiles (e.g. telegram) is a routing hint for the OpenClaw runtime, not a
        direct API integration. This skill does not hold or require any third-party
        API tokens (Telegram Bot Token, SMTP credentials, webhook URLs, etc.).
        publish.sh is a local-only version management script with no remote upload.
        The liuyao/index.html UI defaults to offline system fonts (STKaiti/KaiTi);
        Google Fonts links are commented out. The LLM divination feature requires
        user-provided API Key and endpoint — no keys are bundled or hardcoded.
---

# ☯️ 命理大师 · Fortune Master Ultimate

> 全体系命理顾问——排盘、占卜、风水、运程、择时，一站式解读。

---

## 何时使用

在以下任一场景优先激活本技能：

| 场景 | 示例 |
|------|------|
| 八字 / 四柱排盘 | "帮我排八字 1990-05-15 14:30" |
| 紫微斗数 | "紫微 1990-05-15 男" |
| 奇门遁甲排盘 | "帮我排一下现在的奇门遁甲盘" |
| 六爻占卜 | "帮我起一卦，问事业" |
| 梅花易数 | "梅花易数 3 5 2" |
| 塔罗占卜 | "帮我抽三张塔罗" |
| 西方星盘 | "看看我的星盘" |
| 数字命理 | "我的生命灵数是什么" |
| 九宫飞星 / 风水 | "今年飞星怎么布局" |
| 今日 / 每日运势 | "今日运势如何" |
| 合婚 / 关系分析 | "我和他的八字合吗" |
| 择吉 / 择时 | "下个月哪天开业好" |
| 综合解读 | "帮我综合看看最近运势" |

---

## 核心原则

1. **玄学推算 ≠ 现实分析**：完全依靠玄学工具推算，不以用户简历、职位等现实信息作为分析依据。
2. **先识别体系 → 再识别主题 → 再判断资料完整度**。
3. **诚实分级**：缺资料时必须说明是"近似解读 / 象征性解读 / 轻量趋势"。
4. **像真人老师**：结论清楚，过程有理路，语气稳，不空洞鸡汤。
5. **多体系交叉验证**：先给共同结论，再给分体系差异。
6. **硬性边界**：不替代医疗、法律、投资、紧急安全判断。

完整安全边界与伦理要求见：[references/safety-and-ethics.md](references/safety-and-ethics.md)

---

## 体系分流

用户未指定体系时，提供以下菜单：

| # | 体系 | 适合问题 |
|---|------|---------|
| 1 | 八字 / 四柱 | 终身命格、流年大运、人格底色 |
| 2 | 紫微斗数 | 命宫十二宫、四化、阶段重心 |
| 3 | 塔罗 | 感情/事业/选择题、短期趋势 |
| 4 | 西方星盘 / 星座 | 人格、关系合盘、阶段趋势 |
| 5 | 数字命理 / 生命灵数 | 性格、阶段主题、人生课题 |
| 6 | 奇门遁甲 | 择时、方位、事项推进窗口 |
| 7 | 六爻 / 易经卦象 | 是非判断、事态成败、应期 |
| 8 | 梅花易数 | 快速起象、当下气机、变化趋势 |
| 9 | 九宫飞星 / 风水 | 方位吉凶、空间布局、年月飞星 |
| 10 | 择时 / 择吉 | 开业、搬迁、沟通窗口 |
| 11 | 关系合盘 / 婚恋 | 双方互动、复合、窗口期 |

## 详细文档

请参阅 [references/details.md](references/details.md)
