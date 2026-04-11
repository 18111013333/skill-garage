# TASK_AUTOMATION.md - 任务自动化规范

## 目的
定义任务自动化的设计、执行和监控规范。

## 适用范围
所有可自动化的重复性任务。

## 任务分类

| 类型 | 频率 | 优先级 | 示例 |
|------|------|--------|------|
| 定时任务 | 固定周期 | 中 | 数据同步、报表生成 |
| 事件任务 | 事件触发 | 高 | 告警处理、自动扩容 |
| 批处理任务 | 批量执行 | 低 | 数据迁移、批量处理 |
| 工作流任务 | 流程驱动 | 中 | 审批流程、发布流程 |

## 任务设计

### 任务定义
```yaml
task:
  id: data_sync_001
  name: "用户数据同步"
  type: scheduled
  schedule: "0 2 * * *"  # 每日凌晨2点
  timeout: 3600
  retry:
    max: 3
    backoff: exponential
  steps:
    - name: extract
      action: db_query
      params:
        sql: "SELECT * FROM users WHERE updated_at > ?"
    - name: transform
      action: transform
      params:
        rules: user_transform_rules
    - name: load
      action: db_insert
      params:
        table: users_sync
        batch_size: 1000
```

### 依赖管理
```yaml
dependencies:
  tasks:
    - task: data_extract
      depends_on: []
    - task: data_transform
      depends_on: [data_extract]
    - task: data_load
      depends_on: [data_transform]
  failure_strategy: skip_dependent
```

## 调度配置

### 定时调度
| 调度类型 | 表达式 | 说明 |
|----------|--------|------|
| 固定时间 | 0 2 * * * | 每日2点 |
| 间隔执行 | */5 * * * * | 每5分钟 |
| 工作日 | 0 9 * * 1-5 | 工作日9点 |
| 月末 | 0 0 28-31 * * | 月末 |

### 事件调度
```yaml
event_trigger:
  source: message_queue
  topic: user_events
  consumer_group: task_processor
  batch_size: 100
  max_wait: 10s
```

## 执行控制

### 并发控制
```yaml
concurrency:
  max_parallel: 5
  queue_size: 100
  timeout: 3600
  rejection_policy: queue
```

### 重试策略
| 错误类型 | 重试次数 | 退避策略 | 最大间隔 |
|----------|----------|----------|----------|
| 网络错误 | 3 | 指数退避 | 60s |
| 超时错误 | 2 | 固定间隔 | 30s |
| 数据错误 | 0 | 不重试 | - |
| 资源限制 | 5 | 线性退避 | 300s |

### 幂等设计
```yaml
idempotency:
  enabled: true
  key: "${task_id}:${date}:${batch_id}"
  storage: redis
  ttl: 86400
```

## 监控告警

### 监控指标
| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 执行时间 | 任务耗时 | >预期2倍 |
| 成功率 | 成功/总数 | <95% |
| 队列积压 | 待执行数 | >100 |
| 资源使用 | CPU/内存 | >80% |

### 告警配置
```yaml
alerting:
  channels:
    - type: im
      level: [warning, error]
    - type: sms
      level: [critical]
  rules:
    - name: task_timeout
      condition: duration > timeout
      level: warning
    - name: task_failure
      condition: status == 'failed'
      level: error
    - name: queue_backlog
      condition: queue_size > 100
      level: warning
```

## 任务模板

### 数据同步模板
```yaml
template: data_sync
  params:
    source_db: required
    target_db: required
    table: required
    batch_size: default=1000
    incremental: default=true
  steps:
    - name: check_connection
      action: db_ping
    - name: get_checkpoint
      action: redis_get
    - name: extract_data
      action: db_query
    - name: transform_data
      action: transform
    - name: load_data
      action: db_insert
    - name: update_checkpoint
      action: redis_set
```

### 报表生成模板
```yaml
template: report_generation
  params:
    report_type: required
    date_range: required
    recipients: required
  steps:
    - name: query_data
      action: db_query
    - name: generate_report
      action: report_engine
    - name: send_email
      action: email_send
```

## 错误处理

### 错误分类
| 错误类型 | 处理方式 | 通知 |
|----------|----------|------|
| 临时错误 | 重试 | 否 |
| 永久错误 | 跳过+告警 | 是 |
| 资源错误 | 等待+重试 | 是 |
| 数据错误 | 记录+跳过 | 是 |

### 补偿机制
```yaml
compensation:
  enabled: true
  strategy: reverse
  steps:
    - name: cleanup_temp_data
      action: delete
    - name: restore_checkpoint
      action: restore
```

## 维护方式
- 新增任务: 创建任务定义
- 调整调度: 更新调度配置
- 新增模板: 创建任务模板

## 引用文件
- `runtime/EXECUTION_POLICY.md` - 执行策略
- `optimization/BATCH_PROCESS.md` - 批处理优化
