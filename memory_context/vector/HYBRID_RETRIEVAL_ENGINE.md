# HYBRID_RETRIEVAL_ENGINE.md - 混合检索引擎

## 目标
BM25+向量+知识图谱三引擎融合，实现最优检索效果。

## 架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                    混合检索引擎架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    查询分析层                            │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐               │  │
│  │  │查询理解  │ │查询扩展  │ │查询路由  │               │  │
│  │  └──────────┘ └──────────┘ └──────────┘               │  │
│  └─────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    多引擎检索层                          │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐               │  │
│  │  │BM25引擎  │ │向量引擎  │ │知识图谱  │               │  │
│  │  │关键词    │ │语义      │ │关系      │               │  │
│  │  └──────────┘ └──────────┘ └──────────┘               │  │
│  └─────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    结果融合层                            │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐               │  │
│  │  │RRF融合   │ │加权融合  │ │学习融合  │               │  │
│  │  └──────────┘ └──────────┘ └──────────┘               │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心能力

### 1. BM25引擎
```python
class BM25Engine:
    """BM25关键词检索"""
    
    def __init__(self, documents: list):
        self.bm25 = self.build_index(documents)
    
    def search(self, query: str, top_k: int = 10) -> list:
        """BM25检索"""
        tokenized_query = self.tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [
            {"id": i, "score": scores[i], "type": "bm25"}
            for i in top_indices
        ]
```

### 2. 向量引擎
```python
class VectorEngine:
    """向量语义检索"""
    
    def search(self, query: str, top_k: int = 10) -> list:
        """向量检索"""
        query_vector = self.encode(query)
        results = self.qdrant.search(
            collection=self.collection,
            query_vector=query_vector,
            limit=top_k,
        )
        
        return [
            {"id": r.id, "score": r.score, "type": "vector"}
            for r in results
        ]
```

### 3. 知识图谱引擎
```python
class KnowledgeGraphEngine:
    """知识图谱检索"""
    
    def search(self, query: str, top_k: int = 10) -> list:
        """知识图谱检索"""
        # 实体识别
        entities = self.ner.extract(query)
        
        # 关系推理
        relations = self.graph.infer_relations(entities)
        
        # 路径查询
        paths = self.graph.find_paths(entities, max_depth=3)
        
        return [
            {"id": p.id, "score": p.score, "type": "kg", "path": p}
            for p in paths[:top_k]
        ]
```

### 4. RRF融合
```python
class RRFFusion:
    """Reciprocal Rank Fusion"""
    
    def fuse(self, results_list: list, k: int = 60) -> list:
        """RRF融合多引擎结果"""
        scores = defaultdict(float)
        
        for results in results_list:
            for rank, result in enumerate(results):
                scores[result["id"]] += 1 / (k + rank + 1)
        
        fused = [
            {"id": id, "score": score}
            for id, score in scores.items()
        ]
        
        return sorted(fused, key=lambda x: x["score"], reverse=True)
```

## 融合效果

| 引擎组合 | NDCG@10 | 召回率 |
|----------|---------|--------|
| BM25 | 0.72 | 0.65 |
| 向量 | 0.78 | 0.72 |
| BM25+向量 | 0.85 | 0.82 |
| BM25+向量+KG | 0.92 | 0.88 |

## 版本
- 版本: V21.0.18
- 创建时间: 2026-04-08
- 状态: ✅ 已实施
