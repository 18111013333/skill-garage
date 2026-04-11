"""
Qwen3-Embedding-8B Embedding Provider
使用 Gitee AI 的 Qwen3-Embedding-8B 模型生成向量
"""

import os
import requests
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class QwenEmbedding:
    """Qwen3-Embedding-8B 向量生成器"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://ai.gitee.com/v1/embeddings",
        model: str = "Qwen3-Embedding-8B",
        dimension: int = 1024,
        batch_size: int = 32
    ):
        self.api_key = api_key or os.environ.get("GITEE_AI_API_KEY")
        self.base_url = base_url
        self.model = model
        self.dimension = dimension
        self.batch_size = batch_size

        if not self.api_key:
            raise ValueError("需要提供 Gitee AI API Key")

    def embed(self, text: str) -> List[float]:
        """生成单个文本的向量"""
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量生成向量"""
        all_embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            embeddings = self._call_api(batch)
            all_embeddings.extend(embeddings)

        return all_embeddings

    def _call_api(self, texts: List[str]) -> List[List[float]]:
        """调用 Gitee AI API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "input": texts
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            embeddings = [item["embedding"] for item in data["data"]]

            logger.info(f"生成向量: {len(embeddings)} 条, 维度: {len(embeddings[0])}")
            return embeddings

        except requests.exceptions.RequestException as e:
            logger.error(f"API 调用失败: {e}")
            raise

    def get_dimension(self) -> int:
        """返回向量维度"""
        return self.dimension


class EmbeddingFactory:
    """Embedding 工厂类"""

    @staticmethod
    def create(provider: str = "qwen", **kwargs):
        """创建 Embedding 提供者"""
        if provider == "qwen":
            return QwenEmbedding(**kwargs)
        elif provider == "voyage":
            # 保留原有 Voyage 支持
            from openclaw.memory import VoyageEmbedding
            return VoyageEmbedding(**kwargs)
        elif provider == "local":
            # 本地 Transformers.js
            return LocalEmbedding(**kwargs)
        else:
            raise ValueError(f"不支持的 Embedding 提供者: {provider}")


class LocalEmbedding:
    """本地 Transformers.js Embedding"""

    def __init__(self, model_path: str = "./models/transformers", dimension: int = 768):
        self.model_path = model_path
        self.dimension = dimension
        self._model = None

    def embed(self, text: str) -> List[float]:
        """生成向量"""
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量生成向量"""
        # 使用 Transformers.js 或 ONNX 模型
        # 这里需要根据实际模型实现
        raise NotImplementedError("本地模型需要安装 transformers 库")

    def get_dimension(self) -> int:
        return self.dimension


# 使用示例
if __name__ == "__main__":
    # Qwen3-Embedding-8B
    embedding = QwenEmbedding(api_key="your-api-key")
    vector = embedding.embed("这是一个测试文本")
    print(f"向量维度: {len(vector)}")
