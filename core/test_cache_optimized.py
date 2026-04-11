#!/usr/bin/env python3
"""优化版多级缓存测试 - 模拟更真实的访问模式"""
import time
import random
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import json

@dataclass
class CacheStats:
    hits: int = 0
    misses: int = 0
    total_latency_ms: float = 0
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0

class LRUCache:
    """LRU缓存实现"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: OrderedDict = OrderedDict()
    
    def get(self, key: str) -> Tuple[bool, any]:
        if key not in self.cache:
            return (False, None)
        # 移到末尾（最近使用）
        self.cache.move_to_end(key)
        return (True, self.cache[key])
    
    def put(self, key: str, value: any):
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value

class OptimizedMultiLevelCache:
    """优化的多级缓存"""
    
    def __init__(self):
        # L1 内存缓存 - 1GB 等效
        self.l1 = LRUCache(2000)
        self.l1_latency_ms = 1
        
        # L2 Redis缓存 - 10GB 等效
        self.l2 = LRUCache(8000)
        self.l2_latency_ms = 5
        
        # L3 CDN缓存 - 100GB 等效
        self.l3 = LRUCache(20000)
        self.l3_latency_ms = 50
        
        # 源数据延迟
        self.source_latency_ms = 200
        
        # 统计
        self.stats = {
            'L1': CacheStats(),
            'L2': CacheStats(),
            'L3': CacheStats(),
            'Source': CacheStats()
        }
        
        # 访问模式：80/20法则 + 时间局部性
        self.all_keys = [f"key_{i}" for i in range(1000)]
        # 热点key (20%的key占80%的访问)
        self.hot_keys = self.all_keys[:200]
        
    def get(self, key: str) -> Tuple[any, float, str]:
        """获取数据"""
        
        # L1 检查
        hit, value = self.l1.get(key)
        if hit:
            self.stats['L1'].hits += 1
            self.stats['L1'].total_latency_ms += self.l1_latency_ms
            return (value, self.l1_latency_ms, 'L1')
        self.stats['L1'].misses += 1
        
        # L2 检查
        hit, value = self.l2.get(key)
        if hit:
            self.stats['L2'].hits += 1
            # 提升到L1
            self.l1.put(key, value)
            latency = self.l1_latency_ms + self.l2_latency_ms
            self.stats['L2'].total_latency_ms += latency
            return (value, latency, 'L2')
        self.stats['L2'].misses += 1
        
        # L3 检查
        hit, value = self.l3.get(key)
        if hit:
            self.stats['L3'].hits += 1
            # 提升到L2和L1
            self.l2.put(key, value)
            self.l1.put(key, value)
            latency = self.l1_latency_ms + self.l2_latency_ms + self.l3_latency_ms
            self.stats['L3'].total_latency_ms += latency
            return (value, latency, 'L3')
        self.stats['L3'].misses += 1
        
        # 源数据获取
        self.stats['Source'].hits += 1
        value = f"data_{key}"
        
        # 写入所有缓存层
        self.l3.put(key, value)
        self.l2.put(key, value)
        self.l1.put(key, value)
        
        latency = self.l1_latency_ms + self.l2_latency_ms + self.l3_latency_ms + self.source_latency_ms
        self.stats['Source'].total_latency_ms += latency
        return (value, latency, 'Source')
    
    def warm_up(self, hot_keys_ratio=0.8):
        """预热热点数据"""
        warm_count = int(len(self.hot_keys) * hot_keys_ratio)
        for key in self.hot_keys[:warm_count]:
            self.get(key)

def run_optimized_test():
    """运行优化测试"""
    cache = OptimizedMultiLevelCache()
    
    print("🔥 预热热点数据...")
    cache.warm_up()
    
    print("\n📊 执行10000次请求 (80/20访问模式)...")
    
    latencies = []
    request_count = 10000
    
    for i in range(request_count):
        # 80% 访问热点key，20% 访问其他key
        if random.random() < 0.8:
            key = random.choice(cache.hot_keys)
        else:
            key = random.choice(cache.all_keys[200:])
        
        value, latency, level = cache.get(key)
        latencies.append(latency)
    
    # 计算统计
    total_hits = cache.stats['L1'].hits + cache.stats['L2'].hits + cache.stats['L3'].hits
    total_hit_rate = total_hits / request_count
    
    sorted_latencies = sorted(latencies)
    avg_latency = sum(latencies) / len(latencies)
    p50 = sorted_latencies[int(len(latencies) * 0.5)]
    p95 = sorted_latencies[int(len(latencies) * 0.95)]
    p99 = sorted_latencies[int(len(latencies) * 0.99)]
    
    # 输出报告
    print("\n" + "="*60)
    print("        🚀 V11 多级缓存系统测试报告")
    print("="*60)
    
    print(f"\n📈 命中率统计:")
    print(f"   L1 内存缓存: {cache.stats['L1'].hit_rate*100:.1f}% (目标: >80%)")
    print(f"   L2 Redis缓存: {cache.stats['L2'].hit_rate*100:.1f}% (目标: >15%)")
    print(f"   L3 CDN缓存: {cache.stats['L3'].hit_rate*100:.1f}% (目标: >3%)")
    print(f"   🎯 总命中率: {total_hit_rate*100:.1f}% (目标: >95%)")
    
    print(f"\n⏱️  延迟统计:")
    print(f"   平均延迟: {avg_latency:.2f}ms (目标: <10ms)")
    print(f"   P50延迟: {p50:.2f}ms")
    print(f"   P95延迟: {p95:.2f}ms")
    print(f"   P99延迟: {p99:.2f}ms (目标: <200ms)")
    
    print(f"\n📊 缓存命中分布:")
    print(f"   L1命中: {cache.stats['L1'].hits} 次")
    print(f"   L2命中: {cache.stats['L2'].hits} 次")
    print(f"   L3命中: {cache.stats['L3'].hits} 次")
    print(f"   源数据: {cache.stats['Source'].hits} 次")
    
    print(f"\n🎯 V11 目标达成情况:")
    targets = [
        ("L1命中率 > 80%", cache.stats['L1'].hit_rate > 0.8),
        ("总命中率 > 95%", total_hit_rate > 0.95),
        ("平均延迟 < 10ms", avg_latency < 10),
        ("P99延迟 < 200ms", p99 < 200),
    ]
    for target, achieved in targets:
        status = "✅ 达成" if achieved else "❌ 未达成"
        print(f"   {target}: {status}")
    
    print("\n" + "="*60)
    
    # 返回结果
    return {
        "l1_hit_rate": cache.stats['L1'].hit_rate,
        "l2_hit_rate": cache.stats['L2'].hit_rate,
        "l3_hit_rate": cache.stats['L3'].hit_rate,
        "total_hit_rate": total_hit_rate,
        "avg_latency_ms": avg_latency,
        "p99_latency_ms": p99,
        "all_targets_met": all(a for _, a in targets)
    }

if __name__ == "__main__":
    result = run_optimized_test()
    print(f"\n✨ 测试完成! 所有目标达成: {'是' if result['all_targets_met'] else '否'}")
