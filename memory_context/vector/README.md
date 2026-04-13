# 向量系统配置指南

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动 Qdrant

```bash
# 使用 Docker
docker-compose up -d

# 或直接运行
docker run -p 6333:6333 qdrant/qdrant
```

### 3. 配置 API Key

```bash
# 设置 Gitee AI API Key
export GITEE_AI_API_KEY="your-api-key"
```

### 4. 使用示例

```python
from embedding_qwen import QwenEmbedding
from vector_qdrant import QdrantVectorStore

# 创建 Embedding
embedding = QwenEmbedding(api_key="your-api-key")

# 创建向量存储
store = QdrantVectorStore(host="localhost", port=6333)

# 生成向量
text = "这是一个测试文本"
vector = embedding.embed(text)

# 存储向量
store.upsert(
    ids=["test_001"],
    vectors=[vector],
    payloads=[{"text": text}]
)

# 搜索
query_vector = embedding.embed("测试")
results = store.search(query_vector=query_vector, limit=5)
print(results)
```

## 配置选项

### Qwen3-Embedding-8B

| 参数 | 默认值 | 说明 |
|------|--------|------|
| api_key | 环境变量 | Gitee AI API Key |
| base_url | https://ai.gitee.com/v1/embeddings | API 地址 |
| model | Qwen3-Embedding-8B | 模型名称 |
| dimension | 1024 | 向量维度 |
| batch_size | 32 | 批量大小 |

### Qdrant

| 参数 | 默认值 | 说明 |
|------|--------|------|
| host | localhost | Qdrant 主机 |
| port | 6333 | Qdrant 端口 |
| dimension | 1024 | 向量维度 |
| distance | cosine | 距离度量 |

### ChromaDB

| 参数 | 默认值 | 说明 |
|------|--------|------|
| persist_dir | ./chroma_db | 持久化目录 |
| dimension | 1024 | 向量维度 |

## 方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| Qdrant + Qwen | 高性能、中文优化 | 需要 API 调用 |
| ChromaDB + Qwen | 轻量级、易部署 | 性能略低 |
| Qdrant + 本地 | 完全离线、隐私 | 精度较低 |

## 获取 API Key

1. 访问 https://ai.gitee.com
2. 注册/登录账号
3. 进入 API 管理页面
4. 创建访问令牌
5. 每日免费 100 次

## 故障排查

### Qdrant 连接失败
```bash
# 检查 Qdrant 是否运行
curl http://localhost:6333/collections

# 重启 Qdrant
docker-compose restart
```

### API 调用失败
```bash
# 检查 API Key
echo $GITEE_AI_API_KEY

# 测试 API
curl -X POST https://ai.gitee.com/v1/embeddings \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen3-Embedding-8B", "input": "测试"}'
```
