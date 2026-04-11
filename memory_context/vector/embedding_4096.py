"""
Qwen3-Embedding-8B 4096维向量生成
完整配置示例
"""

from openai import OpenAI
import os

# 环境变量配置
API_TOKEN = os.getenv("API_TOKEN")
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
    dimensions=4096,  # 升级到 4096 维
)

# 获取向量
vector = response.data[0].embedding
print(f"向量维度: {len(vector)}")  # 4096
print(f"向量前10个值: {vector[:10]}")
