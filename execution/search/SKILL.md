# L4 能力执行层 - 搜索模块

## 模块概述

本模块从 `llm-memory-integration` 技能集成，提供搜索执行、优化搜索和语义去重能力。

## 模块列表

| 模块 | 文件 | 功能 |
|------|------|------|
| 搜索执行 | `search.py` | 向量 + FTS 混合搜索 |
| 优化搜索 | `search_optimized.py` | AVX-512 优化搜索 |
| 语义去重 | `dedup.py` | 结果去重增强 |

## 搜索执行 (search.py)

### 搜索模式
- `vector` - 纯向量搜索
- `fts` - 纯全文搜索
- `hybrid` - 混合搜索

### 使用示例
```python
from execution.search.search import HybridSearch

search = HybridSearch(
    db_path="~/.openclaw/vectors.db",
    embedding_client=embedding_client
)

results = search.query(
    query="如何配置记忆系统",
    mode="hybrid",
    top_k=10
)
# results = [{"id": 1, "content": "...", "score": 0.95}, ...]
```

## 优化搜索 (search_optimized.py)

### AVX-512 优化
- 向量点积加速: **15.6x**
- 批量搜索加速: **10x**
- 内存操作加速: **13.7x**

### 使用示例
```python
from execution.search.search_optimized import OptimizedSearch

search = OptimizedSearch(
    db_path="~/.openclaw/vectors.db",
    use_avx512=True  # 自动检测 AVX-512 支持
)

results = search.batch_query(
    queries=["推送规则", "记忆配置", "性能优化"],
    top_k=5
)
```

## 语义去重 (dedup.py)

### 去重策略
- 精确去重: 内容完全相同
- 语义去重: 相似度 > 0.95
- 模糊去重: 编辑距离 < 3

### 使用示例
```python
from execution.search.dedup import SemanticDeduplicator

dedup = SemanticDeduplicator(
    embedding_client=embedding_client,
    threshold=0.95
)

results = [
    {"id": 1, "content": "推送规则配置"},
    {"id": 2, "content": "推送规则配置"},  # 重复
    {"id": 3, "content": "记忆系统配置"}
]

unique = dedup.deduplicate(results)
# unique = [{"id": 1, "content": "推送规则配置"}, {"id": 3, "content": "记忆系统配置"}]
```

## 性能指标

| 操作 | 标准耗时 | AVX-512 优化后 |
|------|----------|----------------|
| 单次搜索 | 100ms | 15ms |
| 批量搜索(10) | 1000ms | 100ms |
| 语义去重 | 50ms | 8ms |

## 来源
- 集成自: llm-memory-integration v2.2.0
- 作者: @xkzs2007
- 链接: https://clawhub.ai/xkzs2007/llm-memory-integration
