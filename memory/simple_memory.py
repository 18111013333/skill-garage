#!/usr/bin/env python3
"""
简化版记忆系统
单一 ChromaDB 集合，无融合，简单高效
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
COLLECTION_NAME = 'memory'

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


class SimpleMemory:
    """简化版记忆系统"""
    
    def __init__(self):
        # 连接 ChromaDB
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        
        # 创建/获取单一集合
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={'description': '简化版记忆存储'}
        )
        
        print(f"简化版记忆系统初始化完成")
        print(f"  - 集合: {COLLECTION_NAME}")
        print(f"  - 记录数: {self.collection.count()}")
    
    def _generate_id(self, content: str) -> str:
        """生成唯一 ID"""
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def add(self, content: str, metadata: Dict = None) -> Dict:
        """添加记忆"""
        doc_id = self._generate_id(content)
        
        if metadata is None:
            metadata = {}
        
        metadata['created_at'] = datetime.now().isoformat()
        
        # 获取 Embedding
        print(f"添加记忆: {content[:50]}...")
        embedding = get_embedding(content)
        
        if embedding is None:
            print("  Embedding 失败")
            return {'success': False, 'error': 'embedding_failed'}
        
        try:
            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[content],
                metadatas=[metadata]
            )
            print(f"  ✅ 添加成功: {doc_id}")
            return {'success': True, 'id': doc_id}
        except Exception as e:
            print(f"  ❌ 添加失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """搜索记忆"""
        print(f"搜索: {query}")
        
        # 使用 ChromaDB 内置的文本搜索（不需要 Embedding）
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # 格式化结果
        memories = []
        for i, doc_id in enumerate(results['ids'][0]):
            memories.append({
                'id': doc_id,
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                'distance': results['distances'][0][i] if results['distances'] else None
            })
        
        return memories
    
    def get(self, doc_id: str) -> Optional[Dict]:
        """获取单条记忆"""
        try:
            result = self.collection.get(ids=[doc_id])
            if result['ids']:
                return {
                    'id': result['ids'][0],
                    'content': result['documents'][0],
                    'metadata': result['metadatas'][0] if result['metadatas'] else {}
                }
        except:
            pass
        return None
    
    def delete(self, doc_id: str) -> bool:
        """删除记忆"""
        try:
            self.collection.delete(ids=[doc_id])
            print(f"删除成功: {doc_id}")
            return True
        except Exception as e:
            print(f"删除失败: {e}")
            return False
    
    def list_all(self, limit: int = 100) -> List[Dict]:
        """列出所有记忆"""
        results = self.collection.get(limit=limit)
        
        memories = []
        for i, doc_id in enumerate(results['ids']):
            memories.append({
                'id': doc_id,
                'content': results['documents'][i][:100] + '...',
                'metadata': results['metadatas'][i] if results['metadatas'] else {}
            })
        
        return memories
    
    def count(self) -> int:
        """获取记忆数量"""
        return self.collection.count()
    
    def clear(self) -> bool:
        """清空所有记忆"""
        try:
            # 获取所有 ID
            results = self.collection.get()
            if results['ids']:
                self.collection.delete(ids=results['ids'])
            print("清空成功")
            return True
        except Exception as e:
            print(f"清空失败: {e}")
            return False
    
    def migrate_from_unified(self) -> Dict:
        """从 unified_memory 迁移数据"""
        print("\n从 unified_memory 迁移数据...")
        
        try:
            unified = self.client.get_collection('unified_memory')
            results = unified.get()
            
            if not results['ids']:
                print("  unified_memory 为空")
                return {'migrated': 0}
            
            # 批量迁移
            self.collection.add(
                ids=results['ids'],
                embeddings=results['embeddings'] if results['embeddings'] else None,
                documents=results['documents'],
                metadatas=results['metadatas']
            )
            
            print(f"  ✅ 迁移成功: {len(results['ids'])} 条")
            return {'migrated': len(results['ids'])}
        except Exception as e:
            print(f"  ❌ 迁移失败: {e}")
            return {'migrated': 0, 'error': str(e)}


# 命令行接口
if __name__ == "__main__":
    import sys
    
    memory = SimpleMemory()
    
    if len(sys.argv) < 2:
        print("用法: python simple_memory.py <command>")
        print("命令: add <content>, search <query>, list, count, migrate")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'add':
        if len(sys.argv) < 3:
            print("请输入内容")
            sys.exit(1)
        content = ' '.join(sys.argv[2:])
        memory.add(content)
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("请输入搜索查询")
            sys.exit(1)
        query = ' '.join(sys.argv[2:])
        results = memory.search(query)
        
        print(f"\n搜索结果 ({len(results)} 条):")
        print("-" * 60)
        for i, mem in enumerate(results):
            print(f"[{i+1}] {mem['content'][:80]}...")
            print(f"    距离: {mem['distance']:.4f}" if mem['distance'] else "")
    
    elif command == 'list':
        memories = memory.list_all()
        print(f"\n记忆列表 ({len(memories)} 条):")
        print("-" * 60)
        for mem in memories:
            print(f"  {mem['id']}: {mem['content'][:50]}...")
    
    elif command == 'count':
        print(f"记忆数量: {memory.count()}")
    
    elif command == 'migrate':
        result = memory.migrate_from_unified()
        print(f"迁移结果: {result}")
    
    else:
        print(f"未知命令: {command}")
