# POLICY_LEARNING_LOOP.md - 策略学习闭环

## 目的
定义基于反馈和指标的策略学习闭环，确保策略进化有控制回路。

## 适用范围
所有策略的自适应学习和优化。

## 学习闭环流程

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │ 收集表现 │───▶│ 识别场景 │───▶│ 提出调整 │             │
│  │   数据   │    │   特征   │    │   候选   │             │
│  └──────────┘    └──────────┘    └──────────┘             │
│       ▲                                    │               │
│       │                                    ▼               │
│  ┌──────────┐                       ┌──────────┐          │
│  │ 正式发布 │◀──────────────────────│ 灰度验证 │          │
│  │   应用   │                       │   评测   │          │
│  └──────────┘                       └──────────┘          │
│       │                                    ▲               │
│       │                                    │               │
│       ▼                                    │               │
│  ┌──────────┐                       ┌──────────┐          │
│  │ 监控效果 │──────────────────────▶│ 离线评测 │          │
│  │   反馈   │                       │   验证   │          │
│  └──────────┘                       └──────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 阶段详解

### 1. 收集表现数据
```yaml
data_collection:
  sources:
    - task_execution_logs
    - user_feedback
    - quality_metrics
    - cost_metrics
    - latency_metrics
    
  metrics:
    - success_rate
    - accuracy
    - completeness
    - user_satisfaction
    - cost_efficiency
    - latency
    
  aggregation:
    by_strategy: true
    by_task_type: true
    by_time_window: true
    by_user_segment: true
    
  storage:
    retention: "90d"
    sampling_rate: 1.0
```

### 2. 识别场景特征
```yaml
scenario_identification:
  analysis:
    - identify_high_performance_scenarios
    - identify_low_performance_scenarios
    - find_common_patterns
    - detect_anomalies
    
  features:
    - task_type
    - complexity
    - risk_level
    - time_constraint
    - user_preference
    - resource_availability
    
  clustering:
    method: "k-means"
    min_cluster_size: 100
    update_frequency: "weekly"
```

### 3. 提出调整候选
```yaml
adjustment_proposal:
  triggers:
    - performance_below_baseline
    - new_pattern_detected
    - user_feedback_negative
    - cost_efficiency_drop
    
  proposal_types:
    - parameter_tuning
    - strategy_switch
    - new_strategy_creation
    - strategy_deprecation
    
  constraints:
    - within_guardrails: true
    - no_safety_violation: true
    - reversible: true
    
  documentation:
    - proposal_reason
    - expected_impact
    - risk_assessment
    - rollback_plan
```

### 4. 离线评测验证
```yaml
offline_evaluation:
  environment: "staging"
  
  test_sets:
    - historical_data: "last_30d"
    - edge_cases: "collected_edge_cases"
    - regression_tests: "standard_test_suite"
    
  metrics:
    - accuracy_change
    - latency_change
    - cost_change
    - user_satisfaction_prediction
    
  thresholds:
    accuracy_improvement: "> 0"
    no_regression: true
    latency_increase: "< 10%"
    cost_increase: "< 5%"
    
  approval:
    auto_approve: "all_thresholds_met"
    manual_review: "any_threshold_borderline"
    reject: "any_threshold_failed"
```

### 5. 灰度验证
```yaml
canary_deployment:
  stages:
    - percentage: 1
      duration: "1d"
      monitoring: true
    - percentage: 5
      duration: "2d"
      monitoring: true
    - percentage: 20
      duration: "3d"
      monitoring: true
      
  monitoring:
    metrics:
      - error_rate
      - latency_p99
      - user_feedback
    alert_thresholds:
      error_rate_increase: "> 50%"
      latency_increase: "> 20%"
      negative_feedback: "> 10%"
      
  rollback:
    auto_trigger: "alert_threshold_breached"
    manual_trigger: "user_request"
```

### 6. 正式发布应用
```yaml
production_release:
  prerequisites:
    - canary_success: true
    - no_critical_issues: true
    - documentation_updated: true
    
  process:
    - update_strategy_registry
    - notify_stakeholders
    - update_monitoring_dashboards
    
  post_release:
    - monitor_for_24h
    - collect_feedback
    - document_results
```

### 7. 监控效果反馈
```yaml
effect_monitoring:
  metrics:
    - before_after_comparison
    - trend_analysis
    - user_feedback_analysis
    
  feedback_types:
    - positive:
        action: "reinforce_strategy"
    - neutral:
        action: "continue_monitoring"
    - negative:
        action: "trigger_review"
        
  reporting:
    frequency: "daily"
    channels: ["dashboard", "alerts"]
```

## 禁止规则

### 禁止直接在线修改
```yaml
forbidden_actions:
  - direct_online_modification:
      reason: "必须经过离线评测"
      
  - bypass_canary:
      reason: "必须经过灰度验证"
      
  - modify_core_policies:
      reason: "核心策略不可自动修改"
      includes:
        - safety_rules
        - rejection_rules
        - permission_controls
```

## 学习限制

### 变更限制
```yaml
change_limits:
  frequency:
    max_changes_per_day: 5
    min_interval_between_changes: "4h"
    
  scope:
    max_parameters_per_change: 3
    max_adjustment_per_parameter: "20%"
    
  approval:
    high_impact_changes: "require_manual_approval"
    new_strategy_creation: "require_manual_approval"
```

### 回滚机制
```yaml
rollback_mechanism:
  auto_rollback:
    triggers:
      - error_rate > baseline * 2
      - user_satisfaction < baseline * 0.8
      - critical_issue_detected
      
  manual_rollback:
    authority: ["admin", "ops"]
    process:
      - request_rollback
      - confirm_impact
      - execute_rollback
      - verify_recovery
```

## 学习记录

### 记录内容
```yaml
learning_records:
  fields:
    - learning_id
    - trigger_reason
    - data_analyzed
    - proposal_details
    - evaluation_results
    - canary_results
    - final_decision
    - impact_measured
    
  retention: "365d"
  audit: true
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 学习周期时长 | 完整闭环时长 | >7天 |
| 评测通过率 | 通过/总候选 | <50% |
| 灰度成功率 | 成功/总灰度 | <80% |
| 回滚率 | 回滚/总发布 | >10% |

## 维护方式
- 调整流程: 更新闭环流程
- 新增触发: 更新触发条件
- 调整限制: 更新学习限制

## 引用文件
- `strategy/STRATEGY_REGISTRY.json` - 策略注册表
- `strategy/ADAPTATION_GUARDRAILS.md` - 自适应护栏
- `strategy/STRATEGY_EVAL.md` - 策略评测
