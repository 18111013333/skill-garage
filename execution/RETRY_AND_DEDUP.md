# RETRY_AND_DEDUP.md - 重试与去重规则

## 目的
解决事件重复与失败重试问题，确保事件系统稳定。

## 适用范围
所有事件的重试和去重处理。

## 重试策略

### 重试分类
| 类型 | 说明 | 最大重试 | 重试间隔 |
|------|------|----------|----------|
| 短暂失败 | 临时性错误 | 3次 | 指数退避 |
| 资源限制 | 资源不足 | 2次 | 固定间隔 |
| 超时 | 处理超时 | 2次 | 固定间隔 |
| 永久失败 | 不可恢复 | 0次 | 终止 |

### 重试配置
```yaml
retry_policy:
  transient_failure:
    max_retries: 3
    initial_delay_ms: 1000
    backoff_multiplier: 2
    max_delay_ms: 30000
    jitter: true
  
  resource_limit:
    max_retries: 2
    delay_ms: 5000
    backoff: none
  
  timeout:
    max_retries: 2
    delay_ms: 10000
    backoff: none
  
  permanent_failure:
    max_retries: 0
    action: "dead_letter"
```

### 重试流程
```
事件处理失败
    ↓
┌─────────────────────────────────────┐
│ 1. 分析失败原因                      │
│    - 短暂失败                        │
│    - 资源限制                        │
│    - 超时                            │
│    - 永久失败                        │
└─────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 判断是否可重试                    │
│    - 检查重试次数                    │
│    - 检查失败类型                    │
└─────────────────────────────────────┘
    │
    ├─ 可重试 → 计算延迟
    │           ↓
    │           等待后重试
    │
    └─ 不可重试 → 发送到死信队列
```

### 退避算法
```yaml
backoff_algorithm:
  exponential:
    formula: "delay = min(initial * multiplier^retry_count, max_delay)"
    example:
      - retry_1: 1000ms
      - retry_2: 2000ms
      - retry_3: 4000ms
  
  linear:
    formula: "delay = initial + (retry_count * step)"
    example:
      - retry_1: 1000ms
      - retry_2: 1500ms
      - retry_3: 2000ms
  
  fixed:
    formula: "delay = constant"
    example:
      - retry_1: 5000ms
      - retry_2: 5000ms
      - retry_3: 5000ms
```

## 去重策略

### 去重方法
| 方法 | 说明 | 精确度 | 性能 |
|------|------|--------|------|
| ID去重 | 基于事件ID | 100% | 高 |
| 哈希去重 | 基于内容哈希 | 99% | 高 |
| 幂等键去重 | 基于业务键 | 100% | 中 |
| 时间窗口去重 | 时间窗口内去重 | 95% | 中 |

### 去重配置
```yaml
dedup_config:
  methods:
    - type: "event_id"
      enabled: true
      ttl_seconds: 86400
      storage: "redis"
    
    - type: "content_hash"
      enabled: true
      ttl_seconds: 3600
      storage: "redis"
    
    - type: "idempotency_key"
      enabled: true
      ttl_seconds: 604800
      storage: "database"
  
  window:
    size_seconds: 300
    max_events: 10000
```

### 去重流程
```
事件到达
    ↓
┌─────────────────────────────────────┐
│ 1. 提取去重键                        │
│    - event_id                        │
│    - content_hash                    │
│    - idempotency_key                 │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 检查是否重复                      │
│    - 查询去重存储                    │
│    - 比较时间窗口                    │
└─────────────────────────────────────┘
    │
    ├─ 重复 → 丢弃 + 记录
    │
    └─ 不重复 → 记录去重键
                ↓
                继续处理
```

## 幂等约束

### 幂等要求
| 操作类型 | 幂等要求 | 实现方式 |
|----------|----------|----------|
| 创建操作 | 必须幂等 | 唯一键检查 |
| 更新操作 | 必须幂等 | 版本号/时间戳 |
| 删除操作 | 必须幂等 | 状态检查 |
| 查询操作 | 天然幂等 | 无需处理 |

### 幂等实现
```yaml
idempotency:
  create:
    method: "unique_key"
    key_fields: ["tenant_id", "source", "event_type", "payload_hash"]
    on_duplicate: "skip"
  
  update:
    method: "version"
    version_field: "version"
    on_conflict: "skip"
  
  delete:
    method: "state_check"
    check_field: "status"
    on_not_found: "skip"
```

## 顺序敏感事件

### 顺序要求
| 事件类型 | 顺序要求 | 说明 |
|----------|----------|------|
| 状态变更 | 严格顺序 | 状态机依赖 |
| 审批流程 | 严格顺序 | 审批链依赖 |
| 数据更新 | 严格顺序 | 数据一致性 |
| 通知发送 | 宽松顺序 | 可容忍乱序 |
| 日志记录 | 无顺序 | 独立事件 |

### 顺序保证
```yaml
ordering:
  strict:
    enabled: true
    event_types: ["state_change", "approval", "data_update"]
    
    implementation:
      method: "partition_queue"
      partition_key: "correlation_id"
      max_in_flight: 1
  
  loose:
    enabled: true
    event_types: ["notification", "log"]
    
    implementation:
      method: "timestamp_order"
      tolerance_ms: 1000
```

### 排队策略
```yaml
queue_strategy:
  strict_order:
    queue_type: "fifo"
    partition_by: "correlation_id"
    max_parallel: 1
  
  loose_order:
    queue_type: "standard"
    batch_size: 10
    max_parallel: 5
```

## Correlation ID

### ID生成规则
```yaml
correlation_id:
  generation:
    source: "event"
    fields: ["source", "event_type", "timestamp", "random"]
    format: "{source}_{event_type}_{timestamp}_{random}"
  
  propagation:
    enabled: true
    header: "X-Correlation-ID"
    log: true
```

### ID用途
| 用途 | 说明 |
|------|------|
| 事件追踪 | 追踪事件处理链 |
| 去重判断 | 辅助去重 |
| 顺序保证 | 分区键 |
| 审计关联 | 关联相关事件 |

## 监控指标

### 重试监控
| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 重试率 | 重试/总数 | > 5% |
| 平均重试次数 | 平均重试数 | > 2 |
| 重试延迟 | 重试等待时间 | > 30s |
| 最终失败率 | 最终失败/总数 | > 1% |

### 去重监控
| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 去重率 | 去重/总数 | > 10% |
| 去重存储 | 存储使用率 | > 80% |
| 去重延迟 | 去重检查耗时 | > 10ms |

## 异常处理

| 异常 | 处理 |
|------|------|
| 重试耗尽 | 发送到死信队列 |
| 去重存储失败 | 放行 + 告警 |
| 顺序冲突 | 重新排队 |
| 幂等检查失败 | 记录 + 放行 |

## 完成标准

- [x] 重试策略完整
- [x] 去重策略完整
- [x] 幂等约束明确
- [x] 顺序保证清晰
- [x] 监控指标完整

## 引用文件
- `events/EVENT_SCHEMA.json` - 事件结构
- `events/TRIGGER_POLICY.md` - 触发策略
- `events/EVENT_ROUTING.md` - 事件路由
