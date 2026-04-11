# SCHEDULED_REPORTS.md - 定时报表规则

## 目的
定义定时报表的生成、订阅、推送规则。

## 适用范围
平台所有周期性报表的自动生成和推送场景。

## 与其他模块联动
| 模块 | 联动内容 |
|------|----------|
| reporting | 报表生成 |
| audit | 报表审计 |
| events | 报表事件 |
| notification | 报表通知 |

## 报表周期

### 支持周期
| 周期 | 说明 | 生成时间 | 保留期限 |
|------|------|----------|----------|
| 每小时 | 实时监控 | 每小时整点 | 7天 |
| 每日 | 日常运营 | 每日06:00 | 30天 |
| 每周 | 周度汇总 | 每周一06:00 | 90天 |
| 每月 | 月度报告 | 每月1日06:00 | 365天 |
| 每季 | 季度报告 | 每季首日06:00 | 3年 |
| 每年 | 年度报告 | 每年1月1日06:00 | 7年 |

### 周期配置
```yaml
schedule_config:
  hourly:
    cron: "0 * * * *"
    retention_days: 7
    max_subscribers: 10
  
  daily:
    cron: "0 6 * * *"
    retention_days: 30
    max_subscribers: 50
  
  weekly:
    cron: "0 6 * * 1"
    retention_days: 90
    max_subscribers: 30
  
  monthly:
    cron: "0 6 1 * *"
    retention_days: 365
    max_subscribers: 20
  
  quarterly:
    cron: "0 6 1 1,4,7,10 *"
    retention_days: 1095
    max_subscribers: 10
  
  yearly:
    cron: "0 6 1 1 *"
    retention_days: 2555
    max_subscribers: 10
```

## 可订阅报表

### 报表类型
| 报表 | 周期 | 订阅权限 | 敏感级别 |
|------|------|----------|----------|
| 系统健康日报 | 每日 | 所有用户 | L0 |
| 性能监控日报 | 每日 | 运营人员 | L1 |
| 错误统计日报 | 每日 | 运营人员 | L1 |
| 使用量周报 | 每周 | 运营人员 | L1 |
| 成本分析月报 | 每月 | 财务人员 | L2 |
| 合规审计月报 | 每月 | 审计人员 | L2 |
| 安全事件周报 | 每周 | 安全人员 | L2 |
| 高管摘要月报 | 每月 | 管理层 | L2 |

### 订阅规则
```yaml
subscription_rules:
  system_health_daily:
    name: "系统健康日报"
    schedule: "daily"
    allowed_subscribers:
      - all_users
    max_per_tenant: 100
    auto_subscribe_new_users: false
  
  performance_daily:
    name: "性能监控日报"
    schedule: "daily"
    allowed_subscribers:
      - operator
      - manager
    max_per_tenant: 20
    requires_approval: false
  
  cost_monthly:
    name: "成本分析月报"
    schedule: "monthly"
    allowed_subscribers:
      - finance
      - admin
    max_per_tenant: 10
    requires_approval: true
  
  executive_monthly:
    name: "高管摘要月报"
    schedule: "monthly"
    allowed_subscribers:
      - executive
      - board
    max_per_tenant: 5
    requires_approval: true
```

## 订阅管理

### 订阅流程
```yaml
subscription_flow:
  steps:
    - name: "选择报表"
      actions:
        - browse_available_reports
        - check_subscription_permission
    
    - name: "配置订阅"
      actions:
        - select_schedule
        - choose_delivery_method
        - set_filters
    
    - name: "确认订阅"
      actions:
        - review_subscription
        - confirm_subscription
        - receive_confirmation
```

### 订阅记录
```json
{
  "subscription_id": "sub_001",
  "report_type": "performance_daily",
  "subscriber": "user_001",
  "subscriber_role": "operator",
  "tenant_id": "tenant_001",
  "schedule": "daily",
  "delivery_method": "email",
  "delivery_address": "user@example.com",
  "filters": {
    "modules": ["all"],
    "severity": ["warning", "error"]
  },
  "subscribed_at": "2026-04-01T00:00:00+08:00",
  "status": "active",
  "last_sent": "2026-04-06T06:00:00+08:00",
  "next_send": "2026-04-07T06:00:00+08:00"
}
```

## 推送方式

### 支持方式
| 方式 | 说明 | 适用场景 |
|------|------|----------|
| 邮件 | 发送到邮箱 | 标准报表 |
| 站内信 | 平台内通知 | 即时通知 |
| Webhook | 推送到URL | 系统集成 |
| API | 主动拉取 | 自动化系统 |

### 推送配置
```yaml
delivery_config:
  email:
    enabled: true
    max_size: 10MB
    formats: [pdf, csv]
    include_summary: true
  
  in_app:
    enabled: true
    retention: 7_days
    include_attachment: false
  
  webhook:
    enabled: true
    timeout: 30s
    retry: 3
    authentication: "bearer_token"
  
  api:
    enabled: true
    rate_limit: 100/hour
    authentication: "api_key"
```

## 失败重试

### 重试规则
```yaml
retry_rules:
  max_retries: 3
  retry_interval: 300
  
  retry_conditions:
    - network_error
    - timeout
    - server_error
  
  no_retry_conditions:
    - authentication_failed
    - permission_denied
    - invalid_format
  
  failure_notification:
    - notify_subscriber
    - notify_admin
    - log_failure
```

### 失败处理
```yaml
failure_handling:
  on_failure:
    - log_error
    - notify_subscriber
    - schedule_retry
  
  on_max_retries_exceeded:
    - mark_subscription_failed
    - notify_admin
    - disable_auto_retry
    - require_manual_intervention
```

## 敏感报表处理

### 敏感报表定义
| 条件 | 说明 |
|------|------|
| 数据级别L2+ | 包含敏感数据 |
| 跨租户数据 | 涉及多租户 |
| 财务数据 | 成本收益数据 |
| 合规数据 | 审计合规数据 |

### 敏感报表规则
```yaml
sensitive_report_rules:
  # 禁止自动发送
  auto_send:
    allowed: false
    reason: "敏感报表需人工确认"
  
  # 必须审批
  approval:
    required: true
    approver: "data_owner"
    validity: 24_hours
  
  # 推送限制
  delivery:
    allowed_methods: ["in_app", "api"]
    forbidden_methods: ["email", "webhook"]
  
  # 访问限制
  access:
    require_mfa: true
    log_access: true
    expire_link: 24_hours
```

## 报表生成

### 生成流程
```yaml
generation_flow:
  steps:
    - name: "触发生成"
      trigger: "schedule_or_manual"
      actions:
        - check_generation_permission
        - prepare_data_sources
    
    - name: "数据收集"
      actions:
        - query_data_sources
        - apply_filters
        - validate_data
    
    - name: "报表生成"
      actions:
        - apply_template
        - calculate_metrics
        - generate_charts
    
    - name: "质量检查"
      actions:
        - validate_completeness
        - check_accuracy
        - verify_format
    
    - name: "分发推送"
      actions:
        - prepare_delivery
        - send_notifications
        - store_archive
```

### 生成监控
```yaml
generation_monitoring:
  metrics:
    - generation_time
    - data_freshness
    - report_size
    - subscriber_count
  
  alerts:
    - condition: "generation_time > 30min"
      severity: "warning"
    
    - condition: "data_freshness > 24h"
      severity: "error"
    
    - condition: "generation_failed"
      severity: "critical"
```

## 报表存储

### 存储规则
| 周期 | 存储位置 | 格式 | 压缩 |
|------|----------|------|------|
| 每小时 | temp/ | JSON | 否 |
| 每日 | reports/daily/ | PDF+CSV | 是 |
| 每周 | reports/weekly/ | PDF+CSV | 是 |
| 每月 | reports/monthly/ | PDF+XLSX | 是 |
| 每季 | reports/quarterly/ | PDF | 是 |
| 每年 | reports/yearly/ | PDF | 是 |

### 清理规则
```yaml
cleanup_rules:
  hourly:
    retention: 7_days
    cleanup_schedule: "daily"
  
  daily:
    retention: 30_days
    cleanup_schedule: "weekly"
  
  weekly:
    retention: 90_days
    cleanup_schedule: "monthly"
  
  monthly:
    retention: 365_days
    cleanup_schedule: "quarterly"
```

## 引用文件
- `reporting/REPORT_SCHEMA.json` - 报表结构
- `reporting/EXPORT_POLICY.md` - 导出规则
- `reporting/EXECUTIVE_REPORTING.md` - 高管报表
- `audit/AUDIT_POLICY.md` - 审计策略
