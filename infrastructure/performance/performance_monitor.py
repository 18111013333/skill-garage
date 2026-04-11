#!/usr/bin/env python3
"""
性能监控器
V2.7.0 - 2026-04-10

实时监控所有性能指标
"""

import time
import psutil
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import deque
from datetime import datetime

@dataclass
class MetricPoint:
    """指标数据点"""
    timestamp: float
    value: float
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class PerformanceSnapshot:
    """性能快照"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    disk_io_read_mb: float
    disk_io_write_mb: float
    net_io_sent_mb: float
    net_io_recv_mb: float
    process_count: int
    thread_count: int

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, history_size: int = 1000):
        self._history_size = history_size
        self._metrics: Dict[str, deque] = {}
        self._snapshots: deque = deque(maxlen=history_size)
        self._alerts: List[Dict] = []
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        
        # 阈值配置
        self._thresholds = {
            "cpu_percent": 80,
            "memory_percent": 85,
            "response_time_ms": 100,
            "cache_hit_rate": 0.8,
        }
        
        # 进程信息
        self._process = psutil.Process()
    
    def start_monitoring(self, interval: float = 1.0):
        """开始监控"""
        if self._monitoring:
            return
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self._monitor_thread.start()
    
    def stop_monitoring(self):
        """停止监控"""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
    
    def _monitor_loop(self, interval: float):
        """监控循环"""
        last_disk_io = psutil.disk_io_counters()
        last_net_io = psutil.net_io_counters()
        
        while self._monitoring:
            try:
                # 获取系统指标
                cpu = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                
                # 获取IO指标
                disk_io = psutil.disk_io_counters()
                net_io = psutil.net_io_counters()
                
                # 计算增量
                disk_read = (disk_io.read_bytes - last_disk_io.read_bytes) / 1024 / 1024
                disk_write = (disk_io.write_bytes - last_disk_io.write_bytes) / 1024 / 1024
                net_sent = (net_io.bytes_sent - last_net_io.bytes_sent) / 1024 / 1024
                net_recv = (net_io.bytes_recv - last_net_io.bytes_recv) / 1024 / 1024
                
                last_disk_io = disk_io
                last_net_io = net_io
                
                # 创建快照
                snapshot = PerformanceSnapshot(
                    timestamp=time.time(),
                    cpu_percent=cpu,
                    memory_percent=memory.percent,
                    memory_mb=memory.used / 1024 / 1024,
                    disk_io_read_mb=disk_read,
                    disk_io_write_mb=disk_write,
                    net_io_sent_mb=net_sent,
                    net_io_recv_mb=net_recv,
                    process_count=len(psutil.pids()),
                    thread_count=self._process.num_threads()
                )
                
                self._snapshots.append(snapshot)
                
                # 检查告警
                self._check_alerts(snapshot)
                
                time.sleep(interval)
                
            except Exception as e:
                time.sleep(interval)
    
    def _check_alerts(self, snapshot: PerformanceSnapshot):
        """检查告警"""
        alerts = []
        
        if snapshot.cpu_percent > self._thresholds["cpu_percent"]:
            alerts.append({
                "type": "cpu_high",
                "value": snapshot.cpu_percent,
                "threshold": self._thresholds["cpu_percent"],
                "timestamp": snapshot.timestamp
            })
        
        if snapshot.memory_percent > self._thresholds["memory_percent"]:
            alerts.append({
                "type": "memory_high",
                "value": snapshot.memory_percent,
                "threshold": self._thresholds["memory_percent"],
                "timestamp": snapshot.timestamp
            })
        
        self._alerts.extend(alerts)
        
        # 只保留最近100条告警
        if len(self._alerts) > 100:
            self._alerts = self._alerts[-100:]
    
    def record_metric(self, name: str, value: float, tags: Dict[str, str] = None):
        """记录指标"""
        if name not in self._metrics:
            self._metrics[name] = deque(maxlen=self._history_size)
        
        self._metrics[name].append(MetricPoint(
            timestamp=time.time(),
            value=value,
            tags=tags or {}
        ))
    
    def get_metric_stats(self, name: str, window_seconds: float = 60) -> Dict:
        """获取指标统计"""
        if name not in self._metrics:
            return {"count": 0}
        
        now = time.time()
        values = [
            m.value for m in self._metrics[name]
            if now - m.timestamp <= window_seconds
        ]
        
        if not values:
            return {"count": 0}
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "latest": values[-1]
        }
    
    def get_current_snapshot(self) -> Optional[PerformanceSnapshot]:
        """获取当前快照"""
        if self._snapshots:
            return self._snapshots[-1]
        return None
    
    def get_alerts(self, limit: int = 10) -> List[Dict]:
        """获取告警"""
        return self._alerts[-limit:]
    
    def get_summary(self) -> Dict:
        """获取摘要"""
        snapshot = self.get_current_snapshot()
        
        summary = {
            "monitoring": self._monitoring,
            "snapshot_count": len(self._snapshots),
            "alert_count": len(self._alerts),
            "metrics_count": len(self._metrics),
        }
        
        if snapshot:
            summary.update({
                "cpu_percent": round(snapshot.cpu_percent, 1),
                "memory_percent": round(snapshot.memory_percent, 1),
                "memory_mb": round(snapshot.memory_mb, 1),
                "thread_count": snapshot.thread_count,
            })
        
        return summary
    
    def export_metrics(self) -> Dict:
        """导出所有指标"""
        return {
            name: [
                {"timestamp": m.timestamp, "value": m.value, "tags": m.tags}
                for m in metrics
            ]
            for name, metrics in self._metrics.items()
        }

# 全局单例
_monitor: Optional[PerformanceMonitor] = None

def get_monitor() -> PerformanceMonitor:
    """获取全局监控器"""
    global _monitor
    if _monitor is None:
        _monitor = PerformanceMonitor()
    return _monitor
