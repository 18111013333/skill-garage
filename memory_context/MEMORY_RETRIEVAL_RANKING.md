# MEMORY_RETRIEVAL_RANKING.md - 记忆检索排序

## 目的
定义记忆检索时的排序权重，确保高质量记忆优先返回。

## 适用范围
所有记忆检索结果的排序。

## 排序维度

| 维度 | 权重 | 说明 | 取值范围 |
|------|------|------|----------|
| 任务相关性 | 30% | 与当前任务的关联度 | 0-100 |
| 最近使用 | 20% | 最近访问时间 | 0-100 |
| 质量评分 | 20% | 记忆质量分数 | 0-100 |
| 项目作用域 | 15% | 项目相关程度 | 0-100 |
| 来源可信度 | 10% | 来源的可靠性 | 0-100 |
| 时效性 | 5% | 是否过期 | 0-100 |

## 排序计算

### 综合评分公式
```javascript
function calculateRetrievalScore(memory, context) {
  const weights = {
    taskRelevance: 0.30,
    recentUse: 0.20,
    qualityScore: 0.20,
    projectScope: 0.15,
    sourceCredibility: 0.10,
    timeliness: 0.05
  };
  
  const scores = {
    taskRelevance: calculateTaskRelevance(memory, context.currentTask),
    recentUse: calculateRecentUse(memory.lastAccessedAt),
    qualityScore: memory.qualityScore || 50,
    projectScope: calculateProjectScope(memory, context.projectId),
    sourceCredibility: getSourceCredibility(memory.source),
    timeliness: calculateTimeliness(memory)
  };
  
  let totalScore = 0;
  for (const [dimension, weight] of Object.entries(weights)) {
    totalScore += scores[dimension] * weight;
  }
  
  // 应用惩罚因子
  if (memory.isExpired) {
    totalScore *= 0.1;  // 过期记忆大幅降权
  }
  
  if (memory.hasConflict && !memory.conflictResolved) {
    totalScore *= 0.5;  // 未解决冲突降权
  }
  
  return {
    total: Math.round(totalScore),
    dimensions: scores,
    penalties: {
      expired: memory.isExpired,
      conflict: memory.hasConflict && !memory.conflictResolved
    }
  };
}
```

## 维度计算

### 1. 任务相关性
```javascript
function calculateTaskRelevance(memory, currentTask) {
  let score = 0;
  
  // 直接关联
  if (memory.taskId === currentTask.id) {
    score = 100;
  }
  // 项目关联
  else if (memory.projectId === currentTask.projectId) {
    score = 80;
  }
  // 类型匹配
  else if (memory.taskType === currentTask.type) {
    score = 60;
  }
  // 语义相似
  else {
    const similarity = calculateSemanticSimilarity(
      memory.content,
      currentTask.query
    );
    score = similarity * 50;
  }
  
  return score;
}
```

### 2. 最近使用
```javascript
function calculateRecentUse(lastAccessedAt) {
  const hoursSinceAccess = (Date.now() - lastAccessedAt) / (1000 * 60 * 60);
  
  if (hoursSinceAccess < 1) return 100;
  if (hoursSinceAccess < 24) return 90;
  if (hoursSinceAccess < 168) return 70;  // 1周
  if (hoursSinceAccess < 720) return 50;  // 1月
  if (hoursSinceAccess < 2160) return 30; // 3月
  return 10;
}
```

### 3. 项目作用域
```javascript
function calculateProjectScope(memory, currentProjectId) {
  if (!currentProjectId) return 50;  // 无项目上下文
  
  if (memory.projectScope === currentProjectId) {
    return 100;  // 当前项目
  }
  
  if (memory.projectScope === 'global') {
    return 70;  // 全局记忆
  }
  
  if (memory.projectScope && memory.projectScope !== currentProjectId) {
    return 20;  // 其他项目
  }
  
  return 50;  // 未指定
}
```

### 4. 来源可信度
```yaml
source_credibility_scores:
  user_direct_input: 100
  user_confirmed: 95
  system_verified: 85
  external_verified_source: 75
  system_inferred_high_conf: 60
  system_inferred_medium_conf: 40
  unverified: 20
  contradictory_source: 10
```

### 5. 时效性
```javascript
function calculateTimeliness(memory) {
  if (!memory.expiresAt) return 100;  // 无过期时间
  
  const now = Date.now();
  const expiresAt = new Date(memory.expiresAt).getTime();
  
  if (now > expiresAt) return 0;  // 已过期
  
  const hoursUntilExpiry = (expiresAt - now) / (1000 * 60 * 60);
  
  if (hoursUntilExpiry < 24) return 50;  // 即将过期
  if (hoursUntilExpiry < 168) return 80;  // 1周内过期
  
  return 100;  // 有效期充足
}
```

## 排序规则

### 基础排序
```yaml
basic_sorting:
  primary: "total_score desc"
  secondary: "created_at desc"
  tertiary: "access_count desc"
```

### 分组排序
```yaml
grouped_sorting:
  groups:
    - name: "high_quality"
      filter: "quality_score >= 80"
      sort: "task_relevance desc"
      
    - name: "medium_quality"
      filter: "60 <= quality_score < 80"
      sort: "total_score desc"
      
    - name: "low_quality"
      filter: "quality_score < 60"
      sort: "recent_use desc"
      
  group_order: ["high_quality", "medium_quality", "low_quality"]
```

## 过滤规则

### 硬过滤
```yaml
hard_filters:
  - condition: "is_expired == true"
    action: "exclude"
    unless: "explicitly_requested"
    
  - condition: "quality_score < 30"
    action: "exclude"
    
  - condition: "has_critical_conflict == true"
    action: "exclude"
    unless: "conflict_context"
```

### 软过滤
```yaml
soft_filters:
  - condition: "quality_score < 50"
    action: "deprioritize"
    penalty: 0.5
    
  - condition: "source == 'unverified'"
    action: "deprioritize"
    penalty: 0.7
    
  - condition: "age > 180d"
    action: "deprioritize"
    penalty: 0.8
```

## 结果限制

### 数量限制
```yaml
result_limits:
  default: 10
  max: 50
  min_quality_score: 40
  
  by_context:
    simple_query: 5
    complex_analysis: 20
    comprehensive_search: 50
```

### 多样性控制
```yaml
diversity:
  enabled: true
  max_same_source: 3
  max_same_project: 5
  max_same_type: 4
  
  deduplication:
    enabled: true
    threshold: 0.9  # 相似度阈值
```

## 特殊场景排序

### 项目上下文
```yaml
project_context:
  boost_project_memory: 1.5
  boost_recent_project: 1.2
  penalize_other_project: 0.5
```

### 决策支持
```yaml
decision_support:
  boost_decision_records: 1.3
  boost_verified_facts: 1.2
  penalize_inferred: 0.8
```

### 冲突场景
```yaml
conflict_scenario:
  show_conflicting: true
  group_conflicts: true
  highlight_conflict: true
  sort_by_confidence: true
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 首条命中率 | 首条结果被采用率 | <60% |
| 前三命中率 | 前三条结果被采用率 | <80% |
| 平均排序位置 | 被采用结果平均位置 | >3 |
| 过滤率 | 被过滤/总结果 | >50% |

## 维护方式
- 调整权重: 更新排序维度权重
- 新增规则: 创建排序规则
- 调整过滤: 更新过滤规则

## 引用文件
- `memory_quality/MEMORY_SCORING.md` - 记忆评分
- `graph/GRAPH_RETRIEVAL_POLICY.md` - 图谱检索策略
- `MEMORY.md` - 记忆系统总索引
