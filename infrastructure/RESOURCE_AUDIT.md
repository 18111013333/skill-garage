# RESOURCE_AUDIT.md - 资源使用审计规则

## 目的
定义资源使用审计规则，确保资源消耗可追踪、可追责、可优化。

## 适用范围
所有资源的使用审计。

## 审计内容

### 审计记录项
```yaml
audit_record:
  record_id: "AUD-RES-001"
  timestamp: "2024-01-15T10:00:00Z"
  
  requester:
    user_id: "user_001"
    project_id: "PROJ-001"
    task_id: "TASK-001"
    
  resource:
    resource_id: "RES-model-001"
    resource_type: "model_compute"
    
  request:
    amount: 10000
    unit: "tokens"
    reason: "完成报告生成任务"
    priority: "P1"
    
  allocation:
    allocated: 10000
    allocation_type: "dynamic"
    allocation_time: "2024-01-15T10:00:05Z"
    
  usage:
    actual_used: 8500
    waste: 1500
    usage_duration: "5m"
    
  cost:
    unit_cost: 0.001
    total_cost: 8.5
    
  compliance:
    within_quota: true
    within_budget: true
    approved: true
    
  release:
    released_at: "2024-01-15T10:05:00Z"
    release_type: "auto"
    abnormal_release: false
    
  flags:
    - flag: "high_usage_variance"
      details: "实际使用与申请差异较大"
```

## 审计维度

### 申请审计
```yaml
request_audit:
  checks:
    - valid_requester: true
    - valid_reason: true
    - reasonable_amount: true
    - within_permissions: true
    
  anomalies:
    - excessive_request:
        threshold: "> 2x average"
        action: "flag_for_review"
        
    - unusual_pattern:
        detection: "pattern_anomaly"
        action: "alert"
```

### 使用审计
```yaml
usage_audit:
  checks:
    - usage_within_allocation: true
    - no_unauthorized_use: true
    - efficient_utilization: true
    
  metrics:
    - utilization_rate: "actual/allocated"
    - waste_rate: "waste/allocated"
    - efficiency_score: "utilization * (1 - waste_rate)"
    
  anomalies:
    - low_utilization:
        threshold: "< 50%"
        action: "flag_for_optimization"
        
    - high_waste:
        threshold: "> 20%"
        action: "review_request_accuracy"
```

### 成本审计
```yaml
cost_audit:
  checks:
    - within_budget: true
    - cost_reasonable: true
    - no_cost_anomaly: true
    
  tracking:
    - daily_cost
    - project_cost
    - user_cost
    - resource_type_cost
    
  anomalies:
    - cost_spike:
        threshold: "> 2x daily_average"
        action: "alert_and_investigate"
        
    - budget_approaching:
        threshold: "> 80%"
        action: "notify_and_throttle"
```

### 释放审计
```yaml
release_audit:
  checks:
    - timely_release: true
    - complete_release: true
    - no_leak: true
    
  anomalies:
    - delayed_release:
        threshold: "> 1h after use"
        action: "auto_release_and_flag"
        
    - incomplete_release:
        detection: "residual_allocation"
        action: "force_release"
        
    - leak_detected:
        detection: "unreleased_resource"
        action: "immediate_release_and_alert"
```

## 审计流程

### 实时审计
```yaml
real_time_audit:
  enabled: true
  
  triggers:
    - on_allocation
    - on_usage_update
    - on_release
    
  actions:
    - record_event
    - check_anomalies
    - update_metrics
    - trigger_alerts
```

### 定期审计
```yaml
periodic_audit:
  daily:
    - summarize_daily_usage
    - identify_anomalies
    - generate_daily_report
    
  weekly:
    - analyze_usage_patterns
    - identify_optimization_opportunities
    - review_flagged_items
    
  monthly:
    - comprehensive_cost_analysis
    - efficiency_report
    - compliance_review
```

## 异常处理

### 异常分类
```yaml
anomaly_classification:
  minor:
    - slight_over_request
    - minor_delay
    action: "log_and_monitor"
    
  moderate:
    - significant_waste
    - budget_approaching
    action: "notify_and_recommend"
    
  severe:
    - budget_exceeded
    - unauthorized_use
    action: "alert_and_investigate"
    
  critical:
    - resource_leak
    - security_concern
    action: "immediate_action"
```

### 处理流程
```yaml
anomaly_handling:
  steps:
    - detect_anomaly
    - classify_severity
    - notify_appropriate_parties
    - initiate_investigation
    - implement_corrective_action
    - document_resolution
```

## 审计报告

### 日报内容
```yaml
daily_report:
  summary:
    - total_allocations
    - total_usage
    - total_cost
    - anomaly_count
    
  details:
    - top_users
    - top_projects
    - resource_breakdown
    - flagged_items
```

### 月报内容
```yaml
monthly_report:
  overview:
    - cost_trend
    - usage_trend
    - efficiency_trend
    
  analysis:
    - cost_by_project
    - cost_by_resource_type
    - efficiency_by_project
    
  recommendations:
    - optimization_opportunities
    - budget_adjustments
    - policy_updates
```

## 与审计系统联动

### 联动配置
```yaml
audit_integration:
  system: "governance/AUDIT_LOG.md"
  
  events_to_log:
    - allocation_events
    - usage_events
    - release_events
    - anomaly_events
    
  retention: "1_year"
  searchable: true
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 审计覆盖率 | 已审计/总使用 | <95% |
| 异常发现率 | 发现异常/审计 | >5% |
| 异常处理率 | 已处理/发现 | <90% |
| 审计延迟 | 审计完成延迟 | >1h |

## 维护方式
- 新增审计项: 更新审计内容
- 调整阈值: 更新异常阈值
- 新增报告: 创建报告模板

## 引用文件
- `resources/RESOURCE_SCHEMA.json` - 资源结构
- `resources/ALLOCATION_POLICY.md` - 分配策略
- `governance/AUDIT_LOG.md` - 审计日志
