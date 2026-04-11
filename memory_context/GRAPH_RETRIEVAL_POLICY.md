# GRAPH_RETRIEVAL_POLICY.md - 图谱检索策略

## 目的
定义何时优先走图谱检索，何时走向量检索，何时混合检索。

## 适用范围
所有知识检索场景。

## 检索方式对比

| 方式 | 优势 | 劣势 | 适用场景 |
|------|------|------|----------|
| 图谱检索 | 关系准确、可追溯、结构化 | 覆盖有限、需要结构化数据 | 关系查询、依赖链 |
| 向量检索 | 语义理解、覆盖广、模糊匹配 | 无结构、可能幻觉 | 文本匹配、语义搜索 |
| 混合检索 | 兼顾两者优点 | 复杂度高、需要融合 | 综合查询 |

## 检索场景分类

### 优先图谱检索
```yaml
graph_priority_scenarios:
  - name: "依赖链查询"
    patterns:
      - "X依赖什么"
      - "谁依赖X"
      - "X的前置条件"
    example: "这个任务依赖哪些其他任务？"
    
  - name: "项目关系查询"
    patterns:
      - "X项目相关的人"
      - "X参与的项目"
      - "项目间的关联"
    example: "张三参与了哪些项目？"
    
  - name: "用户偏好关联"
    patterns:
      - "X喜欢什么"
      - "X的偏好"
      - "类似用户的偏好"
    example: "这个用户有什么偏好？"
    
  - name: "历史决策链"
    patterns:
      - "为什么做X"
      - "X的决策依据"
      - "决策历史"
    example: "为什么选择这个方案？"
    
  - name: "实体间关系查询"
    patterns:
      - "X和Y的关系"
      - "X关联的实体"
      - "通过关系查找"
    example: "这个文档和哪些任务相关？"
```

### 优先向量检索
```yaml
vector_priority_scenarios:
  - name: "文本内容匹配"
    patterns:
      - "关于X的内容"
      - "提到X的文档"
      - "X相关的文本"
    example: "有哪些关于性能优化的文档？"
    
  - name: "语义相似查询"
    patterns:
      - "类似X的内容"
      - "X风格的"
      - "语义相近"
    example: "有没有类似这个方案的文档？"
    
  - name: "模糊描述查询"
    patterns:
      - "大概是X的东西"
      - "好像叫X"
      - "模糊描述"
    example: "那个关于缓存的配置在哪？"
    
  - name: "知识问答"
    patterns:
      - "什么是X"
      - "X是什么意思"
      - "X的定义"
    example: "什么是熔断器？"
```

### 混合检索
```yaml
hybrid_scenarios:
  - name: "综合信息查询"
    patterns:
      - "X的所有相关信息"
      - "X的完整上下文"
    strategy:
      - graph: "获取关系网络"
      - vector: "获取相关内容"
      - merge: "按相关性排序"
      
  - name: "上下文增强查询"
    patterns:
      - "在X上下文中查找Y"
      - "结合X关系查Y内容"
    strategy:
      - graph: "获取X的关系上下文"
      - vector: "在上下文中检索Y"
      
  - name: "验证性查询"
    patterns:
      - "确认X是否Y"
      - "验证X的关系"
    strategy:
      - graph: "检查结构化关系"
      - vector: "检查文本证据"
      - merge: "交叉验证"
```

## 检索决策

### 决策流程
```
查询输入
    ↓
┌─────────────────────────────────────┐
│ 1. 查询分析                          │
│    - 识别查询类型                    │
│    - 提取实体和关系                  │
│    - 判断查询意图                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 检索方式选择                      │
│    - 匹配场景模式                    │
│    - 评估图谱覆盖率                  │
│    - 考虑查询复杂度                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 执行检索                          │
│    - 单一方式 或 混合方式            │
│    - 应用检索参数                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 结果融合                          │
│    - 多源结果合并                    │
│    - 去重和排序                      │
│    - 置信度计算                      │
└─────────────────────────────────────┘
```

### 决策规则
```yaml
decision_rules:
  - rule: "graph_first"
    conditions:
      - query_type: "relation_query"
      - graph_coverage: "> 50%"
    action: "graph_retrieval"
    
  - rule: "vector_first"
    conditions:
      - query_type: "content_query"
      - or:
          - graph_coverage: "< 30%"
          - entity_not_in_graph
    action: "vector_retrieval"
    
  - rule: "hybrid"
    conditions:
      - query_type: "complex_query"
      - or:
          - both_sources_available
          - verification_needed
    action: "hybrid_retrieval"
```

## 图谱检索实现

### 查询构建
```javascript
function buildGraphQuery(parsedQuery) {
  const { entities, relations, intent } = parsedQuery;
  
  // 构建图查询
  let query = {
    start_nodes: entities.map(e => e.id),
    relation_types: relations.map(r => r.type),
    direction: intent.direction || 'both',
    max_depth: intent.depth || 3,
    filters: buildFilters(intent.conditions)
  };
  
  return query;
}
```

### 路径查询
```yaml
path_query:
  types:
    - name: "shortest_path"
      use: "查找最短关系路径"
      algorithm: "bfs"
      
    - name: "all_paths"
      use: "查找所有路径"
      algorithm: "dfs"
      max_paths: 10
      
    - name: "subgraph"
      use: "提取子图"
      params:
        center: "entity_id"
        radius: 2
```

## 向量检索实现

### 查询构建
```javascript
function buildVectorQuery(parsedQuery) {
  const queryText = constructQueryText(parsedQuery);
  const queryVector = await embed(queryText);
  
  return {
    vector: queryVector,
    top_k: 10,
    filters: buildFilters(parsedQuery.filters),
    min_score: 0.7
  };
}
```

## 混合检索融合

### 融合策略
```yaml
fusion_strategies:
  - name: "weighted_merge"
    weights:
      graph: 0.6
      vector: 0.4
    use: "默认融合"
    
  - name: "graph_enhanced"
    primary: "vector"
    enhancement: "graph_context"
    use: "向量为主，图谱补充上下文"
    
  - name: "vector_validated"
    primary: "graph"
    validation: "vector_evidence"
    use: "图谱为主，向量验证"
    
  - name: "intersection"
    use: "取交集，高置信"
    
  - name: "union"
    use: "取并集，高召回"
```

### 结果排序
```javascript
function rankResults(graphResults, vectorResults, strategy) {
  let merged = [];
  
  for (const result of [...graphResults, ...vectorResults]) {
    const existing = merged.find(r => r.id === result.id);
    
    if (existing) {
      // 合并分数
      existing.score = combineScores(existing, result, strategy);
      existing.sources.push(result.source);
    } else {
      merged.push({
        ...result,
        sources: [result.source]
      });
    }
  }
  
  // 按综合分数排序
  merged.sort((a, b) => b.score - a.score);
  
  return merged;
}
```

## 检索优化

### 缓存策略
```yaml
caching:
  graph_queries:
    enabled: true
    ttl: "5m"
    key: "query_hash"
    
  vector_queries:
    enabled: true
    ttl: "10m"
    key: "query_vector_hash"
    
  results:
    enabled: true
    ttl: "1m"
    key: "full_query_hash"
```

### 性能优化
```yaml
optimization:
  graph:
    - use_index
    - limit_depth
    - batch_queries
    
  vector:
    - precompute_embeddings
    - use_approximate_search
    - partition_index
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 图谱命中率 | 图谱检索成功/总图谱检索 | <80% |
| 向量命中率 | 向量检索成功/总向量检索 | <70% |
| 混合检索延迟 | 混合检索耗时 | >2s |
| 结果相关性 | 用户反馈相关性 | <80% |

## 维护方式
- 新增场景: 更新场景分类
- 调整策略: 更新融合策略
- 优化规则: 更新决策规则

## 引用文件
- `graph/GRAPH_SCHEMA.json` - 图谱结构
- `graph/GRAPH_REASONING.md` - 图谱推理
- `memory_quality/MEMORY_RETRIEVAL_RANKING.md` - 记忆检索排序
