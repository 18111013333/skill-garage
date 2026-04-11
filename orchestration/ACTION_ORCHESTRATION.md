# ACTION_ORCHESTRATION.md - 跨系统动作编排规则

## 目的
定义跨系统动作编排规则，确保系统能安全串联多个外部动作。

## 适用范围
所有需要跨多个外部系统执行的动作编排。

## 编排模式

| 模式 | 说明 | 适用场景 | 特点 |
|------|------|----------|------|
| 顺序执行 | 按顺序依次执行 | 有依赖关系的动作 | 简单可靠 |
| 并行执行 | 同时执行多个动作 | 无依赖的动作 | 效率高 |
| 条件分支 | 根据条件选择路径 | 有判断逻辑的场景 | 灵活 |
| 循环执行 | 重复执行动作 | 批量处理场景 | 可控循环 |

## 编排结构

### 编排定义
```yaml
orchestration:
  orchestration_id: "ORCH-001"
  name: "报告发布流程"
  description: "生成报告并发送通知"
  
  trigger:
    type: "manual"  # manual, scheduled, event
    conditions: []
    
  steps:
    - step_id: "STEP-001"
      name: "收集数据"
      action:
        type: "query"
        integration: "INT-database-001"
        operation: "select"
        params:
          sql: "SELECT * FROM reports"
      validation:
        - result_not_empty
      on_failure: "abort"
      
    - step_id: "STEP-002"
      name: "生成报告"
      depends_on: ["STEP-001"]
      action:
        type: "generate"
        integration: "INT-docs-001"
        operation: "create_document"
        params:
          template: "report_template"
          data_from: "STEP-001"
      validation:
        - document_created
      on_failure: "retry"
      
    - step_id: "STEP-003"
      name: "发送邮件"
      depends_on: ["STEP-002"]
      action:
        type: "send"
        integration: "INT-email-001"
        operation: "send_email"
        params:
          to: "${user_email}"
          subject: "报告已生成"
          attachment_from: "STEP-002"
      approval:
        required: true
        timeout: "1h"
      on_failure: "notify_and_pause"
      
    - step_id: "STEP-004"
      name: "创建日程"
      depends_on: ["STEP-003"]
      action:
        type: "create"
        integration: "INT-calendar-001"
        operation: "create_event"
        params:
          title: "报告评审会议"
          time: "+3d"
      on_failure: "continue"
      
    - step_id: "STEP-005"
      name: "记录审计"
      depends_on: ["STEP-003"]
      action:
        type: "log"
        integration: "internal"
        operation: "audit_log"
        params:
          action: "report_published"
          details: "${orchestration_context}"
```

## 编排流程

### 执行流程
```
编排启动
    ↓
┌─────────────────────────────────────┐
│ 1. 前置验证                          │
│    - 验证触发条件                    │
│    - 检查依赖可用                    │
│    - 确认权限足够                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 步骤执行                          │
│    - 按依赖顺序执行                  │
│    - 每步验证结果                    │
│    - 处理失败情况                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 审批处理                          │
│    - 遇审批节点暂停                  │
│    - 等待审批结果                    │
│    - 处理审批决策                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 完成处理                          │
│    - 记录执行结果                    │
│    - 通知相关方                      │
│    - 归档执行记录                    │
└─────────────────────────────────────┘
```

## 步骤控制

### 验证规则
```yaml
validation_rules:
  pre_step:
    - dependencies_satisfied
    - resources_available
    - permissions_valid
    
  post_step:
    - action_succeeded
    - result_valid
    - no_side_effects
    
  validation_actions:
    pass: "continue"
    fail: "handle_failure"
    warning: "log_and_continue"
```

### 失败处理
```yaml
failure_handling:
  strategies:
    abort:
      description: "终止整个编排"
      rollback: true
      notify: true
      
    retry:
      description: "重试当前步骤"
      max_retries: 3
      backoff: exponential
      
    skip:
      description: "跳过当前步骤"
      condition: "non_critical"
      continue: true
      
    pause:
      description: "暂停等待处理"
      notify: true
      resume_on: "manual"
```

### 回滚机制
```yaml
rollback:
  trigger:
    - critical_step_failed
    - user_abort
    - timeout_exceeded
    
  process:
    - identify_completed_steps
    - execute_rollback_in_reverse
    - verify_rollback_success
    - notify_affected_parties
```

## 审批集成

### 审批节点
```yaml
approval_nodes:
  placement:
    - before_high_risk_action
    - before_external_write
    - before_batch_operation
    - at_phase_boundary
    
  configuration:
    approvers: ["admin", "owner"]
    timeout: "4h"
    timeout_action: "abort"
    
  notification:
    on_pending: true
    on_approved: true
    on_rejected: true
```

### 审批流程
```yaml
approval_flow:
  steps:
    - pause_execution
    - send_approval_request
    - wait_for_decision
    - process_decision:
        approved: "continue"
        rejected: "abort_with_rollback"
        timeout: "escalate"
```

## 暂停与恢复

### 暂停触发
```yaml
pause_triggers:
  - approval_required
  - resource_unavailable
  - user_request
  - error_detected
```

### 恢复条件
```yaml
resume_conditions:
  - approval_granted
  - resource_available
  - user_resume_request
  - error_resolved
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 编排成功率 | 成功/总数 | <90% |
| 平均执行时间 | 编排耗时 | >预期2倍 |
| 审批等待时间 | 审批等待时长 | >2h |
| 回滚成功率 | 回滚成功/回滚 | <95% |

## 维护方式
- 新增模式: 创建编排模式
- 新增步骤类型: 更新步骤定义
- 调整规则: 更新控制规则

## 引用文件
- `orchestration/INTEGRATION_REGISTRY.json` - 集成注册表
- `orchestration/APPROVAL_GATEWAY.md` - 审批网关
- `orchestration/TRANSACTION_POLICY.md` - 事务策略
