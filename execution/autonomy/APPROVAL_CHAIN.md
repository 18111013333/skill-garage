# APPROVAL_CHAIN.md - 自主计划审批链

## 目的
定义自主计划中的审批链，确保关键节点都能被管住。

## 适用范围
所有自主执行计划中的审批管理。

## 审批类型

| 类型 | 说明 | 触发时机 | 审批人 |
|------|------|----------|--------|
| 预审批 | 计划开始前 | 计划提交时 | 管理员/负责人 |
| 步骤审批 | 关键步骤前 | 步骤执行前 | 按风险级别 |
| 结果审批 | 阶段完成后 | 阶段结束时 | 负责人 |
| 异常升级审批 | 异常情况时 | 异常发生时 | 管理员 |

## 审批链结构

### 审批链定义
```yaml
approval_chain:
  chain_id: "CHAIN-001"
  plan_id: "PLAN-2024-001"
  
  nodes:
    - node_id: "NODE-001"
      type: "pre_approval"
      name: "计划启动审批"
      position: "before_plan_start"
      
      approvers:
        primary: ["admin", "owner"]
        quorum: 1
        
      content:
        - plan_objective
        - risk_assessment
        - resource_requirements
        
      timeout: "24h"
      on_timeout: "escalate"
      
    - node_id: "NODE-002"
      type: "step_approval"
      name: "高风险步骤审批"
      position: "before_step:STEP-005"
      
      approvers:
        primary: ["owner"]
        quorum: 1
        
      content:
        - step_details
        - risk_mitigation
        - rollback_plan
        
      timeout: "4h"
      
    - node_id: "NODE-003"
      type: "phase_approval"
      name: "阶段完成审批"
      position: "after_phase:PHASE-001"
      
      approvers:
        primary: ["owner"]
        
      content:
        - phase_results
        - quality_metrics
        - next_phase_plan
        
      timeout: "8h"
      
    - node_id: "NODE-004"
      type: "result_approval"
      name: "最终结果审批"
      position: "after_plan_complete"
      
      approvers:
        primary: ["admin", "owner"]
        quorum: 2
        
      content:
        - final_results
        - success_criteria_verification
        - lessons_learned
        
      timeout: "48h"
```

## 审批节点配置

### 预审批
```yaml
pre_approval:
  trigger: "plan_submission"
  
  requirements:
    - plan_validated: true
    - risk_assessed: true
    - resources_identified: true
    
  approvers:
    - role: "admin"
      for_risk: ["high", "critical"]
    - role: "owner"
      for_risk: ["low", "medium", "high"]
      
  content:
    - 计划目标
    - 风险评估
    - 资源需求
    - 时间预估
    - 回滚方案
    
  decision:
    approved: "start_plan"
    rejected: "revise_plan"
    timeout: "escalate_to_higher"
```

### 步骤审批
```yaml
step_approval:
  trigger: "before_high_risk_step"
  
  conditions:
    - step_risk_level: ["high", "critical"]
    - or: step_type in ["external_write", "batch_operation"]
    
  approvers:
    high_risk:
      - owner
    critical_risk:
      - admin
      - owner
      
  content:
    - 步骤详情
    - 预期影响
    - 风险缓解
    - 回滚方案
    
  timeout: "4h"
```

### 结果审批
```yaml
result_approval:
  trigger: "phase_or_plan_complete"
  
  requirements:
    - all_steps_completed
    - quality_metrics_met
    - no_unresolved_issues
    
  approvers:
    - owner
    - admin (for high risk)
    
  content:
    - 执行结果
    - 质量指标
    - 问题记录
    - 后续建议
    
  timeout: "24h"
```

### 异常升级审批
```yaml
escalation_approval:
  trigger: "exception_detected"
  
  exceptions:
    - execution_error
    - resource_exhaustion
    - boundary_violation
    - unexpected_result
    
  approvers:
    - admin
    - security_officer (if security_related)
    
  urgency: "immediate"
  timeout: "1h"
  
  actions:
    approved: "continue_with_modification"
    rejected: "abort_and_rollback"
```

## 审批流程

### 单节点流程
```
审批触发
    ↓
┌─────────────────────────────────────┐
│ 1. 准备审批内容                      │
│    - 收集相关信息                    │
│    - 生成审批请求                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 发送审批请求                      │
│    - 通知审批人                      │
│    - 设置超时计时                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 等待审批决策                      │
│    - 监控审批状态                    │
│    - 处理超时提醒                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 执行审批决策                      │
│    - 记录审批结果                    │
│    - 执行后续动作                    │
└─────────────────────────────────────┘
```

### 多节点流程
```yaml
multi_node_flow:
  sequence: "strict_order"
  
  on_node_approved:
    - record_approval
    - proceed_to_next_node
    
  on_node_rejected:
    - record_rejection
    - halt_chain
    - notify_plan_owner
    
  on_node_timeout:
    - escalate
    - wait_for_escalation_result
```

## 审批权限

### 权限矩阵
```yaml
permission_matrix:
  plan_pre_approval:
    admin: approve_reject
    owner: approve_reject
    observer: view_only
    
  step_approval:
    admin: approve_reject
    owner: approve_reject
    
  result_approval:
    admin: approve_reject
    owner: approve_reject
    
  escalation:
    admin: approve_reject_modify
    security_officer: approve_reject
```

### 委托规则
```yaml
delegation:
  allowed: true
  conditions:
    - delegatee_has_permission
    - delegation_recorded
  max_delegation_depth: 1
```

## 审批加速

### 快速通道
```yaml
fast_track:
  conditions:
    - low_risk_plan
    - trusted_user
    - routine_operation
    
  process:
    - auto_approve: true
    - notify_only: true
    - audit: comprehensive
```

### 并行审批
```yaml
parallel_approval:
  enabled: true
  conditions:
    - multiple_approvers_required
    - independent_decisions
    
  aggregation:
    - all_approve: "proceed"
    - any_reject: "halt"
    - quorum_approve: "proceed"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 审批通过率 | 通过/总审批 | <70% |
| 平均审批时间 | 审批等待时长 | >4h |
| 超时率 | 超时/总审批 | >10% |
| 升级率 | 升级/总审批 | >5% |

## 维护方式
- 新增审批类型: 创建审批节点类型
- 调整权限: 更新权限矩阵
- 调整流程: 更新审批流程

## 引用文件
- `autonomy/AUTONOMY_LEVELS.md` - 自主等级
- `autonomy/PLAN_GENERATION.md` - 计划生成
- `autonomy/SUPERVISED_EXECUTION.md` - 强监管执行
