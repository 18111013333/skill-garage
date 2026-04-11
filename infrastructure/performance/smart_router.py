#!/usr/bin/env python3
"""
智能路由器
V2.7.0 - 2026-04-10

根据负载和性能自动选择最优路由
"""

import time
import random
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

class RouteType(Enum):
    """路由类型"""
    DIRECT = "direct"           # 直连
    CACHED = "cached"           # 缓存
    LOAD_BALANCED = "balanced"  # 负载均衡
    FAILOVER = "failover"       # 故障转移
    CIRCUIT_BREAK = "circuit"   # 熔断

@dataclass
class RouteEndpoint:
    """路由端点"""
    name: str
    handler: Callable
    weight: int = 1
    latency_ms: float = 0
    success_rate: float = 1.0
    last_error: Optional[str] = None
    error_count: int = 0
    total_calls: int = 0

@dataclass
class RouteResult:
    """路由结果"""
    endpoint: str
    route_type: RouteType
    latency_ms: float
    success: bool
    cached: bool = False
    error: Optional[str] = None

class SmartRouter:
    """智能路由器"""
    
    def __init__(self):
        self._routes: Dict[str, List[RouteEndpoint]] = defaultdict(list)
        self._cache: Dict[str, Any] = {}
        self._cache_ttl: Dict[str, float] = {}
        self._circuit_breaker: Dict[str, Dict] = {}
        self._stats = {
            "total_calls": 0,
            "cache_hits": 0,
            "failovers": 0,
            "circuit_breaks": 0,
        }
        
        # 配置
        self._config = {
            "cache_ttl": 300,
            "circuit_break_threshold": 5,
            "circuit_break_timeout": 60,
            "max_latency_ms": 1000,
            "retry_count": 3,
        }
    
    def register(self, route_name: str, handler: Callable, weight: int = 1):
        """注册路由"""
        endpoint = RouteEndpoint(
            name=f"{route_name}_{len(self._routes[route_name])}",
            handler=handler,
            weight=weight
        )
        self._routes[route_name].append(endpoint)
    
    def route(self, route_name: str, *args, **kwargs) -> RouteResult:
        """智能路由"""
        start = time.perf_counter()
        self._stats["total_calls"] += 1
        
        # 1. 检查缓存
        cache_key = self._make_cache_key(route_name, args, kwargs)
        if cache_key in self._cache:
            if time.time() < self._cache_ttl.get(cache_key, 0):
                self._stats["cache_hits"] += 1
                return RouteResult(
                    endpoint="cache",
                    route_type=RouteType.CACHED,
                    latency_ms=(time.perf_counter() - start) * 1000,
                    success=True,
                    cached=True
                )
        
        # 2. 获取可用端点
        endpoints = self._get_available_endpoints(route_name)
        if not endpoints:
            return RouteResult(
                endpoint="none",
                route_type=RouteType.CIRCUIT_BREAK,
                latency_ms=(time.perf_counter() - start) * 1000,
                success=False,
                error="No available endpoints"
            )
        
        # 3. 选择最优端点
        endpoint = self._select_endpoint(endpoints)
        
        # 4. 执行调用
        result = self._execute_with_retry(endpoint, args, kwargs)
        
        # 5. 缓存结果
        if result.success:
            self._cache[cache_key] = result
            self._cache_ttl[cache_key] = time.time() + self._config["cache_ttl"]
        
        return result
    
    def _make_cache_key(self, route_name: str, args, kwargs) -> str:
        """生成缓存键"""
        return f"{route_name}:{hash(str(args) + str(kwargs))}"
    
    def _get_available_endpoints(self, route_name: str) -> List[RouteEndpoint]:
        """获取可用端点"""
        all_endpoints = self._routes.get(route_name, [])
        available = []
        
        for ep in all_endpoints:
            # 检查熔断状态
            cb_state = self._circuit_breaker.get(ep.name, {})
            if cb_state.get("open", False):
                # 检查是否可以恢复
                if time.time() - cb_state.get("opened_at", 0) > self._config["circuit_break_timeout"]:
                    # 半开状态，允许尝试
                    available.append(ep)
                continue
            
            available.append(ep)
        
        return available
    
    def _select_endpoint(self, endpoints: List[RouteEndpoint]) -> RouteEndpoint:
        """选择端点（加权随机 + 最小延迟）"""
        if len(endpoints) == 1:
            return endpoints[0]
        
        # 计算权重（考虑延迟和成功率）
        weights = []
        for ep in endpoints:
            # 基础权重
            w = ep.weight
            
            # 延迟惩罚
            if ep.latency_ms > 0:
                w *= max(0.1, 1 - ep.latency_ms / self._config["max_latency_ms"])
            
            # 成功率奖励
            w *= ep.success_rate
            
            weights.append(max(0.1, w))
        
        # 加权随机选择
        total = sum(weights)
        r = random.uniform(0, total)
        
        cumulative = 0
        for i, w in enumerate(weights):
            cumulative += w
            if r <= cumulative:
                return endpoints[i]
        
        return endpoints[-1]
    
    def _execute_with_retry(self, endpoint: RouteEndpoint, args, kwargs) -> RouteResult:
        """带重试的执行"""
        start = time.perf_counter()
        last_error = None
        
        for attempt in range(self._config["retry_count"]):
            try:
                result = endpoint.handler(*args, **kwargs)
                
                # 更新端点统计
                latency = (time.perf_counter() - start) * 1000
                endpoint.latency_ms = (endpoint.latency_ms + latency) / 2
                endpoint.total_calls += 1
                endpoint.success_rate = (
                    endpoint.success_rate * 0.9 + 0.1
                )
                
                # 重置熔断状态
                if endpoint.name in self._circuit_breaker:
                    self._circuit_breaker[endpoint.name]["open"] = False
                
                return RouteResult(
                    endpoint=endpoint.name,
                    route_type=RouteType.DIRECT,
                    latency_ms=latency,
                    success=True
                )
                
            except Exception as e:
                last_error = str(e)
                endpoint.error_count += 1
                endpoint.last_error = last_error
                endpoint.success_rate = (
                    endpoint.success_rate * 0.9
                )
                
                # 检查是否需要熔断
                if endpoint.error_count >= self._config["circuit_break_threshold"]:
                    self._circuit_breaker[endpoint.name] = {
                        "open": True,
                        "opened_at": time.time(),
                        "error": last_error
                    }
                    self._stats["circuit_breaks"] += 1
                    break
        
        # 所有重试失败
        return RouteResult(
            endpoint=endpoint.name,
            route_type=RouteType.FAILOVER,
            latency_ms=(time.perf_counter() - start) * 1000,
            success=False,
            error=last_error
        )
    
    def get_stats(self) -> Dict:
        """获取统计"""
        total = self._stats["total_calls"]
        return {
            **self._stats,
            "cache_hit_rate": self._stats["cache_hits"] / total if total > 0 else 0,
            "routes": {
                name: [
                    {
                        "name": ep.name,
                        "latency_ms": round(ep.latency_ms, 2),
                        "success_rate": round(ep.success_rate, 3),
                        "total_calls": ep.total_calls,
                        "error_count": ep.error_count,
                    }
                    for ep in endpoints
                ]
                for name, endpoints in self._routes.items()
            }
        }
    
    def clear_cache(self):
        """清理缓存"""
        self._cache.clear()
        self._cache_ttl.clear()
    
    def reset_circuit_breakers(self):
        """重置熔断器"""
        self._circuit_breaker.clear()

# 全局单例
_router: Optional[SmartRouter] = None

def get_router() -> SmartRouter:
    """获取全局路由器"""
    global _router
    if _router is None:
        _router = SmartRouter()
    return _router
