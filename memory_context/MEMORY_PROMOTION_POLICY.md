# MEMORY_PROMOTION_POLICY.md - 记忆晋升策略

## 目的
定义记忆升降级规则，控制记忆从会话级晋升到长期记忆的门槛。

## 适用范围
所有记忆条目的层级管理。

## 记忆层级

| 层级 | 存储 | 生命周期 | 容量 | 晋升来源 |
|------|------|----------|------|----------|
| L1 会话记忆 | session-summaries | 单次会话 | 100条 | 用户输入 |
| L2 场景记忆 | scenarios/ | 跨会话 | 500条 | L1晋升 |
| L3 长期记忆 | MEMORY.md + memory/ | 永久 | 2000条 | L2晋升 |

## 晋升条件

### L1 → L2 晋升
```yaml
promotion_l1_to_l2:
  required_conditions:
    - access_count: ">= 3"  # 被访问3次以上
    - quality_score: ">= 60"  # 质量分60以上
    - session_span: "> 1"  # 跨越多个会话
    
  bonus_conditions:
    - user_explicit_save: true  # 用户明确保存
    - project_related: true  # 项目相关
    - decision_record: true  # 决策记录
    
  blocking_conditions:
    - conflict_with_higher_memory: true
    - quality_score: "< 40"
    - temporary_constraint: true  # 临时约束
    
  formula: |
    promotion_score = 
      quality_score * 0.4 +
      access_count * 5 * 0.2 +
      session_span * 10 * 0.2 +
      bonus_points * 0.2
    
    promote if promotion_score >= 50
```

### L2 → L3 晋升
```yaml
promotion_l2_to_l3:
  required_conditions:
    - quality_score: ">= 80"  # 高质量
    - access_count: ">= 10"  # 高频使用
    - age: ">= 7d"  # 存在7天以上
    - no_unresolved_conflict: true
    
  bonus_conditions:
    - core_project_memory: true  # 项目核心记忆
    - user_preference: true  # 用户偏好
    - verified_fact: true  # 已验证事实
    
  blocking_conditions:
    - quality_score: "< 60"
    - high_conflict_risk: true
    - temporary_context: true
    
  formula: |
    promotion_score = 
      quality_score * 0.35 +
      access_count * 2 * 0.25 +
      age_factor * 0.15 +
      bonus_points * 0.25
    
    promote if promotion_score >= 70
    
  approval:
    auto_approve: "score >= 85"
    manual_review: "70 <= score < 85"
```

## 降级条件

### L3 → L2 降级
```yaml
demotion_l3_to_l2:
  conditions:
    - quality_score: "< 50"
    - conflict_detected: true
    - not_accessed_for: "90d"
    - user_marked_obsolete: true
    
  actions:
    - move_to_l2_storage
    - mark_as_demoted
    - record_demotion_reason
```

### L2 → L1 降级
```yaml
demotion_l2_to_l1:
  conditions:
    - quality_score: "< 40"
    - not_accessed_for: "30d"
    - project_completed: true
    - user_marked_obsolete: true
    
  actions:
    - move_to_l1_storage
    - set_expiry_timer
```

### L1 → 清理
```yaml
cleanup_l1:
  conditions:
    - session_ended: true
    - not_promoted: true
    - quality_score: "< 30"
    
  actions:
    - archive_or_delete
    - update_statistics
```

## 晋升流程

```
记忆条目
    ↓
┌─────────────────────────────────────┐
│ 1. 评估晋升条件                      │
│    - 计算质量分数                    │
│    - 检查访问统计                    │
│    - 评估冲突情况                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 计算晋升分数                      │
│    - 应用晋升公式                    │
│    - 加上奖励分                      │
│    - 减去惩罚分                      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 晋升决策                          │
│    - 分数达标 → 晋升                 │
│    - 需要审批 → 提交审批             │
│    - 分数不足 → 保持当前层级         │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 执行晋升                          │
│    - 复制到目标层级存储              │
│    - 更新索引                        │
│    - 记录晋升历史                    │
└─────────────────────────────────────┘
```

## 冲突处理

### 晋升时冲突检测
```yaml
conflict_detection:
  on_promotion:
    - check_existing_memory:
        scope: "target_level"
        match: "semantic_similarity > 0.9"
    - check_contradiction:
        scope: "target_level"
        match: "content_contradicts"
        
  conflict_resolution:
    - if_same_content:
        action: "merge_with_existing"
    - if_contradicts:
        action: "block_promotion"
        notify: "conflict_detected"
    - if_supersedes:
        action: "archive_old_promote_new"
```

## 晋升限制

### 配额限制
```yaml
quotas:
  l2_max_entries: 500
  l3_max_entries: 2000
  
  promotion_rate_limit:
    l1_to_l2: "50/day"
    l2_to_l3: "20/day"
    
  storage_limit:
    l2_max_size: "10MB"
    l3_max_size: "50MB"
```

### 优先级队列
```yaml
priority_queue:
  high_priority:
    - user_explicit_save
    - project_core_memory
    - decision_records
    
  medium_priority:
    - frequently_accessed
    - high_quality_score
    
  low_priority:
    - general_context
    - temporary_preferences
```

## 晋升审计

### 审计记录
```yaml
audit_log:
  events:
    - promotion_requested
    - promotion_approved
    - promotion_rejected
    - demotion_triggered
    
  fields:
    - memory_id
    - from_level
    - to_level
    - promotion_score
    - decision_reason
    - timestamp
    - reviewer (if manual)
```

### 定期审查
```yaml
periodic_review:
  frequency: "weekly"
  scope:
    - recently_promoted
    - high_conflict_memories
    - low_access_long_term
    
  actions:
    - verify_promotion_validity
    - identify_demotion_candidates
    - update_quality_scores
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 晋升成功率 | 成功/申请 | <80% |
| 平均晋升分数 | 晋升记忆平均分 | <70 |
| 降级率 | 降级/总长期记忆 | >5% |
| 冲突阻断率 | 冲突阻断/申请 | >10% |

## 维护方式
- 调整条件: 更新晋升/降级条件
- 调整公式: 更新晋升公式
- 调整配额: 更新配额限制

## 引用文件
- `memory_quality/MEMORY_SCORING.md` - 记忆评分
- `memory_quality/MEMORY_DECAY_RULES.md` - 记忆衰减
- `MEMORY.md` - 记忆系统总索引
