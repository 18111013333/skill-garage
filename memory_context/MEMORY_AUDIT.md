# MEMORY_AUDIT.md - 记忆审计流程

## 目的
定义记忆审计流程，确保记忆系统有质量检查。

## 适用范围
所有记忆条目的定期审计。

## 审计类型

| 类型 | 频率 | 对象 | 目的 |
|------|------|------|------|
| 随机抽查 | 每日 | 随机样本 | 常规质量检查 |
| 高频命中审计 | 每周 | 高频使用记忆 | 确保核心记忆质量 |
| 低置信审计 | 每周 | 低置信高影响记忆 | 风险控制 |
| 冲突审计 | 实时 | 冲突记忆 | 冲突解决 |
| 项目核心审计 | 每月 | 项目核心记忆 | 项目质量保障 |

## 审计流程

### 标准审计流程
```
审计触发
    ↓
┌─────────────────────────────────────┐
│ 1. 样本选择                          │
│    - 按审计类型选择样本              │
│    - 确定审计范围                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 质量检查                          │
│    - 验证内容准确性                  │
│    - 检查来源可靠性                  │
│    - 评估时效性                      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 问题识别                          │
│    - 识别质量问题                    │
│    - 分类问题严重程度                │
│    - 记录审计发现                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 处理决策                          │
│    - 自动修复                        │
│    - 标记待处理                      │
│    - 触发升级                        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 5. 结果记录                          │
│    - 记录审计结果                    │
│    - 更新质量分数                    │
│    - 反馈到治理系统                  │
└─────────────────────────────────────┘
```

## 审计规则

### 1. 随机抽查
```yaml
random_audit:
  sample_size: 100
  selection:
    method: "stratified_random"
    strata:
      - by_type
      - by_age
      - by_quality_score
      
  checks:
    - name: "内容完整性"
      check: "content_not_empty"
      pass_criteria: true
      
    - name: "来源可追溯"
      check: "source_documented"
      pass_criteria: true
      
    - name: "格式正确"
      check: "schema_valid"
      pass_criteria: true
      
    - name: "时效有效"
      check: "not_expired"
      pass_criteria: true
```

### 2. 高频命中审计
```yaml
high_frequency_audit:
  selection:
    criteria: "access_count > 50"
    sample_size: 50
    
  checks:
    - name: "准确性验证"
      check: "verify_against_source"
      pass_criteria: "accuracy > 0.9"
      
    - name: "一致性检查"
      check: "no_internal_conflict"
      pass_criteria: true
      
    - name: "时效性检查"
      check: "update_within_90d"
      pass_criteria: true
      
  actions_on_failure:
    - mark_for_review
    - reduce_quality_score
    - notify_maintainer
```

### 3. 低置信高影响审计
```yaml
low_confidence_high_impact_audit:
  selection:
    criteria:
      - confidence: "< 0.6"
      - impact: "high"  # 被引用次数多
      
  checks:
    - name: "来源验证"
      check: "source_reliable"
      
    - name: "冲突检查"
      check: "no_conflict_with_verified"
      
    - name: "必要性评估"
      check: "is_still_needed"
      
  actions:
    - if_source_unreliable: "mark_for_removal"
    - if_conflict: "initiate_conflict_resolution"
    - if_not_needed: "mark_for_archive"
```

### 4. 冲突审计
```yaml
conflict_audit:
  trigger: "conflict_detected"
  
  process:
    - identify_conflicting_memories
    - analyze_conflict_type
    - assess_severity
    - propose_resolution
    
  resolution_options:
    - keep_newer
    - keep_higher_confidence
    - keep_user_confirmed
    - request_user_input
    - mark_both_uncertain
```

### 5. 项目核心审计
```yaml
project_core_audit:
  selection:
    criteria: "project_core_memory == true"
    
  checks:
    - name: "项目状态一致"
      check: "project_status_consistent"
      
    - name: "决策记录完整"
      check: "decision_fully_documented"
      
    - name: "依赖关系正确"
      check: "dependencies_accurate"
      
  frequency: "monthly"
  report_to: "project_owner"
```

## 审计检查项

### 内容检查
```yaml
content_checks:
  - id: "C001"
    name: "内容非空"
    check: "content != null && content != ''"
    severity: "critical"
    
  - id: "C002"
    name: "内容有意义"
    check: "content_length > 10"
    severity: "warning"
    
  - id: "C003"
    name: "无敏感信息"
    check: "no_sensitive_data_exposure"
    severity: "critical"
```

### 来源检查
```yaml
source_checks:
  - id: "S001"
    name: "来源已记录"
    check: "source != null"
    severity: "warning"
    
  - id: "S002"
    name: "来源可访问"
    check: "source_accessible"
    severity: "warning"
    
  - id: "S003"
    name: "来源可信"
    check: "source_credibility > 0.5"
    severity: "info"
```

### 时效检查
```yaml
timeliness_checks:
  - id: "T001"
    name: "未过期"
    check: "expiry_date == null || expiry_date > now"
    severity: "warning"
    
  - id: "T002"
    name: "更新及时"
    check: "last_updated_within_90d"
    severity: "info"
```

## 审计结果处理

### 自动修复
```yaml
auto_fix:
  conditions:
    - fix_safe: true
    - fix_deterministic: true
    
  actions:
    - update_timestamp
    - correct_format
    - remove_duplicates
```

### 标记待处理
```yaml
mark_for_action:
  conditions:
    - requires_human_review
    - complex_issue
    
  actions:
    - create_issue_ticket
    - assign_to_queue
    - set_priority
```

### 触发升级
```yaml
escalate:
  conditions:
    - critical_issue
    - security_concern
    - data_integrity_risk
    
  actions:
    - notify_admin
    - block_memory_usage
    - initiate_investigation
```

## 审计报告

### 报告内容
```yaml
audit_report:
  summary:
    - audit_id
    - audit_type
    - audit_date
    - sample_size
    - pass_rate
    
  findings:
    - issue_id
    - memory_id
    - issue_type
    - severity
    - description
    - recommendation
    
  metrics:
    - quality_score_distribution
    - issue_by_type
    - issue_by_severity
    
  actions_taken:
    - auto_fixed_count
    - marked_for_review_count
    - escalated_count
```

### 报告频率
```yaml
report_frequency:
  daily_summary: true
  weekly_detailed: true
  monthly_comprehensive: true
```

## 反馈到治理

### 反馈内容
```yaml
feedback_to_governance:
  - update_quality_metrics
  - identify_systemic_issues
  - propose_policy_changes
  - update_test_sets
```

### 测试集更新
```yaml
test_set_update:
  trigger: "audit_completed"
  actions:
    - add_problematic_cases
    - update_expected_results
    - validate_test_coverage
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 审计覆盖率 | 已审计/总记忆 | <10%/月 |
| 问题发现率 | 发现问题/审计样本 | >5% |
| 问题修复率 | 已修复/发现问题 | <80% |
| 审计延迟 | 审计执行延迟 | >1天 |

## 维护方式
- 新增审计类型: 创建审计规则
- 新增检查项: 更新检查项定义
- 调整频率: 更新审计频率配置

## 引用文件
- `memory_quality/MEMORY_SCORING.md` - 记忆评分
- `memory_quality/MEMORY_MERGE_RULES.md` - 记忆合并
- `governance/AUDIT_LOG.md` - 审计日志
