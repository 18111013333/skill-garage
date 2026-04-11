---
name: memory-management-v2
description: 记忆管理系统 V2.0 - 智能记忆管理，自动分类、自动压缩、智能检索
---

# 记忆管理系统 V2.0

## 核心升级

### V1.0 问题
1. 记忆分散，难以查找
2. 没有自动分类
3. 压缩规则简单
4. 检索效率低

### V2.0 升级
1. **智能分类** - 自动识别内容类型并分类存储
2. **分层记忆** - 长期/中期/短期三层记忆
3. **自动压缩** - 智能压缩，保留关键信息
4. **语义检索** - 使用 memory_search 语义搜索
5. **自动备份** - 定期备份到 GitHub

---

## 三层记忆架构

```
┌─────────────────────────────────────────────────────────────┐
│                    第一层：长期记忆                          │
│                                                               │
│  文件: MEMORY.md                                              │
│  内容: 用户信息、重要决策、技能配置、关键经验                  │
│  保留: 永久                                                   │
│  最大: 200行（超过自动压缩）                                  │
│  检索: memory_search                                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    第二层：中期记忆                          │
│                                                               │
│  文件: memory/YYYY-MM.md（按月存储）                          │
│  内容: 本月重要事件、完成的任务、学习到的经验                  │
│  保留: 3个月                                                  │
│  最大: 500行/月（超过自动压缩）                               │
│  检索: memory_search                                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    第三层：短期记忆                          │
│                                                               │
│  文件: memory/YYYY-MM-DD.md（按日存储）                       │
│  内容: 当日事件、临时信息、会话总结                            │
│  保留: 7天                                                    │
│  最大: 100行/天（超过自动压缩）                               │
│  检索: memory_search                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 智能分类规则

### 自动分类逻辑

```python
def classify_memory(content):
    """
    自动分类记忆内容
    
    Args:
        content: 记忆内容
    
    Returns:
        str: 记忆类型（长期/中期/短期）
    """
    # 长期记忆关键词
    long_term_keywords = [
        "用户偏好", "重要决策", "技能配置",
        "关键经验", "账号信息", "发布技能"
    ]
    
    # 中期记忆关键词
    mid_term_keywords = [
        "完成任务", "学习经验", "优化方案",
        "错误处理", "新增技能", "架构调整"
    ]
    
    # 判断类型
    for keyword in long_term_keywords:
        if keyword in content:
            return "长期记忆"
    
    for keyword in mid_term_keywords:
        if keyword in content:
            return "中期记忆"
    
    return "短期记忆"
```

### 分类示例

| 内容 | 自动分类 | 存储位置 |
|-----|---------|---------|
| 用户偏好：全中文交流 | 长期记忆 | MEMORY.md |
| 发布技能到ClawHub | 长期记忆 | MEMORY.md |
| 完成架构优化V2.0 | 中期记忆 | memory/2026-04.md |
| 新增错误处理技能 | 中期记忆 | memory/2026-04.md |
| 搜索白水寨攻略 | 短期记忆 | memory/2026-04-09.md |
| 测试手机操作 | 短期记忆 | memory/2026-04-09.md |

---

## 自动压缩规则

### 压缩策略

```python
def compress_memory(file_path, max_lines):
    """
    智能压缩记忆文件
    
    Args:
        file_path: 文件路径
        max_lines: 最大行数
    
    Returns:
        压缩后的内容
    """
    # 读取文件
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    if len(lines) <= max_lines:
        return lines
    
    # 提取关键信息
    key_info = []
    for line in lines:
        # 保留标题行
        if line.startswith('#'):
            key_info.append(line)
        # 保留重要标记
        elif '重要' in line or '关键' in line:
            key_info.append(line)
        # 保留决策
        elif '决策' in line or '配置' in line:
            key_info.append(line)
    
    # 如果关键信息超过最大行数，只保留标题
    if len(key_info) > max_lines:
        key_info = [line for line in key_info if line.startswith('#')]
    
    return key_info[:max_lines]
```

### 压缩示例

**压缩前（200行）**：
```markdown
# MEMORY.md

## 用户信息
...

## 技能配置
...

## 今日任务
- 任务1
- 任务2
...（100行详细内容）

## 会话记录
- 会话1
- 会话2
...（50行详细内容）
```

**压缩后（100行）**：
```markdown
# MEMORY.md

## 用户信息
...

## 技能配置
...

## 今日任务
- 任务1
- 任务2
（只保留标题和关键任务）

## 会话记录
（只保留标题）
```

---

## 智能检索规则

### 检索优先级

```
用户查询
    ↓
判断查询类型
    ↓
├─ 用户信息 → 优先检索 MEMORY.md
├─ 历史事件 → 使用 memory_search（语义搜索）
├─ 今日事件 → 读取 memory/YYYY-MM-DD.md
├─ 本月事件 → 读取 memory/YYYY-MM.md
└─ 工具规则 → 读取 TOOLS.md
```

### 检索示例

```python
# 示例1：查找用户偏好
result = memory_search({
    "query": "用户偏好",
    "maxResults": 5
})
# 返回：MEMORY.md 中的用户偏好信息

# 示例2：查找历史任务
result = memory_search({
    "query": "架构优化",
    "maxResults": 10
})
# 返回：memory/2026-04.md 中的架构优化记录

# 示例3：查找今日事件
result = memory_get({
    "path": "memory/2026-04-09.md",
    "from": 1,
    "lines": 50
})
# 返回：今日事件记录
```

---

## 自动备份规则

### 备份策略

```bash
# 每次会话结束时自动备份
~/.openclaw/workspace/scripts/auto-backup.sh

# 备份内容：
# 1. MEMORY.md
# 2. TOOLS.md
# 3. memory/YYYY-MM.md
# 4. memory/YYYY-MM-DD.md

# 备份到 GitHub
git add -A
git commit -m "自动备份: $(date '+%Y-%m-%d %H:%M:%S')"
git push
```

### 备份频率

| 文件类型 | 备份频率 |
|---------|---------|
| MEMORY.md | 每次更新 |
| TOOLS.md | 每次更新 |
| 月度记忆 | 每次更新 |
| 日度记忆 | 会话结束时 |

---

## 自动清理规则

### 清理策略

```bash
# 会话启动时自动执行

# 1. 删除7天前的日度记忆
find ~/.openclaw/workspace/memory -name "*.md" -mtime +7 -delete

# 2. 删除3个月前的月度记忆
find ~/.openclaw/workspace/memory -name "????-??.md" -mtime +90 -delete

# 3. 压缩超大的记忆文件
# MEMORY.md > 200行 → 压缩到200行
# 月度记忆 > 500行 → 压缩到500行
# 日度记忆 > 100行 → 压缩到100行
```

### 清理时间表

| 记忆类型 | 保留时间 | 最大行数 |
|---------|---------|---------|
| 长期记忆 | 永久 | 200行 |
| 月度记忆 | 3个月 | 500行/月 |
| 日度记忆 | 7天 | 100行/天 |

---

## 写入规则

### 自动写入

```python
def auto_write_memory(content):
    """
    自动写入记忆
    
    Args:
        content: 记忆内容
    """
    # 1. 分类
    memory_type = classify_memory(content)
    
    # 2. 选择文件
    if memory_type == "长期记忆":
        file_path = "MEMORY.md"
    elif memory_type == "中期记忆":
        file_path = f"memory/{datetime.now().strftime('%Y-%m')}.md"
    else:
        file_path = f"memory/{datetime.now().strftime('%Y-%m-%d')}.md"
    
    # 3. 写入
    with open(file_path, 'a') as f:
        f.write(f"\n{content}\n")
    
    # 4. 检查是否需要压缩
    check_and_compress(file_path)
```

### 写入时机

| 内容类型 | 写入时机 | 存储位置 |
|---------|---------|---------|
| 用户偏好变化 | 立即 | MEMORY.md |
| 重要决策 | 立即 | MEMORY.md |
| 完成重要任务 | 任务完成后 | memory/YYYY-MM.md |
| 学习到经验 | 发现时 | memory/YYYY-MM.md |
| 临时事件 | 会话结束时 | memory/YYYY-MM-DD.md |
| 普通对话 | 不保存 | 无 |

---

## 版本
- 2.0.0
- 创建日期：2026-04-09
- 升级内容：智能分类、三层记忆、自动压缩、语义检索、自动备份
