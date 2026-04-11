#!/usr/bin/env python3
"""
层间调用缓存
V2.7.0 - 2026-04-10
多级缓存系统
"""

import time
import hashlib
from typing import Any, Dict, Optional, Tuple
from dataclasses import dataclass
from threading import RLock

@dataclass
class CacheEntry:
    """缓存条目"""
    value: Any
    created_at: float
    ttl: float
    hits: int = 0
    size_bytes: int = 0

class LayerCache:
    """多级缓存"""
    
    def __init__(self, max_size_mb: float = 100):
        self._l1_cache: Dict[str, CacheEntry] = {}  # 热数据
        self._l2_cache: Dict[str, CacheEntry] = {}  # 温数据
        self._l3_cache: Dict[str, CacheEntry] = {}  # 冷数据
        
        self._lock = RLock()
        self._max_size_bytes = int(max_size_mb * 1024 * 1024)
        
        # 缓存层级配置
        self._l1_ttl = 60       # 1分钟
        self._l2_ttl = 300      # 5分钟
        self._l3_ttl = 3600     # 1小时
        
        self._l1_max = 0.1      # 10%
        self._l2_max = 0.3      # 30%
        self._l3_max = 0.6      # 60%
    
    def _hash_key(self, key: str) -> str:
        """生成哈希键"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _estimate_size(self, value: Any) -> int:
        """估算数据大小"""
        try:
            return len(str(value))
        except:
            return 100  # 默认100字节
    
    def _current_size(self, cache: Dict) -> int:
        """计算缓存大小"""
        return sum(e.size_bytes for e in cache.values())
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        hashed = self._hash_key(key)
        
        with self._lock:
            # L1 查找
            if hashed in self._l1_cache:
                entry = self._l1_cache[hashed]
                if time.time() - entry.created_at < entry.ttl:
                    entry.hits += 1
                    return entry.value
                else:
                    del self._l1_cache[hashed]
            
            # L2 查找
            if hashed in self._l2_cache:
                entry = self._l2_cache[hashed]
                if time.time() - entry.created_at < entry.ttl:
                    # 提升到 L1
                    entry.hits += 1
                    self._l1_cache[hashed] = entry
                    del self._l2_cache[hashed]
                    return entry.value
                else:
                    del self._l2_cache[hashed]
            
            # L3 查找
            if hashed in self._l3_cache:
                entry = self._l3_cache[hashed]
                if time.time() - entry.created_at < entry.ttl:
                    # 提升到 L2
                    entry.hits += 1
                    self._l2_cache[hashed] = entry
                    del self._l3_cache[hashed]
                    return entry.value
                else:
                    del self._l3_cache[hashed]
            
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None):
        """设置缓存"""
        hashed = self._hash_key(key)
        size = self._estimate_size(value)
        
        with self._lock:
            entry = CacheEntry(
                value=value,
                created_at=time.time(),
                ttl=ttl or self._l1_ttl,
                size_bytes=size
            )
            
            # 根据大小决定放入哪一级
            if size < 1024:  # < 1KB
                self._l1_cache[hashed] = entry
                self._evict_l1()
            elif size < 10240:  # < 10KB
                self._l2_cache[hashed] = entry
                self._evict_l2()
            else:
                self._l3_cache[hashed] = entry
                self._evict_l3()
    
    def _evict_l1(self):
        """L1 淘汰"""
        max_bytes = self._max_size_bytes * self._l1_max
        while self._current_size(self._l1_cache) > max_bytes:
            if not self._l1_cache:
                break
            # LRU 淘汰
            oldest = min(self._l1_cache.items(), key=lambda x: x[1].created_at)
            del self._l1_cache[oldest[0]]
    
    def _evict_l2(self):
        """L2 淘汰"""
        max_bytes = self._max_size_bytes * self._l2_max
        while self._current_size(self._l2_cache) > max_bytes:
            if not self._l2_cache:
                break
            oldest = min(self._l2_cache.items(), key=lambda x: x[1].created_at)
            # 降级到 L3
            self._l3_cache[oldest[0]] = oldest[1]
            del self._l2_cache[oldest[0]]
    
    def _evict_l3(self):
        """L3 淘汰"""
        max_bytes = self._max_size_bytes * self._l3_max
        while self._current_size(self._l3_cache) > max_bytes:
            if not self._l3_cache:
                break
            oldest = min(self._l3_cache.items(), key=lambda x: x[1].created_at)
            del self._l3_cache[oldest[0]]
    
    def invalidate(self, key: str):
        """使缓存失效"""
        hashed = self._hash_key(key)
        with self._lock:
            self._l1_cache.pop(hashed, None)
            self._l2_cache.pop(hashed, None)
            self._l3_cache.pop(hashed, None)
    
    def clear(self):
        """清空缓存"""
        with self._lock:
            self._l1_cache.clear()
            self._l2_cache.clear()
            self._l3_cache.clear()
    
    def get_stats(self) -> Dict:
        """获取统计"""
        with self._lock:
            total_hits = sum(e.hits for e in self._l1_cache.values())
            total_hits += sum(e.hits for e in self._l2_cache.values())
            total_hits += sum(e.hits for e in self._l3_cache.values())
            
            return {
                "l1": {
                    "count": len(self._l1_cache),
                    "size_bytes": self._current_size(self._l1_cache)
                },
                "l2": {
                    "count": len(self._l2_cache),
                    "size_bytes": self._current_size(self._l2_cache)
                },
                "l3": {
                    "count": len(self._l3_cache),
                    "size_bytes": self._current_size(self._l3_cache)
                },
                "total_hits": total_hits
            }

# 全局单例
_layer_cache: Optional[LayerCache] = None

def get_layer_cache() -> LayerCache:
    """获取全局缓存"""
    global _layer_cache
    if _layer_cache is None:
        _layer_cache = LayerCache()
    return _layer_cache

def cache_get(key: str) -> Optional[Any]:
    """缓存获取（便捷函数）"""
    return get_layer_cache().get(key)

def cache_set(key: str, value: Any, ttl: Optional[float] = None):
    """缓存设置（便捷函数）"""
    get_layer_cache().set(key, value, ttl)
