# 记忆增强系统

## V2.7.0 - 2026-04-10

提升记忆能力，减少 Token 消耗。

---

## 一、记忆架构

```
┌─────────────────────────────────────────────────┐
│                  记忆系统架构                    │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────┐    ┌─────────────┐            │
│  │ 短期记忆    │    │ 工作记忆    │            │
│  │ (会话级)    │    │ (任务级)    │            │
│  │ TTL: 1h     │    │ TTL: 24h    │            │
│  └──────┬──────┘    └──────┬──────┘            │
│         │                  │                    │
│         └────────┬─────────┘                    │
│                  │                              │
│                  ▼                              │
│         ┌─────────────┐                         │
│         │ 长期记忆    │                         │
│         │ (持久化)    │                         │
│         │ TTL: 永久   │                         │
│         └─────────────┘                         │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 二、记忆类型

### 2.1 短期记忆

| 属性 | 值 |
|------|-----|
| 存储 | 会话上下文 |
| TTL | 1小时 |
| 容量 | 最近100条消息 |
| Token | <1000 |

### 2.2 工作记忆

| 属性 | 值 |
|------|-----|
| 存储 | 当前任务相关 |
| TTL | 24小时 |
| 容量 | 最近10个任务 |
| Token | <2000 |

### 2.3 长期记忆

| 属性 | 值 |
|------|-----|
| 存储 | MEMORY.md + memory/*.md |
| TTL | 永久 |
| 容量 | 无限制 |
| Token | 按需加载 |

---

## 三、记忆操作

### 3.1 存储记忆

```python
def store_memory(content: str, memory_type: str = "long_term"):
    """存储记忆"""
    if memory_type == "short_term":
        session_context.append(content)
    elif memory_type == "working":
        task_memory.append(content)
    else:
        # 长期记忆
        memory_file = f"memory/{date}.md"
        append_to_file(memory_file, content)
```

### 3.2 检索记忆

```python
def recall_memory(query: str, limit: int = 5) -> List[str]:
    """检索记忆"""
    # 1. 搜索短期记忆
    short_term = search_session(query)
    
    # 2. 搜索工作记忆
    working = search_tasks(query)
    
    # 3. 搜索长期记忆
    long_term = search_files(query)
    
    # 合并结果
    return merge_results(short_term, working, long_term)[:limit]
```

### 3.3 遗忘策略

```python
def forget_expired():
    """清理过期记忆"""
    # 短期记忆: 1小时后清理
    clean_session(older_than="1h")
    
    # 工作记忆: 24小时后清理
    clean_tasks(older_than="24h")
    
    # 长期记忆: 压缩旧文件
    compress_memory_files(older_than="30d")
```

---

## 四、Token 优化

### 4.1 按需加载

```python
# 只加载必要的记忆
def load_memory_for_query(query: str) -> str:
    # 1. 分析查询意图
    intent = analyze_intent(query)
    
    # 2. 确定需要的记忆范围
    if intent == "recent":
        return load_recent_memory(days=7)
    elif intent == "specific":
        return search_memory(query)
    else:
        return load_summary()
```

### 4.2 摘要生成

```python
def generate_memory_summary(memory: str) -> str:
    """生成记忆摘要"""
    # 提取关键信息
    key_points = extract_key_points(memory)
    
    # 生成摘要
    summary = summarize(key_points, max_tokens=500)
    
    return summary
```

### 4.3 压缩策略

```python
# 记忆文件压缩规则
COMPRESSION_RULES = {
    "daily": {
        "keep_full": 7,      # 保留7天完整记录
        "compress_after": 7, # 7天后压缩
        "delete_after": 90   # 90天后删除
    },
    "important": {
        "keep_full": 30,     # 重要记忆保留30天
        "compress_after": 30,
        "delete_after": 365
    }
}
```

---

## 五、记忆提示

### 5.1 自动提示

当检测到以下情况时，自动提示记忆：

```python
TRIGGER_PATTERNS = {
    "recall": ["记得", "上次", "之前", "以前"],
    "preference": ["我喜欢", "我想要", "我的"],
    "context": ["继续", "接着", "刚才"],
}
```

### 5.2 提示格式

```
📚 记忆提示:
- 上次你提到: [相关记忆]
- 你的偏好: [用户偏好]
- 相关上下文: [上下文信息]
```

---

## 六、性能指标

| 指标 | 目标 | 说明 |
|------|------|------|
| 记忆检索延迟 | <50ms | 搜索记忆 |
| Token 消耗 | <2000 | 单次记忆加载 |
| 命中率 | >90% | 找到相关记忆 |
| 存储效率 | >80% | 压缩率 |

---

**版本**: V2.7.0
**作者**: @18816132863
