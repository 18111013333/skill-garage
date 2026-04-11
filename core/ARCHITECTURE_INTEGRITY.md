# 架构完整性规范 - V4.3.2

## 说明

本文件仅定义校验规范、验收规则、约束条件。
**不再定义第二套六层架构**，唯一主架构引用 `core/ARCHITECTURE.md`。

---

## 一、架构引用

**唯一主架构**: `core/ARCHITECTURE.md`

所有层级定义、职责划分、模块归属均以 `core/ARCHITECTURE.md` 为准。

---

## 二、注册表校验规范

### 2.1 技能注册表

路径: `infrastructure/inventory/skill_registry.json`

**必需字段**:
- `name`: 技能名称
- `registered`: 是否已注册
- `routable`: 是否可路由
- `callable`: 是否可调用
- `executor_type`: 执行类型 (python/script/api/skill_md)
- `entry_point`: 入口文件
- `path`: 技能路径（相对路径）

**一致性校验**:
- `executor_type=skill_md` → `callable=false`
- `callable=true` → `entry_point` 不能是 `SKILL.md`
- `registered=true` → `routable` 和 `callable` 必须有明确值

### 2.2 反向索引

路径: `infrastructure/inventory/skill_inverted_index.json`

**校验规则**:
- 只索引 `registered=true && routable=true && callable=true` 的技能
- 索引条目数应与可执行技能数一致

---

## 三、路径规范

### 3.1 禁止硬编码路径

**禁止**:
- `Path.home()`
- `~/.openclaw`
- `/home/sandbox/.openclaw/workspace`
- 任何绝对路径

**必须**:
- 使用 `infrastructure/path_resolver.py` 提供的函数
- `get_project_root()` 获取项目根目录
- `get_skills_dir()` 获取技能目录
- `get_infrastructure_dir()` 获取基础设施目录

### 3.2 相对路径

所有注册表中的路径必须是相对路径，相对于项目根目录。

---

## 四、索引排除规范

### 4.1 排除目录

以下目录不进入主搜索和主上下文:
- `node_modules`, `__pycache__`, `.git`
- `archive`, `reports`, `backups`
- `dist`, `build`, `.cache`, `logs`

### 4.2 排除文件类型

以下文件类型不进入索引:
- 二进制文件: `.pyc`, `.so`, `.dll`, `.dylib`
- 压缩文件: `.tar`, `.gz`, `.zip`, `.rar`
- 媒体文件: `.mp3`, `.mp4`, `.jpg`, `.png`
- 大型文档: `.pdf`, `.docx`, `.xlsx` (超过 10MB)
- 锁文件: `package-lock.json`, `yarn.lock`

### 4.3 大小限制

- 单文件最大: 10MB
- 超过限制的文件不进入索引

---

## 五、验收规则

### 5.1 第一阶段验收

- [ ] 技能注册表字段完整
- [ ] 反向索引与注册表一致
- [ ] 路由能命中可执行技能
- [ ] 技能能真实执行
- [ ] Task 不返回假成功

### 5.2 第二阶段验收

- [ ] 统一搜索入口可用
- [ ] 搜索结果经过 RRF 融合
- [ ] 搜索结果经过去重
- [ ] 索引排除名单生效
- [ ] 无硬编码路径

---

## 六、约束条件

1. **单一真源**: 架构定义只在 `core/ARCHITECTURE.md`
2. **路径统一**: 所有路径通过 `path_resolver` 获取
3. **状态一致**: 注册表、索引、路由器状态必须一致
4. **真实执行**: 不允许假成功，没有真实执行必须失败
5. **参数过滤**: 按技能协议过滤参数，不传递无关参数

---

**版本**: V4.3.2
**更新**: 2026-04-11
