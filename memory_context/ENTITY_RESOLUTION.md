# ENTITY_RESOLUTION.md - 实体消歧规则

## 目的
定义实体消歧规则，确保图谱中同一实体正确归并。

## 适用范围
所有知识图谱中的实体识别和归并。

## 消歧场景

| 场景 | 说明 | 示例 |
|------|------|------|
| 用户昵称 | 用户使用不同称呼 | "张三"/"老张"/"Zhang" |
| 项目简称 | 项目使用缩写 | "OpenClaw项目"/"OC项目" |
| 文档别名 | 文档有多个名称 | "需求文档"/"PRD"/"产品需求" |
| 任务短称 | 任务使用简称 | "用户登录功能"/"登录功能" |
| 模糊实体 | 描述性提及 | "那个数据库"/"上次的项目" |

## 消歧策略

### 1. 精确匹配
```yaml
exact_match:
  conditions:
    - entity_id_match
    - canonical_name_match
  confidence: 1.0
  action: direct_merge
```

### 2. 别名匹配
```yaml
alias_match:
  conditions:
    - name_in_aliases_list
    - alias_verified
  confidence: 0.95
  action: merge_with_verification
```

### 3. 模糊匹配
```yaml
fuzzy_match:
  conditions:
    - similarity_score > 0.8
    - same_entity_type
    - same_project_scope
  confidence: 0.7
  action: propose_merge
```

### 4. 上下文推断
```yaml
context_inference:
  conditions:
    - context_clues_match
    - temporal_proximity
    - relationship_consistency
  confidence: 0.6
  action: tentative_merge
```

## 消歧流程

```
新实体输入
    ↓
┌─────────────────────────────────────┐
│ 1. 候选实体检索                      │
│    - 精确ID匹配                      │
│    - 名称匹配                        │
│    - 别名匹配                        │
│    - 模糊匹配                        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 相似度计算                        │
│    - 名称相似度                      │
│    - 属性相似度                      │
│    - 关系相似度                      │
│    - 上下文相似度                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 消歧决策                          │
│    - 高置信度 → 自动合并             │
│    - 中置信度 → 提示确认             │
│    - 低置信度 → 创建新实体           │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 执行合并或创建                    │
│    - 合并到现有实体                  │
│    - 创建新实体                      │
│    - 建立关联关系                    │
└─────────────────────────────────────┘
```

## 相似度计算

### 名称相似度
```javascript
function calculateNameSimilarity(name1, name2) {
  // 1. 编辑距离
  const editDistance = levenshteinDistance(name1, name2);
  const editSimilarity = 1 - editDistance / Math.max(name1.length, name2.length);
  
  // 2. Jaccard相似度（字符级）
  const jaccardSimilarity = jaccard(
    new Set(name1.split('')),
    new Set(name2.split(''))
  );
  
  // 3. 拼音相似度（中文）
  const pinyinSimilarity = comparePinyin(name1, name2);
  
  // 4. 缩写匹配
  const abbreviationMatch = checkAbbreviation(name1, name2);
  
  // 综合评分
  return {
    edit: editSimilarity,
    jaccard: jaccardSimilarity,
    pinyin: pinyinSimilarity,
    abbreviation: abbreviationMatch,
    overall: weightedAverage([editSimilarity, jaccardSimilarity, pinyinSimilarity])
  };
}
```

### 属性相似度
```javascript
function calculateAttributeSimilarity(entity1, entity2) {
  const commonAttrs = getCommonAttributes(entity1, entity2);
  let matchCount = 0;
  let totalCount = commonAttrs.length;
  
  for (const attr of commonAttrs) {
    if (entity1.attributes[attr] === entity2.attributes[attr]) {
      matchCount++;
    }
  }
  
  return matchCount / totalCount;
}
```

### 关系相似度
```javascript
function calculateRelationSimilarity(entity1, entity2) {
  const relations1 = getRelations(entity1.entity_id);
  const relations2 = getRelations(entity2.entity_id);
  
  // 共同邻居
  const commonNeighbors = intersection(
    getNeighborIds(relations1),
    getNeighborIds(relations2)
  );
  
  // 关系类型匹配
  const commonRelationTypes = intersection(
    getRelationTypes(relations1),
    getRelationTypes(relations2)
  );
  
  return {
    neighborSimilarity: commonNeighbors.length / Math.min(neighbors1.length, neighbors2.length),
    relationTypeSimilarity: commonRelationTypes.length / Math.min(types1.length, types2.length)
  };
}
```

## 置信度阈值

| 操作 | 置信度阈值 | 说明 |
|------|------------|------|
| 自动合并 | ≥ 0.95 | 无需确认直接合并 |
| 提示确认 | 0.7 - 0.95 | 需要用户或系统确认 |
| 创建关联 | 0.5 - 0.7 | 创建"可能相同"关系 |
| 创建新实体 | < 0.5 | 作为新实体处理 |

## 合并策略

### 合并规则
```yaml
merge_rules:
  primary_entity_selection:
    - prefer_earlier_created
    - prefer_higher_confidence
    - prefer_more_relations
    - prefer_canonical_name
    
  attribute_merge:
    strategy: "keep_all_with_source"
    conflict_resolution: "prefer_higher_confidence"
    
  relation_merge:
    strategy: "union_all"
    duplicate_handling: "keep_one_with_max_confidence"
    
  alias_management:
    action: "add_to_aliases"
    track_source: true
```

### 合并示例
```yaml
merge_example:
  entity1:
    entity_id: "user_zhang_san"
    name: "张三"
    aliases: ["老张"]
    attributes:
      department: "技术部"
    confidence: 0.9
    
  entity2:
    entity_id: "user_zhangsan"
    name: "Zhang San"
    aliases: []
    attributes:
      email: "zhangsan@example.com"
    confidence: 0.8
    
  merged_result:
    entity_id: "user_zhang_san"  # 保留较早的
    name: "张三"  # 保留canonical
    aliases: ["老张", "Zhang San", "zhangsan"]
    attributes:
      department: "技术部"
      email: "zhangsan@example.com"
    confidence: 0.95  # 合并后提升
    merge_history:
      - from: "user_zhangsan"
        at: "2024-01-15T10:00:00Z"
        confidence: 0.85
```

## 模糊实体处理

### 指代消解
```yaml
reference_resolution:
  patterns:
    - pattern: "那个{entity_type}"
      resolution: "most_recent_mentioned"
    - pattern: "上次{action}的{entity_type}"
      resolution: "by_action_history"
    - pattern: "{user}的{entity_type}"
      resolution: "by_user_relation"
      
  context_window: "current_session"
  fallback: "request_clarification"
```

### 消歧提示
```yaml
clarification_request:
  trigger: "confidence < 0.7"
  template: |
    您提到的"${mention}"可能指：
    1. ${candidate1.name} (${candidate1.description})
    2. ${candidate2.name} (${candidate2.description})
    3. 新的${entity_type}
    
    请确认是哪一个？
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 自动合并准确率 | 正确/总自动合并 | <95% |
| 误合并率 | 错误合并/总合并 | >2% |
| 消歧延迟 | 消歧处理耗时 | >500ms |
| 待确认数量 | 等待确认的消歧 | >100 |

## 维护方式
- 调整阈值: 更新置信度阈值配置
- 新增策略: 创建消歧策略
- 优化算法: 更新相似度计算

## 引用文件
- `graph/GRAPH_SCHEMA.json` - 图谱结构
- `graph/GRAPH_HYGIENE.md` - 图谱清理
- `memory_quality/MEMORY_MERGE_RULES.md` - 记忆合并
