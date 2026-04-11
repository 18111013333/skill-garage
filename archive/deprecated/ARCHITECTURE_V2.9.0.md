<!--
历史兼容 / 归档说明
本文档已归档，运行以 core/ARCHITECTURE.md 为准
归档时间: 2026-04-11 17:19:21
-->
# 终极精简架构 V2.9.0

## 设计原则

1. **目录极简** - 从36个目录精简到6个
2. **文件聚合** - 同类文件合并，减少碎片
3. **层级清晰** - L1-L6职责明确，无交叉
4. **按需加载** - 启动只加载L1，其他按需

---

## 目录结构 (精简后)

```
workspace/
├── core/                    # L1-L2: 核心认知 + 记忆
│   ├── AGENTS.md           # 工作空间规则
│   ├── SOUL.md             # 身份定义
│   ├── USER.md             # 用户信息
│   ├── TOOLS.md            # 工具规则
│   ├── IDENTITY.md         # 身份标识
│   ├── MEMORY.md           # 长期记忆
│   ├── CONFIG.json         # 核心配置
│   └── guide/              # 引导模块
│
├── engine/                  # L3-L4: 编排 + 执行
│   ├── router.py           # 技能路由器
│   ├── workflows/          # 工作流包
│   ├── executors/          # 执行器
│   └── validators/         # 验证器
│
├── skills/                  # L4: 技能库 (151个)
│   ├── _core/              # 核心技能 (始终可用)
│   ├── _document/          # 文档类
│   ├── _data/              # 数据类
│   ├── _search/            # 搜索类
│   ├── _image/             # 图片类
│   ├── _code/              # 代码类
│   ├── _content/           # 内容类
│   ├── _social/            # 社交类
│   ├── _business/          # 商业类
│   └── ...                 # 其他技能
│
├── guard/                   # L5: 安全治理
│   ├── security.py         # 安全检查
│   ├── permissions.py      # 权限管理
│   └── audit.py            # 审计日志
│
├── infra/                   # L6: 基础设施
│   ├── paths.py            # 路径解析
│   ├── plugins.py          # 插件标准
│   ├── performance.py      # 性能模块
│   └── registry.py         # 技能注册表
│
└── memory/                  # 日记目录
    ├── 2026-04-11.md
    └── ...
```

---

## 六层架构 (精简版)

### L1: 核心认知层 (立即加载, Token: 3000)

**职责**: 身份、规则、引导

**文件**:
- `core/AGENTS.md` - 工作空间规则
- `core/SOUL.md` - 身份定义
- `core/USER.md` - 用户信息
- `core/TOOLS.md` - 工具规则
- `core/IDENTITY.md` - 身份标识
- `core/guide/` - 引导模块

**Token预算**: 3000 (从5000压缩)

**加载**: 会话启动时立即加载

---

### L2: 记忆上下文层 (按需加载, Token: 2000)

**职责**: 记忆存储、检索

**文件**:
- `core/MEMORY.md` - 长期记忆
- `core/CONFIG.json` - 核心配置
- `memory/YYYY-MM-DD.md` - 日记

**技能**: memory, obsidian, find-skills

**触发词**: "记得"、"上次"、"回忆"

---

### L3: 任务编排层 (按需加载, Token: 1500)

**职责**: 路由、工作流、调度

**文件**:
- `engine/router.py` - 技能路由器
- `engine/workflows/` - 工作流包

**技能**: planning-with-files, today-task, post-job, cron, proactivity, self-improving-agent, command-center, command-hook

**触发词**: "工作流"、"定时"、"计划"

---

### L4: 能力执行层 (按类别加载, Token: 1500)

**职责**: 技能执行、结果验证

**文件**:
- `engine/executors/` - 执行器
- `engine/validators/` - 验证器
- `skills/` - 技能库

**技能分类**:

| 类别 | 技能数 | 目录前缀 |
|------|--------|----------|
| 核心 | 5 | `_core` |
| 文档 | 8 | `_document` |
| 数据 | 8 | `_data` |
| 搜索 | 8 | `_search` |
| 图片 | 8 | `_image` |
| 多媒体 | 6 | `_media` |
| 代码 | 10 | `_code` |
| 内容 | 8 | `_content` |
| 社交 | 6 | `_social` |
| 文件 | 6 | `_file` |
| 工具 | 6 | `_utility` |
| 商业 | 12 | `_business` |
| 专业 | 6 | `_professional` |
| 设计 | 5 | `_design` |
| 自动化 | 4 | `_automation` |
| 辅助 | 6 | `_auxiliary` |
| 特殊 | 3 | `_special` |

---

### L5: 安全治理层 (敏感操作加载, Token: 800)

**职责**: 安全、权限、审计

**文件**:
- `guard/security.py` - 安全检查
- `guard/permissions.py` - 权限管理
- `guard/audit.py` - 审计日志

**技能**: clawsec-suite, senior-security, risk-management-specialist, verified-agent-identity, moltguard, secret-guardian

**触发词**: "安全"、"权限"、"敏感"

---

### L6: 基础设施层 (系统操作加载, Token: 700)

**职责**: 路径、插件、性能、注册

**文件**:
- `infra/paths.py` - 路径解析
- `infra/plugins.py` - 插件标准
- `infra/performance.py` - 性能模块
- `infra/registry.py` - 技能注册表

**技能**: skill-creator, skill-safe-install, openclaw-agent-optimize, performance-upgrade

**触发词**: "系统"、"安装"、"配置"

---

## Token 预算对比

| 层级 | V2.8.2 | V2.9.0 | 节省 |
|------|--------|--------|------|
| L1 | 5000 | 3000 | 40% |
| L2 | 3000 | 2000 | 33% |
| L3 | 2000 | 1500 | 25% |
| L4 | 2000 | 1500 | 25% |
| L5 | 1000 | 800 | 20% |
| L6 | 1000 | 700 | 30% |
| **总计** | **14000** | **9500** | **32%** |

---

## 目录精简对比

| 项目 | V2.8.2 | V2.9.0 | 精简 |
|------|--------|--------|------|
| 顶级目录 | 36 | 6 | 83% |
| 配置文件 | 96 | 10 | 90% |
| 文档文件 | 355 | 50 | 86% |
| Python文件 | 76 | 20 | 74% |

---

## 加载策略

### 启动加载 (L1 only)

```python
# 只加载核心认知层
startup_files = [
    "core/AGENTS.md",
    "core/SOUL.md", 
    "core/USER.md",
    "core/TOOLS.md",
    "core/IDENTITY.md",
]
# Token: ~2000
```

### 按需加载

```python
LOAD_TRIGGERS = {
    "L2": ["记得", "上次", "回忆", "历史"],
    "L3": ["工作流", "定时", "计划", "任务"],
    "L4_document": ["文档", "word", "pdf", "ppt"],
    "L4_data": ["数据", "分析", "excel", "sql"],
    "L4_search": ["搜索", "查找", "网页"],
    "L4_image": ["图片", "照片", "截图"],
    "L4_code": ["代码", "git", "docker"],
    "L4_content": ["写作", "文章", "创作"],
    "L4_social": ["小红书", "b站", "邮件"],
    "L5": ["安全", "权限", "敏感"],
    "L6": ["系统", "安装", "配置"],
}
```

---

## 性能目标

| 指标 | V2.8.2 | V2.9.0 |
|------|--------|--------|
| 启动延迟 | 50ms | 30ms |
| 启动Token | 5000 | 2000 |
| 技能查找 | 10ms | 5ms |
| 总响应 | 100ms | 60ms |

---

## 迁移计划

### Phase 1: 目录合并
- 合并 `autonomy`, `collaboration`, `compliance`, `delivery`, `ecosystem`, `extension`, `openapi`, `ops`, `portfolio`, `product`, `release`, `reliability`, `simulation`, `standards`, `strategy`, `templates`, `tenant`, `billing`, `business` → 删除或归档

### Phase 2: 文件聚合
- 合并所有配置文件到 `core/CONFIG.json`
- 合并所有文档到对应层级目录
- 删除重复和过时文件

### Phase 3: 技能重组
- 技能目录加前缀 `_类别_` 便于分类加载
- 创建技能索引文件

### Phase 4: 测试验证
- 验证所有功能正常
- 性能测试达标

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| V2.8.0 | 2026-04-10 | 十阶段升级 |
| V2.8.1 | 2026-04-11 | 安全加固 |
| V2.8.2 | 2026-04-11 | 层级优化 |
| V2.9.0 | 2026-04-11 | 终极精简 |

---

💡 **核心优化**:
- 目录从36个精简到6个 (83%精简)
- 启动Token从5000降到2000 (60%精简)
- 文件从527个精简到80个 (85%精简)
- 响应延迟从100ms降到60ms (40%提升)
