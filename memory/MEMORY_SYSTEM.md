# 记忆系统架构说明

## 架构版本
**V3.9.5 + V3.0.0** - 2026-04-11

---

## 一、记忆系统概述

本系统采用 **yaoyao-memory-v2 + llm-memory-integration-v3** 双引擎架构：

| 模块 | 功能 | 技术 |
|------|------|------|
| yaoyao-memory-v2 | 四层渐进式记忆 | ChromaDB + Feature Flag |
| llm-memory-integration-v3 | 向量搜索 | SQLite vec0 + PTL防御 |

---

## 二、四层渐进式记忆

| 层级 | 存储 | 保留期 | 升级条件 |
|------|------|--------|----------|
| **L0** | 对话上下文 | 当前会话 | 自动 |
| **L1** | `memory/YYYY-MM-DD.md` | 7-30天 | 每日自动 |
| **L2** | `MEMORY.md` | 30天+ | 引用≥3次 |
| **L3** | IMA 知识库 | 永久 | 核心知识/重大决策 |

---

## 三、记忆类型（自动分类）

| 类型 | 触发词 | 说明 |
|------|--------|------|
| `decision` | 决定、采用、选择、用、配置变更 | 技术/产品决策 |
| `preference` | 喜欢、偏好、倾向、习惯 | 用户偏好 |
| `learning` | 学会、理解、发现、掌握 | 新知识 |
| `task` | 需要做、计划、下一步、TODO | 待办事项 |
| `error` | 错误、失败、bug、修复 | 踩坑教训 |
| `progress` | 完成、达成、里程碑 | 进展记录 |
| `info` | 默认 | 一般信息 |

---

## 四、重要性等级

| 标志 | 含义 | 触发词 |
|------|------|--------|
| `-i c` | Critical 关键 | 永远、绝不、核心 |
| `-i h` | High 高 | 重要、关键、决策、偏好 |
| `-i n` | Normal 普通 | 默认 |
| `-i l` | Low 低 | 临时笔记 |

---

## 五、核心命令

```bash
# 统计（查看分类）
python3 scripts/memory.py stats

# 搜索
python3 scripts/memory.py search <query>

# 获取主题记忆
python3 scripts/memory.py get <topic>

# 清理缓存（强制重载）
python3 scripts/memory.py clear-cache

# 健康检测
python3 scripts/health_check.py

# 系统诊断
python3 scripts/config_manager.py doctor
```

---

## 六、静默操作规则

**绝对禁止：**
- ❌ "要不要记录这个？"
- ❌ "我会记住的"
- ❌ 主动提及记忆操作

**正确做法：**
- ✅ 检测到重要信息 → 直接静默记录
- ✅ 用户询问记忆 → 静默检索后回答

---

## 七、隐私规则

**永不记录：**
- ❌ 密码、密钥、Token
- ❌ 银行卡、身份证
- ❌ 用户明确要求不记录的

---

## 八、自修复系统

| 问题 | 检测 | 自动修复 |
|------|------|----------|
| Embedding缓存损坏 | JSON解析失败 | 删除缓存文件 |
| 配置文件损坏 | JSON解析失败 | 备份+重建 |
| Feature Flag损坏 | JSON解析失败 | 重置 Flags |
| 记忆目录缺失 | 目录不存在 | 创建目录 |

---

## 九、Feature Flag 体系

30 个内置开关，支持 A/B 测试和灰度发布：

```bash
# 查看所有开关
python3 scripts/feature_flag.py list

# 启用/禁用
python3 scripts/feature_flag.py enable memory.auto_promote
python3 scripts/feature_flag.py disable exp.smart_routing
```

开关分组：memory.* | search.* | shell.* | feedback.* | ux.* | exp.* | ab.*

---

## 十、与六层架构的融合

| 层级 | 记忆系统组件 | 说明 |
|------|--------------|------|
| L1 | SOUL.md, USER.md, IDENTITY.md | 身份记忆 |
| L2 | MEMORY.md, memory/*.md, yaoyao-memory-v2, llm-memory-integration-v3 | 长期记忆 + 向量搜索 |
| L3 | fast_path.py, predictive_cache.py | 编排优化 |
| L4 | memory.py, search.py, promote.py, VectorSearch, MemoryStore | 执行脚本 |
| L5 | governance.py, audit.py, PTLGuard | 治理审计 + PTL防御 |
| L6 | infrastructure.py, backup_manager.py | 基础设施 |

---

## 十一、双引擎协同

### yaoyao-memory-v2 负责
- 四层渐进式记忆管理
- Feature Flag 功能开关
- 自修复系统
- 记忆升级/清理

### llm-memory-integration-v3 负责
- 向量搜索 (SQLite vec0)
- Embedding 缓存
- PTL 防御截断
- 安全扩展加载

### 协同工作流
```
用户输入 → yaoyao-memory 分类存储
         → llm-memory-integration 向量索引
         → 搜索时双引擎并行
         → 结果合并返回
```

---

**架构版本**: V3.9.5 + V3.0.0
**更新时间**: 2026-04-11
