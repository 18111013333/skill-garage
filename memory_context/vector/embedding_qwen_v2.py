"""
Qwen3-Embedding-8B 高级配置
支持 1024/2048/4096 维度
"""

import os
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class QwenEmbeddingAdvanced:
    """
    Qwen3-Embedding-8B 高级版
    支持多种维度：1024, 2048, 4096
    """

    # 支持的维度
    SUPPORTED_DIMENSIONS = [1024, 2048, 4096]

    def __init__(
        self,
        api_key: Optional[str] = None,
        dimension: int = 4096,
        model: str = "Qwen3-Embedding-8B",
        batch_size: int = 32,
        base_url: str = "https://ai.gitee.com/v1"
    ):
        # API Key
        self.api_key = api_key or os.environ.get("GITEE_AI_API_KEY") or os.environ.get("API_TOKEN")
        if not self.api_key:
            raise RuntimeError("需要设置环境变量 GITEE_AI_API_KEY 或 API_TOKEN")

        # 维度验证
        if dimension not in self.SUPPORTED_DIMENSIONS:
            raise ValueError(f"不支持的维度: {dimension}，支持: {self.SUPPORTED_DIMENSIONS}")

        self.dimension = dimension
        self.model = model
        self.batch_size = batch_size
        self.base_url = base_url

        logger.info(f"Qwen3-Embedding-8B 初始化: 维度={dimension}")

    def embed(self, text: str) -> List[float]:
        """生成单个文本的向量"""
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量生成向量"""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("需要安装 openai: pip install openai")

        client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            default_headers={"X-Failover-Enabled": "true"}
        )

        all_embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]

            response = client.embeddings.create(
                input=batch,
                model=self.model,
                dimensions=self.dimension
            )

            embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(embeddings)

            logger.info(f"生成向量: {len(embeddings)} 条, 维度: {len(embeddings[0])}")

        return all_embeddings

    def get_dimension(self) -> int:
        return self.dimension

    def get_model_name(self) -> str:
        return f"{self.model} (dim={self.dimension})"


# 使用示例
if __name__ == "__main__":
    import os

    # 环境变量方式
    API_TOKEN = os.getenv("API_TOKEN")
    if not API_TOKEN:
        raise RuntimeError("The environment variable API_TOKEN is not set correctly")

    # 创建 4096 维 Embedding
    embedding = QwenEmbeddingAdvanced(
        api_key=API_TOKEN,
        dimension=4096
    )

    # 生成向量
    text = "Today is a sunny day and I will get some ice cream."
    vector = embedding.embed(text)

    print(f"向量维度: {len(vector)}")  # 4096
    print(f"前10个值: {vector[:10]}")
