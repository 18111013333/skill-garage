# SEMANTIC_RERANKING_V2.md - 语义重排序优化

## 目标
NDCG > 0.95，实现精准的语义重排序。

## 核心能力

### 1. 多因素重排序
```python
class MultiFactorReranker:
    """多因素重排序"""
    
    def rerank(self, results: list, query: dict) -> list:
        """多因素重排序"""
        scored_results = []
        
        for result in results:
            score = 0
            
            # 向量相似度
            score += result["vector_score"] * 0.4
            
            # BM25分数
            score += result["bm25_score"] * 0.2
            
            # 时间新鲜度
            score += self.freshness_score(result) * 0.15
            
            # 用户偏好
            score += self.preference_score(result) * 0.15
            
            # 上下文相关性
            score += self.context_score(result, query) * 0.1
            
            scored_results.append({**result, "final_score": score})
        
        return sorted(scored_results, key=lambda x: x["final_score"], reverse=True)
```

### 2. 学习排序
```python
class LearningToRank:
    """学习排序"""
    
    def __init__(self):
        self.model = self.load_ltr_model()
    
    def rank(self, query: str, candidates: list) -> list:
        """学习排序"""
        features = [self.extract_features(query, c) for c in candidates]
        scores = self.model.predict(features)
        
        ranked = list(zip(candidates, scores))
        ranked.sort(key=lambda x: x[1], reverse=True)
        
        return [c for c, s in ranked]
```

### 3. 多样性优化
```python
class DiversityOptimizer:
    """多样性优化"""
    
    def optimize(self, results: list, diversity_weight: float = 0.3) -> list:
        """优化结果多样性"""
        selected = []
        remaining = results[:]
        
        while remaining and len(selected) < self.max_results:
            if not selected:
                selected.append(remaining.pop(0))
                continue
            
            # 计算与已选结果的差异
            for r in remaining:
                r["diversity_score"] = self.compute_diversity(r, selected)
            
            # 综合排序
            remaining.sort(
                key=lambda x: x["relevance_score"] * (1 - diversity_weight) +
                             x["diversity_score"] * diversity_weight,
                reverse=True
            )
            
            selected.append(remaining.pop(0))
        
        return selected
```

## 版本
- 版本: V21.0.15
- 创建时间: 2026-04-08
- 状态: ✅ 已实施
