# ADAPTATION_GUARDRAILS.md - 自适应护栏

## 目的
定义策略自适应的护栏，防止系统越调越偏。

## 适用范围
所有自适应学习和策略调整场景。

## 护栏原则

1. **安全边界不可突破**: 核心安全规则不允许自适应修改
2. **拒绝规则不可绕过**: 用户拒绝和权限控制不可自动调整
3. **评测门禁不可降级**: 质量评测标准不可降低
4. **灰度发布不可跳过**: 策略变更必须经过灰度

## 禁止自适应区域

### 完全禁止区域
```yaml
forbidden_zones:
  - name: "安全边界"
    components:
      - safety/RISK_POLICY.md
      - safety/BOUNDARY.json
    reason: "安全规则不可自动修改"
    violation_action: "block_and_alert"
    
  - name: "拒绝规则"
    components:
      - user_rejection_rules
      - permission_controls
    reason: "用户拒绝不可自动绕过"
    violation_action: "block_and_alert"
    
  - name: "权限控制"
    components:
      - access_control_rules
      - authentication_config
    reason: "权限不可自动调整"
    violation_action: "block_and_alert"
    
  - name: "核心评测门禁"
    components:
      - evaluation/OUTPUT_VALIDATOR.md
      - evaluation/QUALITY_METRICS.md
    reason: "评测标准不可降低"
    violation_action: "block_and_alert"
```

### 条件限制区域
```yaml
restricted_zones:
  - name: "策略参数"
    components:
      - strategy/STRATEGY_REGISTRY.json
    allowed_changes:
      - weight_adjustment
      - threshold_tuning
    conditions:
      - within_bounds: "±20%"
      - requires_approval: true
      - requires_testing: true
      
  - name: "检索参数"
    components:
      - retrieval_config
    allowed_changes:
      - top_k_adjustment
      - score_threshold_tuning
    conditions:
      - within_bounds: "±30%"
      - requires_validation: true
      
  - name: "缓存策略"
    components:
      - cache_config
    allowed_changes:
      - ttl_adjustment
      - size_adjustment
    conditions:
      - within_bounds: "±50%"
      - no_data_loss: true
```

## 变更限制

### 变更幅度限制
```yaml
change_limits:
  single_change:
    max_adjustment: "20%"
    max_parameters: 3
    
  cumulative_change:
    daily_max: "50%"
    weekly_max: "100%"
    
  rate_limit:
    changes_per_hour: 5
    changes_per_day: 20
```

### 变更类型限制
```yaml
change_type_limits:
  allowed:
    - parameter_tuning
    - weight_adjustment
    - threshold_change
    - strategy_selection
    
  requires_approval:
    - new_strategy_addition
    - strategy_removal
    - major_parameter_change
    
  forbidden:
    - safety_rule_modification
    - permission_bypass
    - evaluation_criteria_lowering
```

## 变更验证

### 变更前验证
```yaml
pre_change_validation:
  checks:
    - name: "护栏检查"
      action: "verify_not_in_forbidden_zone"
      
    - name: "幅度检查"
      action: "verify_within_change_limits"
      
    - name: "依赖检查"
      action: "verify_dependencies_not_affected"
      
    - name: "回退检查"
      action: "verify_rollback_possible"
      
  failure_action: "block_change"
```

### 变更后验证
```yaml
post_change_validation:
  checks:
    - name: "效果验证"
      action: "verify_improvement"
      threshold: "no_regression"
      
    - name: "安全验证"
      action: "verify_safety_not_compromised"
      
    - name: "性能验证"
      action: "verify_performance_acceptable"
      
  failure_action: "auto_rollback"
```

## 回滚机制

### 自动回滚触发
```yaml
auto_rollback_triggers:
  - condition: "error_rate > baseline * 2"
    delay: "5m"
    
  - condition: "user_satisfaction < baseline * 0.8"
    delay: "10m"
    
  - condition: "safety_violation_detected"
    delay: "immediate"
    
  - condition: "critical_metric_degradation"
    delay: "immediate"
```

### 回滚流程
```yaml
rollback_flow:
  steps:
    - name: "检测问题"
      action: "detect_trigger_condition"
      
    - name: "暂停变更"
      action: "pause_all_adaptations"
      
    - name: "执行回滚"
      action: "restore_previous_state"
      
    - name: "验证恢复"
      action: "verify_rollback_success"
      
    - name: "记录分析"
      action: "log_and_analyze_failure"
```

## 审批流程

### 需要审批的变更
```yaml
approval_required:
  - change_type: "new_strategy"
    approver: "admin"
    timeout: "24h"
    
  - change_type: "major_parameter_change"
    approver: "admin"
    timeout: "4h"
    
  - change_type: "restricted_zone_change"
    approver: "admin + security"
    timeout: "48h"
```

### 审批流程
```yaml
approval_flow:
  steps:
    - name: "提交变更请求"
      content:
        - change_description
        - expected_impact
        - risk_assessment
        - rollback_plan
        
    - name: "自动预审"
      checks:
        -护栏检查
        - 格式验证
        - 基本合理性
        
    - name: "人工审批"
      actions:
        - review_request
        - approve_or_reject
        - add_conditions
        
    - name: "执行变更"
      conditions:
        - approval_granted
        - conditions_met
```

## 监控告警

### 护栏告警
```yaml
guardrail_alerts:
  - name: "护栏触碰"
    condition: "forbidden_zone_access_attempted"
    level: "critical"
    action: "block_and_notify_admin"
    
  - name: "变更超限"
    condition: "change_exceeds_limits"
    level: "high"
    action: "block_and_notify"
    
  - name: "回滚触发"
    condition: "auto_rollback_executed"
    level: "high"
    action: "notify_and_log"
```

### 监控指标
| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 护栏触碰次数 | 尝试突破护栏次数 | >0 |
| 自动回滚次数 | 自动回滚执行次数 | >3/天 |
| 审批拒绝率 | 被拒绝/总申请 | >30% |
| 变更失败率 | 失败/总变更 | >10% |

## 审计日志

### 审计内容
```yaml
audit_log:
  events:
    - adaptation_proposed
    - adaptation_approved
    - adaptation_rejected
    - adaptation_executed
    - adaptation_rolled_back
    - guardrail_triggered
    
  fields:
    - timestamp
    - change_type
    - change_details
    - affected_components
    - approval_status
    - execution_result
    - rollback_reason (if applicable)
```

## 维护方式
- 新增护栏: 更新禁止/限制区域
- 调整限制: 更新变更限制配置
- 新增告警: 更新告警规则

## 引用文件
- `safety/RISK_POLICY.md` - 风险策略
- `safety/BOUNDARY.json` - 安全边界
- `strategy/POLICY_LEARNING_LOOP.md` - 策略学习闭环
