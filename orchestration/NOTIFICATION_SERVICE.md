# NOTIFICATION_SERVICE.md - 通知服务规范

## 目的
定义通知的发送、管理和追踪规范。

## 适用范围
所有通知发送场景，包括邮件、短信、IM、推送。

## 通知渠道

| 渠道 | 延迟 | 到达率 | 适用场景 |
|------|------|--------|----------|
| 邮件 | 秒级 | 高 | 正式通知 |
| 短信 | 秒级 | 高 | 紧急通知 |
| IM | 毫秒级 | 高 | 即时通知 |
| 推送 | 秒级 | 中 | 移动通知 |
| 站内信 | 毫秒级 | 高 | 系统通知 |

## 通知类型

| 类型 | 优先级 | 渠道 | 模板 |
|------|--------|------|------|
| 告警通知 | P0 | 短信+IM | alert_template |
| 审批通知 | P1 | IM+邮件 | approval_template |
| 任务通知 | P2 | IM | task_template |
| 营销通知 | P3 | 邮件 | marketing_template |

## 通知配置

### 模板定义
```yaml
template:
  id: alert_template
  name: "告警通知模板"
  channels:
    - sms
    - im
  content:
    sms: "【告警】${service}服务异常，请及时处理。详情: ${detail}"
    im:
      title: "🚨 服务告警"
      content: |
        服务: ${service}
        级别: ${level}
        详情: ${detail}
        时间: ${time}
  variables:
    - service
    - level
    - detail
    - time
```

### 发送规则
```yaml
sending_rules:
  - id: alert_rule
    type: alert
    channels:
      - sms
      - im
    conditions:
      - level: P0
        channels: [sms, im, call]
      - level: P1
        channels: [sms, im]
      - level: P2
        channels: [im]
    rate_limit:
      per_user: 10/hour
      per_type: 100/minute
```

## 发送流程

### 标准流程
```
通知请求
    ↓
┌─────────────────────────────────────┐
│ 1. 请求验证                          │
│    - 参数校验                        │
│    - 权限检查                        │
│    - 频率限制                        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 模板渲染                          │
│    - 选择模板                        │
│    - 变量替换                        │
│    - 内容生成                        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 渠道发送                          │
│    - 选择渠道                        │
│    - 调用发送接口                    │
│    - 记录发送状态                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 状态追踪                          │
│    - 更新发送状态                    │
│    - 处理回执                        │
│    - 重试失败                        │
└─────────────────────────────────────┘
```

### 重试策略
```yaml
retry:
  max_attempts: 3
  backoff: exponential
  initial_delay: 10s
  max_delay: 300s
  retry_on:
    - timeout
    - rate_limit
    - service_unavailable
```

## 批量发送

### 批量配置
```yaml
batch_sending:
  batch_size: 100
  concurrency: 10
  rate_limit:
    per_batch: 1000/minute
  deduplication:
    enabled: true
    window: 1h
```

### 批量模板
```yaml
batch_template:
  id: batch_notification
  merge_fields:
    - user_name
    - content
  chunk_size: 50
```

## 通知追踪

### 状态管理
| 状态 | 说明 | 后续动作 |
|------|------|----------|
| pending | 待发送 | 发送 |
| sent | 已发送 | 等待回执 |
| delivered | 已送达 | 完成 |
| read | 已读 | 完成 |
| failed | 发送失败 | 重试/告警 |

### 追踪记录
```yaml
tracking:
  enabled: true
  retention: 30d
  fields:
    - notification_id
    - user_id
    - channel
    - status
    - sent_time
    - delivered_time
    - read_time
```

## 通知聚合

### 聚合策略
```yaml
aggregation:
  enabled: true
  window: 5m
  group_by:
    - user_id
    - type
  max_count: 10
  template: aggregated_notification
```

### 聚合示例
```
【聚合通知】
您有 5 条告警通知:
1. CPU使用率超过80%
2. 内存使用率超过85%
3. 磁盘空间不足
4. 服务响应超时
5. 错误率上升
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 发送成功率 | 成功/总数 | <95% |
| 发送延迟 | 请求到发送 | >10s |
| 到达率 | 送达/发送 | <90% |
| 队列积压 | 待发送数 | >1000 |

## 权限管理

### 权限配置
```yaml
permissions:
  roles:
    - name: admin
      channels: [all]
      types: [all]
    - name: operator
      channels: [im, email]
      types: [alert, task]
    - name: user
      channels: [im, email]
      types: [notification]
```

## 维护方式
- 新增渠道: 更新渠道配置
- 新增模板: 创建通知模板
- 调整规则: 更新发送规则

## 引用文件
- `automation/TRIGGER_SYSTEM.md` - 触发器系统
- `governance/AUDIT_LOG.md` - 审计日志
