"""
Qdrant 向量数据库客户端
支持本地和云端部署
"""

import os
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# 尝试导入 qdrant-client
try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import (
        Distance, VectorParams, PointStruct,
        Filter, FieldCondition, MatchValue
    )
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    logger.warning("qdrant-client 未安装，请运行: pip install qdrant-client")


class QdrantVectorStore:
    """Qdrant 向量存储"""

    DEFAULT_COLLECTION = "openclaw_memory"

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        api_key: Optional[str] = None,
        url: Optional[str] = None,
        dimension: int = 4096,  # 默认升级到 4096
        distance: str = "cosine"
    ):
        if not QDRANT_AVAILABLE:
            raise ImportError("需要安装 qdrant-client: pip install qdrant-client")

        # 连接方式
        if url:
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            self.client = QdrantClient(host=host, port=port, api_key=api_key)

        self.dimension = dimension
        self.distance = Distance.COSINE if distance == "cosine" else Distance.EUCLID

    def create_collection(self, collection_name: str = None):
        """创建集合"""
        collection_name = collection_name or self.DEFAULT_COLLECTION

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=self.dimension,
                distance=self.distance
            )
        )
        logger.info(f"创建集合: {collection_name}")

    def delete_collection(self, collection_name: str = None):
        """删除集合"""
        collection_name = collection_name or self.DEFAULT_COLLECTION
        self.client.delete_collection(collection_name=collection_name)
        logger.info(f"删除集合: {collection_name}")

    def collection_exists(self, collection_name: str = None) -> bool:
        """检查集合是否存在"""
        collection_name = collection_name or self.DEFAULT_COLLECTION
        collections = self.client.get_collections()
        return any(c.name == collection_name for c in collections.collections)

    def upsert(
        self,
        ids: List[str],
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
        collection_name: str = None
    ):
        """插入或更新向量"""
        collection_name = collection_name or self.DEFAULT_COLLECTION

        # 确保集合存在
        if not self.collection_exists(collection_name):
            self.create_collection(collection_name)

        # 构建点
        points = [
            PointStruct(
                id=id_,
                vector=vector,
                payload=payload
            )
            for id_, vector, payload in zip(ids, vectors, payloads)
        ]

        # 批量插入
        self.client.upsert(
            collection_name=collection_name,
            points=points
        )
        logger.info(f"插入向量: {len(points)} 条")

    def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        filter_conditions: Optional[Dict] = None,
        collection_name: str = None
    ) -> List[Dict[str, Any]]:
        """搜索相似向量"""
        collection_name = collection_name or self.DEFAULT_COLLECTION

        # 构建过滤条件
        query_filter = None
        if filter_conditions:
            conditions = [
                FieldCondition(
                    key=k,
                    match=MatchValue(value=v)
                )
                for k, v in filter_conditions.items()
            ]
            query_filter = Filter(must=conditions)

        # 搜索
        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=query_filter
        )

        return [
            {
                "id": str(result.id),
                "score": result.score,
                "payload": result.payload
            }
            for result in results
        ]

    def delete(self, ids: List[str], collection_name: str = None):
        """删除向量"""
        collection_name = collection_name or self.DEFAULT_COLLECTION
        self.client.delete(
            collection_name=collection_name,
            points_selector=ids
        )
        logger.info(f"删除向量: {len(ids)} 条")

    def count(self, collection_name: str = None) -> int:
        """统计向量数量"""
        collection_name = collection_name or self.DEFAULT_COLLECTION
        info = self.client.get_collection(collection_name=collection_name)
        return info.points_count


class ChromaVectorStore:
    """ChromaDB 向量存储"""

    DEFAULT_COLLECTION = "openclaw_memory"

    def __init__(
        self,
        persist_dir: str = "./chroma_db",
        dimension: int = 4096  # 默认升级到 4096
    ):
        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError:
            raise ImportError("需要安装 chromadb: pip install chromadb")

        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_dir=persist_dir
        ))
        self.dimension = dimension

    def get_collection(self, name: str = None):
        """获取或创建集合"""
        name = name or self.DEFAULT_COLLECTION
        return self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )

    def upsert(
        self,
        ids: List[str],
        vectors: List[List[float]],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        collection_name: str = None
    ):
        """插入或更新向量"""
        collection = self.get_collection(collection_name)
        collection.upsert(
            ids=ids,
            embeddings=vectors,
            documents=documents,
            metadatas=metadatas
        )
        logger.info(f"插入向量: {len(ids)} 条")

    def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        filter_conditions: Optional[Dict] = None,
        collection_name: str = None
    ) -> List[Dict[str, Any]]:
        """搜索相似向量"""
        collection = self.get_collection(collection_name)
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=limit,
            where=filter_conditions
        )

        return [
            {
                "id": id_,
                "score": 1 - distance,  # ChromaDB 返回距离，转换为相似度
                "document": doc,
                "metadata": meta
            }
            for id_, distance, doc, meta in zip(
                results["ids"][0],
                results["distances"][0],
                results["documents"][0],
                results["metadatas"][0]
            )
        ]

    def delete(self, ids: List[str], collection_name: str = None):
        """删除向量"""
        collection = self.get_collection(collection_name)
        collection.delete(ids=ids)
        logger.info(f"删除向量: {len(ids)} 条")

    def count(self, collection_name: str = None) -> int:
        """统计向量数量"""
        collection = self.get_collection(collection_name)
        return collection.count()


class VectorStoreFactory:
    """向量存储工厂"""

    @staticmethod
    def create(store_type: str = "qdrant", **kwargs):
        """创建向量存储"""
        if store_type == "qdrant":
            return QdrantVectorStore(**kwargs)
        elif store_type == "chroma":
            return ChromaVectorStore(**kwargs)
        else:
            raise ValueError(f"不支持的向量存储类型: {store_type}")


# 使用示例
if __name__ == "__main__":
    # Qdrant
    store = QdrantVectorStore(host="localhost", port=6333)

    # 插入向量
    store.upsert(
        ids=["mem_001", "mem_002"],
        vectors=[[0.1] * 1024, [0.2] * 1024],
        payloads=[
            {"text": "记忆1", "source": "memory"},
            {"text": "记忆2", "source": "memory"}
        ]
    )

    # 搜索
    results = store.search(query_vector=[0.1] * 1024, limit=5)
    print(f"搜索结果: {results}")
