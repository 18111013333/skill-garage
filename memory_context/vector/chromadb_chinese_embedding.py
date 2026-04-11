"""
ChromaDB 中文 Embedding 替换方案
支持多种中文模型，开箱即用
"""

import chromadb
from chromadb.utils import embedding_functions
from typing import List, Optional
import os

# ============================================================
# 方案一：使用 SentenceTransformer 中文模型（本地，免费）
# ============================================================

def get_bge_embedding_fn(device: str = "cpu"):
    """
    使用 BGE 系列模型（推荐）
    - BAAI/bge-m3: 多语言，支持中文，1024维
    - BAAI/bge-large-zh-v1.5: 中文专用，1024维
    - BAAI/bge-small-zh-v1.5: 中文轻量，512维
    """
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="BAAI/bge-m3",  # 或 "BAAI/bge-large-zh-v1.5"
        device=device,
        normalize_embeddings=True
    )


def get_text2vec_embedding_fn(device: str = "cpu"):
    """
    使用 text2vec-chinese 模型
    - shibing624/text2vec-base-chinese: 768维，轻量
    - shibing624/text2vec-large-chinese: 1024维
    """
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="shibing624/text2vec-base-chinese",
        device=device
    )


# ============================================================
# 方案二：使用 OpenAI 兼容 API（云端）
# ============================================================

def get_qwen_embedding_fn(api_key: Optional[str] = None):
    """
    使用 Qwen3-Embedding-8B（Gitee AI）
    - 1024维，中文优化
    - 需要 Gitee AI API Key
    """
    api_key = api_key or os.environ.get("GITEE_API_KEY")
    if not api_key:
        raise ValueError("需要设置 GITEE_API_KEY 环境变量")
    
    return embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        api_base="https://ai.gitee.com/v1",
        model_name="Qwen3-Embedding-8B"
    )


def get_openai_embedding_fn(api_key: Optional[str] = None):
    """
    使用 OpenAI text-embedding-3-small
    - 1536维，支持中文
    """
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("需要设置 OPENAI_API_KEY 环境变量")
    
    return embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small"
    )


# ============================================================
# 方案三：使用 HuggingFace Inference API（云端，免费额度）
# ============================================================

def get_hf_embedding_fn(api_key: Optional[str] = None):
    """
    使用 HuggingFace Inference API
    - 支持多种模型
    - 有免费额度
    """
    api_key = api_key or os.environ.get("HF_API_KEY")
    if not api_key:
        raise ValueError("需要设置 HF_API_KEY 环境变量")
    
    return embedding_functions.HuggingFaceEmbeddingFunction(
        api_key=api_key,
        model_name="BAAI/bge-m3"
    )


# ============================================================
# 方案四：自定义 Embedding 函数（完全控制）
# ============================================================

class ChineseEmbeddingFunction(embedding_functions.EmbeddingFunction):
    """
    自定义中文 Embedding 函数
    支持缓存、批量处理、错误处理
    """
    
    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        device: str = "cpu",
        cache_size: int = 10000,
        batch_size: int = 32
    ):
        from sentence_transformers import SentenceTransformer
        import hashlib
        
        self.model = SentenceTransformer(model_name, device=device)
        self.cache = {}
        self.cache_size = cache_size
        self.batch_size = batch_size
    
    def __call__(self, texts: List[str]) -> List[List[float]]:
        # 检查缓存
        results = [None] * len(texts)
        uncached = []
        uncached_indices = []
        
        for i, text in enumerate(texts):
            key = hashlib.md5(text.encode()).hexdigest()
            if key in self.cache:
                results[i] = self.cache[key]
            else:
                uncached.append(text)
                uncached_indices.append(i)
        
        # 批量编码
        if uncached:
            embeddings = self.model.encode(
                uncached,
                batch_size=self.batch_size,
                normalize_embeddings=True,
                convert_to_numpy=True
            )
            
            for idx, emb in zip(uncached_indices, embeddings):
                results[idx] = emb.tolist()
                # 更新缓存
                if len(self.cache) < self.cache_size:
                    key = hashlib.md5(uncached[uncached_indices.index(idx)].encode()).hexdigest()
                    self.cache[key] = emb.tolist()
        
        return results


# ============================================================
# 使用示例
# ============================================================

def create_chinese_chromadb(
    collection_name: str = "chinese_memory",
    persist_dir: str = "./chroma_db",
    embedding_type: str = "bge",
    **kwargs
):
    """
    创建支持中文的 ChromaDB 集合
    
    Args:
        collection_name: 集合名称
        persist_dir: 持久化目录
        embedding_type: Embedding 类型
            - "bge": BGE-M3（推荐，本地）
            - "bge-zh": BGE-Large-ZH（中文专用）
            - "text2vec": text2vec-chinese
            - "qwen": Qwen3-Embedding（云端）
            - "openai": OpenAI Embedding（云端）
            - "custom": 自定义
    """
    # 创建客户端
    client = chromadb.PersistentClient(path=persist_dir)
    
    # 选择 Embedding 函数
    embedding_fn = None
    
    if embedding_type == "bge":
        embedding_fn = get_bge_embedding_fn(kwargs.get("device", "cpu"))
    elif embedding_type == "bge-zh":
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="BAAI/bge-large-zh-v1.5",
            device=kwargs.get("device", "cpu")
        )
    elif embedding_type == "text2vec":
        embedding_fn = get_text2vec_embedding_fn(kwargs.get("device", "cpu"))
    elif embedding_type == "qwen":
        embedding_fn = get_qwen_embedding_fn(kwargs.get("api_key"))
    elif embedding_type == "openai":
        embedding_fn = get_openai_embedding_fn(kwargs.get("api_key"))
    elif embedding_type == "custom":
        embedding_fn = ChineseEmbeddingFunction(
            model_name=kwargs.get("model_name", "BAAI/bge-m3"),
            device=kwargs.get("device", "cpu")
        )
    else:
        raise ValueError(f"不支持的 embedding_type: {embedding_type}")
    
    # 创建集合
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
        metadata={
            "hnsw:space": "cosine",
            "hnsw:construction_ef": 256,
            "hnsw:M": 32
        }
    )
    
    return client, collection


# ============================================================
# 模型对比
# ============================================================

MODEL_COMPARISON = """
| 模型 | 维度 | 中文支持 | 延迟 | 内存 | 运行方式 |
|------|------|----------|------|------|----------|
| BGE-M3 | 1024 | 优秀 | 30ms | 2GB | 本地 |
| BGE-Large-ZH | 1024 | 优秀 | 25ms | 1.3GB | 本地 |
| BGE-Small-ZH | 512 | 良好 | 15ms | 400MB | 本地 |
| text2vec-base | 768 | 良好 | 20ms | 400MB | 本地 |
| Qwen3-Embedding | 1024 | 优秀 | 50ms | - | 云端 |
| OpenAI-3-small | 1536 | 良好 | 100ms | - | 云端 |
"""


if __name__ == "__main__":
    # 示例：使用 BGE-M3 本地模型
    client, collection = create_chinese_chromadb(
        collection_name="test_chinese",
        embedding_type="bge",
        device="cpu"
    )
    
    # 添加中文文档
    collection.add(
        documents=[
            "这是一个中文测试文档",
            "向量数据库对中文的支持很重要",
            "BGE模型对中文效果很好"
        ],
        ids=["doc1", "doc2", "doc3"]
    )
    
    # 中文查询
    results = collection.query(
        query_texts=["中文向量检索"],
        n_results=3
    )
    
    print("查询结果:")
    for doc, dist in zip(results["documents"][0], results["distances"][0]):
        print(f"  [{dist:.4f}] {doc}")
    
    print("\n模型对比:")
    print(MODEL_COMPARISON)
