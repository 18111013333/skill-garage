#!/usr/bin/env python3
"""
HNSW索引系统 - 基于小艺Claw技术优化
Hierarchical Navigable Small World 图索引实现
"""

import os
import json
import heapq
import random
import sqlite3
import numpy as np
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict

# 配置
MEMORY_DIR = os.path.dirname(os.path.abspath(__file__))
HNSW_DB_PATH = os.path.join(MEMORY_DIR, 'hnsw_index.db')


@dataclass
class HNSWNode:
    """HNSW节点"""
    id: str
    vector: List[float]
    level: int
    neighbors: Dict[int, List[str]] = field(default_factory=dict)  # level -> neighbor_ids


class HNSWIndex:
    """
    HNSW (Hierarchical Navigable Small World) 索引
    
    特点：
    - 多层图结构，上层稀疏，下层密集
    - 对数复杂度的近似最近邻搜索
    - 支持高维向量高效检索
    """
    
    def __init__(self, 
                 dim: int = 128,
                 max_elements: int = 10000,
                 m: int = 16,  # 每层最大连接数
                 ef_construction: int = 200,  # 构建时的搜索宽度
                 ef_search: int = 50,  # 搜索时的搜索宽度
                 ml: float = None):  # 层级因子
        
        self.dim = dim
        self.max_elements = max_elements
        self.m = m
        self.ef_construction = ef_construction
        self.ef_search = ef_search
        self.ml = ml if ml else 1.0 / np.log(m)
        
        # 节点存储
        self.nodes: Dict[str, HNSWNode] = {}
        
        # 入口点（最高层节点）
        self.entry_point: Optional[str] = None
        self.max_level = -1
        
        # 数据库持久化
        self.conn = sqlite3.connect(HNSW_DB_PATH)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS hnsw_nodes (
                id TEXT PRIMARY KEY,
                vector BLOB,
                level INTEGER,
                neighbors TEXT
            )
        ''')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_level ON hnsw_nodes(level)')
        self.conn.commit()
    
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
    
    def _distance(self, v1: List[float], v2: List[float]) -> float:
        """计算距离（1 - 余弦相似度）"""
        return 1.0 - self._cosine_similarity(v1, v2)
    
    def _random_level(self) -> int:
        """随机生成节点层级"""
        level = 0
        while random.random() < self.ml and level < 10:
            level += 1
        return level
    
    def _search_layer(self, 
                      query: List[float], 
                      entry_points: List[str], 
                      ef: int, 
                      level: int) -> List[Tuple[float, str]]:
        """
        在指定层搜索最近邻
        
        返回: [(distance, node_id), ...] 按距离排序
        """
        visited: Set[str] = set(entry_points)
        
        # 候选集（最小堆）
        candidates = []
        for ep in entry_points:
            if ep in self.nodes:
                dist = self._distance(query, self.nodes[ep].vector)
                heapq.heappush(candidates, (dist, ep))
        
        # 结果集（最大堆，用负距离模拟）
        results = []
        for ep in entry_points:
            if ep in self.nodes:
                dist = self._distance(query, self.nodes[ep].vector)
                heapq.heappush(results, (-dist, ep))
        
        while candidates:
            # 取出最近的候选
            c_dist, c_id = heapq.heappop(candidates)
            
            # 如果候选比结果中最远的还远，停止
            if results and c_dist > -results[0][0]:
                break
            
            # 遍历候选的邻居
            if c_id in self.nodes:
                node = self.nodes[c_id]
                neighbors = node.neighbors.get(level, [])
                
                for n_id in neighbors:
                    if n_id not in visited and n_id in self.nodes:
                        visited.add(n_id)
                        n_dist = self._distance(query, self.nodes[n_id].vector)
                        
                        # 如果比结果中最远的近，加入候选和结果
                        if len(results) < ef or n_dist < -results[0][0]:
                            heapq.heappush(candidates, (n_dist, n_id))
                            heapq.heappush(results, (-n_dist, n_id))
                            
                            # 保持结果集大小
                            if len(results) > ef:
                                heapq.heappop(results)
        
        # 转换为排序后的列表
        return [(-dist, node_id) for dist, node_id in sorted(results, reverse=True)]
    
    def _select_neighbors_simple(self, 
                                  candidates: List[Tuple[float, str]], 
                                  m: int) -> List[str]:
        """简单邻居选择：选最近的m个"""
        return [node_id for _, node_id in sorted(candidates)[:m]]
    
    def _select_neighbors_heuristic(self, 
                                     candidates: List[Tuple[float, str]], 
                                     m: int,
                                     query: List[float]) -> List[str]:
        """
        启发式邻居选择
        考虑邻居之间的距离，避免聚集
        """
        if len(candidates) <= m:
            return [node_id for _, node_id in candidates]
        
        selected = []
        candidates = sorted(candidates)
        
        for dist, node_id in candidates:
            if len(selected) >= m:
                break
            
            # 检查是否与已选邻居太近
            is_good = True
            for s_id in selected:
                if s_id in self.nodes and node_id in self.nodes:
                    s_dist = self._distance(
                        self.nodes[s_id].vector,
                        self.nodes[node_id].vector
                    )
                    # 如果邻居之间距离小于到查询点的距离，跳过
                    if s_dist < dist:
                        is_good = False
                        break
            
            if is_good:
                selected.append(node_id)
        
        return selected
    
    def insert(self, node_id: str, vector: List[float]):
        """插入节点"""
        # 随机层级
        level = self._random_level()
        
        # 创建节点
        node = HNSWNode(
            id=node_id,
            vector=vector,
            level=level,
            neighbors={}
        )
        
        # 如果是第一个节点
        if self.entry_point is None:
            self.nodes[node_id] = node
            self.entry_point = node_id
            self.max_level = level
            self._save_node(node)
            return
        
        # 从入口点开始搜索
        current_ep = [self.entry_point]
        
        # 从最高层向下搜索
        for lc in range(self.max_level, level, -1):
            results = self._search_layer(vector, current_ep, ef=1, level=lc)
            if results:
                current_ep = [results[0][1]]
        
        # 在level及以下层插入
        for lc in range(min(level, self.max_level), -1, -1):
            results = self._search_layer(vector, current_ep, ef=self.ef_construction, level=lc)
            
            # 选择邻居
            neighbors = self._select_neighbors_heuristic(results, self.m, vector)
            node.neighbors[lc] = neighbors
            
            # 更新邻居的反向连接
            for n_id in neighbors:
                if n_id in self.nodes:
                    n_node = self.nodes[n_id]
                    if lc not in n_node.neighbors:
                        n_node.neighbors[lc] = []
                    
                    # 添加反向连接
                    if node_id not in n_node.neighbors[lc]:
                        n_node.neighbors[lc].append(node_id)
                        
                        # 如果超过最大连接数，修剪
                        if len(n_node.neighbors[lc]) > self.m:
                            n_node.neighbors[lc] = self._select_neighbors_simple(
                                [(self._distance(n_node.vector, self.nodes[nn].vector), nn) 
                                 for nn in n_node.neighbors[lc] if nn in self.nodes],
                                self.m
                            )
        
        # 存储节点
        self.nodes[node_id] = node
        
        # 更新入口点
        if level > self.max_level:
            self.entry_point = node_id
            self.max_level = level
        
        # 持久化
        self._save_node(node)
    
    def search(self, query: List[float], k: int = 10) -> List[Tuple[float, str]]:
        """
        搜索最近邻
        
        返回: [(distance, node_id), ...] 按距离排序
        """
        if self.entry_point is None:
            return []
        
        # 从入口点开始
        current_ep = [self.entry_point]
        
        # 从最高层向下搜索
        for lc in range(self.max_level, 0, -1):
            results = self._search_layer(query, current_ep, ef=1, level=lc)
            if results:
                current_ep = [results[0][1]]
        
        # 在底层详细搜索
        results = self._search_layer(query, current_ep, ef=self.ef_search, level=0)
        
        return results[:k]
    
    def _save_node(self, node: HNSWNode):
        """保存节点到数据库"""
        self.conn.execute('''
            INSERT OR REPLACE INTO hnsw_nodes (id, vector, level, neighbors)
            VALUES (?, ?, ?, ?)
        ''', (
            node.id,
            json.dumps(node.vector).encode(),
            node.level,
            json.dumps(node.neighbors)
        ))
        self.conn.commit()
    
    def load_nodes(self):
        """从数据库加载节点"""
        cursor = self.conn.execute('SELECT id, vector, level, neighbors FROM hnsw_nodes')
        
        for row in cursor.fetchall():
            node = HNSWNode(
                id=row[0],
                vector=json.loads(row[1]),
                level=row[2],
                neighbors=json.loads(row[3])
            )
            self.nodes[node.id] = node
            
            if node.level > self.max_level:
                self.max_level = node.level
                self.entry_point = node.id
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        total_connections = sum(
            sum(len(neighbors) for neighbors in node.neighbors.values())
            for node in self.nodes.values()
        )
        
        return {
            'total_nodes': len(self.nodes),
            'max_level': self.max_level,
            'entry_point': self.entry_point,
            'avg_connections': total_connections / len(self.nodes) if self.nodes else 0,
            'm': self.m,
            'ef_construction': self.ef_construction,
            'ef_search': self.ef_search
        }
    
    def close(self):
        """关闭连接"""
        self.conn.close()


# 测试代码
if __name__ == '__main__':
    print("=== HNSW索引系统测试 ===\n")
    
    # 创建索引
    index = HNSWIndex(dim=128, m=16, ef_construction=100, ef_search=50)
    
    # 生成测试向量
    print("生成测试向量...")
    test_vectors = []
    for i in range(100):
        vec = np.random.randn(128).astype(np.float32)
        vec = vec / np.linalg.norm(vec)  # 归一化
        test_vectors.append((f"vec_{i}", vec.tolist()))
    
    # 插入向量
    print("插入向量...")
    for node_id, vector in test_vectors:
        index.insert(node_id, vector)
    
    # 搜索测试
    print("\n搜索测试...")
    query = test_vectors[0][1]  # 用第一个向量作为查询
    results = index.search(query, k=5)
    
    print("Top 5 最近邻:")
    for dist, node_id in results:
        print(f"  距离: {dist:.4f} | ID: {node_id}")
    
    # 统计信息
    print("\n=== 索引统计 ===")
    stats = index.get_stats()
    print(json.dumps(stats, indent=2))
    
    index.close()
    print("\nHNSW索引系统测试完成！")
