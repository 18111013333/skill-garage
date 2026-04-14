#!/usr/bin/env python3
"""
Numba JIT加速系统 - 基于小艺收藏技术优化
使用Numba即时编译加速数值计算
"""

import os
import time
import numpy as np
from typing import List, Tuple

# 尝试导入Numba
try:
    from numba import jit, njit, prange, cuda
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    print("警告: Numba未安装，将使用纯Python实现")


class NumbaAccelerator:
    """
    Numba JIT加速器
    
    特点：
    - 即时编译Python代码
    - 支持CPU和GPU加速
    - 自动并行化
    """
    
    def __init__(self, use_cuda: bool = False):
        self.use_cuda = use_cuda and NUMBA_AVAILABLE and cuda.is_available()
        self.stats = {
            'total_calls': 0,
            'total_time_saved': 0.0
        }
    
    @staticmethod
    def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
        """计算余弦相似度（纯Python版本）"""
        dot = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)


if NUMBA_AVAILABLE:
    # Numba加速版本
    
    @njit(fastmath=True)
    def cosine_similarity_numba(v1: np.ndarray, v2: np.ndarray) -> float:
        """计算余弦相似度（Numba加速）"""
        dot = 0.0
        norm1 = 0.0
        norm2 = 0.0
        n = v1.shape[0]
        
        for i in range(n):
            dot += v1[i] * v2[i]
            norm1 += v1[i] * v1[i]
            norm2 += v2[i] * v2[i]
        
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        
        return dot / (np.sqrt(norm1) * np.sqrt(norm2))
    
    @njit(fastmath=True, parallel=True)
    def batch_cosine_similarity_numba(query: np.ndarray, vectors: np.ndarray) -> np.ndarray:
        """批量计算余弦相似度（Numba并行加速）"""
        n = vectors.shape[0]
        results = np.empty(n, dtype=np.float32)
        
        query_norm = 0.0
        for i in range(query.shape[0]):
            query_norm += query[i] * query[i]
        query_norm = np.sqrt(query_norm)
        
        for i in prange(n):
            dot = 0.0
            vec_norm = 0.0
            for j in range(vectors.shape[1]):
                dot += query[j] * vectors[i, j]
                vec_norm += vectors[i, j] * vectors[i, j]
            vec_norm = np.sqrt(vec_norm)
            
            if query_norm == 0.0 or vec_norm == 0.0:
                results[i] = 0.0
            else:
                results[i] = dot / (query_norm * vec_norm)
        
        return results
    
    @njit(fastmath=True)
    def euclidean_distance_numba(v1: np.ndarray, v2: np.ndarray) -> float:
        """计算欧氏距离（Numba加速）"""
        dist = 0.0
        n = v1.shape[0]
        
        for i in range(n):
            diff = v1[i] - v2[i]
            dist += diff * diff
        
        return np.sqrt(dist)
    
    @njit(fastmath=True, parallel=True)
    def top_k_indices_numba(arr: np.ndarray, k: int) -> np.ndarray:
        """获取Top-K索引（Numba加速）"""
        n = arr.shape[0]
        k = min(k, n)
        indices = np.empty(k, dtype=np.int64)
        
        # 简单选择排序找Top-K
        for i in range(k):
            max_idx = 0
            max_val = arr[0]
            for j in range(1, n):
                if arr[j] > max_val:
                    max_val = arr[j]
                    max_idx = j
            indices[i] = max_idx
            arr[max_idx] = -np.inf  # 标记为已选
        
        return indices
    
    @njit(fastmath=True)
    def normalize_vector_numba(v: np.ndarray) -> np.ndarray:
        """向量归一化（Numba加速）"""
        norm = 0.0
        n = v.shape[0]
        result = np.empty(n, dtype=np.float32)
        
        for i in range(n):
            norm += v[i] * v[i]
        norm = np.sqrt(norm)
        
        if norm == 0.0:
            for i in range(n):
                result[i] = 0.0
        else:
            for i in range(n):
                result[i] = v[i] / norm
        
        return result

else:
    # 纯Python回退版本
    def cosine_similarity_numba(v1, v2):
        return NumbaAccelerator.cosine_similarity(v1, v2)
    
    def batch_cosine_similarity_numba(query, vectors):
        return np.array([NumbaAccelerator.cosine_similarity(query, v) for v in vectors])
    
    def euclidean_distance_numba(v1, v2):
        return np.linalg.norm(v1 - v2)
    
    def top_k_indices_numba(arr, k):
        return np.argsort(arr)[-k:][::-1]
    
    def normalize_vector_numba(v):
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        return v / norm


class VectorOperations:
    """向量操作加速类"""
    
    @staticmethod
    def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
        """计算余弦相似度"""
        return cosine_similarity_numba(v1.astype(np.float32), v2.astype(np.float32))
    
    @staticmethod
    def batch_cosine_similarity(query: np.ndarray, vectors: np.ndarray) -> np.ndarray:
        """批量计算余弦相似度"""
        return batch_cosine_similarity_numba(
            query.astype(np.float32), 
            vectors.astype(np.float32)
        )
    
    @staticmethod
    def euclidean_distance(v1: np.ndarray, v2: np.ndarray) -> float:
        """计算欧氏距离"""
        return euclidean_distance_numba(v1.astype(np.float32), v2.astype(np.float32))
    
    @staticmethod
    def top_k_indices(arr: np.ndarray, k: int) -> np.ndarray:
        """获取Top-K索引"""
        arr_copy = arr.copy()
        return top_k_indices_numba(arr_copy, k)
    
    @staticmethod
    def normalize(v: np.ndarray) -> np.ndarray:
        """向量归一化"""
        return normalize_vector_numba(v.astype(np.float32))


# 测试代码
if __name__ == '__main__':
    print("=== Numba JIT加速系统测试 ===\n")
    
    # 生成测试数据
    dim = 128
    n_vectors = 1000
    
    print(f"生成测试数据: {n_vectors}个{dim}维向量...")
    vectors = np.random.randn(n_vectors, dim).astype(np.float32)
    query = np.random.randn(dim).astype(np.float32)
    
    # 归一化
    print("归一化向量...")
    vectors = np.array([VectorOperations.normalize(v) for v in vectors])
    query = VectorOperations.normalize(query)
    
    # 测试单个相似度计算
    print("\n测试单个相似度计算...")
    start = time.time()
    for _ in range(1000):
        sim = VectorOperations.cosine_similarity(query, vectors[0])
    single_time = time.time() - start
    print(f"  1000次计算耗时: {single_time:.4f}秒")
    print(f"  相似度: {sim:.4f}")
    
    # 测试批量相似度计算
    print("\n测试批量相似度计算...")
    start = time.time()
    similarities = VectorOperations.batch_cosine_similarity(query, vectors)
    batch_time = time.time() - start
    print(f"  {n_vectors}个向量耗时: {batch_time:.4f}秒")
    print(f"  平均每个向量: {batch_time/n_vectors*1000:.4f}毫秒")
    
    # 测试Top-K
    print("\n测试Top-K索引...")
    start = time.time()
    top_k = VectorOperations.top_k_indices(similarities, 10)
    topk_time = time.time() - start
    print(f"  Top-10耗时: {topk_time*1000:.4f}毫秒")
    print(f"  Top-10索引: {top_k}")
    print(f"  Top-10相似度: {similarities[top_k]}")
    
    # 统计信息
    print("\n=== 系统信息 ===")
    print(f"Numba可用: {NUMBA_AVAILABLE}")
    if NUMBA_AVAILABLE:
        print(f"CUDA可用: {cuda.is_available()}")
    
    print("\nNumba JIT加速系统测试完成！")
