#!/usr/bin/env python3
"""
优化版向量记忆系统 V4
集成 Numba JIT 加速 + FAISS 索引 + MKL/OpenBLAS 优化
"""

import os
import json
import hashlib
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import numpy as np

# Numba JIT 加速
try:
    import numba
    from numba import jit, prange
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    # 回退到普通函数
    def jit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    prange = range

# FAISS 向量索引
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

# 配置
MEMORY_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DB_PATH = os.path.join(MEMORY_DIR, 'optimized_vector_memory.db')
FAISS_INDEX_PATH = os.path.join(MEMORY_DIR, 'faiss_index.bin')
CACHE_DIR = os.path.join(MEMORY_DIR, 'cache')

os.makedirs(CACHE_DIR, exist_ok=True)

# 向量维度
VECTOR_DIM = 768


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    content: str
    source: str
    timestamp: str
    access_count: int = 0
    last_access: str = ""
    tier: str = "warm"


# ============== Numba JIT 加速函数 ==============

if NUMBA_AVAILABLE:
    @jit(nopython=True, cache=True)
    def cosine_similarity_numba(a: np.ndarray, b: np.ndarray) -> float:
        """Numba 加速的余弦相似度计算"""
        dot = 0.0
        norm_a = 0.0
        norm_b = 0.0
        for i in range(len(a)):
            dot += a[i] * b[i]
            norm_a += a[i] * a[i]
            norm_b += b[i] * b[i]
        
        norm = np.sqrt(norm_a) * np.sqrt(norm_b)
        if norm > 0:
            return dot / norm
        return 0.0

    @jit(nopython=True, parallel=True, cache=True)
    def batch_cosine_similarity_numba(query: np.ndarray, vectors: np.ndarray) -> np.ndarray:
        """批量余弦相似度计算（并行）"""
        n = vectors.shape[0]
        results = np.zeros(n, dtype=np.float32)
        
        for i in prange(n):
            dot = 0.0
            norm_q = 0.0
            norm_v = 0.0
            for j in range(len(query)):
                dot += query[j] * vectors[i, j]
                norm_q += query[j] * query[j]
                norm_v += vectors[i, j] * vectors[i, j]
            
            norm = np.sqrt(norm_q) * np.sqrt(norm_v)
            if norm > 0:
                results[i] = dot / norm
        
        return results

    @jit(nopython=True, cache=True)
    def vector_to_binary_numba(vector: np.ndarray) -> np.ndarray:
        """向量二值量化"""
        return (vector > 0).astype(np.uint8)

    @jit(nopython=True, cache=True)
    def hamming_distance_numba(a: np.ndarray, b: np.ndarray) -> int:
        """汉明距离计算"""
        return np.sum(a != b)

else:
    def cosine_similarity_numba(a: np.ndarray, b: np.ndarray) -> float:
        """回退实现"""
        dot = np.dot(a, b)
        norm = np.linalg.norm(a) * np.linalg.norm(b)
        return dot / norm if norm > 0 else 0.0

    def batch_cosine_similarity_numba(query: np.ndarray, vectors: np.ndarray) -> np.ndarray:
        """回退实现"""
        norms_q = np.linalg.norm(query)
        norms_v = np.linalg.norm(vectors, axis=1)
        dots = np.dot(vectors, query)
        return dots / (norms_q * norms_v + 1e-10)


class OptimizedVectorMemorySystem:
    """优化版向量记忆系统"""
    
    def __init__(self, use_faiss: bool = True, use_numba: bool = True):
        self.use_faiss = use_faiss and FAISS_AVAILABLE
        self.use_numba = use_numba and NUMBA_AVAILABLE
        
        # SQLite 数据库
        self.conn = sqlite3.connect(VECTOR_DB_PATH)
        self._init_db()
        
        # FAISS 索引
        self.faiss_index = None
        self.id_to_idx: Dict[str, int] = {}
        self.idx_to_id: List[str] = []
        
        if self.use_faiss:
            self._init_faiss()
        
        # 内存缓存
        self.cache: Dict[str, MemoryEntry] = {}
        self.vector_cache: Dict[str, np.ndarray] = {}
        
        # 性能统计
        self.stats = {
            'searches': 0,
            'total_search_time': 0.0,
            'cache_hits': 0,
            'faiss_searches': 0,
            'numba_accelerated': 0
        }
        
        print(f"向量记忆系统初始化完成:")
        print(f"  - FAISS: {'✅ 已启用' if self.use_faiss else '❌ 未启用'}")
        print(f"  - Numba: {'✅ 已启用' if self.use_numba else '❌ 未启用'}")
        print(f"  - 向量维度: {VECTOR_DIM}")
    
    def _init_db(self):
        """初始化数据库"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                source TEXT,
                timestamp TEXT,
                access_count INTEGER DEFAULT 0,
                last_access TEXT,
                tier TEXT DEFAULT 'warm',
                vector BLOB
            )
        ''')
        
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_tier ON memories(tier)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_access ON memories(access_count)')
        self.conn.commit()
    
    def _init_faiss(self):
        """初始化 FAISS 索引"""
        if os.path.exists(FAISS_INDEX_PATH):
            try:
                self.faiss_index = faiss.read_index(FAISS_INDEX_PATH)
                print(f"  - FAISS 索引已加载: {self.faiss_index.ntotal} 条向量")
            except Exception as e:
                print(f"  - FAISS 索引加载失败: {e}")
                self._create_faiss_index()
        else:
            self._create_faiss_index()
        
        # 加载 ID 映射
        self._load_id_mapping()
    
    def _create_faiss_index(self):
        """创建 FAISS 索引"""
        # 使用 IndexFlatIP（内积索引，适合小规模数据）
        # 对于大规模数据，可以切换到 IVF + PQ
        self.faiss_index = faiss.IndexFlatIP(VECTOR_DIM)
        
        print(f"  - FAISS 索引已创建 (IndexFlatIP, dim={VECTOR_DIM})")
    
    def _load_id_mapping(self):
        """加载 ID 映射"""
        cursor = self.conn.execute('SELECT id FROM memories ORDER BY rowid')
        self.idx_to_id = [row[0] for row in cursor.fetchall()]
        self.id_to_idx = {id_: idx for idx, id_ in enumerate(self.idx_to_id)}
    
    def _generate_id(self, content: str) -> str:
        """生成唯一 ID"""
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def _text_to_vector(self, text: str) -> np.ndarray:
        """文本转向量（简化版，实际应使用 Embedding API）
        
        注意：这是一个简化的实现，仅用于演示。
        实际应用中应使用：
        - sentence-transformers
        - OpenAI Embedding API
        - 或其他专业的 Embedding 模型
        
        当前实现使用词袋模型 + 哈希技巧，语义相似性有限。
        """
        vector = np.zeros(VECTOR_DIM, dtype=np.float32)
        
        text_lower = text.lower()
        words = text_lower.split()
        
        # 词袋模型：每个词映射到固定位置
        for word in words:
            # 使用多个哈希函数减少冲突
            for seed in range(3):
                h = int(hashlib.md5(f"{word}_{seed}".encode()).hexdigest(), 16)
                idx = h % VECTOR_DIM
                vector[idx] += 1.0 / (seed + 1)
        
        # 添加字符级特征（捕获词形变化）
        for i in range(len(text_lower) - 2):
            ngram = text_lower[i:i+3]
            h = int(hashlib.md5(ngram.encode()).hexdigest(), 16)
            idx = h % VECTOR_DIM
            vector[idx] += 0.3
        
        # L2 归一化
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def add_memory(self, content: str, source: str = "manual") -> str:
        """添加记忆"""
        entry_id = self._generate_id(content)
        timestamp = datetime.now().isoformat()
        
        # 生成向量
        vector = self._text_to_vector(content)
        
        # 存入数据库
        self.conn.execute('''
            INSERT OR REPLACE INTO memories 
            (id, content, source, timestamp, access_count, last_access, tier, vector)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry_id, content, source, timestamp,
            0, timestamp, "warm", vector.tobytes()
        ))
        self.conn.commit()
        
        # 添加到 FAISS 索引
        if self.use_faiss and self.faiss_index is not None:
            self._add_to_faiss(entry_id, vector)
        
        # 更新缓存
        entry = MemoryEntry(
            id=entry_id,
            content=content,
            source=source,
            timestamp=timestamp,
            access_count=0,
            last_access=timestamp,
            tier="warm"
        )
        self.cache[entry_id] = entry
        self.vector_cache[entry_id] = vector
        
        return entry_id
    
    def _add_to_faiss(self, entry_id: str, vector: np.ndarray):
        """添加向量到 FAISS 索引"""
        vector = vector.reshape(1, -1).astype(np.float32)
        
        # IndexFlatIP 不需要训练
        self.faiss_index.add(vector)
        
        # 更新映射
        idx = len(self.idx_to_id)
        self.idx_to_id.append(entry_id)
        self.id_to_idx[entry_id] = idx
        
        # 保存索引
        faiss.write_index(self.faiss_index, FAISS_INDEX_PATH)
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[MemoryEntry, float]]:
        """向量检索"""
        import time
        start_time = time.time()
        
        query_vector = self._text_to_vector(query)
        results = []
        
        if self.use_faiss and self.faiss_index is not None and self.faiss_index.ntotal > 0:
            # FAISS 搜索
            query_vec = query_vector.reshape(1, -1).astype(np.float32)
            similarities, indices = self.faiss_index.search(query_vec, min(top_k * 2, self.faiss_index.ntotal))
            
            for sim, idx in zip(similarities[0], indices[0]):
                if idx >= 0 and idx < len(self.idx_to_id):  # FAISS 返回 -1 表示无效索引
                    entry_id = self.idx_to_id[idx]
                    entry = self._get_entry(entry_id)
                    if entry:
                        results.append((entry, float(sim)))
            
            self.stats['faiss_searches'] += 1
        else:
            # 回退到暴力搜索
            results = self._brute_force_search(query_vector, top_k)
        
        # 更新统计
        self.stats['searches'] += 1
        self.stats['total_search_time'] += time.time() - start_time
        
        return results[:top_k]
    
    def _brute_force_search(self, query_vector: np.ndarray, top_k: int) -> List[Tuple[MemoryEntry, float]]:
        """暴力搜索（无 FAISS 时使用）"""
        results = []
        
        # 从数据库加载所有向量
        cursor = self.conn.execute('SELECT id, content, source, timestamp, access_count, last_access, tier, vector FROM memories')
        
        vectors = []
        entries = []
        
        for row in cursor.fetchall():
            if row[7]:
                vector = np.frombuffer(row[7], dtype=np.float32)
                if len(vector) == VECTOR_DIM:
                    vectors.append(vector)
                    entries.append(MemoryEntry(
                        id=row[0], content=row[1], source=row[2],
                        timestamp=row[3], access_count=row[4],
                        last_access=row[5], tier=row[6]
                    ))
        
        if vectors:
            vectors = np.array(vectors)
            
            if self.use_numba:
                # Numba 加速批量计算
                similarities = batch_cosine_similarity_numba(query_vector, vectors)
                self.stats['numba_accelerated'] += 1
            else:
                # NumPy 批量计算
                norms_q = np.linalg.norm(query_vector)
                norms_v = np.linalg.norm(vectors, axis=1)
                similarities = np.dot(vectors, query_vector) / (norms_q * norms_v + 1e-10)
            
            # 排序
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            for idx in top_indices:
                results.append((entries[idx], float(similarities[idx])))
        
        return results
    
    def _get_entry(self, entry_id: str) -> Optional[MemoryEntry]:
        """获取记忆条目"""
        if entry_id in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[entry_id]
        
        cursor = self.conn.execute('SELECT id, content, source, timestamp, access_count, last_access, tier FROM memories WHERE id = ?', (entry_id,))
        row = cursor.fetchone()
        
        if row:
            entry = MemoryEntry(
                id=row[0], content=row[1], source=row[2],
                timestamp=row[3], access_count=row[4],
                last_access=row[5], tier=row[6]
            )
            self.cache[entry_id] = entry
            return entry
        
        return None
    
    def get_stats(self) -> Dict:
        """获取性能统计"""
        stats = self.stats.copy()
        stats['avg_search_time'] = (
            stats['total_search_time'] / stats['searches'] 
            if stats['searches'] > 0 else 0
        )
        stats['faiss_vectors'] = self.faiss_index.ntotal if self.faiss_index else 0
        stats['cache_size'] = len(self.cache)
        return stats
    
    def close(self):
        """关闭系统"""
        if self.faiss_index:
            faiss.write_index(self.faiss_index, FAISS_INDEX_PATH)
        self.conn.close()


# 测试代码
if __name__ == "__main__":
    import time
    
    print("=" * 50)
    print("优化版向量记忆系统测试")
    print("=" * 50)
    
    system = OptimizedVectorMemorySystem()
    
    # 添加测试数据
    test_data = [
        "用户喜欢简洁的回复风格",
        "项目使用六层架构设计",
        "记忆系统支持向量检索",
        "FAISS 提供高效的近似最近邻搜索",
        "Numba JIT 加速数值计算",
        "系统版本为 V4.3.6",
        "Embedding 使用 Qwen3-Embedding-8B",
        "LLM 使用 Qwen3-235B-A22B",
        "API 端点为 Gitee AI",
        "性能模式设置为 maximum"
    ]
    
    print("\n添加测试数据...")
    for data in test_data:
        system.add_memory(data, "test")
    
    # 搜索测试
    print("\n搜索测试:")
    queries = [
        ("向量检索", "记忆系统支持向量检索"),
        ("用户喜欢", "用户喜欢简洁的回复风格"),
        ("系统版本", "系统版本为 V4.3.6"),
        ("FAISS", "FAISS 提供高效的近似最近邻搜索"),
        ("Numba", "Numba JIT 加速数值计算"),
    ]
    
    correct = 0
    total = len(queries)
    
    for query, expected in queries:
        start = time.time()
        results = system.search(query, top_k=1)
        elapsed = (time.time() - start) * 1000
        
        if results:
            top_result = results[0][0].content
            sim = results[0][1]
            is_correct = expected in top_result or top_result in expected
            if is_correct:
                correct += 1
            status = "✅" if is_correct else "❌"
            print(f"\n查询: '{query}' ({elapsed:.2f}ms) {status}")
            print(f"  期望: {expected}")
            print(f"  结果: {top_result} [{sim:.3f}]")
        else:
            print(f"\n查询: '{query}' - 无结果 ❌")
    
    print(f"\n准确率: {correct}/{total} ({100*correct/total:.0f}%)")
    
    # 性能统计
    print("\n" + "=" * 50)
    print("性能统计:")
    stats = system.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    system.close()
    print("\n测试完成!")
