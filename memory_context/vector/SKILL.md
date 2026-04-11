# L2 记忆与上下文层 - 向量处理模块

## 模块概述

本模块从 `llm-memory-integration` 技能集成，提供向量嵌入、缓存管理和查询历史能力。

## 模块列表

| 模块 | 文件 | 功能 |
|------|------|------|
| 向量嵌入 | `embedding.py` | Embedding API 调用 |
| 缓存管理 | `cache.py` | 增量缓存 + 压缩存储 |
| 查询历史 | `history.py` | 高频查询缓存 |

## 向量嵌入 (embedding.py)

### 支持的 Embedding 提供商
- OpenAI (text-embedding-3-*)
- Gitee AI (Qwen3-Embedding-8B)
- 本地模型

### 使用示例
```python
from memory_context.vector.embedding import EmbeddingClient

client = EmbeddingClient(
    provider="openai-compatible",
    base_url="https://api.example.com/v1",
    api_key="your-api-key",
    model="text-embedding-3-small"
)

vectors = client.embed(["Hello world", "你好世界"])
# vectors = [[0.1, 0.2, ...], [0.3, 0.4, ...]]
```

## 缓存管理 (cache.py)

### 功能
- 增量缓存
- 压缩存储
- LRU 淘汰策略
- 缓存命中率统计

### 使用示例
```python
from memory_context.vector.cache import QueryCache

cache = QueryCache(max_size=1000)

# 缓存查询
cache.set("query_key", {"result": "data"})

# 获取缓存
result = cache.get("query_key")

# 统计
stats = cache.stats()
# stats = {"hits": 100, "misses": 10, "hit_rate": 0.91}
```

## 查询历史 (history.py)

### 功能
- 高频查询记录
- 查询频率统计
- 热门查询推荐

### 使用示例
```python
from memory_context.vector.history import QueryHistory

history = QueryHistory()

# 记录查询
history.record("推送规则")

# 获取热门查询
hot = history.get_hot_queries(top_n=10)
# hot = [{"query": "推送规则", "count": 50}, ...]
```

## 性能指标

| 操作 | 耗时 |
|------|------|
| 向量嵌入 | 100-500ms |
| 缓存命中 | < 5ms |
| 历史查询 | < 10ms |

## 来源
- 集成自: llm-memory-integration v2.2.0
- 作者: @xkzs2007
- 链接: https://clawhub.ai/xkzs2007/llm-memory-integration
