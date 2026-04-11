# PORTFOLIO_RISK_MATRIX.md - 组合级风险矩阵

## 目的
定义组合级风险矩阵，确保多项目风险可视、可量化、可干预。

## 适用范围
所有项目组合的风险管理。

## 风险类别

| 类别 | 说明 | 影响范围 | 典型表现 |
|------|------|----------|----------|
| 单点资源依赖 | 单一资源瓶颈 | 多项目 | 关键资源不可用 |
| 关键项目延误 | 核心项目延期 | 组合整体 | P0项目延期 |
| 共享系统故障 | 共享服务故障 | 所有项目 | API服务宕机 |
| 审批堵点 | 审批流程阻塞 | 多项目 | 审批超时 |
| 预算超支 | 成本超限 | 组合整体 | 预算耗尽 |
| 策略冲突 | 策略不一致 | 项目间 | 优先级冲突 |

## 风险矩阵

### 风险评估矩阵
```yaml
risk_matrix:
  dimensions:
    probability: [low, medium, high]
    impact: [low, medium, high, critical]
    
  scoring:
    low_low: 1
    low_medium: 2
    low_high: 3
    low_critical: 4
    medium_low: 2
    medium_medium: 4
    medium_high: 6
    medium_critical: 8
    high_low: 3
    high_medium: 6
    high_high: 9
    high_critical: 12
    
  levels:
    low: "1-3"
    medium: "4-6"
    high: "7-9"
    critical: "10-12"
```

## 风险定义

### 单点资源依赖
```yaml
risk_single_point_dependency:
  risk_id: "RISK-SPD"
  name: "单点资源依赖"
  description: "关键资源无备份，故障影响多项目"
  
  indicators:
    - single_provider: true
    - no_fallback: true
    - multiple_projects_depend: true
    
  probability_factors:
    high:
      - resource_age > 1year
      - recent_failures > 2
    medium:
      - resource_age > 6months
    low:
      - new_resource
      
  impact_factors:
    critical:
      - affected_projects > 3
      - affected_priority: "P0"
    high:
      - affected_projects > 2
    medium:
      - affected_projects = 1
      
  mitigation:
    - 建立备用资源
    - 资源冗余配置
    - 定期健康检查
    
  trigger_threshold:
    score: 6
    action: "immediate_mitigation"
```

### 关键项目延误
```yaml
risk_critical_project_delay:
  risk_id: "RISK-CPD"
  name: "关键项目延误"
  description: "高优先级项目延期影响组合目标"
  
  indicators:
    - project_priority: "P0"
    - schedule_variance: "> 20%"
    - blocking_dependencies: "> 0"
    
  probability_factors:
    high:
      - already_delayed: true
      - unresolved_blockers: "> 2"
    medium:
      - schedule_risk_detected: true
    low:
      - on_track: true
      
  impact_factors:
    critical:
      - strategic_project: true
      - cascading_delay: "> 3 projects"
    high:
      - cascading_delay: "> 1 project"
    medium:
      - isolated_delay: true
      
  mitigation:
    - 资源优先分配
    - 移除阻塞项
    - 调整依赖项目计划
    
  escalation:
    - score > 8: "escalate_to_management"
```

### 共享系统故障
```yaml
risk_shared_system_failure:
  risk_id: "RISK-SSF"
  name: "共享系统故障"
  description: "共享服务故障导致多项目停滞"
  
  indicators:
    - shared_system: true
    - no_redundancy: true
    
  probability_factors:
    high:
      - recent_outages: "> 1"
      - health_score: "< 80"
    medium:
      - maintenance_due: true
    low:
      - stable_history: true
      
  impact_factors:
    critical:
      - all_projects_depend: true
    high:
      - majority_projects_depend: true
    medium:
      - minority_projects_depend: true
      
  mitigation:
    - 系统冗余
    - 故障转移机制
    - 降级方案
    
  monitoring:
    - health_check: "5m"
    - auto_alert: true
```

### 审批堵点
```yaml
risk_approval_bottleneck:
  risk_id: "RISK-AB"
  name: "审批堵点"
  description: "审批流程阻塞导致项目停滞"
  
  indicators:
    - pending_approvals: "> 5"
    - avg_approval_time: "> 4h"
    
  probability_factors:
    high:
      - approver_unavailable: true
      - approval_backlog: "> 10"
    medium:
      - approval_delay: "> 2h"
    low:
      - normal_flow: true
      
  impact_factors:
    critical:
      - blocked_projects: "> 3"
      - blocked_priority: "P0"
    high:
      - blocked_projects: "> 1"
    medium:
      - single_project_blocked: true
      
  mitigation:
    - 增加审批人
    - 设置审批代理
    - 快速通道机制
```

### 预算超支
```yaml
risk_budget_overrun:
  risk_id: "RISK-BO"
  name: "预算超支"
  description: "组合预算耗尽影响项目执行"
  
  indicators:
    - budget_utilization: "> 80%"
    - burn_rate: "above_plan"
    
  probability_factors:
    high:
      - utilization: "> 90%"
      - unplanned_costs: "> 0"
    medium:
      - utilization: "> 80%"
    low:
      - utilization: "< 70%"
      
  impact_factors:
    critical:
      - will_exhaust: "< 7d"
      - critical_projects_affected: true
    high:
      - will_exhaust: "< 30d"
    medium:
      - will_exhaust: "< 60d"
      
  mitigation:
    - 申请追加预算
    - 暂停低优先级项目
    - 成本优化措施
```

### 策略冲突
```yaml
risk_strategy_conflict:
  risk_id: "RISK-SC"
  name: "策略冲突"
  description: "项目间策略不一致导致资源冲突"
  
  indicators:
    - conflicting_priorities: true
    - resource_contention: "> 0"
    
  probability_factors:
    high:
      - unresolved_conflicts: "> 2"
      - frequent_contention: true
    medium:
      - occasional_conflict: true
    low:
      - aligned_strategies: true
      
  impact_factors:
    critical:
      - P0_projects_conflict: true
    high:
      - multiple_conflicts: true
    medium:
      - single_conflict: true
      
  mitigation:
    - 明确优先级规则
    - 资源分配仲裁
    - 定期策略对齐
```

## 风险监控

### 监控配置
```yaml
risk_monitoring:
  frequency: "daily"
  
  checks:
    - check_all_risks
    - update_risk_scores
    - detect_new_risks
    - verify_mitigation_status
    
  alerts:
    - new_critical_risk: "immediate"
    - risk_score_increase: "> 2"
    - mitigation_failed: "immediate"
```

### 风险仪表盘
```yaml
risk_dashboard:
  views:
    - overall_risk_level
    - risk_distribution
    - trending_risks
    - mitigation_progress
    
  refresh: "real_time"
```

## 升级路径

### 升级规则
```yaml
escalation_rules:
  - condition: "risk_score >= 10"
    level: "management"
    action: "immediate_review"
    
  - condition: "risk_score >= 8"
    level: "portfolio_owner"
    action: "urgent_mitigation"
    
  - condition: "risk_score >= 6"
    level: "project_owner"
    action: "plan_mitigation"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 高风险数量 | 高风险项数量 | >3 |
| 平均风险分数 | 组合平均风险分 | >6 |
| 缓解完成率 | 已缓解/总风险 | <80% |
| 新增风险率 | 新增/周期 | >2/周 |

## 维护方式
- 新增风险类型: 创建风险定义
- 调整阈值: 更新触发阈值
- 优化缓解: 更新缓解措施

## 引用文件
- `portfolio/PORTFOLIO_SCHEMA.json` - 项目组合结构
- `portfolio/PORTFOLIO_REVIEW.md` - 组合复盘
- `safety/RISK_POLICY.md` - 风险策略
