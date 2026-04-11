#!/usr/bin/env python3
"""
history - V4.3.2 融合版

融合自:
- memory_context/search/history.py
- memory_context/vector/history.py

此模块为统一实现，其他位置通过兼容层引用
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque

@dataclass
class HistoryEntry:
    """历史条目"""
    query: str
    result: Any
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

class SearchHistory:
    """搜索历史"""
    
    def __init__(self, max_size: int = 100):
        self._history: deque = deque(maxlen=max_size)
    
    def add(self, query: str, result: Any, metadata: Dict[str, Any] = None):
        """添加历史"""
        self._history.append(HistoryEntry(query, result, metadata=metadata or {}))
    
    def get_recent(self, n: int = 10) -> List[HistoryEntry]:
        """获取最近的历史"""
        return list(self._history)[-n:]
    
    def search(self, query: str) -> List[HistoryEntry]:
        """搜索历史"""
        return [h for h in self._history if query.lower() in h.query.lower()]
    
    def clear(self):
        """清空历史"""
        self._history.clear()

# 全局实例
_history: Optional[SearchHistory] = None

def get_history() -> SearchHistory:
    global _history
    if _history is None:
        _history = SearchHistory()
    return _history
