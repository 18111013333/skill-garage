"""
Qwen3-Embedding-8B 4096 维向量生成示例
"""

from openai import OpenAI
import os

# 环境变量方式（推荐）
API_TOKEN = os.getenv("API_TOKEN") or os.getenv("GITEE_AI_API_KEY")
if not API_TOKEN:
    raise RuntimeError("The environment variable API_TOKEN is not set correctly")

# 创建客户端
client = OpenAI(
    base_url="https://ai.gitee.com/v1",
    api_key=API_TOKEN,
    default_headers={"X-Failover-Enabled": "true"},
)

# 生成 4096 维向量
response = client.embeddings.create(
    input="Today is a sunny day and I will get some ice cream.",
    model="Qwen3-Embedding-8B",
    dimensions=4096,
)

# 获取向量
vector = response.data[0].embedding
print(f"向量维度: {len(vector)}")  # 4096
print(f"向量前10个值: {vector[:10]}")


# ============================================
# 批量生成示例
# ============================================

texts = [
    "机器学习是人工智能的一个分支",
    "深度学习使用神经网络进行学习",
    "自然语言处理处理人类语言"
]

response = client.embeddings.create(
    input=texts,
    model="Qwen3-Embedding-8B",
    dimensions=4096,
)

vectors = [item.embedding for item in response.data]
print(f"生成了 {len(vectors)} 个向量，每个维度: {len(vectors[0])}")


# ============================================
# 维度对比
# ============================================

print("\n=== 维度对比 ===")
for dim in [1024, 2048, 4096]:
    response = client.embeddings.create(
        input="测试文本",
        model="Qwen3-Embedding-8B",
        dimensions=dim,
    )
    print(f"维度 {dim}: 向量长度 = {len(response.data[0].embedding)}")
