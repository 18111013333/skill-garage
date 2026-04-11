#!/usr/bin/env python3
"""多级缓存命中率测试脚本"""
import time
import random
import hashlib
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional
import json

@dataclass
class CacheStats:
    """缓存统计"""
    hits: int = 0
    misses: int = 0
    total_latency_ms: float = 0
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0
    
    @property
    def avg_latency_ms(self) -> float:
        total = self.hits + self.misses
        return self.total_latency_ms / total if total > 0 else 0

class MultiLevelCache:
    """多级缓存模拟器"""
    
    def __init__(self):
        # L1 内存缓存
        self.l1_cache: Dict[str, any] = {}
        self.l1_max_size = 1000
        self.l1_latency_ms = 1
        
        # L2 Redis缓存
        self.l2_cache: Dict[str, any] = {}
        self.l2_max_size = 5000
        self.l2_latency_ms = 5
        
        # L3 CDN缓存
        self.l3_cache: Dict[str, any] = {}
        self.l3_max_size = 10000
        self.l3_latency_ms = 50
        
        # 源数据延迟
        self.source_latency_ms = 500
        
        # 统计
        self.stats = {
            'L1': CacheStats(),
            'L2': CacheStats(),
            'L3': CacheStats(),
            'Source': CacheStats()
        }
        
        # 热点数据模拟
        self.hot_keys = [f"hot_key_{i}" for i in range(50)]
        self.warm_keys = [f"warm_key_{i}" for i in range(200)]
        self.cold_keys = [f"cold_key_{i}" for i in range(750)]
        
    def _get_key_type(self, key: str) -> str:
        if key in self.hot_keys:
            return 'hot'
        elif key in self.warm_keys:
            return 'warm'
        else:
            return 'cold'
    
    def _simulate_lru_eviction(self, cache: Dict, max_size: int):
        if len(cache) >= max_size:
            # 简单LRU：删除最早的key
            oldest_key = next(iter(cache))
            del cache[oldest_key]
    
    def get(self, key: str) -> tuple:
        """获取缓存，返回 (value, latency_ms, level)"""
        
        # L1 检查
        if key in self.l1_cache:
            self.stats['L1'].hits += 1
            self.stats['L1'].total_latency_ms += self.l1_latency_ms
            return (self.l1_cache[key], self.l1_latency_ms, 'L1')
        
        self.stats['L1'].misses += 1
        
        # L2 检查
        if key in self.l2_cache:
            self.stats['L2'].hits += 1
            self.stats['L2'].total_latency_ms += self.l2_latency_ms
            # 提升到L1
            self._simulate_lru_eviction(self.l1_cache, self.l1_max_size)
            self.l1_cache[key] = self.l2_cache[key]
            total_latency = self.l1_latency_ms + self.l2_latency_ms
            self.stats['L2'].total_latency_ms += total_latency
            return (self.l2_cache[key], total_latency, 'L2')
        
        self.stats['L2'].misses += 1
        
        # L3 检查
        if key in self.l3_cache:
            self.stats['L3'].hits += 1
            self.stats['L3'].total_latency_ms += self.l3_latency_ms
            # 提升到L2和L1
            self._simulate_lru_eviction(self.l2_cache, self.l2_max_size)
            self.l2_cache[key] = self.l3_cache[key]
            self._simulate_lru_eviction(self.l1_cache, self.l1_max_size)
            self.l1_cache[key] = self.l3_cache[key]
            total_latency = self.l1_latency_ms + self.l2_latency_ms + self.l3_latency_ms
            self.stats['L3'].total_latency_ms += total_latency
            return (self.l3_cache[key], total_latency, 'L3')
        
        self.stats['L3'].misses += 1
        
        # 源数据获取
        self.stats['Source'].hits += 1
        value = f"value_for_{key}"
        
        # 写入各级缓存
        self._simulate_lru_eviction(self.l3_cache, self.l3_max_size)
        self.l3_cache[key] = value
        self._simulate_lru_eviction(self.l2_cache, self.l2_max_size)
        self.l2_cache[key] = value
        self._simulate_lru_eviction(self.l1_cache, self.l1_max_size)
        self.l1_cache[key] = value
        
        total_latency = self.l1_latency_ms + self.l2_latency_ms + self.l3_latency_ms + self.source_latency_ms
        self.stats['Source'].total_latency_ms += total_latency
        
        return (value, total_latency, 'Source')
    
    def warm_up(self):
        """预热热点数据"""
        for key in self.hot_keys:
            self.get(key)
        for key in self.warm_keys[:100]:
            self.get(key)

def run_cache_test():
    """运行缓存测试"""
    cache = MultiLevelCache()
    
    # 预热
    print("🔥 预热缓存...")
    cache.warm_up()
    
    # 模拟真实访问模式
    print("\n📊 模拟访问模式 (10000次请求)...")
    
    requests = []
    for _ in range(10000):
        r = random.random()
        if r < 0.6:  # 60% 热点数据
            key = random.choice(cache.hot_keys)
        elif r < 0.85:  # 25% 温数据
            key = random.choice(cache.warm_keys)
        else:  # 15% 冷数据
            key = random.choice(cache.cold_keys)
        requests.append(key)
    
    # 执行请求
    latencies = []
    for key in requests:
        value, latency, level = cache.get(key)
        latencies.append(latency)
    
    # 计算结果
    total_requests = len(requests)
    total_hits = cache.stats['L1'].hits + cache.stats['L2'].hits + cache.stats['L3'].hits
    total_hit_rate = total_hits / total_requests
    
    avg_latency = sum(latencies) / len(latencies)
    p50 = sorted(latencies)[int(len(latencies) * 0.5)]
    p95 = sorted(latencies)[int(len(latencies) * 0.95)]
    p99 = sorted(latencies)[int(len(latencies) * 0.99)]
    
    # 输出结果
    results = {
        "test_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_requests": total_requests,
        "hit_rates": {
            "L1_内存缓存": f"{cache.stats['L1'].hit_rate*100:.1f}%",
            "L2_Redis缓存": f"{cache.stats['L2'].hit_rate*100:.1f}%",
            "L3_CDN缓存": f"{cache.stats['L3'].hit_rate*100:.1f}%",
            "总命中率": f"{total_hit_rate*100:.1f}%"
        },
        "latency": {
            "平均延迟": f"{avg_latency:.2f}ms",
            "P50延迟": f"{p50:.2f}ms",
            "P95延迟": f"{p95:.2f}ms",
            "P99延迟": f"{p99:.2f}ms"
        },
        "cache_distribution": {
            "L1命中数": cache.stats['L1'].hits,
            "L2命中数": cache.stats['L2'].hits,
            "L3命中数": cache.stats['L3'].hits,
            "源数据获取": cache.stats['Source'].hits
        },
        "target_achievement": {
            "L1命中率目标>80%": "✅ 达成" if cache.stats['L1'].hit_rate > 0.8 else "❌ 未达成",
            "总命中率目标>95%": "✅ 达成" if total_hit_rate > 0.95 else "❌ 未达成",
            "平均延迟目标<10ms": "✅ 达成" if avg_latency < 10 else "❌ 未达成",
            "P99延迟目标<200ms": "✅ 达成" if p99 < 200 else "❌ 未达成"
        }
    }
    
    print("\n" + "="*60)
    print("           多级缓存系统测试报告")
    print("="*60)
    print(f"\n📈 命中率统计:")
    for k, v in results["hit_rates"].items():
        print(f"   {k}: {v}")
    
    print(f"\n⏱️  延迟统计:")
    for k, v in results["latency"].items():
        print(f"   {k}: {v}")
    
    print(f"\n📊 缓存分布:")
    for k, v in results["cache_distribution"].items():
        print(f"   {k}: {v}")
    
    print(f"\n🎯 目标达成:")
    for k, v in results["target_achievement"].items():
        print(f"   {k}: {v}")
    
    print("\n" + "="*60)
    
    return results

if __name__ == "__main__":
    results = run_cache_test()
    print("\n📄 测试完成!")
