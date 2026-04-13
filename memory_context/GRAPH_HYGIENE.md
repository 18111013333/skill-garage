# GRAPH_HYGIENE.md - 图谱清理与健康规则

## 目的
定义图谱清理与健康规则，确保图谱长期可维护。

## 适用范围
所有知识图谱的维护和清理。

## 清理类型

| 类型 | 说明 | 频率 | 影响 |
|------|------|------|------|
| 孤立节点清理 | 清理无连接节点 | 每周 | 低 |
| 低置信边衰减 | 降低低置信边权重 | 每日 | 中 |
| 冲突边标记 | 标记矛盾关系 | 实时 | 高 |
| 陈旧关系降权 | 降低过期关系权重 | 每日 | 中 |
| 重复实体合并 | 合并重复实体 | 每周 | 高 |

## 清理规则

### 1. 孤立节点清理
```yaml
orphan_node_cleanup:
  definition:
    - no_incoming_relations: true
    - no_outgoing_relations: true
    - age > 30d  # 存在超过30天
    
  exceptions:
    - newly_created: "age < 7d"
    - user_marked_important: true
    - project_core_entity: true
    
  actions:
    - mark_for_review
    - archive_after_confirmation
    - delete_after_grace_period: "14d"
    
  schedule: "weekly"
```

### 2. 低置信边衰减
```yaml
low_confidence_edge_decay:
  threshold: 0.5
  
  decay_formula: |
    new_confidence = confidence * decay_factor
    decay_factor = 0.95 ^ (days_since_last_access / 30)
    
  actions:
    - if confidence < 0.3:
        action: "mark_for_removal"
    - if confidence < 0.2:
        action: "remove_edge"
        
  refresh_triggers:
    - edge_used_successfully
    - user_confirmed_valid
    - new_evidence_supports
    
  schedule: "daily"
```

### 3. 冲突边标记
```yaml
conflict_edge_marking:
  detection:
    - direct_conflict:
        pattern: "A relates_to B AND A conflicts_with B"
        action: "mark_conflict"
        
    - transitive_conflict:
        pattern: "path contains conflict relation"
        action: "mark_potential_conflict"
        
    - attribute_conflict:
        pattern: "connected entities have conflicting attributes"
        action: "mark_attribute_conflict"
        
  marking:
    - add_conflict_flag: true
    - record_conflict_reason: true
    - notify_maintainer: true
    
  resolution:
    - await_user_input
    - auto_resolve_if_obvious
    - escalate_if_critical
```

### 4. 陈旧关系降权
```yaml
stale_relation_downgrade:
  staleness_criteria:
    - relation_age > 180d
    - no_access_in_days: 90
    - source_expired: true
    
  downgrade_formula: |
    weight = base_weight * staleness_factor
    staleness_factor = max(0.1, 1 - (days_stale / 365))
    
  actions:
    - reduce_weight
    - mark_as_stale
    - schedule_for_review
    
  revival_conditions:
    - accessed_again
    - source_refreshed
    - user_reconfirmed
```

### 5. 重复实体合并
```yaml
duplicate_entity_merge:
  detection:
    - exact_match:
        criteria: "same_entity_id OR same_canonical_name"
        confidence: 1.0
        
    - alias_match:
        criteria: "name_in_aliases"
        confidence: 0.95
        
    - fuzzy_match:
        criteria: "similarity > 0.9 AND same_type"
        confidence: 0.8
        
  merge_process:
    - select_primary_entity
    - merge_attributes
    - merge_relations
    - update_aliases
    - redirect_references
    - archive_duplicate
    
  review_required:
    - confidence < 0.9
    - high_impact_entity
    - user_owned_entity
    
  schedule: "weekly"
```

## 清理流程

```
清理触发
    ↓
┌─────────────────────────────────────┐
│ 1. 扫描检测                          │
│    - 识别清理候选                    │
│    - 评估清理风险                    │
│    - 分类清理类型                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 风险评估                          │
│    - 评估影响范围                    │
│    - 检查依赖关系                    │
│    - 确认无副作用                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 执行清理                          │
│    - 低风险：自动执行                │
│    - 中风险：记录后执行              │
│    - 高风险：需确认后执行            │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 验证确认                          │
│    - 验证清理结果                    │
│    - 检查图谱完整性                  │
│    - 更新统计信息                    │
└─────────────────────────────────────┘
```

## 健康指标

### 图谱健康度
```yaml
health_metrics:
  connectivity:
    - average_degree: "平均连接度"
      target: "> 2"
    - isolated_ratio: "孤立节点比例"
      target: "< 5%"
      
  quality:
    - average_confidence: "平均置信度"
      target: "> 0.7"
    - conflict_ratio: "冲突关系比例"
      target: "< 2%"
    
  freshness:
    - stale_ratio: "陈旧关系比例"
      target: "< 10%"
    - avg_age: "平均关系年龄"
      target: "< 90d"
    
  consistency:
    - duplicate_ratio: "重复实体比例"
      target: "< 1%"
    - orphan_ratio: "孤立节点比例"
      target: "< 5%"
```

### 健康评分
```javascript
function calculateGraphHealth(metrics) {
  const weights = {
    connectivity: 0.25,
    quality: 0.30,
    freshness: 0.25,
    consistency: 0.20
  };
  
  const scores = {
    connectivity: scoreConnectivity(metrics),
    quality: scoreQuality(metrics),
    freshness: scoreFreshness(metrics),
    consistency: scoreConsistency(metrics)
  };
  
  let total = 0;
  for (const [key, weight] of Object.entries(weights)) {
    total += scores[key] * weight;
  }
  
  return {
    total: Math.round(total),
    dimensions: scores,
    grade: getHealthGrade(total)
  };
}
```

## 清理配置

### 自动清理配置
```yaml
auto_cleanup:
  enabled: true
  
  low_risk:
    - orphan_nodes_age > 60d
    - confidence < 0.1
    - auto_approve: true
    
  medium_risk:
    - stale_relations
    - low_confidence_edges
    - auto_approve: false
    - log_and_execute: true
    
  high_risk:
    - duplicate_merge
    - conflict_resolution
    - require_approval: true
```

### 清理限制
```yaml
cleanup_limits:
  max_entities_per_run: 1000
  max_relations_per_run: 5000
  
  rate_limit:
    entities_per_hour: 100
    relations_per_hour: 500
    
  protected:
    - user_marked_important
    - project_core_entities
    - recently_accessed: "7d"
```

## 清理日志

### 日志内容
```yaml
cleanup_log:
  fields:
    - cleanup_id
    - cleanup_type
    - affected_entities
    - affected_relations
    - reason
    - risk_level
    - executed_at
    - executed_by
    - verification_result
    
  retention: "90d"
```

## 监控告警

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 图谱健康度 | 综合健康评分 | <70 |
| 孤立节点比例 | 孤立/总节点 | >10% |
| 冲突比例 | 冲突/总关系 | >5% |
| 清理失败率 | 失败/总清理 | >5% |

## 维护方式
- 新增清理类型: 创建清理规则
- 调整阈值: 更新健康指标阈值
- 优化流程: 更新清理流程

## 引用文件
- `graph/GRAPH_SCHEMA.json` - 图谱结构
- `graph/ENTITY_RESOLUTION.md` - 实体消歧
- `graph/RELATION_INFERENCE.md` - 关系推断
