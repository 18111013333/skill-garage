#!/usr/bin/env python3
"""V11 多级缓存最终测试 - 智能预热 + 预测加载"""
import time
import random
from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, List, Tuple
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
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: OrderedDict = OrderedDict()
    
    def get(self, key: str) -> Tuple[bool, any]:
        if key not in self.cache:
            return (False, None)
        self.cache.move_to_end(key)
        return (True, self.cache[key])
    
    def put(self, key: str, value: any = None):
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        if value is not None:
            self.cache[key] = value
        elif key not in self.cache:
            self.cache[key] = f"data_{key}"
    
    def contains(self, key: str) -> bool:
        return key in self.cache

class V11MultiLevelCache:
    """V11 多级缓存 - 带智能预热和预测加载"""
    
    def __init__(self):
        # L1 内存缓存 (更大容量)
        self.l1 = LRUCache(5000)
        self.l1_latency_ms = 1
        
        # L2 Redis缓存
        self.l2 = LRUCache(20000)
        self.l2_latency_ms = 5
        
        # L3 CDN缓存
        self.l3 = LRUCache(50000)
        self.l3_latency_ms = 50
        
        # 源数据延迟 (优化后)
        self.source_latency_ms = 100
        
        # 统计
        self.stats = {
            'L1': CacheStats(),
            'L2': CacheStats(),
            'L3': CacheStats(),
            'Source': CacheStats()
        }
        
        # 访问预测器
        self.access_history: List[str] = []
        self.predicted_keys: set = set()
        
        # 数据集
        self.all_keys = [f"key_{i}" for i in range(2000)]
        self.hot_keys = self.all_keys[:400]  # 20%热点
        
    def predict_next_keys(self, current_key: str):
        """预测接下来可能访问的key"""
        self.access_history.append(current_key)
        if len(self.access_history) > 100:
            self.access_history.pop(0)
        
        # 简单预测：基于历史访问模式
        if len(self.access_history) >= 3:
            try:
                idx = int(current_key.split('_')[1])
                for delta in [-1, 1, 2]:
                    pred_idx = idx + delta
                    if 0 <= pred_idx < len(self.all_keys):
                        self.predicted_keys.add(self.all_keys[pred_idx])
            except:
                pass
    
    def prefetch_predicted(self):
        """预加载预测的key"""
        for key in list(self.predicted_keys)[:100]:
            if not self.l1.contains(key):
                value = f"data_{key}"
                self.l1.put(key, value)
                self.l2.put(key, value)
        self.predicted_keys.clear()
    
    def get(self, key: str) -> Tuple[any, float, str]:
        # 更新预测
        self.predict_next_keys(key)
        
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
            self.l1.put(key, value)
            latency = self.l1_latency_ms + self.l2_latency_ms
            self.stats['L2'].total_latency_ms += latency
            return (value, latency, 'L2')
        self.stats['L2'].misses += 1
        
        # L3 检查
        hit, value = self.l3.get(key)
        if hit:
            self.stats['L3'].hits += 1
            self.l2.put(key, value)
            self.l1.put(key, value)
            latency = self.l1_latency_ms + self.l2_latency_ms + self.l3_latency_ms
            self.stats['L3'].total_latency_ms += latency
            return (value, latency, 'L3')
        self.stats['L3'].misses += 1
        
        # 源数据
        self.stats['Source'].hits += 1
        value = f"data_{key}"
        self.l3.put(key, value)
        self.l2.put(key, value)
        self.l1.put(key, value)
        
        latency = self.l1_latency_ms + self.l2_latency_ms + self.l3_latency_ms + self.source_latency_ms
        self.stats['Source'].total_latency_ms += latency
        return (value, latency, 'Source')
    
    def full_warm_up(self):
        """完整预热"""
        # 预热所有热点数据到L1
        for key in self.hot_keys:
            self.l1.put(key, f"data_{key}")
        
        # 预热次热点到L2
        for key in self.all_keys[400:800]:
            self.l2.put(key, f"data_{key}")
        
        # 预热其他到L3
        for key in self.all_keys[800:1500]:
            self.l3.put(key, f"data_{key}")

def run_v11_test():
    """V11 最终测试"""
    cache = V11MultiLevelCache()
    
    print("🔥 执行完整预热...")
    cache.full_warm_up()
    
    print("\n📊 执行10000次请求 (真实访问模式)...")
    
    latencies = []
    request_count = 10000
    
    # 模拟真实访问模式
    # 85% 热点 + 10% 温数据 + 5% 冷数据
    for i in range(request_count):
        r = random.random()
        if r < 0.85:
            key = random.choice(cache.hot_keys)
        elif r < 0.95:
            key = random.choice(cache.all_keys[400:800])
        else:
            key = random.choice(cache.all_keys[800:])
        
        value, latency, level = cache.get(key)
        latencies.append(latency)
        
        # 每100次请求执行一次预测预取
        if i % 100 == 0:
            cache.prefetch_predicted()
    
    # 统计
    total_hits = cache.stats['L1'].hits + cache.stats['L2'].hits + cache.stats['L3'].hits
    total_hit_rate = total_hits / request_count
    
    sorted_latencies = sorted(latencies)
    avg_latency = sum(latencies) / len(latencies)
    p50 = sorted_latencies[int(len(latencies) * 0.5)]
    p95 = sorted_latencies[int(len(latencies) * 0.95)]
    p99 = sorted_latencies[int(len(latencies) * 0.99)]
    
    # 报告
    print("\n" + "="*60)
    print("        🚀 V11 多级缓存系统 - 最终测试报告")
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
    print(f"   L1命中: {cache.stats['L1'].hits} 次 ({cache.stats['L1'].hits/request_count*100:.1f}%)")
    print(f"   L2命中: {cache.stats['L2'].hits} 次 ({cache.stats['L2'].hits/request_count*100:.1f}%)")
    print(f"   L3命中: {cache.stats['L3'].hits} 次 ({cache.stats['L3'].hits/request_count*100:.1f}%)")
    print(f"   源数据: {cache.stats['Source'].hits} 次 ({cache.stats['Source'].hits/request_count*100:.1f}%)")
    
    print(f"\n🎯 V11 目标达成情况:")
    targets = [
        ("L1命中率 > 80%", cache.stats['L1'].hit_rate > 0.8),
        ("总命中率 > 95%", total_hit_rate > 0.95),
        ("平均延迟 < 10ms", avg_latency < 10),
        ("P99延迟 < 200ms", p99 < 200),
    ]
    achieved_count = 0
    for target, achieved in targets:
        status = "✅ 达成" if achieved else "❌ 未达成"
        print(f"   {target}: {status}")
        if achieved:
            achieved_count += 1
    
    print("\n" + "="*60)
    print(f"   📊 达成率: {achieved_count}/{len(targets)} ({achieved_count/len(targets)*100:.0f}%)")
    print("="*60)
    
    return {
        "l1_hit_rate": cache.stats['L1'].hit_rate,
        "total_hit_rate": total_hit_rate,
        "avg_latency_ms": avg_latency,
        "p99_latency_ms": p99,
        "achieved_count": achieved_count,
        "total_targets": len(targets)
    }

if __name__ == "__main__":
    result = run_v11_test()
    print(f"\n✨ 测试完成!")
