# MEMORY_SCORING.md - 记忆质量评分

## 目的
定义记忆质量评分维度和计算方法，为每条记忆建立质量等级。

## 适用范围
所有记忆条目的质量评估。

## 评分维度

### 维度定义

| 维度 | 权重 | 说明 | 评分范围 |
|------|------|------|----------|
| 真实性 | 25% | 信息来源可靠程度 | 0-100 |
| 时效性 | 20% | 信息是否过时 | 0-100 |
| 来源强度 | 15% | 来源的可信度 | 0-100 |
| 冲突程度 | 15% | 与其他记忆的冲突情况 | 0-100（反向） |
| 复用价值 | 15% | 被引用和使用的价值 | 0-100 |
| 项目相关性 | 10% | 与当前项目的关联度 | 0-100 |

### 维度详解

#### 1. 真实性（Authenticity）
```yaml
scoring:
  user_direct_input: 100
  user_confirmed: 90
  system_verified: 80
  external_source: 70
  system_inferred: 50
  unverified: 30
  contradictory: 10
```

#### 2. 时效性（Timeliness）
```yaml
scoring:
  fresh_24h: 100
  fresh_7d: 90
  fresh_30d: 70
  fresh_90d: 50
  fresh_180d: 30
  stale: 10
  
decay_formula: "max(0, 100 - days_since_update * 0.5)"
```

#### 3. 来源强度（Source Strength）
```yaml
scoring:
  primary_source: 100      # 用户直接提供
  secondary_source: 80     # 系统从行为推断
  tertiary_source: 60      # 外部数据
  inferred_source: 40      # 推理得出
  unknown_source: 20       # 来源不明
```

#### 4. 冲突程度（Conflict Level）
```yaml
scoring:
  no_conflict: 100
  minor_conflict: 80       # 存在轻微不一致
  moderate_conflict: 60    # 存在明显不一致
  major_conflict: 30       # 存在严重冲突
  critical_conflict: 0     # 完全矛盾

# 注意：冲突程度是反向评分，冲突越高分数越低
```

#### 5. 复用价值（Reuse Value）
```yaml
scoring:
  high_frequency_use: 100  # 高频使用
  medium_frequency: 80     # 中频使用
  low_frequency: 60        # 低频使用
  rarely_used: 40          # 很少使用
  never_used: 20           # 从未使用

factors:
  - access_count
  - last_access_recency
  - query_match_rate
```

#### 6. 项目相关性（Project Relevance）
```yaml
scoring:
  core_project_memory: 100  # 项目核心记忆
  related_project: 80       # 相关项目
  general_context: 60       # 通用上下文
  user_preference: 50       # 用户偏好
  unrelated: 20             # 无关
```

## 综合评分计算

### 计算公式
```javascript
function calculateMemoryScore(memory) {
  const weights = {
    authenticity: 0.25,
    timeliness: 0.20,
    sourceStrength: 0.15,
    conflictLevel: 0.15,  // 反向
    reuseValue: 0.15,
    projectRelevance: 0.10
  };
  
  const scores = {
    authenticity: scoreAuthenticity(memory),
    timeliness: scoreTimeliness(memory),
    sourceStrength: scoreSourceStrength(memory),
    conflictLevel: 100 - scoreConflict(memory),  // 反向
    reuseValue: scoreReuseValue(memory),
    projectRelevance: scoreProjectRelevance(memory)
  };
  
  let totalScore = 0;
  for (const [dimension, weight] of Object.entries(weights)) {
    totalScore += scores[dimension] * weight;
  }
  
  return {
    total: Math.round(totalScore),
    dimensions: scores,
    grade: getGrade(totalScore)
  };
}
```

### 质量等级

| 等级 | 分数范围 | 说明 | 处理策略 |
|------|----------|------|----------|
| A+ | 90-100 | 极高质量 | 优先使用，长期保留 |
| A | 80-89 | 高质量 | 正常使用，长期保留 |
| B | 70-79 | 中高质量 | 正常使用，定期验证 |
| C | 60-69 | 中等质量 | 谨慎使用，需要验证 |
| D | 50-59 | 低质量 | 限制使用，标记待验证 |
| F | 0-49 | 极低质量 | 不使用，标记清理 |

## 评分更新

### 触发条件
```yaml
update_triggers:
  - memory_created
  - memory_accessed
  - memory_conflict_detected
  - memory_verified
  - memory_updated
  - periodic_review
```

### 更新频率
```yaml
update_frequency:
  new_memory: immediate
  accessed_memory: on_access
  periodic_review: weekly
  conflict_check: on_conflict
```

## 评分存储

### 存储结构
```yaml
storage:
  path: memory/scores/
  format: jsonl
  fields:
    - memory_id
    - total_score
    - grade
    - dimension_scores
    - last_scored_at
    - scoring_version
```

## 评分应用

### 应用场景
| 场景 | 使用方式 |
|------|----------|
| 检索排序 | 高分记忆优先返回 |
| 晋升决策 | 高分记忆可晋升长期记忆 |
| 清理决策 | 低分记忆优先清理 |
| 冲突解决 | 高分记忆优先采用 |
| 展示优先级 | 高分记忆优先展示 |

### 评分阈值
```yaml
thresholds:
  for_retrieval: 60        # 检索最低分数
  for_promotion: 80        # 晋升最低分数
  for_cleanup: 40          # 清理最高分数
  for_conflict_resolution: 70  # 冲突解决最低分数
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 平均分数 | 所有记忆平均分 | <60 |
| A级比例 | A级记忆占比 | <30% |
| F级比例 | F级记忆占比 | >20% |
| 评分更新延迟 | 评分更新耗时 | >1小时 |

## 维护方式
- 调整权重: 更新权重配置
- 新增维度: 更新维度定义
- 调整阈值: 更新阈值配置

## 引用文件
- `memory_quality/MEMORY_PROMOTION_POLICY.md` - 晋升策略
- `memory_quality/MEMORY_RETRIEVAL_RANKING.md` - 检索排序
- `MEMORY.md` - 记忆系统总索引
