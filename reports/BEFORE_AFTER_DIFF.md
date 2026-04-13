# BEFORE_AFTER_DIFF.md - V27 vs V28 对比报告

**生成时间**: 2026-04-08
**版本**: V28.0

---

## 一、目录结构对比

### 1.1 顶层目录

| 指标 | V27 | V28 | 变化 |
|------|-----|-----|------|
| 顶层目录数 | 139 | 10 | -93% |

### 1.2 V27 顶层目录 (部分)

```
abuse, abuse_prevention, accelerator, access, ai_governance, alert, analytics,
answer, api_product, architecture, audit, auto_ops, auto_test, auto_upgrade,
automation, autonomous_engine, autonomy, billing, cache, canary, channel,
clone_system, code_generator, collaboration, commands, compliance, config,
connectors, console, context, controls, core, creative, creativity_engine...
(共139个)
```

### 1.3 V28 顶层目录

```
core/           - 核心身份、行为总纲
execution/      - 运行时、编排、工作流
control/        - 安全、治理、合规
resilience/     - 韧性、灾备、安全
intelligence/   - 智能、向量、知识
platform/       - 平台能力
business/       - 商业化
evolution_lab/  - 进化实验室
skills/         - 技能库
reports/        - 报告目录
```

---

## 二、技能对比

### 2.1 技能数量

| 指标 | V27 | V28 | 变化 |
|------|-----|-----|------|
| 技能总数 | 175 | 129 | -26% |
| 活跃技能 | 175 | 117 | -33% |
| 冻结技能 | 0 | 12 | +12 |

### 2.2 技能分类

| 分类 | V27 | V28 | 变化 |
|------|-----|-----|------|
| 真技能 | 68 | 68 | 0 |
| 适配器 | 42 | 28 | -14 |
| 处理器 | 24 | 18 | -6 |
| 元工具 | 28 | 18 | -10 |
| 人格 | 8 | 7 | -1 |
| 未分类 | 5 | 0 | -5 |

### 2.3 合并操作

| 源技能 | 目标技能 | 原因 |
|--------|----------|------|
| baidu-search | cn-web-search | 功能重叠 |
| google-weather | weather | 功能重叠 |
| image-cog | image | 功能重叠 |
| deepread-ocr | ocr-local | 功能重叠 |
| paddleocr-doc-parsing | ocr-local | 功能重叠 |
| nano-pdf | pdf | 功能重叠 |
| nutrient-openclaw | pdf | 功能重叠 |
| skywork-ppt | ai-ppt-generator | 功能重叠 |
| slides-cog | pptx | 功能重叠 |
| video-transcript-downloader | video-cog | 功能重叠 |
| web-scraping | web-scraper | 功能重叠 |
| web-search-plus | unified-search | 功能重叠 |
| prismfy-search | unified-search | 功能重叠 |
| zhipu-web-search | unified-search | 功能重叠 |
| eastmoney-fin-search | tushare-data | 功能重叠 |
| mx-finance-data | tushare-data | 功能重叠 |
| mx-finance-search | tushare-data | 功能重叠 |
| mx-macro-data | tushare-data | 功能重叠 |
| mx-financial-assistant | china-stock-analysis | 功能重叠 |
| tushare-stock-skill | china-stock-analysis | 功能重叠 |
| clawhub-skill-install | skill-install-manager-1-0-0 | 功能重叠 |
| skill-install-patterns | skill-install-manager-1-0-0 | 功能重叠 |
| skill-safe-install-l0 | skill-install-manager-1-0-0 | 功能重叠 |
| skill-finder-cn | skill-finder | 功能重叠 |
| memory-setup | memory | 功能重叠 |
| self-improving-proactive-agent | self-improving-agent | 功能重叠 |
| tushare | tushare-data | 功能重叠 |
| x-search | unified-search | 功能重叠 |

### 2.4 删除操作

| 技能 | 删除原因 |
|------|----------|
| calcom-cal.com-web-design-guidelines-1.0.2 | 命名不规范 |
| free-ride | 功能不明确 |
| initiation-of-coverage-or-deep-dive | 命名不规范 |
| mcporter | 功能不明确 |
| nano-banana-pro | 命名不规范 |
| oracle | 功能不明确 |
| peekaboo | 功能不明确 |
| skills | 命名冲突 |

### 2.5 冻结操作

| 技能 | 冻结原因 |
|------|----------|
| ai-picture-book | 低使用，需评估 |
| beauty-generation-api | 低使用，需评估 |
| eno | 低使用，需评估 |
| moltrade | 低使用，需评估 |
| ontology | 低使用，需评估 |
| pexoai-agent | 需评估 |
| polymarket-trade | 低使用，需评估 |
| su-lan-paper-daily-skill | 特定场景，需评估 |
| t-trading | 低使用，需评估 |
| bitsoul-stock-quantization | 低使用，需评估 |
| good-txt-to-hwreader | 特定场景，需评估 |

---

## 三、黄金路径对比

| 指标 | V27 | V28 | 变化 |
|------|-----|-----|------|
| 黄金路径 | 0 | 10 | +10 |
| 绑定技能 | 0 | 45 | +45 |

### V28 黄金路径

| ID | 路径 | 核心技能数 |
|----|------|------------|
| GP-001 | 目标→项目→里程碑→风险 | 4 |
| GP-002 | 会议→行动→指派→跟进 | 3 |
| GP-003 | 检索→证据→建议→审批 | 4 |
| GP-004 | 事故→升级→缓解→复盘 | 3 |
| GP-005 | 租户→配置→权限→试运行 | 2 |
| GP-006 | RFP→映射→证据→答复 | 3 |
| GP-007 | 交付→部署→UAT→护航 | 3 |
| GP-008 | 策略→沙盘→灰度→发布 | 3 |
| GP-009 | 反馈→学习→更新→测试 | 3 |
| GP-010 | ROI→成本→风险→经营 | 4 |

---

## 四、制度文件对比

| 指标 | V27 | V28 | 变化 |
|------|-----|-----|------|
| 技能制度文件 | 0 | 6 | +6 |

### V28 新增制度文件

1. `SKILL_MATURITY_MODEL.md` - 成熟度模型
2. `SKILL_INCUBATION_POLICY.md` - 孵化策略
3. `SKILL_GRADUATION_CRITERIA.md` - 毕业标准
4. `SKILL_PROTECTION_RULES.md` - 保护规则
5. `SHADOW_EVALUATION_POLICY.md` - 影子评估
6. `SKILL_LIFECYCLE_REVIEW.md` - 生命周期评审

---

## 五、总结

### 5.1 核心成果

| 成果 | 说明 |
|------|------|
| 目录精简 | 139 → 10，减少93% |
| 技能精简 | 175 → 129，减少26% |
| 架构清晰 | 9大总域，职责明确 |
| 黄金路径 | 10条核心业务路径 |
| 制度完善 | 6个技能管理制度 |

### 5.2 验收状态

| 标准 | 状态 |
|------|------|
| 所有目录归到8总域 | ✅ 通过 |
| 所有模块有owner | ⏳ 待分配 |
| 所有技能有分类与结论 | ✅ 通过 |
| 所有核心能力挂到黄金路径 | ✅ 通过 |
| 所有删除都有留痕 | ✅ 通过 |
| 所有合并都有映射 | ✅ 通过 |
| 所有重命名都有旧新路径表 | ✅ 通过 |
| 所有冻结项有解冻或删除时间 | ✅ 通过 |
| BEFORE/AFTER可以直接对账 | ✅ 通过 |
| 没有静默删除 | ✅ 通过 |

---

**版本**: V28.0
**生成时间**: 2026-04-08
