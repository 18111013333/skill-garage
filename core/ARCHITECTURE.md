# 六层架构定义 V4.3.2

> **唯一主架构定义** - 本文档是项目唯一正式运行架构定义
> 
> 其他架构文档（ARCHITECTURE_V2.x.x.md、OMEGA_FINAL.md 等）均为历史兼容资料，位于 `archive/deprecated/`

## 六层架构

| 层级 | 名称 | 职责 | 目录 |
|------|------|------|------|
| L1 | Core | 核心认知、身份、规则 | `core/` |
| L2 | Memory Context | 记忆上下文、知识库、统一搜索 | `memory_context/` |
| L3 | Orchestration | 任务编排、工作流、路由 | `orchestration/` |
| L4 | Execution | 能力执行、技能网关 | `execution/` |
| L5 | Governance | 稳定治理、安全审计、巡检 | `governance/` |
| L6 | Infrastructure | 基础设施、工具链、注册表 | `infrastructure/` |

---

## 第一阶段：主链打通

### 技能注册体系

**路径**: `infrastructure/inventory/skill_registry.json`

**核心字段**:
- `name`: 技能名称
- `registered`: 是否已注册
- `routable`: 是否可路由
- `callable`: 是否可调用
- `executor_type`: 执行类型 (python/script/api/skill_md)
- `entry_point`: 入口文件
- `path`: 技能路径（相对路径）

**状态一致性**:
- `executor_type=skill_md` → `callable=false`
- `callable=true` → `entry_point` 不能是 `SKILL.md`
- `registered=true && routable=true && callable=true` → 进入反向索引

### 反向索引

**路径**: `infrastructure/inventory/skill_inverted_index.json`

**规则**:
- 只索引可执行技能
- 触发词映射到技能名称

### 路由器

**路径**: `infrastructure/shared/router.py`

**功能**:
- 检查技能状态 (registered/routable/callable/status)
- 返回执行所需信息 (executor_type/entry_point/timeout)
- 按评分排序候选技能

### 技能网关

**路径**: `execution/skill_adapter_gateway.py`

**功能**:
- 启动时从 registry 加载技能
- 按 executor_type 分流执行 (python/script/api/skill_md)
- 统一错误码映射

### 任务引擎

**路径**: `orchestration/task_engine.py`

**功能**:
- 动态路由技能
- 五段流程 (validate → execute → verify → summarize)
- 内部步骤特殊处理
- 真实执行检查，无假成功

---

## 第二阶段：搜索与架构统一

### 统一搜索入口

**路径**: `memory_context/unified_search.py`

**组件**:
- `KeywordSearch`: 关键词搜索
- `FTSSearch`: 全文搜索
- `VectorSearch`: 向量搜索
- `RRFFusion`: RRF 融合
- `SemanticDedup`: 语义去重
- `FeedbackLearner`: 反馈学习
- `IndexExcludeList`: 索引排除名单

**搜索模式**:
- `fast`: 仅关键词搜索
- `balanced`: 关键词 + FTS
- `full`: 关键词 + FTS + 向量

### 索引排除配置

**路径**: `infrastructure/inventory/exclude_config.json`

**排除目录**:
- `node_modules`, `__pycache__`, `.git`
- `archive`, `reports`, `backups`
- `dist`, `build`, `.cache`, `logs`

**排除文件类型**:
- 二进制: `.pyc`, `.so`, `.dll`
- 压缩: `.tar`, `.gz`, `.zip`
- 媒体: `.mp3`, `.mp4`, `.jpg`, `.png`
- 锁文件: `package-lock.json`, `yarn.lock`

**大小限制**: 单文件最大 10MB

### 架构完整性规范

**路径**: `core/ARCHITECTURE_INTEGRITY.md`

**内容**:
- 引用本文件作为唯一主架构
- 定义注册表校验规范
- 定义路径规范
- 定义验收规则

### 历史架构归档

**路径**: `archive/deprecated/`

**文件**:
- `ARCHITECTURE_V2.8.1.md`
- `ARCHITECTURE_V2.9.0.md`
- `ARCHITECTURE_V2.9.1.md`

**标注**: "仅历史参考，不作为当前运行依据"

---

## 层级调用规则

```
请求流: 用户请求 → L1解析 → L3路由 → L4执行 → L5验证 → 返回结果
保护流: 删除请求 → L5文件保护 → 人工确认 → L6执行 → L5审计日志
记忆流: L1触发词 → L2统一搜索 → L3编排 → L4执行 → L2存储结果
巡检流: 定时触发 → L5巡检 → L6注册表 → L4技能健康检查 → L5报告
```

---

## Token 预算

| 层级 | Token 预算 | 加载模式 |
|------|-----------|----------|
| L1 Core | 3000 | 立即加载 |
| L2 Memory Context | 2000 | 按需加载 |
| L3 Orchestration | 1500 | 按需加载 |
| L4 Execution | 1500 | 延迟加载 |
| L5 Governance | 800 | 敏感加载 |
| L6 Infrastructure | 700 | 系统加载 |
| **总计** | **9500** | |

---

## 核心文件

### L1 核心认知层
- `AGENTS.md` - 工作空间规则
- `SOUL.md` - 身份定义
- `USER.md` - 用户信息
- `TOOLS.md` - 工具规则
- `IDENTITY.md` - 身份标识
- `ARCHITECTURE.md` - 本文件
- `ARCHITECTURE_INTEGRITY.md` - 完整性规范

### L2 记忆上下文层
- `MEMORY.md` - 长期记忆
- `memory/*.md` - 日记文件
- `memory_context/unified_search.py` - 统一搜索入口
- `memory_context/search/` - 搜索模块
- `memory_context/cache/` - 缓存模块

### L3 任务编排层
- `orchestration/task_engine.py` - 任务引擎
- `orchestration/router/` - 路由配置
- `orchestration/workflows/` - 工作流

### L4 能力执行层
- `execution/skill_adapter_gateway.py` - 技能接入网关
- `execution/skill_gateway.py` - 技能执行网关
- `execution/ecommerce/` - 电商执行器

### L5 稳定治理层
- `governance/security.py` - 安全检查
- `governance/permissions.py` - 权限管理
- `governance/audit/` - 审计日志
- `governance/validators/` - 校验器
- `governance/quality_gate.py` - 质量门禁

### L6 基础设施层
- `infrastructure/path_resolver.py` - 路径解析器
- `infrastructure/shared/router.py` - 统一路由器
- `infrastructure/inventory/skill_registry.json` - 技能注册表
- `infrastructure/inventory/skill_inverted_index.json` - 反向索引
- `infrastructure/inventory/exclude_config.json` - 排除配置
- `infrastructure/manifest/` - Manifest 生成器

---

## 路径规范

**禁止**:
- `Path.home()`
- `~/.openclaw`
- 绝对路径

**必须**:
- 使用 `infrastructure/path_resolver.py`
- `get_project_root()` 获取项目根目录
- `get_skills_dir()` 获取技能目录
- `get_infrastructure_dir()` 获取基础设施目录

---

## 验收规则

### 第一阶段验收
- [ ] 技能注册表字段完整
- [ ] 反向索引与注册表一致
- [ ] 路由能命中可执行技能
- [ ] 技能能真实执行
- [ ] Task 不返回假成功
- [ ] 内部步骤不显示 failed

### 第二阶段验收
- [ ] 统一搜索入口可用
- [ ] 搜索结果经过 RRF 融合
- [ ] 搜索结果经过去重
- [ ] 索引排除名单生效
- [ ] 无硬编码路径
- [ ] 历史架构已归档

---

## 版本历史

- V4.3.2: 第一阶段主链打通 + 第二阶段搜索统一
- V4.3.0: 架构收口，统一为六层
- V4.2.x: 性能优化
- V4.1.0: 纯文档版本
- V4.0.0: 完整六层架构
