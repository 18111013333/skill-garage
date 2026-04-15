#!/usr/bin/env python3
"""
记忆系统融合器 V2
整合 yaoyao-memory 和 llm-memory-integration 到共享 ChromaDB
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
import chromadb
from chromadb.config import Settings

# 配置
MEMORY_DIR = os.path.dirname(__file__)
CHROMA_DB_PATH = os.path.join(MEMORY_DIR, 'chroma_db')

# Embedding API 配置
EMBEDDING_API_KEY = 'QTOGJC8FYEJPI0NNJOSMCSQOD8U30XNPDVIY1T1Q'
EMBEDDING_API_URL = 'https://ai.gitee.com/v1/embeddings'
EMBEDDING_MODEL = 'Qwen3-Embedding-8B'


def get_embedding(text: str) -> Optional[List[float]]:
    """获取文本的 Embedding 向量"""
    try:
        import requests
        
        headers = {
            'Authorization': f'Bearer {EMBEDDING_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': EMBEDDING_MODEL,
            'input': text[:2000]
        }
        
        response = requests.post(EMBEDDING_API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['data'][0]['embedding']
    except Exception as e:
        print(f"Embedding 错误: {e}")
    
    return None


class MemoryFusionV2:
    """记忆系统融合器 V2"""
    
    def __init__(self):
        # 连接 ChromaDB
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        
        # 创建/获取集合
        self.unified_collection = self.client.get_or_create_collection(
            name='unified_memory',
            metadata={'description': '统一记忆存储 - yaoyao-memory + llm-memory-integration'}
        )
        
        # yaoyao-memory 集合（存储层）
        self.yaoyao_collection = self.client.get_or_create_collection(
            name='yaoyao_memory',
            metadata={'description': 'yaoyao-memory 存储层'}
        )
        
        # llm-memory-integration 集合（检索层）
        self.llm_collection = self.client.get_or_create_collection(
            name='llm_memory',
            metadata={'description': 'llm-memory-integration 检索层'}
        )
        
        print(f"记忆系统融合器初始化完成")
        print(f"  - unified_memory: {self.unified_collection.count()} 条")
        print(f"  - yaoyao_memory: {self.yaoyao_collection.count()} 条")
        print(f"  - llm_memory: {self.llm_collection.count()} 条")
    
    def _generate_id(self, content: str) -> str:
        """生成唯一 ID"""
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def sync_from_unified(self) -> Dict:
        """从 unified_memory 同步到 yaoyao_memory 和 llm_memory"""
        print("\n同步 unified_memory 到两个集合...")
        
        # 获取 unified_memory 所有数据
        results = self.unified_collection.get()
        
        stats = {
            'total': len(results['ids']),
            'yaoyao_synced': 0,
            'llm_synced': 0,
            'errors': 0
        }
        
        if not results['ids']:
            print("  unified_memory 为空，无需同步")
            return stats
        
        # 批量同步到 yaoyao_memory
        yaoyao_ids = []
        yaoyao_docs = []
        yaoyao_metadatas = []
        
        # 批量同步到 llm_memory
        llm_ids = []
        llm_docs = []
        llm_metadatas = []
        
        for i, doc_id in enumerate(results['ids']):
            doc = results['documents'][i]
            metadata = results['metadatas'][i] if results['metadatas'] else {}
            
            # 添加到 yaoyao_memory（存储层）
            yaoyao_ids.append(f"yao_{doc_id}")
            yaoyao_docs.append(doc)
            yaoyao_metadatas.append({
                **metadata,
                'source': 'yaoyao-memory',
                'role': 'storage',
                'synced_at': datetime.now().isoformat()
            })
            
            # 添加到 llm_memory（检索层）
            llm_ids.append(f"llm_{doc_id}")
            llm_docs.append(doc)
            llm_metadatas.append({
                **metadata,
                'source': 'llm-memory-integration',
                'role': 'retrieval',
                'synced_at': datetime.now().isoformat()
            })
        
        # 批量插入 yaoyao_memory
        if yaoyao_ids:
            try:
                self.yaoyao_collection.upsert(
                    ids=yaoyao_ids,
                    documents=yaoyao_docs,
                    metadatas=yaoyao_metadatas
                )
                stats['yaoyao_synced'] = len(yaoyao_ids)
                print(f"  yaoyao_memory 同步: {len(yaoyao_ids)} 条")
            except Exception as e:
                print(f"  yaoyao_memory 同步失败: {e}")
                stats['errors'] += 1
        
        # 批量插入 llm_memory
        if llm_ids:
            try:
                self.llm_collection.upsert(
                    ids=llm_ids,
                    documents=llm_docs,
                    metadatas=llm_metadatas
                )
                stats['llm_synced'] = len(llm_ids)
                print(f"  llm_memory 同步: {len(llm_ids)} 条")
            except Exception as e:
                print(f"  llm_memory 同步失败: {e}")
                stats['errors'] += 1
        
        return stats
    
    def add_memory(self, content: str, source: str = "manual", metadata: Dict = None) -> Dict:
        """添加记忆到所有集合"""
        doc_id = self._generate_id(content)
        
        if metadata is None:
            metadata = {}
        
        metadata['source'] = source
        metadata['created_at'] = datetime.now().isoformat()
        
        # 获取 Embedding
        print(f"获取 Embedding: {content[:50]}...")
        embedding = get_embedding(content)
        
        result = {
            'id': doc_id,
            'success': False,
            'collections': []
        }
        
        if embedding is None:
            print("  Embedding 失败")
            return result
        
        # 添加到 unified_memory
        try:
            self.unified_collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[content],
                metadatas=[{**metadata, 'role': 'unified'}]
            )
            result['collections'].append('unified_memory')
        except Exception as e:
            print(f"  unified_memory 添加失败: {e}")
        
        # 添加到 yaoyao_memory
        try:
            self.yaoyao_collection.add(
                ids=[f"yao_{doc_id}"],
                embeddings=[embedding],
                documents=[content],
                metadatas=[{**metadata, 'role': 'storage'}]
            )
            result['collections'].append('yaoyao_memory')
        except Exception as e:
            print(f"  yaoyao_memory 添加失败: {e}")
        
        # 添加到 llm_memory
        try:
            self.llm_collection.add(
                ids=[f"llm_{doc_id}"],
                embeddings=[embedding],
                documents=[content],
                metadatas=[{**metadata, 'role': 'retrieval'}]
            )
            result['collections'].append('llm_memory')
        except Exception as e:
            print(f"  llm_memory 添加失败: {e}")
        
        result['success'] = len(result['collections']) == 3
        print(f"  添加成功: {result['collections']}")
        
        return result
    
    def search(self, query: str, top_k: int = 5, collection: str = "unified") -> List[Dict]:
        """搜索记忆"""
        print(f"\n搜索 ({collection}): {query}")
        
        # 选择集合
        if collection == "yaoyao":
            col = self.yaoyao_collection
        elif collection == "llm":
            col = self.llm_collection
        else:
            col = self.unified_collection
        
        # 获取查询 Embedding
        query_embedding = get_embedding(query)
        
        if query_embedding is None:
            print("获取查询 Embedding 失败")
            return []
        
        # 搜索
        results = col.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # 格式化结果
        memories = []
        for i, doc_id in enumerate(results['ids'][0]):
            memories.append({
                'id': doc_id,
                'content': results['documents'][0][i][:500] + '...',
                'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                'distance': results['distances'][0][i] if results['distances'] else None
            })
        
        return memories
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'unified_memory': self.unified_collection.count(),
            'yaoyao_memory': self.yaoyao_collection.count(),
            'llm_memory': self.llm_collection.count(),
            'total_unique': self.unified_collection.count(),
            'db_path': CHROMA_DB_PATH
        }
    
    def verify_sync(self) -> Dict:
        """验证同步状态"""
        unified_count = self.unified_collection.count()
        yaoyao_count = self.yaoyao_collection.count()
        llm_count = self.llm_collection.count()
        
        expected_yaoyao = unified_count
        expected_llm = unified_count
        
        return {
            'unified_count': unified_count,
            'yaoyao_count': yaoyao_count,
            'llm_count': llm_count,
            'yaoyao_synced': yaoyao_count >= expected_yaoyao,
            'llm_synced': llm_count >= expected_llm,
            'all_synced': yaoyao_count >= expected_yaoyao and llm_count >= expected_llm
        }


# 命令行接口
if __name__ == "__main__":
    import sys
    
    fusion = MemoryFusionV2()
    
    if len(sys.argv) < 2:
        print("用法: python memory_fusion_v2.py <command>")
        print("命令: sync, stats, verify, search <query>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'sync':
        result = fusion.sync_from_unified()
        print(f"\n同步结果: {result}")
    
    elif command == 'stats':
        stats = fusion.get_stats()
        print("\n记忆系统统计:")
        print("-" * 40)
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    elif command == 'verify':
        result = fusion.verify_sync()
        print("\n同步验证:")
        print("-" * 40)
        for key, value in result.items():
            status = "✅" if value else "❌" if isinstance(value, bool) else ""
            print(f"  {key}: {value} {status}")
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("请输入搜索查询")
            sys.exit(1)
        query = ' '.join(sys.argv[2:])
        
        # 搜索所有集合
        for col_name in ['unified', 'yaoyao', 'llm']:
            results = fusion.search(query, collection=col_name)
            print(f"\n[{col_name}] 搜索结果 ({len(results)} 条):")
            for i, mem in enumerate(results[:3]):
                print(f"  [{i+1}] {mem['content'][:50]}...")
    
    else:
        print(f"未知命令: {command}")
