# L3 任务编排层 - 路由模块

## 模块概述

本模块从 `llm-memory-integration` 技能集成，提供智能路由、动态权重和 RRF 融合能力。

## 模块列表

| 模块 | 文件 | 功能 |
|------|------|------|
| 智能路由 | `router.py` | 根据复杂度选择模式 |
| 动态权重 | `weights.py` | 向量/FTS 权重自适应 |
| RRF 融合 | `rrf.py` | 混合检索排序算法 |

## 智能路由 (router.py)

### 路由模式
- `fast` - 快速模式（禁用 LLM）
- `balanced` - 平衡模式（部分 LLM）
- `full` - 完整模式（全部功能）

### 路由规则
```python
from orchestration.router.router import QueryRouter

router = QueryRouter()

mode = router.route("推送规则")
# mode = "balanced" (简单查询)

mode = router.route("如何配置记忆系统并优化性能")
# mode = "full" (复杂查询)
```

### 复杂度判断
| 因素 | 权重 |
|------|------|
| 查询长度 | 0.2 |
| 关键词数量 | 0.3 |
| 是否包含"如何" | 0.2 |
| 是否包含"配置" | 0.15 |
| 是否包含"优化" | 0.15 |

## 动态权重 (weights.py)

### 权重自适应
根据查询类型自动调整向量搜索和 FTS 搜索的权重：

| 查询类型 | 向量权重 | FTS 权重 |
|----------|----------|----------|
| 精确匹配 | 0.3 | 0.7 |
| 语义查询 | 0.7 | 0.3 |
| 混合查询 | 0.5 | 0.5 |

### 使用示例
```python
from orchestration.router.weights import WeightCalculator

calc = WeightCalculator()
weights = calc.calculate("如何配置记忆系统")
# weights = {"vector": 0.7, "fts": 0.3}
```

## RRF 融合 (rrf.py)

### Reciprocal Rank Fusion
将多个搜索结果融合排序：

```
RRF_score(d) = Σ 1/(k + rank_i(d))
```

- `k` = 60 (默认参数)
- `rank_i(d)` = 文档 d 在第 i 个排序列表中的排名

### 使用示例
```python
from orchestration.router.rrf import RRFFusion

fusion = RRFFusion(k=60)

# 融合向量搜索和 FTS 搜索结果
vector_results = [{"id": 1, "score": 0.9}, {"id": 2, "score": 0.8}]
fts_results = [{"id": 2, "score": 0.95}, {"id": 3, "score": 0.7}]

merged = fusion.merge([vector_results, fts_results])
# merged = [{"id": 2, "rrf_score": 0.032}, {"id": 1, "rrf_score": 0.030}, ...]
```

## 性能指标

| 操作 | 耗时 |
|------|------|
| 路由判断 | < 5ms |
| 权重计算 | < 2ms |
| RRF 融合 | < 10ms |

## 来源
- 集成自: llm-memory-integration v2.2.0
- 作者: @xkzs2007
- 链接: https://clawhub.ai/xkzs2007/llm-memory-integration
