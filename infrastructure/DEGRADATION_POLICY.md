# DEGRADATION_POLICY.md - 资源不足降级策略

## 目的
定义资源不足时的系统降级策略，确保优雅降级而非崩溃。

## 适用范围
所有资源紧张或不足的场景。

## 降级等级

| 等级 | 触发条件 | 影响范围 | 恢复条件 |
|------|----------|----------|----------|
| L1 轻度 | 资源使用 > 80% | 非核心功能 | 使用 < 70% |
| L2 中度 | 资源使用 > 90% | 辅助功能 | 使用 < 80% |
| L3 重度 | 资源使用 > 95% | 核心功能受限 | 使用 < 85% |
| L4 紧急 | 资源耗尽 | 仅保核心 | 手动恢复 |

## 降级措施

### L1 轻度降级
```yaml
level_1_degradation:
  trigger:
    - resource_utilization: "> 80%"
    - queue_depth: "> 50"
    
  measures:
    - reduce_validation_depth:
        description: "降低校验深度"
        impact: "校验覆盖率降低"
        reversible: true
        
    - shorten_context_window:
        description: "缩短上下文窗口"
        impact: "上下文信息减少"
        reversible: true
        
    - defer_non_critical:
        description: "延迟非关键任务"
        impact: "低优先级任务延迟"
        reversible: true
        
  preserved:
    - core_functionality
    - safety_guardrails
    - permission_controls
```

### L2 中度降级
```yaml
level_2_degradation:
  trigger:
    - resource_utilization: "> 90%"
    - error_rate: "> 2%"
    
  measures:
    - use_lighter_models:
        description: "使用轻量模型"
        impact: "输出质量可能下降"
        fallback: "标准模型"
        
    - reduce_output_detail:
        description: "减少输出细节"
        impact: "信息完整度降低"
        
    - queue_low_priority:
        description: "低优先级任务排队"
        impact: "响应延迟增加"
        
    - limit_concurrent:
        description: "限制并发数"
        impact: "吞吐量降低"
        
  preserved:
    - safety_guardrails
    - permission_controls
    - core_rejection_rules
```

### L3 重度降级
```yaml
level_3_degradation:
  trigger:
    - resource_utilization: "> 95%"
    - error_rate: "> 5%"
    - queue_overflow: true
    
  measures:
    - minimal_validation:
        description: "最小化校验"
        impact: "仅执行必要校验"
        
    - essential_features_only:
        description: "仅核心功能"
        impact: "辅助功能暂停"
        
    - pause_low_priority_projects:
        description: "暂停低优先级项目"
        impact: "P3/P4项目暂停"
        
    - reduce_quality_target:
        description: "降低质量目标"
        impact: "接受较低质量输出"
        
  preserved:
    - safety_guardrails
    - permission_controls
    - core_rejection_rules
    - audit_logging
```

### L4 紧急降级
```yaml
level_4_degradation:
  trigger:
    - resource_exhausted: true
    - system_unstable: true
    
  measures:
    - emergency_mode:
        description: "紧急模式"
        actions:
          - accept_only_critical_tasks
          - minimal_processing
          - queue_all_others
          
    - graceful_degradation:
        description: "优雅降级"
        actions:
          - complete_in_progress
          - reject_new_non_critical
          - preserve_system_stability
          
  preserved:
    - safety_guardrails
    - permission_controls
    - core_rejection_rules
    - audit_logging
    - kill_switch
```

## 禁止降级项

### 绝对不可降级
```yaml
never_degrade:
  - safety_guardrails:
      description: "安全护栏"
      reason: "安全不可妥协"
      
  - permission_controls:
      description: "权限控制"
      reason: "权限不可绕过"
      
  - core_rejection_rules:
      description: "核心拒绝规则"
      reason: "拒绝规则不可绕过"
      
  - audit_logging:
      description: "审计日志"
      reason: "审计不可中断"
      
  - kill_switch:
      description: "紧急停机"
      reason: "停机能力必须保持"
```

## 降级流程

```
资源紧张检测
    ↓
┌─────────────────────────────────────┐
│ 1. 评估降级需求                      │
│    - 确定资源紧张程度                │
│    - 选择降级等级                    │
│    - 评估影响范围                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 执行降级措施                      │
│    - 按等级执行措施                  │
│    - 通知受影响方                    │
│    - 记录降级事件                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 监控降级效果                      │
│    - 监控资源使用                    │
│    - 监控系统稳定性                  │
│    - 监控用户体验                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 恢复决策                          │
│    - 满足恢复条件 → 逐步恢复         │
│    - 不满足 → 继续降级               │
└─────────────────────────────────────┘
```

## 恢复流程

### 恢复条件
```yaml
recovery_conditions:
  level_1:
    - utilization: "< 70%"
    - queue_depth: "< 30"
    
  level_2:
    - utilization: "< 80%"
    - error_rate: "< 1%"
    
  level_3:
    - utilization: "< 85%"
    - system_stable: true
    
  level_4:
    - manual_approval: true
    - resources_available: true
```

### 恢复步骤
```yaml
recovery_steps:
  - verify_conditions
  - gradual_restore:
      - restore_features_incrementally
      - monitor_after_each_restore
  - full_restore
  - notify_users
  - document_recovery
```

## 降级通知

### 通知内容
```yaml
notification:
  on_degradation:
    to: ["admin", "affected_users"]
    content:
      - degradation_level
      - affected_features
      - expected_duration
      - alternative_actions
      
  on_recovery:
    to: ["admin", "affected_users"]
    content:
      - recovery_status
      - restored_features
      - apology_for_inconvenience
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 降级触发频率 | 降级次数/周 | >3 |
| 平均降级时长 | 降级持续时间 | >1h |
| 恢复成功率 | 成功恢复/降级 | <95% |
| 禁止项触碰 | 触碰禁止项次数 | >0 |

## 维护方式
- 新增措施: 创建降级措施
- 调整等级: 更新降级等级
- 调整触发: 更新触发条件

## 引用文件
- `resources/RESOURCE_SCHEMA.json` - 资源结构
- `resources/CAPACITY_PLANNING.md` - 容量规划
- `safety/RISK_POLICY.md` - 风险策略
