"""
Qwen3-Embedding-8B 自定义 Embedding 函数
用于 ChromaDB 中文优化

使用方法:
    from qwen_embedding import QwenEmbeddingFunction
    
    embedding_fn = QwenEmbeddingFunction(
        api_key="YOUR_GITEE_API_KEY",
        dimension=1024
    )
    
    collection = client.create_collection(
        name="chinese_memory",
        embedding_function=embedding_fn
    )
"""

from typing import List, Optional, Dict
import chromadb
from chromadb.api.types import EmbeddingFunction
import requests
import hashlib
import time
import logging

logger = logging.getLogger(__name__)


class QwenEmbeddingFunction(EmbeddingFunction):
    """
    Qwen3-Embedding-8B Embedding 函数
    
    特点:
    - 支持中文、英文
    - 1024 维向量
    - 最大 8192 tokens
    - 批量处理
    - 内置缓存
    """
    
    def __init__(
        self,
        api_key: str,
        dimension: int = 1024,
        batch_size: int = 32,
        cache_size: int = 10000,
        timeout: int = 30,
        api_base: str = "https://ai.gitee.com/v1/embeddings"
    ):
        """
        初始化
        
        Args:
            api_key: Gitee AI API Key
            dimension: 向量维度 (1024 或 4096)
            batch_size: 批量处理大小
            cache_size: 缓存大小
            timeout: 请求超时时间(秒)
            api_base: API 地址
        """
        self.api_key = api_key
        self.api_base = api_base
        self.model = "Qwen3-Embedding-8B"
        self.dimension = dimension
        self.batch_size = batch_size
        self.timeout = timeout
        self._cache: Dict[str, List[float]] = {}
        self._cache_size = cache_size
        
        # 性能统计
        self._stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "total_latency_ms": 0,
            "total_texts": 0
        }
    
    def __call__(self, texts: List[str]) -> List[List[float]]:
        """
        生成向量
        
        Args:
            texts: 文本列表
            
        Returns:
            向量列表
        """
        if not texts:
            return []
        
        start_time = time.time()
        results: List[Optional[List[float]]] = [None] * len(texts)
        uncached_texts = []
        uncached_indices = []
        
        # 检查缓存
        for i, text in enumerate(texts):
            cache_key = self._get_cache_key(text)
            if cache_key in self._cache:
                results[i] = self._cache[cache_key]
                self._stats["cache_hits"] += 1
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)
        
        # 批量请求未缓存的文本
        if uncached_texts:
            try:
                embeddings = self._batch_embed(uncached_texts)
                for idx, emb in zip(uncached_indices, embeddings):
                    results[idx] = emb
                    # 更新缓存
                    cache_key = self._get_cache_key(uncached_texts[uncached_indices.index(idx)])
                    self._update_cache(cache_key, emb)
            except Exception as e:
                logger.error(f"Embedding error: {e}")
                # 降级：返回零向量
                for idx in uncached_indices:
                    results[idx] = [0.0] * self.dimension
        
        # 更新统计
        latency_ms = (time.time() - start_time) * 1000
        self._stats["total_requests"] += 1
        self._stats["total_latency_ms"] += latency_ms
        self._stats["total_texts"] += len(texts)
        
        return results
    
    def _batch_embed(self, texts: List[str]) -> List[List[float]]:
        """
        批量向量化
        
        Args:
            texts: 文本列表
            
        Returns:
            向量列表
        """
        all_embeddings = []
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            
            response = requests.post(
                self.api_base,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "input": batch,
                    "encoding_format": "float"
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()["data"]
                # 按 index 排序
                data.sort(key=lambda x: x["index"])
                embeddings = [item["embedding"] for item in data]
                all_embeddings.extend(embeddings)
            elif response.status_code == 429:
                # 限流，等待后重试
                logger.warning("Rate limited, waiting...")
                time.sleep(1)
                # 递归重试
                all_embeddings.extend(self._batch_embed(batch))
            else:
                raise Exception(f"Embedding API error: {response.status_code} - {response.text}")
        
        return all_embeddings
    
    def _get_cache_key(self, text: str) -> str:
        """生成缓存键"""
        return hashlib.md5(f"{self.model}:{text}".encode()).hexdigest()
    
    def _update_cache(self, key: str, embedding: List[float]):
        """更新缓存"""
        if len(self._cache) >= self._cache_size:
            # LRU 淘汰
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        self._cache[key] = embedding
    
    def get_stats(self) -> dict:
        """获取性能统计"""
        avg_latency = (
            self._stats["total_latency_ms"] / self._stats["total_requests"]
            if self._stats["total_requests"] > 0 else 0
        )
        cache_hit_rate = (
            self._stats["cache_hits"] / self._stats["total_texts"]
            if self._stats["total_texts"] > 0 else 0
        )
        
        return {
            "total_requests": self._stats["total_requests"],
            "total_texts": self._stats["total_texts"],
            "cache_hits": self._stats["cache_hits"],
            "cache_hit_rate": f"{cache_hit_rate:.2%}",
            "avg_latency_ms": f"{avg_latency:.2f}",
            "cache_size": len(self._cache)
        }
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
    
    def clear_stats(self):
        """重置统计"""
        self._stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "total_latency_ms": 0,
            "total_texts": 0
        }


class CachedQwenEmbeddingFunction(EmbeddingFunction):
    """
    带磁盘缓存的 Qwen Embedding 函数
    适合长期运行的场景
    """
    
    def __init__(
        self,
        api_key: str,
        cache_dir: str = "./embedding_cache",
        dimension: int = 1024,
        **kwargs
    ):
        """
        初始化
        
        Args:
            api_key: API Key
            cache_dir: 缓存目录
            dimension: 向量维度
            **kwargs: 其他参数传递给 QwenEmbeddingFunction
        """
        import os
        import json
        
        self.cache_dir = cache_dir
        self.dimension = dimension
        os.makedirs(cache_dir, exist_ok=True)
        
        self.base_fn = QwenEmbeddingFunction(
            api_key=api_key,
            dimension=dimension,
            **kwargs
        )
        
        self._disk_cache: Dict[str, str] = {}  # key -> cache_file
        self._load_disk_cache_index()
    
    def _load_disk_cache_index(self):
        """加载磁盘缓存索引"""
        import os
        import json
        
        index_file = f"{self.cache_dir}/index.json"
        if os.path.exists(index_file):
            with open(index_file, "r") as f:
                self._disk_cache = json.load(f)
    
    def _save_disk_cache_index(self):
        """保存磁盘缓存索引"""
        import json
        
        index_file = f"{self.cache_dir}/index.json"
        with open(index_file, "w") as f:
            json.dump(self._disk_cache, f)
    
    def __call__(self, texts: List[str]) -> List[List[float]]:
        """生成向量"""
        import os
        import json
        
        results: List[Optional[List[float]]] = [None] * len(texts)
        uncached_texts = []
        uncached_indices = []
        
        # 检查磁盘缓存
        for i, text in enumerate(texts):
            cache_key = hashlib.md5(f"{text}".encode()).hexdigest()
            if cache_key in self._disk_cache:
                cache_file = f"{self.cache_dir}/{cache_key}.json"
                if os.path.exists(cache_file):
                    with open(cache_file, "r") as f:
                        results[i] = json.load(f)
                    continue
            
            uncached_texts.append(text)
            uncached_indices.append(i)
        
        # 请求新向量
        if uncached_texts:
            embeddings = self.base_fn(uncached_texts)
            for idx, emb in zip(uncached_indices, embeddings):
                results[idx] = emb
                
                # 保存到磁盘缓存
                cache_key = hashlib.md5(f"{uncached_texts[uncached_indices.index(idx)]}".encode()).hexdigest()
                cache_file = f"{self.cache_dir}/{cache_key}.json"
                with open(cache_file, "w") as f:
                    json.dump(emb, f)
                self._disk_cache[cache_key] = cache_file
            
            self._save_disk_cache_index()
        
        return results


# 使用示例
if __name__ == "__main__":
    import os
    
    # 从环境变量获取 API Key
    api_key = os.environ.get("GITEE_API_KEY", "your_api_key")
    
    # 创建 Embedding 函数
    embedding_fn = QwenEmbeddingFunction(
        api_key=api_key,
        dimension=1024,
        batch_size=32,
        cache_size=10000
    )
    
    # 创建 ChromaDB 客户端
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # 创建集合
    collection = client.get_or_create_collection(
        name="chinese_memory",
        embedding_function=embedding_fn,
        metadata={
            "hnsw:space": "cosine",
            "hnsw:construction_ef": 256,
            "hnsw:M": 32
        }
    )
    
    # 添加文档
    collection.add(
        documents=[
            "这是一个中文测试文档",
            "向量数据库对中文的支持很重要",
            "Qwen3-Embedding-8B 对中文效果很好"
        ],
        ids=["doc1", "doc2", "doc3"]
    )
    
    # 查询
    results = collection.query(
        query_texts=["中文向量检索"],
        n_results=3
    )
    
    print("查询结果:")
    for doc, dist in zip(results["documents"][0], results["distances"][0]):
        print(f"  [{dist:.4f}] {doc}")
    
    # 打印统计
    print("\n性能统计:")
    stats = embedding_fn.get_stats()
    for k, v in stats.items():
        print(f"  {k}: {v}")
