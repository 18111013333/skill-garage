"""统一搜索集成 - 混合检索 + 智能路由 + 反馈学习"""
from typing import List, Dict, Optional
from pathlib import Path

from .search import QueryRouter, RRFFusion, DynamicWeights, QueryUnderstanding, QueryRewriter, SemanticDedup, QueryHistory
from .cache import CacheManager
from .feedback import FeedbackLearner

class UnifiedSearch:
    """统一搜索入口"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir or Path.home() / ".openclaw")
        
        # 初始化组件
        self.router = QueryRouter()
        self.rrf = RRFFusion(k=60)
        self.weights = DynamicWeights()
        self.understanding = QueryUnderstanding()
        self.rewriter = QueryRewriter()
        self.dedup = SemanticDedup()
        self.history = QueryHistory(self.base_dir / "cache" / "query_history.json")
        self.cache = CacheManager(self.base_dir / "cache", ttl=3600)
        self.feedback = FeedbackLearner(self.base_dir / "feedback")
    
    def search(self, query: str, use_llm: bool = True, use_cache: bool = True) -> Dict:
        """统一搜索"""
        # 1. 检查缓存
        if use_cache:
            cached = self.cache.get(self._cache_key(query))
            if cached:
                return {"results": cached, "source": "cache", "time_ms": 5}
        
        # 2. 查询理解
        analysis = self.understanding.analyze(query)
        
        # 3. 查询改写
        rewritten = self.rewriter.rewrite(query)
        
        # 4. 智能路由
        mode = self.router.select_mode(query, use_llm)
        
        # 5. 动态权重
        vector_weight, fts_weight = self.weights.calculate(query)
        
        # 6. 执行搜索（由外部提供）
        # vector_results = self._vector_search(rewritten)
        # fts_results = self._fts_search(rewritten)
        
        # 7. RRF 融合
        # fused = self.rrf.fuse(vector_results, fts_results)
        
        # 8. 语义去重
        # deduped = self.dedup.dedup(fused)
        
        # 9. 应用反馈
        # final = self.feedback.apply_feedback(query, deduped)
        
        # 10. 记录历史
        self.history.record(query, mode)
        
        return {
            "query": query,
            "rewritten": rewritten,
            "mode": mode,
            "weights": {"vector": vector_weight, "fts": fts_weight},
            "analysis": analysis,
            "source": "search"
        }
    
    def record_click(self, query: str, result_id: str, position: int):
        """记录点击"""
        self.feedback.record_click(query, result_id, position)
    
    def _cache_key(self, query: str) -> str:
        import hashlib
        return hashlib.md5(query.lower().encode()).hexdigest()[:16]
