#!/usr/bin/env python3
"""
内存池管理系统 - 基于小艺收藏技术优化
减少内存分配开销，提升性能
"""

import os
import time
import threading
import numpy as np
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from collections import defaultdict

# 配置
MEMORY_DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass
class MemoryBlock:
    """内存块"""
    data: np.ndarray
    shape: tuple
    dtype: np.dtype
    in_use: bool = False
    last_used: float = 0.0


class MemoryPool:
    """
    内存池管理器
    
    特点：
    - 预分配内存块，减少分配开销
    - 按大小分类管理
    - 自动回收未使用内存
    - 线程安全
    """
    
    def __init__(self, 
                 initial_size: int = 100,  # 初始内存块数量
                 max_size: int = 1000,     # 最大内存块数量
                 gc_interval: float = 60.0,  # GC间隔（秒）
                 gc_threshold: float = 300.0):  # GC阈值（秒）
        
        self.initial_size = initial_size
        self.max_size = max_size
        self.gc_interval = gc_interval
        self.gc_threshold = gc_threshold
        
        # 内存池：shape_key -> List[MemoryBlock]
        self.pools: Dict[str, List[MemoryBlock]] = defaultdict(list)
        self.lock = threading.Lock()
        
        # 统计
        self.stats = {
            'total_allocations': 0,
            'pool_hits': 0,
            'pool_misses': 0,
            'gc_runs': 0,
            'memory_saved': 0
        }
        
        # GC线程
        self.gc_thread: Optional[threading.Thread] = None
        self.running = False
    
    def _shape_key(self, shape: tuple, dtype: np.dtype) -> str:
        """生成形状键"""
        return f"{shape}_{dtype}"
    
    def start(self):
        """启动内存池"""
        self.running = True
        self.gc_thread = threading.Thread(target=self._gc_loop, daemon=True)
        self.gc_thread.start()
    
    def stop(self):
        """停止内存池"""
        self.running = False
        if self.gc_thread:
            self.gc_thread.join(timeout=5)
    
    def _gc_loop(self):
        """GC循环"""
        while self.running:
            time.sleep(self.gc_interval)
            self._garbage_collect()
    
    def _garbage_collect(self):
        """垃圾回收"""
        now = time.time()
        collected = 0
        
        with self.lock:
            for key in list(self.pools.keys()):
                pool = self.pools[key]
                
                # 移除长时间未使用的内存块
                new_pool = []
                for block in pool:
                    if not block.in_use and (now - block.last_used) > self.gc_threshold:
                        collected += 1
                    else:
                        new_pool.append(block)
                
                self.pools[key] = new_pool
        
        if collected > 0:
            self.stats['gc_runs'] += 1
            self.stats['memory_saved'] += collected
    
    def allocate(self, shape: tuple, dtype: np.dtype = np.float32) -> np.ndarray:
        """分配内存"""
        key = self._shape_key(shape, dtype)
        
        with self.lock:
            self.stats['total_allocations'] += 1
            
            # 尝试从池中获取
            pool = self.pools[key]
            for block in pool:
                if not block.in_use:
                    block.in_use = True
                    block.last_used = time.time()
                    self.stats['pool_hits'] += 1
                    return block.data
            
            # 池中没有可用块，创建新的
            self.stats['pool_misses'] += 1
            
            if len(pool) < self.max_size:
                data = np.zeros(shape, dtype=dtype)
                block = MemoryBlock(
                    data=data,
                    shape=shape,
                    dtype=dtype,
                    in_use=True,
                    last_used=time.time()
                )
                pool.append(block)
                return data
            
            # 超过最大限制，直接分配
            return np.zeros(shape, dtype=dtype)
    
    def release(self, data: np.ndarray):
        """释放内存"""
        key = self._shape_key(data.shape, data.dtype)
        
        with self.lock:
            pool = self.pools[key]
            for block in pool:
                if block.data is data:
                    block.in_use = False
                    block.last_used = time.time()
                    return
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self.lock:
            total_blocks = sum(len(pool) for pool in self.pools.values())
            used_blocks = sum(
                sum(1 for block in pool if block.in_use)
                for pool in self.pools.values()
            )
            
            hit_rate = (
                self.stats['pool_hits'] / self.stats['total_allocations'] * 100
                if self.stats['total_allocations'] > 0 else 0
            )
            
            return {
                **self.stats,
                'total_blocks': total_blocks,
                'used_blocks': used_blocks,
                'free_blocks': total_blocks - used_blocks,
                'hit_rate': f"{hit_rate:.2f}%",
                'pool_types': len(self.pools)
            }


class VectorBuffer:
    """向量缓冲区"""
    
    def __init__(self, pool: MemoryPool, dim: int, batch_size: int = 100):
        self.pool = pool
        self.dim = dim
        self.batch_size = batch_size
        
        # 预分配缓冲区
        self.buffer = pool.allocate((batch_size, dim))
        self.current_size = 0
    
    def add(self, vector: np.ndarray) -> int:
        """添加向量，返回索引"""
        if self.current_size >= self.batch_size:
            raise BufferError("缓冲区已满")
        
        self.buffer[self.current_size] = vector
        idx = self.current_size
        self.current_size += 1
        return idx
    
    def get(self, idx: int) -> np.ndarray:
        """获取向量"""
        if idx < 0 or idx >= self.current_size:
            raise IndexError("索引越界")
        return self.buffer[idx]
    
    def clear(self):
        """清空缓冲区"""
        self.current_size = 0
    
    def release(self):
        """释放缓冲区"""
        self.pool.release(self.buffer)


# 测试代码
if __name__ == '__main__':
    print("=== 内存池管理系统测试 ===\n")
    
    # 创建内存池
    pool = MemoryPool(initial_size=50, max_size=200)
    pool.start()
    
    # 测试内存分配
    print("测试内存分配...")
    vectors = []
    
    start = time.time()
    for i in range(100):
        vec = pool.allocate((128,), np.float32)
        vec[:] = np.random.randn(128)
        vectors.append(vec)
    alloc_time = time.time() - start
    print(f"  100次分配耗时: {alloc_time:.4f}秒")
    
    # 测试内存释放和重用
    print("\n测试内存释放和重用...")
    for vec in vectors[:50]:
        pool.release(vec)
    
    start = time.time()
    new_vectors = []
    for i in range(50):
        vec = pool.allocate((128,), np.float32)
        new_vectors.append(vec)
    reuse_time = time.time() - start
    print(f"  50次重用分配耗时: {reuse_time:.4f}秒")
    
    # 测试向量缓冲区
    print("\n测试向量缓冲区...")
    buffer = VectorBuffer(pool, dim=128, batch_size=100)
    
    for i in range(50):
        vec = np.random.randn(128).astype(np.float32)
        buffer.add(vec)
    
    print(f"  缓冲区大小: {buffer.current_size}")
    print(f"  获取向量0: {buffer.get(0)[:5]}...")
    
    # 统计信息
    print("\n=== 内存池统计 ===")
    stats = pool.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 清理
    buffer.release()
    pool.stop()
    
    print("\n内存池管理系统测试完成！")
