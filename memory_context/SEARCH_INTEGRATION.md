# L2 记忆搜索集成

## 融合来源
- 来源: llm-memory-integration (xkzs2007)
- 版本: 3.4.2
- 融合日期: 2026-04-11

## 核心模块

| 模块 | 文件 | 功能 |
|------|------|------|
| 智能路由 | `search/router.py` | 根据查询复杂度选择模式 |
| RRF 融合 | `search/rrf.py` | 混合检索排序算法 |
| 动态权重 | `search/weights.py` | 向量/FTS 权重自适应 |
| 查询理解 | `search/understand.py` | 意图识别 + 实体提取 |
| 查询改写 | `search/rewriter.py` | 拼写纠正 + 同义词扩展 |
| 语义去重 | `search/dedup.py` | 结果去重增强 |
| 查询历史 | `search/history.py` | 高频查询缓存 |
| 缓存管理 | `cache/cache.py` | 增量缓存 + 压缩 |
| 反馈学习 | `feedback/feedback.py` | 记录用户点击优化排序 |

## 渐进式启用 (P0-P3)

| 阶段 | 模块 | 说明 |
|------|------|------|
| P0 | router, weights, rrf, dedup | 核心优化 |
| P1 | understand, rewriter | 查询增强 |
| P2 | feedback, history | 学习优化 |
| P3 | explainer, summarizer | 结果增强 |

## 使用示例

```python
from memory_context.unified_search import UnifiedSearch

search = UnifiedSearch()
result = search.search("如何配置记忆系统")

# 记录点击优化
search.record_click("如何配置记忆系统", "result_123", 1)
```

## 性能目标

| 模式 | 目标 |
|------|------|
| 缓存命中 | < 10ms |
| fast 模式 | < 2s |
| balanced 模式 | < 5s |
| full 模式 | < 15s |
| 准确率 | > 80% |
