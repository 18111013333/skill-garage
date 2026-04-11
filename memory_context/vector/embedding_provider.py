"""
统一 Embedding 接口
支持多种 Embedding 提供者
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import hashlib
import json

logger = logging.getLogger(__name__)


class EmbeddingProvider(ABC):
    """Embedding 提供者基类"""

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """生成单个文本的向量"""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量生成向量"""
        pass

    @abstractmethod
    def get_dimension(self) -> int:
        """获取向量维度"""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """获取提供者名称"""
        pass

    def get_model_name(self) -> str:
        """获取模型名称"""
        return "unknown"


class QwenEmbeddingProvider(EmbeddingProvider):
    """Qwen3-Embedding-8B 提供者"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "Qwen3-Embedding-8B",
        dimension: int = 1024,
        batch_size: int = 32,
        base_url: str = "https://ai.gitee.com/v1/embeddings"
    ):
        # 优先级：参数 > 环境变量 > 配置文件
        self.api_key = api_key or os.environ.get("GITEE_AI_API_KEY")
        self.model = model
        self.dimension = dimension
        self.batch_size = batch_size
        self.base_url = base_url

        if not self.api_key:
            raise ValueError("需要提供 Gitee AI API Key (GITEE_AI_API_KEY 或参数传入)")

    def embed(self, text: str) -> List[float]:
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        import requests

        all_embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "input": batch
            }

            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            data = response.json()
            embeddings = [item["embedding"] for item in data["data"]]
            all_embeddings.extend(embeddings)

            logger.info(f"Qwen Embedding: {len(embeddings)} 条, 维度: {len(embeddings[0])}")

        return all_embeddings

    def get_dimension(self) -> int:
        return self.dimension

    def get_provider_name(self) -> str:
        return "qwen"

    def get_model_name(self) -> str:
        return self.model


class VoyageEmbeddingProvider(EmbeddingProvider):
    """Voyage API 提供者"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "voyage-4-large",
        dimension: int = 1024,
        batch_size: int = 32
    ):
        self.api_key = api_key or os.environ.get("VOYAGE_API_KEY")
        self.model = model
        self.dimension = dimension
        self.batch_size = batch_size
        self.base_url = "https://api.voyageai.com/v1/embeddings"

        if not self.api_key:
            raise ValueError("需要提供 Voyage API Key (VOYAGE_API_KEY)")

    def embed(self, text: str) -> List[float]:
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        import requests

        all_embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "input": batch,
                "output_dimension": self.dimension
            }

            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            data = response.json()
            embeddings = [item["embedding"] for item in data["data"]]
            all_embeddings.extend(embeddings)

            logger.info(f"Voyage Embedding: {len(embeddings)} 条, 维度: {len(embeddings[0])}")

        return all_embeddings

    def get_dimension(self) -> int:
        return self.dimension

    def get_provider_name(self) -> str:
        return "voyage"

    def get_model_name(self) -> str:
        return self.model


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI Embedding 提供者"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "text-embedding-3-large",
        dimension: int = 3072,
        batch_size: int = 32
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.dimension = dimension
        self.batch_size = batch_size
        self.base_url = "https://api.openai.com/v1/embeddings"

        if not self.api_key:
            raise ValueError("需要提供 OpenAI API Key (OPENAI_API_KEY)")

    def embed(self, text: str) -> List[float]:
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        import requests

        all_embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "input": batch,
                "dimensions": self.dimension
            }

            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            data = response.json()
            embeddings = [item["embedding"] for item in data["data"]]
            all_embeddings.extend(embeddings)

            logger.info(f"OpenAI Embedding: {len(embeddings)} 条, 维度: {len(embeddings[0])}")

        return all_embeddings

    def get_dimension(self) -> int:
        return self.dimension

    def get_provider_name(self) -> str:
        return "openai"

    def get_model_name(self) -> str:
        return self.model


class LocalEmbeddingProvider(EmbeddingProvider):
    """本地 Embedding 提供者 (Transformers)"""

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        dimension: int = 384,
        device: str = "cpu"
    ):
        self.model_name = model_name
        self.dimension = dimension
        self.device = device
        self._model = None

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name, device=self.device)
                logger.info(f"加载本地模型: {self.model_name}")
            except ImportError:
                raise ImportError("需要安装 sentence-transformers: pip install sentence-transformers")

    def embed(self, text: str) -> List[float]:
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        self._load_model()
        embeddings = self._model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def get_dimension(self) -> int:
        return self.dimension

    def get_provider_name(self) -> str:
        return "local"

    def get_model_name(self) -> str:
        return self.model_name


class CachedEmbeddingProvider(EmbeddingProvider):
    """带缓存的 Embedding 提供者"""

    def __init__(self, provider: EmbeddingProvider, cache_size: int = 10000):
        self.provider = provider
        self.cache: Dict[str, List[float]] = {}
        self.cache_size = cache_size

    def _get_cache_key(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()

    def embed(self, text: str) -> List[float]:
        key = self._get_cache_key(text)
        if key in self.cache:
            return self.cache[key]

        embedding = self.provider.embed(text)
        self._add_to_cache(key, embedding)
        return embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        # 检查缓存
        results = []
        uncached_texts = []
        uncached_indices = []

        for i, text in enumerate(texts):
            key = self._get_cache_key(text)
            if key in self.cache:
                results.append(self.cache[key])
            else:
                results.append(None)
                uncached_texts.append(text)
                uncached_indices.append(i)

        # 生成未缓存的向量
        if uncached_texts:
            new_embeddings = self.provider.embed_batch(uncached_texts)
            for idx, embedding in zip(uncached_indices, new_embeddings):
                results[idx] = embedding
                key = self._get_cache_key(texts[idx])
                self._add_to_cache(key, embedding)

        return results

    def _add_to_cache(self, key: str, embedding: List[float]):
        if len(self.cache) >= self.cache_size:
            # 简单的 LRU：删除最早的条目
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        self.cache[key] = embedding

    def get_dimension(self) -> int:
        return self.provider.get_dimension()

    def get_provider_name(self) -> str:
        return f"cached_{self.provider.get_provider_name()}"

    def get_model_name(self) -> str:
        return self.provider.get_model_name()

    def clear_cache(self):
        self.cache.clear()


class EmbeddingRegistry:
    """Embedding 提供者注册表"""

    _providers: Dict[str, EmbeddingProvider] = {}
    _default: Optional[str] = None

    @classmethod
    def register(cls, name: str, provider: EmbeddingProvider, is_default: bool = False):
        """注册提供者"""
        cls._providers[name] = provider
        if is_default or cls._default is None:
            cls._default = name
        logger.info(f"注册 Embedding 提供者: {name}")

    @classmethod
    def get(cls, name: Optional[str] = None) -> EmbeddingProvider:
        """获取提供者"""
        name = name or cls._default
        if name is None:
            raise ValueError("没有注册的 Embedding 提供者")
        if name not in cls._providers:
            raise ValueError(f"未知的 Embedding 提供者: {name}")
        return cls._providers[name]

    @classmethod
    def list_providers(cls) -> List[str]:
        """列出所有提供者"""
        return list(cls._providers.keys())

    @classmethod
    def get_default_name(cls) -> Optional[str]:
        """获取默认提供者名称"""
        return cls._default


def create_embedding_provider(config: Dict[str, Any]) -> EmbeddingProvider:
    """根据配置创建 Embedding 提供者"""
    provider_type = config.get("provider", "qwen")

    if provider_type == "qwen":
        provider = QwenEmbeddingProvider(
            api_key=config.get("api_key"),
            model=config.get("model", "Qwen3-Embedding-8B"),
            dimension=config.get("dimension", 1024),
            batch_size=config.get("batch_size", 32)
        )
    elif provider_type == "voyage":
        provider = VoyageEmbeddingProvider(
            api_key=config.get("api_key"),
            model=config.get("model", "voyage-4-large"),
            dimension=config.get("dimension", 1024),
            batch_size=config.get("batch_size", 32)
        )
    elif provider_type == "openai":
        provider = OpenAIEmbeddingProvider(
            api_key=config.get("api_key"),
            model=config.get("model", "text-embedding-3-large"),
            dimension=config.get("dimension", 3072),
            batch_size=config.get("batch_size", 32)
        )
    elif provider_type == "local":
        provider = LocalEmbeddingProvider(
            model_name=config.get("model", "sentence-transformers/all-MiniLM-L6-v2"),
            dimension=config.get("dimension", 384),
            device=config.get("device", "cpu")
        )
    else:
        raise ValueError(f"未知的 Embedding 提供者类型: {provider_type}")

    # 添加缓存
    if config.get("cache", True):
        provider = CachedEmbeddingProvider(
            provider,
            cache_size=config.get("cache_size", 10000)
        )

    return provider


# 使用示例
if __name__ == "__main__":
    # 注册提供者
    EmbeddingRegistry.register(
        "qwen",
        QwenEmbeddingProvider(api_key="your-key"),
        is_default=True
    )

    # 使用
    embedding = EmbeddingRegistry.get()
    vector = embedding.embed("测试文本")
    print(f"向量维度: {len(vector)}")
