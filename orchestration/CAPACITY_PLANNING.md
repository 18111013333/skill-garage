# CAPACITY_PLANNING.md - 容量规划规则

## 目的
定义容量规划规则，确保高负载时系统不会失控。

## 适用范围
所有资源的容量规划和负载管理。

## 容量维度

| 维度 | 说明 | 监控指标 | 告警阈值 |
|------|------|----------|----------|
| 峰值任务 | 任务并发峰值 | concurrent_tasks | >80%容量 |
| 长任务积压 | 长任务排队 | queue_depth | >100 |
| 模型调用峰值 | API调用峰值 | calls_per_minute | >限值80% |
| 工具额度峰值 | 工具使用峰值 | quota_usage | >90% |
| 校验资源峰值 | 校验负载 | validation_queue | >50 |

## 容量评估

### 当前容量评估
```javascript
function assessCurrentCapacity() {
  const resources = getAllResources();
  const usage = getCurrentUsage();
  
  const assessment = {};
  for (const resource of resources) {
    assessment[resource.type] = {
      total: resource.capacity.total,
      used: usage[resource.type] || 0,
      available: resource.capacity.total - (usage[resource.type] || 0),
      utilization: (usage[resource.type] / resource.capacity.total) * 100
    };
  }
  
  return assessment;
}
```

### 峰值预测
```yaml
peak_prediction:
  methods:
    - historical_pattern:
        lookback: "30d"
        pattern_detection: true
        
    - scheduled_events:
        calendar_integration: true
        event_impact_estimation: true
        
    - trend_analysis:
        growth_rate: true
        seasonality: true
        
  forecast_horizon: "7d"
  confidence_interval: 0.95
```

## 扩容策略

### 自动扩容
```yaml
auto_scaling:
  triggers:
    - utilization > 80% for 5m
    - queue_depth > threshold
    - response_time > SLA
    
  actions:
    - request_additional_resources
    - enable_burst_capacity
    - activate_backup_resources
    
  limits:
    max_scale_factor: 2.0
    min_scale_interval: "5m"
```

### 手动扩容
```yaml
manual_scaling:
  request_process:
    - submit_capacity_request
    - approval_by_admin
    - resource_allocation
    - capacity_update
    
  lead_time: "24h"
```

## 削峰策略

### 请求削峰
```yaml
request_shaping:
  techniques:
    - rate_limiting:
        algorithm: "token_bucket"
        burst_allowance: 1.2
        
    - queueing:
        priority_queue: true
        max_wait_time: "30m"
        
    - throttling:
        gradual: true
        min_rate: 0.5
        
  triggers:
    - utilization > 85%
    - error_rate > 2%
```

### 任务削峰
```yaml
task_shaping:
  techniques:
    - batch_scheduling:
        batch_size: 100
        interval: "5m"
        
    - deferred_execution:
        defer_low_priority: true
        max_defer_time: "1h"
        
    - load_spreading:
        spread_over_time: true
        target_utilization: 70%
```

## 排队策略

### 优先级队列
```yaml
priority_queue:
  levels:
    - level: "critical"
      preempt: true
      max_wait: "0s"
      
    - level: "high"
      preempt: true
      max_wait: "5m"
      
    - level: "normal"
      preempt: false
      max_wait: "30m"
      
    - level: "low"
      preempt: false
      max_wait: "2h"
```

### 公平调度
```yaml
fair_scheduling:
  enabled: true
  principles:
    - 每个项目公平份额
    - 防止资源垄断
    - 保障最低服务
    
  implementation:
    - weighted_fair_queue
    - project_quotas
```

## 降级策略

### 降级触发
```yaml
degradation_triggers:
  - utilization > 95%
  - error_rate > 5%
  - queue_overflow
  - resource_exhaustion
```

### 降级措施
```yaml
degradation_measures:
  level_1:  # 轻度降级
    - reduce_validation_depth
    - shorten_context_window
    - defer_non_critical
    
  level_2:  # 中度降级
    - use_lighter_models
    - reduce_output_detail
    - queue_low_priority
    
  level_3:  # 重度降级
    - minimal_validation
    - essential_features_only
    - pause_low_priority_projects
```

## 容量监控

### 实时监控
```yaml
real_time_monitoring:
  metrics:
    - resource_utilization
    - queue_depth
    - response_time
    - error_rate
    
  update_interval: "10s"
  dashboard: true
```

### 容量告警
```yaml
capacity_alerts:
  - condition: "utilization > 80%"
    level: "warning"
    action: "prepare_scaling"
    
  - condition: "utilization > 90%"
    level: "critical"
    action: "auto_scale_or_degrade"
    
  - condition: "utilization > 95%"
    level: "emergency"
    action: "emergency_degradation"
```

## 容量规划报告

### 报告内容
```yaml
capacity_report:
  current_status:
    - resource_utilization
    - queue_status
    - performance_metrics
    
  forecast:
    - 7d_peak_prediction
    - resource_needs
    - bottleneck_analysis
    
  recommendations:
    - scaling_suggestions
    - optimization_opportunities
    - risk_alerts
```

### 报告频率
```yaml
report_frequency:
  daily_summary: true
  weekly_analysis: true
  monthly_planning: true
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 容量利用率 | 已用/总容量 | >85% |
| 扩容成功率 | 成功/请求 | <90% |
| 降级触发次数 | 降级次数 | >3/天 |
| 队列溢出次数 | 溢出次数 | >0 |

## 维护方式
- 调整阈值: 更新告警阈值
- 新增策略: 创建削峰/降级策略
- 优化预测: 更新预测模型

## 引用文件
- `resources/RESOURCE_SCHEMA.json` - 资源结构
- `resources/ALLOCATION_POLICY.md` - 分配策略
- `resources/DEGRADATION_POLICY.md` - 降级策略
