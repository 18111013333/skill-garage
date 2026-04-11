# TRANSACTION_POLICY.md - 跨系统事务性策略

## 目的
定义跨系统事务性策略，确保失败后有补偿逻辑。

## 适用范围
所有跨多个外部系统的事务性操作。

## 事务类型

| 类型 | 说明 | 回滚能力 | 示例 |
|------|------|----------|------|
| 可完全回滚 | 所有操作可撤销 | 完全回滚 | 文档创建+发送 |
| 部分补偿 | 部分操作可补偿 | 补偿动作 | 邮件发送+日程创建 |
| 不可回滚 | 操作不可撤销 | 补救措施 | 外部支付 |

## 事务定义

### 事务结构
```yaml
transaction:
  transaction_id: "TXN-2024-001"
  name: "报告发布事务"
  
  operations:
    - operation_id: "OP-001"
      name: "创建文档"
      system: "INT-docs-001"
      action: "create_document"
      params: {...}
      rollback_action: "delete_document"
      rollback_params:
        document_id: "${OP-001.result.document_id}"
      compensation_supported: true
      
    - operation_id: "OP-002"
      name: "发送邮件"
      system: "INT-email-001"
      action: "send_email"
      params:
        attachment: "${OP-001.result.document_id}"
      rollback_action: "none"  # 邮件无法撤回
      compensation_supported: false
      compensation_action: "send_correction_email"
      
    - operation_id: "OP-003"
      name: "创建日程"
      system: "INT-calendar-001"
      action: "create_event"
      params: {...}
      rollback_action: "delete_event"
      compensation_supported: true
```

## 事务执行

### 执行流程
```
事务开始
    ↓
┌─────────────────────────────────────┐
│ 1. 记录事务开始                      │
│    - 创建事务记录                    │
│    - 设置超时                        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 顺序执行操作                      │
│    - 执行每个操作                    │
│    - 记录操作结果                    │
│    - 检测失败                        │
└─────────────────────────────────────┘
    ↓
    ├─ 全部成功 → 提交事务
    │
    └─ 部分失败 → 触发补偿
```

### 执行实现
```javascript
async function executeTransaction(transaction) {
  const executedOps = [];
  
  try {
    for (const op of transaction.operations) {
      const result = await executeOperation(op);
      executedOps.push({ op, result });
      
      if (!result.success) {
        // 执行失败，触发补偿
        await compensate(executedOps);
        throw new TransactionError(op.operation_id, result.error);
      }
    }
    
    // 全部成功，提交事务
    await commitTransaction(transaction);
    return { success: true };
    
  } catch (error) {
    await recordTransactionFailure(transaction, error);
    return { success: false, error };
  }
}
```

## 补偿机制

### 补偿流程
```yaml
compensation_flow:
  trigger: "operation_failure"
  
  steps:
    - name: "识别已执行操作"
      action: "list_executed_operations"
      
    - name: "逆序执行补偿"
      action: "execute_compensation_in_reverse"
      
    - name: "记录补偿结果"
      action: "record_compensation"
      
    - name: "通知相关方"
      action: "notify_compensation"
```

### 补偿实现
```javascript
async function compensate(executedOps) {
  // 逆序执行补偿
  for (let i = executedOps.length - 1; i >= 0; i--) {
    const { op, result } = executedOps[i];
    
    if (op.compensation_supported && op.rollback_action !== 'none') {
      try {
        await executeRollback(op, result);
      } catch (rollbackError) {
        // 回滚失败，执行补偿动作
        if (op.compensation_action) {
          await executeCompensation(op, result);
        }
        // 记录补偿失败
        await recordCompensationFailure(op, rollbackError);
      }
    } else if (op.compensation_action) {
      // 不支持回滚，执行补偿动作
      await executeCompensation(op, result);
    }
  }
}
```

## 补偿动作

### 回滚动作
```yaml
rollback_actions:
  delete_document:
    description: "删除创建的文档"
    params:
      document_id: "${operation.result.document_id}"
      
  delete_event:
    description: "删除创建的日程"
    params:
      event_id: "${operation.result.event_id}"
      
  cancel_notification:
    description: "取消通知"
    params:
      notification_id: "${operation.result.notification_id}"
```

### 补偿动作
```yaml
compensation_actions:
  send_correction_email:
    description: "发送更正邮件"
    trigger: "邮件已发送但事务失败"
    params:
      to: "${original_params.to}"
      subject: "更正：之前的邮件内容有误"
      content: "请忽略之前的邮件..."
      
  send_apology:
    description: "发送致歉通知"
    trigger: "操作失败且无法回滚"
    
  manual_intervention:
    description: "标记需人工处理"
    trigger: "补偿失败"
```

## 事务状态

### 状态定义
```yaml
transaction_states:
  - pending: "待执行"
  - running: "执行中"
  - committed: "已提交"
  - compensating: "补偿中"
  - compensated: "已补偿"
  - failed: "失败"
  - partial_failure: "部分失败"
```

### 状态转换
```yaml
state_transitions:
  pending → running: "开始执行"
  running → committed: "全部成功"
  running → compensating: "检测到失败"
  compensating → compensated: "补偿完成"
  compensating → partial_failure: "补偿失败"
  running → failed: "执行失败"
```

## 告警与通知

### 告警触发
```yaml
alert_triggers:
  - transaction_failure:
      level: high
      notify: ["admin", "requester"]
      
  - compensation_failure:
      level: critical
      notify: ["admin"]
      escalate: true
      
  - partial_failure:
      level: high
      notify: ["admin"]
```

### 通知内容
```yaml
notification_content:
  - transaction_id
  - failed_operation
  - failure_reason
  - compensation_status
  - required_actions
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 事务成功率 | 成功/总数 | <90% |
| 补偿成功率 | 成功/补偿 | <95% |
| 平均事务时长 | 事务耗时 | >预期2倍 |
| 部分失败率 | 部分失败/总数 | >5% |

## 维护方式
- 新增事务类型: 创建事务定义
- 新增补偿动作: 创建补偿动作
- 调整流程: 更新执行流程

## 引用文件
- `orchestration/INTEGRATION_REGISTRY.json` - 集成注册表
- `orchestration/ACTION_ORCHESTRATION.md` - 动作编排
- `orchestration/IDEMPOTENCY_RULES.md` - 幂等规则
