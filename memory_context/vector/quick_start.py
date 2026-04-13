"""
快速开始 - Embedding 使用示例
"""

# ============================================
# 方式一：环境变量（推荐用于生产环境）
# ============================================

# 1. 先设置环境变量
# export GITEE_AI_API_KEY='your-api-key'

# 2. 在代码中使用
import os
from embedding_provider import QwenEmbeddingProvider

api_key = os.environ.get("GITEE_AI_API_KEY")
embedding = QwenEmbeddingProvider(api_key=api_key)

vector = embedding.embed("测试文本")
print(f"向量维度: {len(vector)}")


# ============================================
# 方式二：配置文件（适合本地开发）
# ============================================

from embedding_config import EmbeddingConfig

config = EmbeddingConfig()
config.set_api_key("qwen", "your-api-key")  # 保存到配置文件

# 后续使用
api_key = config.get_api_key("qwen")
embedding = QwenEmbeddingProvider(api_key=api_key)


# ============================================
# 方式三：直接传入（仅用于快速测试）
# ============================================

# ⚠️ 警告：不要在生产环境使用此方式！
embedding = QwenEmbeddingProvider(api_key="your-api-key")


# ============================================
# 完整示例：向量搜索
# ============================================

from embedding_provider import QwenEmbeddingProvider
from vector_qdrant import QdrantVectorStore

# 1. 创建 Embedding
embedding = QwenEmbeddingProvider(
    api_key=os.environ.get("GITEE_AI_API_KEY"),
    model="Qwen3-Embedding-8B",
    dimension=1024
)

# 2. 创建向量存储
store = QdrantVectorStore(
    host="localhost",
    port=6333,
    dimension=1024
)

# 3. 存储文档
documents = [
    "机器学习是人工智能的一个分支",
    "深度学习使用神经网络进行学习",
    "自然语言处理处理人类语言"
]

vectors = embedding.embed_batch(documents)
store.upsert(
    ids=[f"doc_{i}" for i in range(len(documents))],
    vectors=vectors,
    payloads=[{"text": doc} for doc in documents]
)

# 4. 搜索
query = "什么是 AI"
query_vector = embedding.embed(query)
results = store.search(query_vector=query_vector, limit=3)

for result in results:
    print(f"相似度: {result['score']:.3f}")
    print(f"内容: {result['payload']['text']}")
    print()
