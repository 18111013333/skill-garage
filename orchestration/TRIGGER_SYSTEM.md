# TRIGGER_SYSTEM.md - 触发器系统规范

## 目的
定义触发器的设计、配置和执行规范。

## 适用范围
所有事件驱动的自动化场景。

## 触发器类型

| 类型 | 触发源 | 延迟 | 适用场景 |
|------|--------|------|----------|
| 时间触发 | 定时器 | 无 | 定时任务 |
| 事件触发 | 事件总线 | 毫秒级 | 实时响应 |
| 数据触发 | 数据变更 | 秒级 | 数据同步 |
| API触发 | API调用 | 毫秒级 | 外部集成 |
| 条件触发 | 条件检测 | 秒级 | 阈值告警 |

## 触发器配置

### 时间触发器
```yaml
trigger:
  id: daily_cleanup
  type: schedule
  schedule: "0 3 * * *"
  timezone: "Asia/Shanghai"
  action:
    type: workflow
    id: cleanup_workflow
  enabled: true
```

### 事件触发器
```yaml
trigger:
  id: user_created
  type: event
  source: user_events
  filter:
    event_type: user.created
  action:
    type: workflow
    id: onboarding_workflow
    params:
      user_id: "${event.data.user_id}"
```

### 数据触发器
```yaml
trigger:
  id: order_status_change
  type: database
  source: orders
  watch:
    - field: status
      operation: update
  action:
    type: workflow
    id: order_notification
```

### 条件触发器
```yaml
trigger:
  id: high_cpu_alert
  type: condition
  condition:
    metric: cpu_usage
    operator: ">"
    value: 80
    duration: 60s
  action:
    type: workflow
    id: auto_scale
```

## 触发规则

### 规则定义
```yaml
rules:
  - id: rule_001
    name: "用户注册触发"
    conditions:
      - type: event
        source: user_events
        pattern: "user.created"
      - type: filter
        expression: "event.data.source == 'web'"
    actions:
      - type: workflow
        id: welcome_workflow
      - type: notification
        channel: slack
        message: "新用户注册: ${event.data.user_id}"
```

### 规则优先级
| 优先级 | 说明 | 执行顺序 |
|--------|------|----------|
| P0 | 紧急 | 立即执行 |
| P1 | 高 | 优先执行 |
| P2 | 中 | 正常执行 |
| P3 | 低 | 延迟执行 |

## 触发执行

### 执行流程
```
触发事件
    ↓
┌─────────────────────────────────────┐
│ 1. 事件匹配                          │
│    - 匹配触发器规则                  │
│    - 过滤条件检查                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 动作执行                          │
│    - 执行关联动作                    │
│    - 记录执行日志                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 结果处理                          │
│    - 成功/失败处理                   │
│    - 触发后续事件                    │
└─────────────────────────────────────┘
```

### 执行控制
```yaml
execution:
  timeout: 300
  retry:
    max: 3
    backoff: exponential
  rate_limit:
    max_per_second: 100
  concurrency:
    max: 50
```

## 事件总线

### 事件格式
```json
{
  "id": "evt_001",
  "type": "user.created",
  "source": "user_service",
  "time": "2024-01-01T00:00:00Z",
  "data": {
    "user_id": "user_001",
    "email": "user@example.com"
  },
  "metadata": {
    "correlation_id": "corr_001",
    "trace_id": "trace_001"
  }
}
```

### 事件路由
```yaml
routing:
  topics:
    - name: user_events
      subscriptions:
        - trigger: user_created
        - trigger: user_updated
    - name: order_events
      subscriptions:
        - trigger: order_created
        - trigger: order_updated
```

## 去重机制

### 去重策略
| 策略 | 说明 | 适用场景 |
|------|------|----------|
| 事件ID去重 | 基于事件ID | 通用 |
| 幂等键去重 | 基于业务键 | 业务场景 |
| 时间窗口去重 | 窗口内去重 | 高频事件 |

### 去重配置
```yaml
deduplication:
  enabled: true
  strategy: event_id
  storage: redis
  ttl: 3600
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 触发延迟 | 事件到执行时间 | >1s |
| 执行成功率 | 成功/总数 | <95% |
| 规则匹配率 | 匹配/总数 | 异常波动 |
| 队列积压 | 待处理事件 | >1000 |

## 维护方式
- 新增触发器: 创建触发器配置
- 新增规则: 创建触发规则
- 调整配置: 更新执行控制

## 引用文件
- `automation/WORKFLOW_ENGINE.md` - 工作流引擎
- `automation/SCHEDULE_MANAGER.md` - 调度管理
