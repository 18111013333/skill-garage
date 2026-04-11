# ERROR_BUDGET_POLICY.md - 错误预算规则

## 目的
定义错误预算规则，确保系统退化时知道什么时候必须"收手"。

## 适用范围
- 错误预算计算
- 预算消耗监控
- 预算耗尽处理
- 恢复机制

## 核心规则

### 1. 错误预算计算

```yaml
budget_calculation:
  # 计算公式
  formula: "error_budget = (1 - SLO_target) * measurement_window"
  
  # 示例
  example:
    SLO_target: 99.9%
    measurement_window: "30 days"
    total_minutes: 43200  # 30 * 24 * 60
    error_budget: 43.2 minutes  # (1 - 0.999) * 43200
  
  # 预算周期
  budget_period:
    default: "30 days"
    options: ["7 days", "30 days", "90 days"]
  
  # 预算分配
  allocation:
    system_errors: 60%
    planned_maintenance: 30%
    external_dependencies: 10%
```

### 2. 计入预算的失败

```yaml
budget_consumption:
  # 计入预算
  included:
    - 服务不可用
    - 响应超时
    - 错误响应 (5xx)
    - 功能失效
    - 数据丢失
  
  # 不计入预算
  excluded:
    - 计划维护窗口
    - 第三方服务故障
    - 用户配置错误
    - 不可抗力
    - Beta 功能故障
  
  # 部分计入
  partial:
    - 部分功能降级: 50%
    - 性能低于 SLO: 25%
    - 非关键路径故障: 10%
```

### 3. 预算消耗监控

```yaml
budget_monitoring:
  # 实时监控
  realtime:
    metrics:
      - consumed_budget_percent
      - remaining_budget_minutes
      - burn_rate
    
    update_frequency: "1 minute"
  
  # 燃烧率告警
  burn_rate_alerts:
    - burn_rate: 2x
      severity: "warning"
      message: "预算消耗速度是正常的 2 倍"
    
    - burn_rate: 5x
      severity: "critical"
      message: "预算消耗速度是正常的 5 倍"
    
    - burn_rate: 10x
      severity: "emergency"
      message: "预算即将耗尽"
  
  # 预算阈值告警
  threshold_alerts:
    - threshold: 50%
      severity: "info"
      action: "记录并观察"
    
    - threshold: 75%
      severity: "warning"
      action: "通知团队"
    
    - threshold: 90%
      severity: "critical"
      action: "触发限制措施"
    
    - threshold: 100%
      severity: "emergency"
      action: "暂停高风险操作"
```

### 4. 预算耗尽触发限制

```yaml
budget_exhaustion_limits:
  # 立即触发
  immediate:
    - 暂停所有非紧急变更发布
    - 暂停新功能上线
    - 暂停实验性功能
    - 通知所有干系人
  
  # 逐步触发
  progressive:
    at_75_percent:
      - 限制高风险变更
      - 加强变更审批
      - 增加监控频率
    
    at_90_percent:
      - 仅允许紧急修复
      - 暂停所有计划变更
      - 启动根因分析
    
    at_100_percent:
      - 仅允许紧急修复
      - 暂停所有发布
      - 强制复盘
```

### 5. 预算恢复机制

```yaml
budget_recovery:
  # 自动恢复
  auto_recovery:
    enabled: true
    recovery_rate: "按时间窗口自然恢复"
    example: "30 天窗口，每天恢复 1/30 预算"
  
  # 手动重置
  manual_reset:
    allowed: true
    require_approval: "SRE_lead"
    require_reason: true
    audit: true
  
  # 恢复触发
  recovery_triggers:
    - 问题根因已修复
    - 改进措施已实施
    - 预防措施已部署
```

### 6. 预算与发布决策

```yaml
release_decision:
  # 发布前检查
  pre_release_check:
    - 检查当前预算消耗
    - 评估发布风险
    - 确认回滚方案
  
  # 发布决策矩阵
  decision_matrix:
    budget_healthy:  # < 50%
      normal_release: "允许"
      risky_release: "需审批"
    
    budget_warning:  # 50-75%
      normal_release: "需审批"
      risky_release: "推迟"
    
    budget_critical:  # 75-90%
      normal_release: "推迟"
      risky_release: "禁止"
    
    budget_exhausted:  # > 90%
      normal_release: "仅紧急修复"
      risky_release: "禁止"
```

### 7. 预算报告

```yaml
reporting:
  # 日常报告
  daily:
    - 当前预算状态
    - 过去 24h 消耗
    - 预计耗尽时间
  
  # 周报
  weekly:
    - 预算趋势
    - 主要消耗事件
    - 改进措施状态
  
  # 月报
  monthly:
    - 预算使用总结
    - SLO 达成情况
    - 改进建议
```

## 异常处理

### 预算计算错误
- 使用保守估计
- 通知 SRE 团队
- 修正计算逻辑

### 监控失效
- 使用备用监控
- 人工检查预算
- 修复监控系统

### 限制措施失效
- 手动执行限制
- 通知管理层
- 修复执行机制

## 完成标准
- [x] 错误预算计算规则清晰
- [x] 计入预算的失败明确
- [x] 预算消耗监控完整
- [x] 预算耗尽触发限制明确
- [x] 预算恢复机制完整
- [x] 预算与发布决策规则清晰
- [x] 预算报告机制完整
- [x] 系统退化时知道什么时候必须"收手"

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
