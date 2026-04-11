# APPROVAL_GATEWAY.md - 外部动作审批网关

## 目的
定义外部动作审批网关，确保外部写操作有统一审批入口。

## 适用范围
所有外部系统的写操作审批。

## 审批触发

### 必须审批的动作
```yaml
mandatory_approval_actions:
  - 发送:
      - send_email
      - send_message
      - send_notification
      
  - 删除:
      - delete_document
      - delete_record
      - delete_file
      
  - 修改共享内容:
      - update_shared_document
      - modify_shared_calendar
      - edit_shared_resource
      
  - 批量操作:
      - batch_send
      - batch_update
      - batch_delete
      
  - 高风险跨系统写入:
      - cross_system_sync
      - external_api_write
      - third_party_integration
```

### 按风险级别审批
```yaml
risk_based_approval:
  low:
    actions: ["read", "query"]
    approval: none
    
  medium:
    actions: ["create_draft", "internal_write"]
    approval: optional
    
  high:
    actions: ["send", "update_shared"]
    approval: required
    
  critical:
    actions: ["delete", "batch_operation", "external_write"]
    approval: required_with_escalation
```

## 审批流程

### 标准流程
```
动作请求
    ↓
┌─────────────────────────────────────┐
│ 1. 审批需求评估                      │
│    - 判断是否需要审批                │
│    - 确定审批级别                    │
│    - 识别审批人                      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 创建审批请求                      │
│    - 生成审批ID                      │
│    - 记录请求详情                    │
│    - 设置超时时间                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 发送审批通知                      │
│    - 通知审批人                      │
│    - 提供审批入口                    │
│    - 显示风险提示                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 等待审批决策                      │
│    - 监控审批状态                    │
│    - 处理超时情况                    │
│    - 处理撤回请求                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 5. 执行审批决策                      │
│    - 通过：执行动作                  │
│    - 拒绝：取消并通知                │
│    - 超时：按策略处理                │
└─────────────────────────────────────┘
```

## 审批请求结构

```yaml
approval_request:
  request_id: "APPR-2024-001"
  
  action:
    type: "send_email"
    integration: "INT-email-001"
    details:
      to: "recipient@example.com"
      subject: "报告通知"
      content_preview: "..."
      
  risk_assessment:
    level: "high"
    factors:
      - external_recipient
      - contains_attachment
      
  requester:
    user_id: "user_001"
    project_id: "PROJ-001"
    reason: "发送周报给客户"
    
  approvers:
    primary: ["admin_001"]
    fallback: ["admin_002"]
    
  timeout:
    duration: "4h"
    action: "escalate"
    
  status: "pending"
  created_at: "2024-01-15T10:00:00Z"
```

## 审批人确定

### 审批人规则
```yaml
approver_rules:
  by_action_type:
    send:
      - project_owner
      - admin
      
    delete:
      - admin
      - data_owner
      
    batch_operation:
      - admin
      
  by_risk_level:
    high:
      - admin
    critical:
      - admin
      - security_officer
      
  fallback:
    - if_primary_unavailable: "escalate_to_secondary"
    - if_all_unavailable: "escalate_to_system_admin"
```

## 超时处理

### 超时配置
```yaml
timeout_config:
  by_action_type:
    send: "2h"
    delete: "4h"
    batch_operation: "8h"
    external_write: "4h"
    
  escalation:
    first_reminder: "50% timeout"
    second_reminder: "75% timeout"
    final_escalation: "100% timeout"
```

### 超时动作
```yaml
timeout_actions:
  auto_approve:
    condition: "low_risk && trusted_user"
    action: "approve_and_execute"
    
  auto_reject:
    condition: "high_risk && no_response"
    action: "reject_and_notify"
    
  escalate:
    condition: "default"
    action: "escalate_to_higher"
```

## 撤回处理

### 撤回条件
```yaml
withdrawal_conditions:
  allowed:
    - before_approval
    - within_grace_period
    
  not_allowed:
    - after_approval
    - after_execution
    - critical_action
```

### 撤回流程
```yaml
withdrawal_flow:
  steps:
    - verify_withdrawable
    - cancel_approval_request
    - notify_approvers
    - record_withdrawal
```

## 版本变更处理

### 内容变更检测
```yaml
change_detection:
  monitored_fields:
    - action_params
    - target_recipients
    - content
    
  on_change:
    - invalidate_current_approval
    - require_new_approval
    - notify_requester
```

### 变更处理
```yaml
change_handling:
  minor_change:
    definition: "format_only"
    action: "update_and_continue"
    
  major_change:
    definition: "content_or_target_change"
    action: "require_new_approval"
```

## 审批记录

### 记录内容
```yaml
approval_record:
  request_id: "APPR-2024-001"
  
  decision:
    status: "approved"
    approver: "admin_001"
    decided_at: "2024-01-15T11:00:00Z"
    comments: "确认发送"
    
  execution:
    executed_at: "2024-01-15T11:05:00Z"
    result: "success"
    details: {...}
    
  audit:
    - event: "request_created"
      at: "2024-01-15T10:00:00Z"
    - event: "notification_sent"
      at: "2024-01-15T10:01:00Z"
    - event: "approved"
      at: "2024-01-15T11:00:00Z"
    - event: "executed"
      at: "2024-01-15T11:05:00Z"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 审批通过率 | 通过/总审批 | <80% |
| 平均审批时间 | 审批等待时长 | >2h |
| 超时率 | 超时/总审批 | >10% |
| 撤回率 | 撤回/总审批 | >5% |

## 维护方式
- 新增审批类型: 更新审批触发配置
- 调整规则: 更新审批规则
- 调整超时: 更新超时配置

## 引用文件
- `orchestration/INTEGRATION_REGISTRY.json` - 集成注册表
- `orchestration/ACTION_ORCHESTRATION.md` - 动作编排
- `governance/AUDIT_LOG.md` - 审计日志
