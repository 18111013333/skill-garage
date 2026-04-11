# 自进化链升级配置

## 自进化链核心组件

### 1. self-improving-agent (自进化核心)
- **功能**: 捕获学习、错误和修正，持续改进
- **存储**: `.learnings/LEARNINGS.md`, `.learnings/ERRORS.md`
- **触发**: 命令失败、用户纠正、发现更好方法

### 2. ontology (知识图谱)
- **功能**: 结构化记忆，实体关系管理
- **存储**: `memory/ontology/graph.jsonl`
- **类型**: Person, Project, Task, Event, Document, Skill

### 3. auto-skill-upgrade (技能升级)
- **功能**: 自动扫描、检测、整合、升级技能
- **存储**: `skills-config.json`, `skills-inventory.json`
- **触发**: 新技能安装、定期检查

### 4. skill-creator (技能创建)
- **功能**: 创建和打包新技能
- **流程**: 理解→规划→初始化→编辑→打包→迭代

### 5. find-skills (技能发现)
- **功能**: 查询和安装新技能
- **优先级**: 小艺Skill > 外部Skill
- **安全**: 必须经过 skill-scope 扫描

### 6. moltguard (安全防护)
- **功能**: 防注入、数据防泄露
- **级别**: 系统级安全守卫

---

## 自进化工作流

```
用户请求/错误发生
       ↓
self-improving-agent 捕获
       ↓
┌──────────────────────────────────┐
│  判断类型                         │
│  - 错误 → ERRORS.md               │
│  - 学习 → LEARNINGS.md            │
│  - 功能请求 → FEATURE_REQUESTS.md │
└──────────────────────────────────┘
       ↓
ontology 记录实体
       ↓
┌──────────────────────────────────┐
│  需要新能力？                      │
│  - 是 → find-skills 查找          │
│  - 否 → 继续执行                   │
└──────────────────────────────────┘
       ↓
新技能安装 → skill-scope 扫描
       ↓
auto-skill-upgrade 整合
       ↓
skill-creator 创建/优化
       ↓
moltguard 安全验证
       ↓
升级完成，记录到 MEMORY.md
```

---

## 自进化触发条件

| 触发 | 动作 | 记录位置 |
|------|------|----------|
| 命令失败 | 记录错误 + 尝试修复 | ERRORS.md |
| 用户纠正 | 记录正确做法 | LEARNINGS.md |
| 发现更好方法 | 记录最佳实践 | LEARNINGS.md |
| 需要新能力 | 查找/创建技能 | ontology + find-skills |
| 技能安装 | 整合升级架构 | skills-config.json |
| 知识过时 | 更新知识 | MEMORY.md |

---

## 自进化指标

| 指标 | 当前值 | 目标 |
|------|--------|------|
| 技能总数 | 106 | 150+ |
| 工作流链 | 8 | 15+ |
| 学习记录 | 0 | 持续增长 |
| 错误修复 | 0 | 持续优化 |
| 知识实体 | 0 | 持续积累 |

---

## 下一步升级计划

1. **初始化学习文件**: 创建 `.learnings/` 目录
2. **初始化知识图谱**: 创建 `memory/ontology/` 目录
3. **建立实体模型**: 定义 Skill, Learning, Error 实体类型
4. **配置自动触发**: 在 AGENTS.md 中添加自进化检查
5. **定期自检**: 每周运行 auto-skill-upgrade
