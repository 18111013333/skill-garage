# GRAPH_REASONING.md - 图谱推理规则

## 目的
定义基于图谱的推理规则，实现关系型推理。

## 适用范围
所有需要利用图结构进行推理的场景。

## 推理类型

| 类型 | 说明 | 示例 | 复杂度 |
|------|------|------|--------|
| 路径查找 | 查找实体间路径 | A到B的依赖链 | O(V+E) |
| 依赖链追踪 | 追踪依赖关系 | 任务的所有前置依赖 | O(V+E) |
| 冲突节点识别 | 识别矛盾实体 | 矛盾的需求 | O(V²) |
| 关键实体聚合 | 聚合关键节点 | 项目核心人员 | O(V) |
| 影响范围分析 | 分析变更影响 | 修改影响的任务 | O(V+E) |

## 推理规则

### 1. 路径查找
```yaml
path_finding:
  algorithms:
    - name: "BFS"
      use: "最短路径（无权重）"
      complexity: "O(V+E)"
      
    - name: "Dijkstra"
      use: "最短路径（有权重）"
      complexity: "O(E log V)"
      
    - name: "A*"
      use: "启发式最短路径"
      complexity: "O(E)"
      
  config:
    max_depth: 5
    max_paths: 10
    relation_filter: null  # 可选：只考虑特定关系类型
```

### 2. 依赖链追踪
```yaml
dependency_tracing:
  forward_tracing:
    description: "追踪某实体被谁依赖"
    query: "MATCH (n)<-[:depends_on*]-(m) WHERE n.id = $id RETURN m"
    use: "影响分析"
    
  backward_tracing:
    description: "追踪某实体依赖谁"
    query: "MATCH (n)-[:depends_on*]->(m) WHERE n.id = $id RETURN m"
    use: "前置条件分析"
    
  full_chain:
    description: "完整依赖链"
    query: "MATCH (n)-[:depends_on*]-(m) WHERE n.id = $id RETURN m"
    use: "完整依赖视图"
```

### 3. 冲突节点识别
```yaml
conflict_detection:
  patterns:
    - name: "直接冲突"
      pattern: "A conflicts_with B"
      detection: "relation_exists"
      
    - name: "传递冲突"
      pattern: "A conflicts_with B, B relates_to C => A may conflict C"
      detection: "path_analysis"
      confidence: 0.6
      
    - name: "属性冲突"
      pattern: "A and B have conflicting attributes"
      detection: "attribute_comparison"
      
  resolution:
    - identify_conflict_type
    - assess_severity
    - propose_resolution
```

### 4. 关键实体聚合
```yaml
key_entity_aggregation:
  metrics:
    - name: "度中心性"
      formula: "degree / (n-1)"
      use: "连接最多的实体"
      
    - name: "接近中心性"
      formula: "(n-1) / sum(distances)"
      use: "最接近其他实体的实体"
      
    - name: "介数中心性"
      formula: "shortest_paths_through / all_shortest_paths"
      use: "最关键的桥接实体"
      
  aggregation:
    - filter_by_entity_type
    - calculate_metrics
    - rank_and_select
```

### 5. 影响范围分析
```yaml
impact_analysis:
  scope_calculation:
    - name: "直接影响"
      depth: 1
      relations: ["depends_on", "relates_to"]
      
    - name: "间接影响"
      depth: 3
      relations: ["depends_on", "relates_to", "affects"]
      
    - name: "全链影响"
      depth: -1  # 无限制
      relations: ["all"]
      
  impact_assessment:
    - count_affected_entities
    - categorize_by_type
    - assess_criticality
    - estimate_propagation_time
```

## 推理流程

```
推理请求
    ↓
┌─────────────────────────────────────┐
│ 1. 解析推理需求                      │
│    - 识别推理类型                    │
│    - 提取参数                        │
│    - 确定约束条件                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 构建推理查询                      │
│    - 选择算法                        │
│    - 设置参数                        │
│    - 添加过滤条件                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 执行推理                          │
│    - 遍历图结构                      │
│    - 应用推理规则                    │
│    - 收集结果                        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 结果处理                          │
│    - 过滤无效结果                    │
│    - 计算置信度                      │
│    - 表达不确定性                    │
└─────────────────────────────────────┘
```

## 推理实现

### 路径查找实现
```javascript
function findPaths(startId, endId, options = {}) {
  const maxDepth = options.maxDepth || 5;
  const maxPaths = options.maxPaths || 10;
  const relationFilter = options.relationFilter;
  
  const paths = [];
  const visited = new Set();
  
  function dfs(current, path, depth) {
    if (depth > maxDepth) return;
    if (paths.length >= maxPaths) return;
    
    if (current === endId) {
      paths.push([...path]);
      return;
    }
    
    visited.add(current);
    
    const neighbors = getNeighbors(current, relationFilter);
    for (const neighbor of neighbors) {
      if (!visited.has(neighbor.id)) {
        path.push({
          from: current,
          to: neighbor.id,
          relation: neighbor.relation
        });
        dfs(neighbor.id, path, depth + 1);
        path.pop();
      }
    }
    
    visited.delete(current);
  }
  
  dfs(startId, [], 0);
  return paths;
}
```

### 影响分析实现
```javascript
function analyzeImpact(entityId, options = {}) {
  const depth = options.depth || 3;
  const relationTypes = options.relationTypes || ['depends_on', 'relates_to'];
  
  const affected = new Set();
  const queue = [{ id: entityId, level: 0 }];
  
  while (queue.length > 0) {
    const { id, level } = queue.shift();
    
    if (level > depth) continue;
    if (affected.has(id)) continue;
    
    affected.add(id);
    
    // 获取依赖此实体的其他实体
    const dependents = getDependents(id, relationTypes);
    for (const dependent of dependents) {
      queue.push({ id: dependent, level: level + 1 });
    }
  }
  
  return {
    affected_entities: Array.from(affected),
    count: affected.size,
    by_type: groupByType(affected),
    criticality: assessCriticality(affected)
  };
}
```

## 结果验证

### 验证规则
```yaml
validation_rules:
  - name: "路径有效性"
    check: "路径中所有关系存在且有效"
    
  - name: "置信度校验"
    check: "结果置信度 >= 阈值"
    threshold: 0.5
    
  - name: "逻辑一致性"
    check: "结果不违反已知约束"
    
  - name: "时效性检查"
    check: "使用的关系未过期"
```

### 不确定性表达
```yaml
uncertainty_expression:
  confidence_levels:
    - level: "high"
      range: "0.8-1.0"
      expression: "确定"
      
    - level: "medium"
      range: "0.6-0.8"
      expression: "很可能"
      
    - level: "low"
      range: "0.4-0.6"
      expression: "可能"
      
    - level: "very_low"
      range: "0.0-0.4"
      expression: "不确定"
      
  output_template: |
    推理结果：{result}
    置信度：{confidence} ({level})
    推理路径：{path}
    依据：{basis}
```

## 性能优化

### 索引优化
```yaml
indexing:
  - type: "entity_id_index"
    on: "entity_id"
    
  - type: "relation_type_index"
    on: "relation_type"
    
  - type: "composite_index"
    on: ["from_entity", "relation_type", "to_entity"]
```

### 缓存策略
```yaml
caching:
  - type: "path_cache"
    key: "start:end:relation_types"
    ttl: "5m"
    
  - type: "impact_cache"
    key: "entity_id:depth"
    ttl: "10m"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 推理延迟 | 推理耗时 | >2s |
| 推理准确率 | 正确/总推理 | <80% |
| 路径命中率 | 找到路径/请求 | <70% |
| 缓存命中率 | 缓存命中/请求 | <50% |

## 维护方式
- 新增推理类型: 创建推理规则
- 优化算法: 更新算法实现
- 调整参数: 更新配置参数

## 引用文件
- `graph/GRAPH_SCHEMA.json` - 图谱结构
- `graph/RELATION_INFERENCE.md` - 关系推断
- `graph/GRAPH_RETRIEVAL_POLICY.md` - 图谱检索
