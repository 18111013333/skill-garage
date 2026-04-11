"""
中文 Embedding 云端方案（无需本地安装）
直接使用 API，无需 PyTorch/Sentence-Transformers
"""

import os
import requests
from typing import List, Optional
import chromadb
from chromadb.utils import embedding_functions

# ============================================================
# 方案一：Gitee AI - Qwen3-Embedding-8B（推荐）
# ============================================================

def get_qwen_embedding_fn(api_key: Optional[str] = None):
    """
    Qwen3-Embedding-8B
    - 中文效果: 95/100
    - 维度: 1024
    - 免费额度: 100次/天
    - 需要: GITEE_API_KEY
    """
    api_key = api_key or os.environ.get("GITEE_API_KEY")
    if not api_key:
        raise ValueError("需要设置 GITEE_API_KEY 环境变量")
    
    return embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        api_base="https://ai.gitee.com/v1",
        model_name="Qwen3-Embedding-8B"
    )


# ============================================================
# 方案二：OpenAI API
# ============================================================

def get_openai_embedding_fn(api_key: Optional[str] = None):
    """
    OpenAI text-embedding-3-small
    - 中文效果: 88/100
    - 维度: 1536
    - 需要: OPENAI_API_KEY
    """
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("需要设置 OPENAI_API_KEY 环境变量")
    
    return embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small"
    )


def get_openai_large_embedding_fn(api_key: Optional[str] = None):
    """
    OpenAI text-embedding-3-large
    - 中文效果: 90/100
    - 维度: 3072
    - 需要: OPENAI_API_KEY
    """
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("需要设置 OPENAI_API_KEY 环境变量")
    
    return embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-large"
    )


# ============================================================
# 方案三：自定义 API 调用（通用）
# ============================================================

class CloudEmbeddingFunction(embedding_functions.EmbeddingFunction):
    """
    通用云端 Embedding 函数
    支持任何 OpenAI 兼容 API
    """
    
    def __init__(
        self,
        api_key: str,
        api_base: str,
        model_name: str,
        batch_size: int = 32,
        timeout: int = 30
    ):
        self.api_key = api_key
        self.api_base = api_base.rstrip("/")
        self.model_name = model_name
        self.batch_size = batch_size
        self.timeout = timeout
    
    def __call__(self, texts: List[str]) -> List[List[float]]:
        all_embeddings = []
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            
            response = requests.post(
                f"{self.api_base}/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model_name,
                    "input": batch
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()["data"]
                data.sort(key=lambda x: x["index"])
                embeddings = [item["embedding"] for item in data]
                all_embeddings.extend(embeddings)
            else:
                raise Exception(f"API error: {response.status_code} - {response.text}")
        
        return all_embeddings


# ============================================================
# 方案四：HuggingFace Inference API
# ============================================================

def get_hf_embedding_fn(api_key: Optional[str] = None, model: str = "BAAI/bge-m3"):
    """
    HuggingFace Inference API
    - 免费额度有限
    - 支持多种模型
    """
    api_key = api_key or os.environ.get("HF_API_KEY")
    if not api_key:
        raise ValueError("需要设置 HF_API_KEY 环境变量")
    
    return embedding_functions.HuggingFaceEmbeddingFunction(
        api_key=api_key,
        model_name=model
    )


# ============================================================
# 快速使用
# ============================================================

def create_chromadb_with_cloud_embedding(
    collection_name: str = "chinese_memory",
    persist_dir: str = "./chroma_db",
    provider: str = "qwen",
    api_key: Optional[str] = None
):
    """
    创建使用云端 Embedding 的 ChromaDB
    
    Args:
        provider: "qwen" | "openai" | "openai-large" | "hf"
    """
    client = chromadb.PersistentClient(path=persist_dir)
    
    if provider == "qwen":
        embedding_fn = get_qwen_embedding_fn(api_key)
    elif provider == "openai":
        embedding_fn = get_openai_embedding_fn(api_key)
    elif provider == "openai-large":
        embedding_fn = get_openai_large_embedding_fn(api_key)
    elif provider == "hf":
        embedding_fn = get_hf_embedding_fn(api_key)
    else:
        raise ValueError(f"不支持的 provider: {provider}")
    
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"}
    )
    
    return client, collection


# ============================================================
# 云端方案对比
# ============================================================

CLOUD_PROVIDERS = """
| Provider | 模型 | 维度 | 中文效果 | 免费额度 | 延迟 |
|----------|------|------|----------|----------|------|
| Gitee AI | Qwen3-Embedding-8B | 1024 | 95/100 | 100次/天 | 50ms |
| OpenAI | text-embedding-3-small | 1536 | 88/100 | 付费 | 100ms |
| OpenAI | text-embedding-3-large | 3072 | 90/100 | 付费 | 150ms |
| HuggingFace | BGE-M3 | 1024 | 95/100 | 有限 | 200ms |
"""


if __name__ == "__main__":
    print("云端 Embedding 方案对比:")
    print(CLOUD_PROVIDERS)
    
    print("\n使用示例:")
    print("""
# 设置环境变量
export GITEE_API_KEY="your_api_key"

# 使用
from cloud_embedding_only import create_chromadb_with_cloud_embedding

client, collection = create_chromadb_with_cloud_embedding(
    provider="qwen"
)

collection.add(
    documents=["中文文档"],
    ids=["1"]
)
""")
