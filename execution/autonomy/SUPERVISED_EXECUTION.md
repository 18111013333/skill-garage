# SUPERVISED_EXECUTION.md - 强监管下执行规则

## 目的
定义"强监管下执行"的规则，确保自主执行全程可看、可停、可接管。

## 适用范围
所有L3及以上等级的自主执行。

## 监管框架

```
┌─────────────────────────────────────────────────────────────┐
│                      监管控制层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ 执行前   │  │ 执行中   │  │ 异常处理 │  │ 人工接管 │   │
│  │ 校验     │  │ 监测     │  │ 暂停     │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       │              │              │              │       │
│       ▼              ▼              ▼              ▼       │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                   执行层                            │  │
│  │  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐      │  │
│  │  │步骤1│→│步骤2│→│步骤3│→│步骤4│→│步骤5│      │  │
│  │  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘      │  │
│  └─────────────────────────────────────────────────────┘  │
│                           │                                │
│                           ▼                                │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                   审计层                            │  │
│  │  日志记录 │ 状态追踪 │ 指标收集 │ 告警触发          │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 执行前校验

### 校验项
```yaml
pre_execution_checks:
  plan_validation:
    - plan_approved: true
    - dependencies_satisfied: true
    - resources_available: true
    
  boundary_check:
    - within_time_window: true
    - within_resource_limits: true
    - within_permission_scope: true
    
  safety_check:
    - no_forbidden_actions: true
    - rollback_plan_valid: true
    - kill_switch_active: true
    
  state_check:
    - system_healthy: true
    - no_conflicting_operations: true
```

### 校验流程
```yaml
validation_flow:
  steps:
    - run_all_checks
    - aggregate_results
    - decision:
        all_pass: "proceed"
        any_fail: "halt_and_report"
        any_warning: "proceed_with_caution"
```

## 执行中监测

### 实时监测
```yaml
real_time_monitoring:
  metrics:
    - execution_progress
    - resource_consumption
    - error_rate
    - latency
    - output_quality
    
  frequency: "10s"
  dashboard: true
  alerts: true
```

### 异常检测
```yaml
anomaly_detection:
  patterns:
    - error_rate_spike:
        threshold: "> 5%"
        action: "pause_and_alert"
        
    - resource_exhaustion:
        threshold: "> 90%"
        action: "throttle_or_pause"
        
    - unexpected_output:
        detection: "output_validator"
        action: "pause_for_review"
        
    - boundary_approach:
        threshold: "within 10% of limit"
        action: "alert_and_slow"
```

### 状态追踪
```yaml
state_tracking:
  checkpoints:
    - every_step
    - every_phase
    - on_significant_event
    
  tracking_data:
    - current_step
    - progress_percentage
    - elapsed_time
    - remaining_time_estimate
    - resource_usage
    - issues_encountered
```

## 异常暂停

### 暂停触发
```yaml
pause_triggers:
  automatic:
    - error_rate > 5%
    - resource_usage > 95%
    - unexpected_exception
    - boundary_violation_detected
    - quality_check_failed
    
  manual:
    - user_request
    - admin_intervention
    - system_override
```

### 暂停处理
```yaml
pause_handling:
  actions:
    - stop_current_step
    - save_execution_state
    - preserve_intermediate_results
    - notify_stakeholders
    - await_resolution
    
  notification:
    to: ["plan_owner", "admin"]
    content:
      - pause_reason
      - current_state
      - affected_steps
      - recommended_actions
```

## 人工接管

### 接管触发
```yaml
takeover_triggers:
  - user_explicit_request
  - admin_intervention
  - prolonged_pause: "> 30m"
  - critical_failure
  - security_concern
```

### 接管流程
```yaml
takeover_flow:
  steps:
    - verify_takeover_authority
    - transfer_control_to_human
    - provide_context_summary
    - enable_manual_controls
    - record_takeover_event
    
  manual_controls:
    - resume_execution
    - modify_next_steps
    - rollback_to_checkpoint
    - abort_plan
    - modify_parameters
```

### 接管后处理
```yaml
post_takeover:
  options:
    - human_completes:
        action: "human_finishes_remaining_steps"
        
    - human_modifies:
        action: "update_plan_and_resume"
        
    - human_aborts:
        action: "execute_rollback"
        
  handback:
    condition: "human_requests_handback"
    process:
      - verify_system_state
      - transfer_control_back
      - resume_from_current_point
```

## 阶段汇报

### 汇报配置
```yaml
phase_reporting:
  frequency:
    - after_each_phase
    - periodic: "30m"
    - on_significant_event
    
  content:
    - phase_objective
    - completion_status
    - key_results
    - issues_encountered
    - resource_consumption
    - next_phase_preview
    
  recipients:
    - plan_owner
    - admin
    - stakeholders
```

### 汇报格式
```yaml
report_format:
  summary:
    - phase: "PHASE-001"
      status: "completed"
      duration: "2h"
      
  details:
    - steps_completed: 5
    - steps_remaining: 3
    - issues: 1
      
  metrics:
    - resource_usage: "65%"
    - error_rate: "0.5%"
```

## 最终复核

### 复核内容
```yaml
final_review:
  checks:
    - all_objectives_met: true
    - quality_standards_met: true
    - no_unresolved_issues: true
    - audit_trail_complete: true
    
  verification:
    - output_validation
    - success_criteria_check
    - impact_assessment
    - lessons_learned_extraction
```

### 复核流程
```yaml
review_flow:
  steps:
    - collect_execution_evidence
    - verify_success_criteria
    - assess_overall_quality
    - document_lessons_learned
    - archive_execution_records
    - notify_completion
```

## 转人工条件

### 必须转人工
```yaml
must_transfer_to_human:
  - security_violation_detected
  - legal_compliance_risk
  - data_integrity_concern
  - user_explicit_request
  - system_unable_to_proceed
```

### 建议转人工
```yaml
should_transfer_to_human:
  - complex_decision_required
  - multiple_failures
  - unexpected_scenario
  - ethical_consideration
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 异常暂停率 | 暂停/总执行 | >10% |
| 人工接管率 | 接管/总执行 | >5% |
| 校验通过率 | 通过/校验 | <95% |
| 汇报及时率 | 及时/应汇报 | <90% |

## 维护方式
- 新增校验项: 更新校验配置
- 新增监测指标: 更新监测配置
- 调整触发条件: 更新触发配置

## 引用文件
- `autonomy/AUTONOMY_LEVELS.md` - 自主等级
- `autonomy/APPROVAL_CHAIN.md` - 审批链
- `autonomy/KILL_SWITCH.md` - 紧急停机
