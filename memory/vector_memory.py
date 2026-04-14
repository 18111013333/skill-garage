#!/usr/bin/env python3
"""
向量记忆系统 - 基于小艺收藏技术优化
支持向量检索、二值量化、混合检索、分层存储
"""

import os
import json
import hashlib
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np

# 配置
MEMORY_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DB_PATH = os.path.join(MEMORY_DIR, 'vector_memory.db')
CACHE_DIR = os.path.join(MEMORY_DIR, 'cache')

# 确保目录存在
os.makedirs(CACHE_DIR, exist_ok=True)


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    content: str
    source: str
    timestamp: str
    vector: Optional[List[float]] = None
    binary_vector: Optional[str] = None
    access_count: int = 0
    last_access: str = ""
    tier: str = "warm"  # hot, warm, cold


class VectorMemorySystem:
    """向量记忆系统"""
    
    def __init__(self):
        self.conn = sqlite3.connect(VECTOR_DB_PATH)
        self._init_db()
        self.cache: Dict[str, MemoryEntry] = {}
        self._load_hot_memories()
    
    def _init_db(self):
        """初始化数据库"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                source TEXT,
                timestamp TEXT,
                vector BLOB,
                binary_vector TEXT,
                access_count INTEGER DEFAULT 0,
                last_access TEXT,
                tier TEXT DEFAULT 'warm'
            )
        ''')
        
        # 创建索引
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_tier ON memories(tier)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_access ON memories(access_count)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)')
        
        self.conn.commit()
    
    def _load_hot_memories(self):
        """加载热数据到内存缓存"""
        cursor = self.conn.execute('''
            SELECT * FROM memories 
            WHERE tier = 'hot' OR access_count > 10
            ORDER BY access_count DESC
            LIMIT 100
        ''')
        
        for row in cursor.fetchall():
            entry = MemoryEntry(
                id=row[0],
                content=row[1],
                source=row[2],
                timestamp=row[3],
                vector=json.loads(row[4]) if row[4] else None,
                binary_vector=row[5],
                access_count=row[6],
                last_access=row[7],
                tier=row[8]
            )
            self.cache[entry.id] = entry
    
    def _generate_id(self, content: str) -> str:
        """生成唯一ID"""
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def _text_to_vector(self, text: str) -> List[float]:
        """文本转向量（简化版，实际应使用Embedding模型）"""
        # 使用简单的哈希向量作为示例
        # 实际应用中应使用 sentence-transformers 或 OpenAI Embedding
        words = text.lower().split()
        vector = np.zeros(128, dtype=np.float32)
        
        for word in words:
            h = int(hashlib.md5(word.encode()).hexdigest(), 16)
            idx = h % 128
            vector[idx] += 1.0
        
        # 归一化
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector.tolist()
    
    def _vector_to_binary(self, vector: List[float]) -> str:
        """向量二值量化"""
        arr = np.array(vector, dtype=np.float32)
        # 阈值量化
        binary = (arr > 0).astype(np.uint8)
        # 转为十六进制字符串
        return ''.join([format(byte, '02x') for byte in binary.tobytes()])
    
    def _hamming_distance(self, bin1: str, bin2: str) -> int:
        """计算汉明距离"""
        if len(bin1) != len(bin2):
            return float('inf')
        
        distance = 0
        for c1, c2 in zip(bin1, bin2):
            b1 = int(c1, 16)
            b2 = int(c2, 16)
            distance += bin(b1 ^ b2).count('1')
        
        return distance
    
    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """计算余弦相似度"""
        arr1 = np.array(v1)
        arr2 = np.array(v2)
        
        dot = np.dot(arr1, arr2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot / (norm1 * norm2)
    
    def add_memory(self, content: str, source: str = "manual") -> str:
        """添加记忆"""
        entry_id = self._generate_id(content)
        timestamp = datetime.now().isoformat()
        
        # 生成向量
        vector = self._text_to_vector(content)
        binary_vector = self._vector_to_binary(vector)
        
        entry = MemoryEntry(
            id=entry_id,
            content=content,
            source=source,
            timestamp=timestamp,
            vector=vector,
            binary_vector=binary_vector,
            access_count=0,
            last_access=timestamp,
            tier="warm"
        )
        
        # 存入数据库
        self.conn.execute('''
            INSERT OR REPLACE INTO memories 
            (id, content, source, timestamp, vector, binary_vector, access_count, last_access, tier)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry.id, entry.content, entry.source, entry.timestamp,
            json.dumps(entry.vector), entry.binary_vector,
            entry.access_count, entry.last_access, entry.tier
        ))
        self.conn.commit()
        
        # 加入缓存
        self.cache[entry.id] = entry
        
        return entry_id
    
    def search_vector(self, query: str, top_k: int = 10) -> List[Tuple[MemoryEntry, float]]:
        """向量检索"""
        query_vector = self._text_to_vector(query)
        query_binary = self._vector_to_binary(query_vector)
        
        results = []
        
        # 先搜索缓存（热数据）
        for entry in self.cache.values():
            if entry.vector:
                sim = self._cosine_similarity(query_vector, entry.vector)
                results.append((entry, sim))
        
        # 搜索数据库（温数据）
        cursor = self.conn.execute('''
            SELECT id, content, source, timestamp, vector, binary_vector, 
                   access_count, last_access, tier
            FROM memories
            WHERE tier != 'cold'
        ''')
        
        for row in cursor.fetchall():
            entry_id = row[0]
            if entry_id in self.cache:
                continue  # 已在缓存中
            
            entry = MemoryEntry(
                id=entry_id,
                content=row[1],
                source=row[2],
                timestamp=row[3],
                vector=json.loads(row[4]) if row[4] else None,
                binary_vector=row[5],
                access_count=row[6],
                last_access=row[7],
                tier=row[8]
            )
            
            if entry.vector:
                sim = self._cosine_similarity(query_vector, entry.vector)
                results.append((entry, sim))
        
        # 排序并返回Top-K
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def search_binary(self, query: str, top_k: int = 10) -> List[Tuple[MemoryEntry, int]]:
        """二值向量检索（更快但精度略低）"""
        query_vector = self._text_to_vector(query)
        query_binary = self._vector_to_binary(query_vector)
        
        results = []
        
        cursor = self.conn.execute('SELECT * FROM memories')
        for row in cursor.fetchall():
            entry = MemoryEntry(
                id=row[0],
                content=row[1],
                source=row[2],
                timestamp=row[3],
                binary_vector=row[5],
                access_count=row[6],
                last_access=row[7],
                tier=row[8]
            )
            
            if entry.binary_vector:
                dist = self._hamming_distance(query_binary, entry.binary_vector)
                results.append((entry, dist))
        
        # 按距离排序（越小越相似）
        results.sort(key=lambda x: x[1])
        return results[:top_k]
    
    def search_hybrid(self, query: str, top_k: int = 10, 
                      vector_weight: float = 0.7,
                      keyword_weight: float = 0.3) -> List[Tuple[MemoryEntry, float]]:
        """混合检索（向量 + 关键词）"""
        # 向量检索
        vector_results = self.search_vector(query, top_k * 2)
        
        # 关键词检索
        keywords = query.lower().split()
        keyword_results = []
        
        cursor = self.conn.execute('SELECT * FROM memories')
        for row in cursor.fetchall():
            entry = MemoryEntry(
                id=row[0],
                content=row[1],
                source=row[2],
                timestamp=row[3],
                access_count=row[6],
                last_access=row[7],
                tier=row[8]
            )
            
            # 计算关键词匹配分数
            content_lower = entry.content.lower()
            score = sum(1 for kw in keywords if kw in content_lower)
            if score > 0:
                keyword_results.append((entry, score / len(keywords)))
        
        # RRF融合
        rrf_scores: Dict[str, float] = {}
        k = 60  # RRF参数
        
        for rank, (entry, _) in enumerate(vector_results):
            rrf_scores[entry.id] = rrf_scores.get(entry.id, 0) + vector_weight / (k + rank + 1)
        
        for rank, (entry, _) in enumerate(sorted(keyword_results, key=lambda x: x[1], reverse=True)):
            rrf_scores[entry.id] = rrf_scores.get(entry.id, 0) + keyword_weight / (k + rank + 1)
        
        # 获取最终结果
        final_results = []
        for entry_id, score in sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]:
            cursor = self.conn.execute('SELECT * FROM memories WHERE id = ?', (entry_id,))
            row = cursor.fetchone()
            if row:
                entry = MemoryEntry(
                    id=row[0], content=row[1], source=row[2], timestamp=row[3],
                    access_count=row[6], last_access=row[7], tier=row[8]
                )
                final_results.append((entry, score))
        
        return final_results
    
    def update_tier(self):
        """更新分层存储"""
        now = datetime.now()
        
        # 获取所有记忆
        cursor = self.conn.execute('SELECT id, timestamp, access_count FROM memories')
        entries = cursor.fetchall()
        
        for entry_id, timestamp, access_count in entries:
            entry_time = datetime.fromisoformat(timestamp)
            days_old = (now - entry_time).days
            
            # 分层策略
            if days_old <= 7 and access_count > 5:
                new_tier = 'hot'
            elif days_old <= 30:
                new_tier = 'warm'
            else:
                new_tier = 'cold'
            
            self.conn.execute('UPDATE memories SET tier = ? WHERE id = ?', (new_tier, entry_id))
        
        self.conn.commit()
        
        # 重新加载热数据
        self._load_hot_memories()
    
    def record_access(self, entry_id: str):
        """记录访问"""
        now = datetime.now().isoformat()
        self.conn.execute('''
            UPDATE memories 
            SET access_count = access_count + 1, last_access = ?
            WHERE id = ?
        ''', (now, entry_id))
        self.conn.commit()
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        cursor = self.conn.execute('SELECT COUNT(*) FROM memories')
        total = cursor.fetchone()[0]
        
        cursor = self.conn.execute('SELECT tier, COUNT(*) FROM memories GROUP BY tier')
        tiers = dict(cursor.fetchall())
        
        return {
            'total': total,
            'hot': tiers.get('hot', 0),
            'warm': tiers.get('warm', 0),
            'cold': tiers.get('cold', 0),
            'cache_size': len(self.cache)
        }
    
    def close(self):
        """关闭连接"""
        self.conn.close()


# 测试代码
if __name__ == '__main__':
    system = VectorMemorySystem()
    
    # 添加测试记忆
    test_memories = [
        "老板陈飞是四川南充人，出生于1981年",
        "视元堂眼视光中心位于南充顺庆区白土坝路406号",
        "皇泽寺是中国唯一的女皇帝武则天祀庙",
        "径山寺禅修酒店投资6.5亿元，有72间客房",
        "LLM技能优化包括向量检索、二值量化、混合检索"
    ]
    
    for mem in test_memories:
        system.add_memory(mem, "test")
    
    # 测试检索
    print("=== 向量检索测试 ===")
    results = system.search_vector("武则天", 3)
    for entry, sim in results:
        print(f"相似度: {sim:.3f} | {entry.content[:50]}...")
    
    print("\n=== 混合检索测试 ===")
    results = system.search_hybrid("南充", 3)
    for entry, score in results:
        print(f"分数: {score:.3f} | {entry.content[:50]}...")
    
    # 统计信息
    print("\n=== 系统统计 ===")
    stats = system.get_stats()
    print(json.dumps(stats, indent=2))
    
    system.close()
    print("\n向量记忆系统测试完成！")
