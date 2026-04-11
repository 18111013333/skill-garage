"""性能监控模块 - V1.0.0"""

import time
import json
from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import statistics

@dataclass
class MetricRecord:
    """指标记录"""
    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class PerformanceStats:
    """性能统计"""
    count: int = 0
    total: float = 0.0
    min_val: float = float('inf')
    max_val: float = 0.0
    values: List[float] = field(default_factory=list)
    
    def add(self, value: float):
        self.count += 1
        self.total += value
        self.min_val = min(self.min_val, value)
        self.max_val = max(self.max_val, value)
        self.values.append(value)
        # 保留最近1000个值
        if len(self.values) > 1000:
            self.values = self.values[-1000:]
    
    @property
    def avg(self) -> float:
        return self.total / self.count if self.count > 0 else 0
    
    @property
    def p50(self) -> float:
        return statistics.median(self.values) if self.values else 0
    
    @property
    def p95(self) -> float:
        if not self.values:
            return 0
        sorted_vals = sorted(self.values)
        idx = int(len(sorted_vals) * 0.95)
        return sorted_vals[min(idx, len(sorted_vals) - 1)]
    
    @property
    def p99(self) -> float:
        if not self.values:
            return 0
        sorted_vals = sorted(self.values)
        idx = int(len(sorted_vals) * 0.99)
        return sorted_vals[min(idx, len(sorted_vals) - 1)]

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.metrics: Dict[str, PerformanceStats] = defaultdict(PerformanceStats)
        self.start_times: Dict[str, float] = {}
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.cache_stats = {"hits": 0, "misses": 0}
    
    def start_timer(self, name: str):
        """开始计时"""
        self.start_times[name] = time.time()
    
    def stop_timer(self, name: str) -> float:
        """停止计时并记录"""
        if name not in self.start_times:
            return 0
        elapsed = (time.time() - self.start_times[name]) * 1000  # ms
        self.metrics[name].add(elapsed)
        del self.start_times[name]
        return elapsed
    
    def record(self, name: str, value: float, tags: Dict = None):
        """记录指标"""
        self.metrics[name].add(value)
    
    def record_error(self, error_type: str):
        """记录错误"""
        self.error_counts[error_type] += 1
    
    def record_cache_hit(self):
        """记录缓存命中"""
        self.cache_stats["hits"] += 1
    
    def record_cache_miss(self):
        """记录缓存未命中"""
        self.cache_stats["misses"] += 1
    
    @property
    def cache_hit_rate(self) -> float:
        total = self.cache_stats["hits"] + self.cache_stats["misses"]
        return self.cache_stats["hits"] / total if total > 0 else 0
    
    def get_stats(self, name: str) -> Dict:
        """获取统计"""
        stats = self.metrics.get(name)
        if not stats:
            return {}
        return {
            "count": stats.count,
            "avg_ms": round(stats.avg, 2),
            "min_ms": round(stats.min_val, 2),
            "max_ms": round(stats.max_val, 2),
            "p50_ms": round(stats.p50, 2),
            "p95_ms": round(stats.p95, 2),
            "p99_ms": round(stats.p99, 2)
        }
    
    def get_all_stats(self) -> Dict:
        """获取所有统计"""
        return {
            "metrics": {name: self.get_stats(name) for name in self.metrics},
            "errors": dict(self.error_counts),
            "cache": {
                "hits": self.cache_stats["hits"],
                "misses": self.cache_stats["misses"],
                "hit_rate": round(self.cache_hit_rate * 100, 2)
            }
        }
    
    def get_summary(self) -> str:
        """获取摘要报告"""
        stats = self.get_all_stats()
        lines = ["=== 性能监控报告 ===", ""]
        
        # 指标统计
        if stats["metrics"]:
            lines.append("【延迟统计】")
            for name, s in stats["metrics"].items():
                lines.append(f"  {name}:")
                lines.append(f"    次数: {s['count']}")
                lines.append(f"    平均: {s['avg_ms']}ms")
                lines.append(f"    P95: {s['p95_ms']}ms")
                lines.append(f"    P99: {s['p99_ms']}ms")
            lines.append("")
        
        # 缓存统计
        if stats["cache"]["hits"] + stats["cache"]["misses"] > 0:
            lines.append("【缓存统计】")
            lines.append(f"  命中: {stats['cache']['hits']}")
            lines.append(f"  未命中: {stats['cache']['misses']}")
            lines.append(f"  命中率: {stats['cache']['hit_rate']}%")
            lines.append("")
        
        # 错误统计
        if stats["errors"]:
            lines.append("【错误统计】")
            for error_type, count in stats["errors"].items():
                lines.append(f"  {error_type}: {count}")
        
        return "\n".join(lines)

# 全局监控实例
_monitor = None

def get_monitor() -> PerformanceMonitor:
    """获取全局监控实例"""
    global _monitor
    if _monitor is None:
        _monitor = PerformanceMonitor()
    return _monitor
