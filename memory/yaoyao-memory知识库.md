# Yaoyao Memory 知识库

> 更新时间：2026年4月13日
> 来源：https://llmbase.ai/openclaw/yaoyao-memory-v2/

---

## 一、系统概述

**Yaoyao Memory V2** 是一个六层架构记忆系统，让 AI 跨会话保持上下文、沉淀知识、持续进化。

### 核心特性
- ✅ **本地存储** - SQLite 数据库存储在 ~/.openclaw/workspace/memory/
- ✅ **全文搜索** - FTS5 全文搜索引擎
- ✅ **模块化** - 核心+可选模块，按需安装
- ✅ **自管理** - 自动检测和修复常见问题
- ✅ **隐私保护** - 敏感信息不记录，本地数据由用户控制

### 版本信息
| 项目 | 内容 |
|------|------|
| **版本** | v3.9.28 |
| **更新时间** | 2026年4月12日 |
| **下载量** | 176 |
| **安装命令** | `clawhub install yaoyao-memory-v2` |

---

## 二、架构设计

### 一句话总结
> 鸽子王是楼，yaoyao-memory是仓库，llm-memory-integration是管理员，都在2楼协同工作。

### 架构隐喻
| 组件 | 角色 | 说明 |
|------|------|------|
| **鸽子王** | 楼（基础设施） | OpenClaw 核心系统 |
| **yaoyao-memory** | 仓库（数据存储） | 记忆存储系统 |
| **llm-memory-integration** | 管理员（协调调度） | LLM + 向量集成方案 |

---

## 三、模块说明

### 必装模块
| 模块 | 说明 |
|------|------|
| core | 核心功能 |
| security | 安全检测 |
| health_check | 健康检查 |

### 可选模块
| 模块 | 说明 |
|------|------|
| cloud_backup | 云端备份 |
| stats | 统计分析 |
| summary | 摘要生成 |
| psychology | 心理分析 |
| mcp | MCP 协议支持 |

---

## 四、权限说明

| 权限 | 用途 |
|------|------|
| 本地文件读写 | ~/.openclaw/workspace/memory/ |
| SQLite 数据库 | ~/.openclaw/memory-tdai/vectors.db |
| 云端同步 | 可选，需要时配置 |

**不包含**：网络广播、系统级持久化、其他 skill 目录

---

## 五、首次使用

安装后首次对话时，对我说「开始使用记忆系统」开始配置。

---

# LLM Memory Integration 知识库

> 更新时间：2026年4月13日
> 来源：https://llmbase.ai/openclaw/llm-memory-integration/

---

## 一、系统概述

**LLM Memory Integration** 是 LLM + 向量模型集成方案，支持任意 LLM + Embedding 模型，用户自行配置。

### 核心特性
- ✅ **混合检索** - 向量 + FTS + LLM
- ✅ **智能路由** - fast/balanced/full 模式
- ✅ **渐进式启用** - 分阶段启用功能
- ✅ **用户画像自动更新** - 自动学习用户偏好

---

## 二、核心能力

| 能力 | 功能 | 用户配置 |
|------|------|----------|
| 向量搜索 | 语义相似度匹配 | 用户自选 Embedding 模型 |
| LLM 分析 | 查询扩展、重排序、解释、摘要 | 用户自选 LLM 模型 |
| FTS 搜索 | 关键词快速召回 | SQLite FTS5（内置） |
| 混合检索 | RRF 融合排序 | 向量 + FTS + LLM |
| 智能路由 | 复杂度分析 | fast/balanced/full 模式 |
| 查询理解 | 意图识别 | search/config/explain/compare |
| 反馈学习 | 点击记录 | 优化排序权重 |

---

## 三、渐进式启用

### 启用阶段
| 阶段 | 名称 | 模块 | 状态 |
|------|------|------|------|
| P0 | 核心优化 | router + weights + rrf + dedup | ✅ 启用 |
| P1 | 查询增强 | understand + rewriter | ✅ 启用 |
| P2 | 学习优化 | feedback + history | ✅ 启用 |
| P3 | 结果增强 | explainer + summarizer | ✅ 启用 |

### 优化修复
| 问题 | 修复方案 | 效果 |
|------|----------|------|
| 语义匹配弱 | 放宽距离阈值 0.8，增加 top_k 到 20 | 召回率提升 90% |
| LLM 扩展不准 | 优化 prompt，增加 temperature | 扩展词更相关 |
| 同义词不足 | 扩展词典，增加语义扩展 | 覆盖更多表达 |

---

## 四、性能指标

| 模式 | 目标 | 实测 | 状态 |
|------|------|------|------|
| 缓存命中 | < 10ms | 5ms | ✅ 优秀 |
| 快速模式 | < 2s | 0.05-1.2s | ✅ 优秀 |
| 平衡模式 | < 5s | 4.5s | ✅ 达标 |
| 完整模式 | < 15s | 9-11s | ✅ 达标 |
| 准确率 | > 80% | 90% | ✅ 优秀 |

---

## 五、模型配置

### 支持的模型提供商
| 提供商 | LLM | Embedding |
|--------|-----|-----------|
| OpenAI | GPT-4, GPT-3.5 | text-embedding-3-* |
| Azure OpenAI | GPT-4 | text-embedding-ada-002 |
| Anthropic | Claude 3 | - |
| 华为云 | GLM5 | - |
| Gitee AI | - | Qwen3-Embedding-8B |
| 本地模型 | Ollama | 本地 Embedding |

### 默认配置
| 组件 | 默认值 | 说明 |
|------|--------|------|
| 向量模型 | 用户配置 | 支持 OpenAI、Gitee AI 等 |
| LLM | 用户配置 | 支持 OpenAI、Claude、GLM 等 |
| 数据库 | SQLite + vec0 + FTS5 | 内置 |
| 缓存 | 增量缓存 + 压缩存储 | 内置 |
| RRF 参数 | k=60 | 可调 |
| 向量搜索 | top_k=20, max_distance=0.8 | 可调 |
| LLM 扩展 | max_tokens=150, temperature=0.5 | 可调 |

---

## 六、核心模块

| 模块 | 文件 | 功能 |
|------|------|------|
| 查询理解 | core/understand.py | 意图识别 + 实体提取 |
| 查询改写 | core/rewriter.py | 拼写纠正 + 同义词扩展 + 语义扩展 |
| 语言检测 | core/langdetect.py | 多语言支持 |
| 智能路由 | core/router.py | 根据复杂度选择模式 |
| 动态权重 | core/weights.py | 向量/FTS 权重自适应 |
| RRF 融合 | core/rrf.py | 混合检索排序算法 |
| 语义去重 | core/dedup.py | 结果去重增强 |
| 反馈学习 | core/feedback.py | 记录用户点击优化排序 |
| 查询历史 | core/history.py | 高频查询缓存 |
| 结果解释 | core/explainer.py | LLM 生成结果解释 |
| 结果摘要 | core/summarizer.py | LLM 生成结果摘要 |

---

## 七、脚本列表

| 脚本 | 功能 |
|------|------|
| search.py | 统一搜索入口（完整集成版） |
| one_click_setup.py | 一键配置 |
| progressive_setup.py | 渐进式启用管理 |
| smart_memory_update.py | 智能更新 |
| vsearch | 搜索包装脚本 |
| llm-analyze | 分析包装脚本 |
| vector_coverage_monitor.py | 向量覆盖率监控 + 自动修复 |
| smart_memory_upgrade.py | 智能记忆升级 |
| auto_update_persona.py | 用户画像自动更新 |
| vector_system_optimizer.py | 向量系统优化 |

---

## 八、安全说明

### 数据操作声明
| 操作 | 文件 | 默认状态 |
|------|------|----------|
| 向量搜索 | vectors.db（读/写） | ✅ 启用 |
| 记忆管理 | MEMORY.md（读） | ✅ 启用 |
| 用户画像更新 | persona.md（读/写） | ❌ 禁用 |
| 日志记录 | logs/*（写） | ✅ 启用 |
| SQLite 扩展加载 | vec0.so（加载） | ⚠️ 需确认 |

### 配置文件一致性
- config/llm_config.json - 无硬编码 API 密钥（仅占位符）
- config/persona_update.json - auto_update: false（与文档一致）
- config/unified_config.json - auto_update: false（与文档一致）
- require_confirmation: true（更新前需确认）
- backup_before_update: true（更新前备份）

---

## 九、与我们的系统对比

| 项目 | yaoyao-memory | 我们的系统 |
|------|---------------|------------|
| 架构 | 六层渐进式 | 星空鸽子王 V2.9.0 |
| 存储 | SQLite + FTS5 | MEMORY.md + memory/*.md |
| 向量搜索 | 支持 | 支持（llm-memory-integration） |
| 智能路由 | 支持 | 支持 |
| 用户画像 | 支持 | 支持（USER.md） |
| 健康检查 | 支持 | 支持（定时任务） |

---

*本知识库将持续更新，跟踪 yaoyao-memory 和 llm-memory-integration 最新动态。*
