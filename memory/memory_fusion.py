#!/usr/bin/env python3
"""
记忆系统融合器
将 yaoyao-memory 和 llm-memory-integration 融合到共享 ChromaDB
"""

import os
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings

# 配置
MEMORY_DIR = os.path.dirname(__file__)
CHROMA_DB_PATH = os.path.join(MEMORY_DIR, 'chroma_db')
COLLECTION_NAME = 'unified_memory'

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
            'input': text[:2000]  # 限制长度
        }
        
        response = requests.post(EMBEDDING_API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['data'][0]['embedding']
    except Exception as e:
        print(f"Embedding 错误: {e}")
    
    return None


class MemoryFusion:
    """记忆系统融合器"""
    
    def __init__(self):
        # 连接 ChromaDB
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        
        # 获取或创建统一集合
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={'description': '统一记忆存储'}
        )
        
        print(f"ChromaDB 初始化完成")
        print(f"  - 路径: {CHROMA_DB_PATH}")
        print(f"  - 集合: {COLLECTION_NAME}")
        print(f"  - 现有记录: {self.collection.count()}")
    
    def _generate_id(self, content: str) -> str:
        """生成唯一 ID"""
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def scan_memory_files(self) -> List[Dict]:
        """扫描记忆文件"""
        memory_files = []
        
        # 扫描 .md 文件
        for filename in os.listdir(MEMORY_DIR):
            if filename.endswith('.md') and not filename.startswith('.'):
                filepath = os.path.join(MEMORY_DIR, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if content.strip():
                        memory_files.append({
                            'filename': filename,
                            'filepath': filepath,
                            'content': content,
                            'size': len(content)
                        })
                except Exception as e:
                    print(f"读取文件失败 {filename}: {e}")
        
        return memory_files
    
    def sync_to_chromadb(self, batch_size: int = 10) -> Dict:
        """同步记忆到 ChromaDB"""
        print("\n扫描记忆文件...")
        memory_files = self.scan_memory_files()
        print(f"找到 {len(memory_files)} 个记忆文件")
        
        stats = {
            'total': len(memory_files),
            'synced': 0,
            'skipped': 0,
            'errors': 0
        }
        
        # 批量处理
        batch_ids = []
        batch_embeddings = []
        batch_metadatas = []
        batch_documents = []
        
        for i, mem in enumerate(memory_files):
            print(f"\n处理 [{i+1}/{len(memory_files)}]: {mem['filename']}")
            
            # 生成 ID
            doc_id = self._generate_id(mem['content'])
            
            # 检查是否已存在
            existing = self.collection.get(ids=[doc_id])
            if existing['ids']:
                print(f"  - 已存在，跳过")
                stats['skipped'] += 1
                continue
            
            # 获取 Embedding
            print(f"  - 获取 Embedding...")
            embedding = get_embedding(mem['content'][:2000])
            
            if embedding is None:
                print(f"  - Embedding 失败，跳过")
                stats['errors'] += 1
                continue
            
            # 准备数据
            batch_ids.append(doc_id)
            batch_embeddings.append(embedding)
            batch_metadatas.append({
                'filename': mem['filename'],
                'source': 'memory_fusion',
                'synced_at': datetime.now().isoformat(),
                'size': mem['size']
            })
            batch_documents.append(mem['content'][:5000])  # 限制文档长度
            
            print(f"  - 准备完成")
            stats['synced'] += 1
            
            # 批量插入
            if len(batch_ids) >= batch_size:
                self._insert_batch(batch_ids, batch_embeddings, batch_metadatas, batch_documents)
                batch_ids = []
                batch_embeddings = []
                batch_metadatas = []
                batch_documents = []
        
        # 插入剩余数据
        if batch_ids:
            self._insert_batch(batch_ids, batch_embeddings, batch_metadatas, batch_documents)
        
        print(f"\n同步完成!")
        print(f"  - 总计: {stats['total']}")
        print(f"  - 同步: {stats['synced']}")
        print(f"  - 跳过: {stats['skipped']}")
        print(f"  - 错误: {stats['errors']}")
        print(f"  - ChromaDB 记录数: {self.collection.count()}")
        
        return stats
    
    def _insert_batch(self, ids, embeddings, metadatas, documents):
        """批量插入数据"""
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents
            )
            print(f"  - 批量插入 {len(ids)} 条记录")
        except Exception as e:
            print(f"  - 批量插入失败: {e}")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """搜索记忆"""
        print(f"\n搜索: {query}")
        
        # 获取查询 Embedding
        query_embedding = get_embedding(query)
        
        if query_embedding is None:
            print("获取查询 Embedding 失败")
            return []
        
        # 搜索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # 格式化结果
        memories = []
        for i, doc_id in enumerate(results['ids'][0]):
            memories.append({
                'id': doc_id,
                'content': results['documents'][0][i][:500] + '...',
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if results['distances'] else None
            })
        
        return memories
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'collection_name': COLLECTION_NAME,
            'total_records': self.collection.count(),
            'db_path': CHROMA_DB_PATH
        }


# 命令行接口
if __name__ == "__main__":
    import sys
    
    fusion = MemoryFusion()
    
    if len(sys.argv) < 2:
        print("用法: python memory_fusion.py <command>")
        print("命令: sync, search <query>, stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'sync':
        fusion.sync_to_chromadb()
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("请输入搜索查询")
            sys.exit(1)
        query = ' '.join(sys.argv[2:])
        results = fusion.search(query)
        
        print(f"\n搜索结果 ({len(results)} 条):")
        print("-" * 60)
        for i, mem in enumerate(results):
            print(f"\n[{i+1}] {mem['metadata'].get('filename', 'unknown')}")
            print(f"    距离: {mem['distance']:.4f}" if mem['distance'] else "")
            print(f"    内容: {mem['content'][:100]}...")
    
    elif command == 'stats':
        stats = fusion.get_stats()
        print("\n记忆系统统计:")
        print("-" * 40)
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    else:
        print(f"未知命令: {command}")
