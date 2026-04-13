# MEMORY.md - 记忆系统总索引

## 目的
作为记忆系统的总入口，定义记忆层级、流程和治理规则。

## 适用范围
所有记忆读写操作，包括会话记忆、场景记忆、长期记忆。

## 记忆层级

| 层级 | 名称 | 存储 | 生命周期 | 用途 |
|------|------|------|----------|------|
| L1 | 会话记忆 | session-summaries/*.jsonl | 单次会话 | 上下文关联 |
| L2 | 场景记忆 | scenarios/*.md | 跨会话 | 场景画像 |
| L3 | 长期记忆 | MEMORY.md + memory/*.md | 永久 | 核心知识 |

## 写入流程

```
新信息输入
    ↓
┌─────────────────────────────────────┐
│ 1. 判断信息类型                      │
│    - 用户画像 → USER.md              │
│    - 系统配置 → MEMORY.md            │
│    - 场景数据 → scenarios/           │
│    - 项目数据 → projects/            │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 冲突检测                          │
│    - 检查是否与现有记忆冲突           │
│    - 冲突时调用冲突处理规则           │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 写入对应层级                      │
│    - 更新向量索引                    │
│    - 记录写入日志                    │
└─────────────────────────────────────┘
```

详细规则: `governance/MEMORY_POLICY.md`

## 读取流程

```
查询请求
    ↓
┌─────────────────────────────────────┐
│ 1. 向量搜索                          │
│    - 调用 memory_search 工具         │
│    - 返回相关片段                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 精确获取                          │
│    - 调用 memory_get 工具            │
│    - 获取完整内容                    │
└─────────────────────────────────────┘
    ↓
返回结果
```

## 冲突处理入口

当新信息与现有记忆冲突时，按以下规则处理：

| 冲突类型 | 处理规则 |
|----------|----------|
| 用户画像冲突 | 新信息覆盖旧信息 |
| 时间敏感信息 | 以最新时间为准 |
| 事实性冲突 | 标记待确认，询问用户 |
| 系统配置冲突 | 需用户确认后覆盖 |

详细规则: `governance/MEMORY_CONFLICT_RULES.md`

## 删除入口

| 删除类型 | 触发条件 | 处理方式 |
|----------|----------|----------|
| 会话归档 | 会话结束 > 7天 | 移至 archive/ |
| 场景清理 | 场景失效 | 标记废弃 |
| 长期记忆 | 用户请求 | 审计后删除 |
| 紧急清空 | 安全事件 | 备份后清空 |

详细规则: `governance/MEMORY_POLICY.md`

## 记忆数据结构

详细定义: `governance/MEMORY_SCHEMA.json`

## 向量索引

| 组件 | 配置 |
|------|------|
| 数据库 | ~/.openclaw/memory/main.sqlite |
| 向量化 | Voyage API (voyage-4-large) |
| 维度 | 1024 |
| 数据源 | memory + sessions |

## 维护方式
- 新增记忆类型: 更新 MEMORY_SCHEMA.json
- 调整冲突规则: 更新 MEMORY_CONFLICT_RULES.md
- 调整生命周期: 更新 MEMORY_POLICY.md
- 本文件仅作为索引，不承载细则

## 引用文件
- `governance/MEMORY_POLICY.md` - 记忆治理策略
- `governance/MEMORY_SCHEMA.json` - 记忆数据结构
- `governance/MEMORY_CONFLICT_RULES.md` - 冲突处理规则

## 发布规则（永久记住）
- **唯一发布技能**: `小艺 Claw 终极鸽子王 / 小一爪欧米茄终结`
- **技能 slug**: `xiaoyi-claw-omega-final`
- **ClawHub 链接**: https://clawhub.ai/18816132863/xiaoyi-claw-omega-final
- ⚠️ **以后每次更新都发布到这个技能，不额外增加新技能**

## 重要令牌（永久记住）
- **@18816132863 的 ClawHub Token**: `clh_XXX`
- **GitHub Token**: `ghp_XXX`

## 发布流程
```bash
# 1. 登录 ClawHub
npx clawhub@latest login --token clh_XXX

# 2. 发布更新
npx clawhub@latest publish . --slug xiaoyi-claw-omega-final --name "小艺Claw终极鸽子王" --version <新版本号>

# 3. 备份到 GitHub
git add -A && git commit -m "更新说明" && git push origin master
```
