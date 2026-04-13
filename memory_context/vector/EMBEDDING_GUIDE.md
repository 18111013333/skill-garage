# Embedding 系统完整指南

## 一、支持的 Embedding 模型

### 1.1 云端 API 模型

| 模型 | 提供者 | 维度 | 中文效果 | 免费额度 |
|------|--------|------|----------|----------|
| Qwen3-Embedding-8B | Gitee AI | 1024 | ⭐⭐⭐⭐⭐ | 100次/天 |
| Voyage-4-Large | Voyage AI | 1024 | ⭐⭐⭐⭐ | 付费 |
| text-embedding-3-large | OpenAI | 3072 | ⭐⭐⭐ | 付费 |

### 1.2 本地模型

| 模型 | 维度 | 中文效果 | 大小 | 速度 |
|------|------|----------|------|------|
| text2vec-base-chinese | 768 | ⭐⭐⭐⭐ | ~400MB | 快 |
| all-MiniLM-L6-v2 | 384 | ⭐⭐ | ~90MB | 最快 |
| paraphrase-multilingual | 768 | ⭐⭐⭐ | ~400MB | 中等 |

---

## 二、快速开始

### 2.1 安装依赖

```bash
# 基础依赖
pip install requests

# 本地模型支持
pip install sentence-transformers

# 向量数据库
pip install qdrant-client chromadb
```

### 2.2 配置 API Key

```bash
# Gitee AI (Qwen3-Embedding-8B)
export GITEE_AI_API_KEY="your-api-key"

# Voyage AI
export VOYAGE_API_KEY="your-api-key"

# OpenAI
export OPENAI_API_KEY="your-api-key"
```

### 2.3 基本使用

```python
from embedding_provider import QwenEmbeddingProvider, EmbeddingRegistry

# 方式1: 直接创建
embedding = QwenEmbeddingProvider(api_key="your-key")
vector = embedding.embed("测试文本")
print(f"维度: {len(vector)}")

# 方式2: 使用注册表
EmbeddingRegistry.register("qwen", QwenEmbeddingProvider(api_key="your-key"), is_default=True)
embedding = EmbeddingRegistry.get()
vector = embedding.embed("测试文本")
```

---

## 三、模型对比

### 3.1 维度对比

```
OpenAI text-embedding-3-large:  3072 维 ████████████████████████████████
Qwen3-Embedding-8B:             1024 维 ██████████
Voyage-4-Large:                 1024 维 ██████████
text2vec-base-chinese:           768 维 ███████
all-MiniLM-L6-v2:                384 维 ███
```

### 3.2 性能对比

| 指标 | Qwen | Voyage | OpenAI | 本地 |
|------|------|--------|--------|------|
| 单条延迟 | ~200ms | ~150ms | ~200ms | ~10ms |
| 批量吞吐 | 50/s | 60/s | 50/s | 500/s |
| 中文效果 | 优秀 | 良好 | 一般 | 良好 |
| 成本 | 免费 | 付费 | 付费 | 免费 |

### 3.3 推荐选择

| 场景 | 推荐模型 |
|------|----------|
| 中文为主 | Qwen3-Embedding-8B |
| 英文为主 | Voyage-4-Large |
| 离线环境 | text2vec-base-chinese |
| 成本敏感 | Qwen3-Embedding-8B (免费) |
| 最高精度 | OpenAI text-embedding-3-large |

---

## 四、高级功能

### 4.1 缓存

```python
from embedding_provider import CachedEmbeddingProvider, QwenEmbeddingProvider

# 创建带缓存的提供者
base_provider = QwenEmbeddingProvider(api_key="your-key")
cached_provider = CachedEmbeddingProvider(base_provider, cache_size=10000)

# 重复查询会使用缓存
vector1 = cached_provider.embed("测试")  # 调用 API
vector2 = cached_provider.embed("测试")  # 使用缓存
```

### 4.2 回退链

```python
from embedding_provider import EmbeddingRegistry, QwenEmbeddingProvider, LocalEmbeddingProvider

# 注册多个提供者
EmbeddingRegistry.register("qwen", QwenEmbeddingProvider(api_key="key"))
EmbeddingRegistry.register("local", LocalEmbeddingProvider(), is_default=True)

# 主提供者失败时自动回退
fallback_chain = ["qwen", "local"]
for name in fallback_chain:
    try:
        provider = EmbeddingRegistry.get(name)
        vector = provider.embed("测试")
        break
    except Exception:
        continue
```

### 4.3 批量处理

```python
# 批量生成向量
texts = ["文本1", "文本2", "文本3", ...]
vectors = embedding.embed_batch(texts)

# 存储到向量数据库
from vector_qdrant import QdrantVectorStore

store = QdrantVectorStore()
store.upsert(
    ids=[f"doc_{i}" for i in range(len(texts))],
    vectors=vectors,
    payloads=[{"text": t} for t in texts]
)
```

---

## 五、获取 API Key

### 5.1 Gitee AI (Qwen3-Embedding-8B)

1. 访问 https://ai.gitee.com
2. 注册/登录
3. 进入「API 管理」
4. 创建访问令牌
5. 每日免费 100 次

### 5.2 Voyage AI

1. 访问 https://www.voyageai.com
2. 注册账号
3. 获取 API Key
4. 按使用量付费

### 5.3 OpenAI

1. 访问 https://platform.openai.com
2. 注册账号
3. 获取 API Key
4. 按使用量付费

---

## 六、故障排查

### 6.1 API 调用失败

```python
# 检查 API Key
import os
print(os.environ.get("GITEE_AI_API_KEY"))

# 测试 API
import requests
response = requests.post(
    "https://ai.gitee.com/v1/embeddings",
    headers={"Authorization": "Bearer YOUR_KEY"},
    json={"model": "Qwen3-Embedding-8B", "input": "测试"}
)
print(response.status_code, response.json())
```

### 6.2 本地模型加载失败

```bash
# 安装依赖
pip install sentence-transformers

# 下载模型
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('shibing624/text2vec-base-chinese')"
```

### 6.3 维度不匹配

```python
# 检查维度
embedding = QwenEmbeddingProvider()
print(f"模型维度: {embedding.get_dimension()}")

# 向量数据库配置需要匹配
store = QdrantVectorStore(dimension=embedding.get_dimension())
```

---

## 版本
- 版本: V9.0.1
- 更新时间: 2026-04-07
