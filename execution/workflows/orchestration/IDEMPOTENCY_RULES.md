# IDEMPOTENCY_RULES.md - 幂等规则

## 目的
定义幂等规则，防止重复执行造成外部世界重复操作。

## 适用范围
所有外部系统操作的幂等控制。

## 幂等原则

1. **每个动作有唯一幂等键**
2. **重复请求返回相同结果**
3. **不产生副作用重复执行**
4. **幂等键有合理有效期**

## 幂等键策略

### 幂等键生成
```yaml
idempotency_key_generation:
  strategies:
    - client_provided:
        description: "客户端提供幂等键"
        format: "client_{client_id}_{request_id}"
        
    - system_generated:
        description: "系统生成幂等键"
        format: "sys_{timestamp}_{random}"
        
    - content_hash:
        description: "基于内容哈希"
        format: "hash_{sha256(action_params)}"
        
  composition:
    - default: "{integration_id}_{action_type}_{content_hash}"
```

### 幂等键示例
```yaml
examples:
  - action: "send_email"
    key: "INT-email-001_send_email_hash_abc123"
    
  - action: "create_document"
    key: "INT-docs-001_create_document_hash_def456"
    
  - action: "calendar_event"
    key: "INT-calendar-001_create_event_hash_ghi789"
```

## 幂等检测

### 检测流程
```
请求到达
    ↓
┌─────────────────────────────────────┐
│ 1. 提取幂等键                        │
│    - 从请求头提取                    │
│    - 或生成幂等键                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 查询幂等记录                      │
│    - 检查键是否存在                  │
│    - 检查是否在有效期内              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 判断处理方式                      │
│    - 存在且成功 → 返回缓存结果       │
│    - 存在且处理中 → 等待或返回状态   │
│    - 存在但失败 → 允许重试           │
│    - 不存在 → 执行新请求             │
└─────────────────────────────────────┘
```

### 检测实现
```javascript
async function checkIdempotency(idempotencyKey) {
  const record = await getIdempotencyRecord(idempotencyKey);
  
  if (!record) {
    // 新请求，创建记录
    await createIdempotencyRecord(idempotencyKey, 'processing');
    return { shouldExecute: true };
  }
  
  if (record.status === 'success') {
    // 已成功，返回缓存结果
    return { 
      shouldExecute: false, 
      cachedResult: record.result 
    };
  }
  
  if (record.status === 'processing') {
    // 处理中，等待或返回状态
    return { 
      shouldExecute: false, 
      status: 'processing' 
    };
  }
  
  if (record.status === 'failed') {
    // 失败，允许重试
    if (canRetry(record)) {
      await updateIdempotencyRecord(idempotencyKey, 'processing');
      return { shouldExecute: true };
    }
    return { shouldExecute: false, error: record.error };
  }
}
```

## 重试规则

### 重试条件
```yaml
retry_conditions:
  allowed:
    - previous_failed: true
    - within_retry_window: true
    - retry_count < max_retries
    
  not_allowed:
    - previous_success: true
    - expired: true
    - max_retries_reached: true
```

### 重试配置
```yaml
retry_config:
  max_retries: 3
  backoff:
    strategy: exponential
    initial_delay: 1s
    max_delay: 60s
    
  retry_window:
    duration: 24h
    after: "first_attempt_time"
```

## 重复检测窗口

### 窗口配置
```yaml
detection_window:
  by_action_type:
    send_email: 24h
    create_document: 7d
    update_record: 1h
    delete: 30d
    
  default: 24h
  
  expiry_action: "archive"
```

### 窗口处理
```yaml
window_handling:
  within_window:
    - 检测到重复 → 返回原结果
    
  outside_window:
    - 视为新请求
    - 归档旧记录
    - 创建新记录
```

## 幂等记录

### 记录结构
```yaml
idempotency_record:
  key: "INT-email-001_send_email_hash_abc123"
  
  request:
    action: "send_email"
    integration: "INT-email-001"
    params: {...}
    
  response:
    status: "success"
    result: {...}
    
  timing:
    created_at: "2024-01-15T10:00:00Z"
    completed_at: "2024-01-15T10:00:05Z"
    expires_at: "2024-01-16T10:00:00Z"
    
  retry:
    count: 0
    last_retry: null
```

### 记录存储
```yaml
storage:
  type: "database"
  table: "idempotency_records"
  indexes:
    - key
    - created_at
    - expires_at
    
  cleanup:
    frequency: "daily"
    action: "archive_expired"
```

## 特殊场景

### 批量操作幂等
```yaml
batch_idempotency:
  key_strategy: "batch_{batch_id}_{item_index}"
  
  handling:
    - 部分成功: "记录每项状态"
    - 重试: "仅重试失败项"
```

### 长时间操作幂等
```yaml
long_operation_idempotency:
  polling:
    enabled: true
    interval: 10s
    
  status_update:
    - 更新处理状态
    - 允许状态查询
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 重复请求率 | 重复/总请求 | >10% |
| 幂等命中率 | 命中/检测 | <50% |
| 重试成功率 | 成功/重试 | <80% |
| 记录清理率 | 清理/过期 | <90% |

## 维护方式
- 新增策略: 创建幂等键策略
- 调整窗口: 更新检测窗口
- 调整重试: 更新重试配置

## 引用文件
- `orchestration/INTEGRATION_REGISTRY.json` - 集成注册表
- `orchestration/ACTION_ORCHESTRATION.md` - 动作编排
- `orchestration/TRANSACTION_POLICY.md` - 事务策略
