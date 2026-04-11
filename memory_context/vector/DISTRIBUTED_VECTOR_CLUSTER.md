# DISTRIBUTED_VECTOR_CLUSTER.md - 分布式向量集群

## 目标
支持 10亿+ 向量，实现大规模分布式向量存储。

## 架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                    分布式向量集群架构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    路由层                                │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐               │  │
│  │  │哈希路由  │ │范围路由  │ │智能路由  │               │  │
│  │  └──────────┘ └──────────┘ └──────────┘               │  │
│  └─────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    分片层                                │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │  │
│  │  │ Shard 1  │ │ Shard 2  │ │ Shard 3  │ │ Shard N  │  │  │
│  │  │ 1亿向量  │ │ 1亿向量  │ │ 1亿向量  │ │ 1亿向量  │  │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │  │
│  └─────────────────────────────────────────────────────────┘  │
│                            ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    复制层                                │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐               │  │
│  │  │主副本    │ │从副本1   │ │从副本2   │               │  │
│  │  └──────────┘ └──────────┘ └──────────┘               │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心能力

### 1. 分片策略
```python
class VectorSharding:
    """向量分片"""
    
    def __init__(self, n_shards: int = 10):
        self.n_shards = n_shards
        self.shards = [QdrantClient(f"shard_{i}") for i in range(n_shards)]
    
    def get_shard(self, vector_id: str) -> int:
        """计算向量所属分片"""
        return hash(vector_id) % self.n_shards
    
    async def add_vector(self, vector_id: str, vector: list, metadata: dict):
        """添加向量到对应分片"""
        shard_idx = self.get_shard(vector_id)
        await self.shards[shard_idx].add_vector(vector_id, vector, metadata)
    
    async def search(self, query_vector: list, top_k: int = 10) -> list:
        """并行搜索所有分片"""
        tasks = [
            shard.search(query_vector, top_k=top_k)
            for shard in self.shards
        ]
        results = await asyncio.gather(*tasks)
        
        # 合并结果
        all_results = [r for shard_results in results for r in shard_results]
        all_results.sort(key=lambda x: x["score"], reverse=True)
        
        return all_results[:top_k]
```

### 2. 复制策略
```yaml
replication:
  factor: 3
  strategy: synchronous
  consistency: eventual
  failover: automatic
```

### 3. 容量规划
| 集群规模 | 向量容量 | 查询QPS | 存储需求 |
|----------|----------|---------|----------|
| 10节点 | 10亿 | 10000 | 4TB |
| 50节点 | 50亿 | 50000 | 20TB |
| 100节点 | 100亿 | 100000 | 40TB |

## 版本
- 版本: V21.0.17
- 创建时间: 2026-04-08
- 状态: ✅ 已实施
