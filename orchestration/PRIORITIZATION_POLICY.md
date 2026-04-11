# PRIORITIZATION_POLICY.md - 多项目优先级排序规则

## 目的
定义多项目优先级排序规则，确保系统知道"先推进哪个"。

## 适用范围
所有项目组合中的项目优先级管理。

## 优先级维度

| 维度 | 权重 | 说明 | 评分范围 |
|------|------|------|----------|
| 用户价值 | 25% | 对用户的重要程度 | 1-100 |
| 截止时间 | 20% | 时间紧迫程度 | 1-100 |
| 风险等级 | 15% | 风险影响程度 | 1-100 |
| 战略重要性 | 15% | 与战略目标的对齐度 | 1-100 |
| 依赖影响面 | 10% | 被其他项目依赖的程度 | 1-100 |
| 资源占用 | 10% | 资源消耗程度（反向） | 1-100 |
| 阻塞成本 | 5% | 阻塞造成的损失 | 1-100 |

## 优先级计算

### 计算公式
```javascript
function calculatePriority(project, context) {
  const weights = {
    userValue: 0.25,
    deadline: 0.20,
    riskLevel: 0.15,
    strategicImportance: 0.15,
    dependencyImpact: 0.10,
    resourceUsage: 0.10,  // 反向：资源占用越高优先级越低
    blockingCost: 0.05
  };
  
  const scores = {
    userValue: scoreUserValue(project),
    deadline: scoreDeadline(project, context.currentTime),
    riskLevel: scoreRiskLevel(project),
    strategicImportance: scoreStrategicImportance(project),
    dependencyImpact: scoreDependencyImpact(project),
    resourceUsage: 100 - scoreResourceUsage(project),  // 反向
    blockingCost: scoreBlockingCost(project)
  };
  
  let priority = 0;
  for (const [dimension, weight] of Object.entries(weights)) {
    priority += scores[dimension] * weight;
  }
  
  return {
    score: Math.round(priority),
    dimensions: scores,
    level: getPriorityLevel(priority)
  };
}
```

### 维度评分

#### 用户价值
```yaml
user_value_scoring:
  critical_user_need: 100
  high_user_impact: 80
  moderate_user_impact: 60
  low_user_impact: 40
  internal_only: 20
```

#### 截止时间
```javascript
function scoreDeadline(project, currentTime) {
  const daysUntilDeadline = getDaysUntilDeadline(project, currentTime);
  
  if (daysUntilDeadline < 0) return 100;  // 已逾期
  if (daysUntilDeadline < 3) return 95;   // 3天内
  if (daysUntilDeadline < 7) return 85;   // 1周内
  if (daysUntilDeadline < 14) return 70;  // 2周内
  if (daysUntilDeadline < 30) return 50;  // 1月内
  return 30;  // 1月以上
}
```

#### 风险等级
```yaml
risk_level_scoring:
  critical: 100
  high: 80
  medium: 50
  low: 20
```

#### 依赖影响面
```javascript
function scoreDependencyImpact(project) {
  const dependentCount = countDependentProjects(project);
  
  if (dependentCount > 5) return 100;
  if (dependentCount > 3) return 80;
  if (dependentCount > 1) return 60;
  if (dependentCount === 1) return 40;
  return 20;
}
```

## 优先级等级

| 等级 | 分数范围 | 说明 | 处理策略 |
|------|----------|------|----------|
| P0 | 90-100 | 最高优先 | 立即处理，可抢占资源 |
| P1 | 75-89 | 高优先 | 优先处理，资源优先分配 |
| P2 | 60-74 | 中优先 | 正常处理，按计划推进 |
| P3 | 40-59 | 低优先 | 空闲时处理 |
| P4 | 0-39 | 最低优先 | 可延期或取消 |

## 资源抢占规则

### 抢占条件
```yaml
preemption_conditions:
  allowed:
    - preemptor_priority: "P0"
      target_priority: "< P0"
      resource_type: "flexible"
      
    - preemptor_priority: "P1"
      target_priority: "< P1"
      resource_type: "flexible"
      requires_approval: true
      
  forbidden:
    - target_has_fixed_allocation: true
    - target_is_at_critical_phase: true
    - preemptor_is_new_project: true
```

### 抢占流程
```yaml
preemption_flow:
  steps:
    - name: "评估抢占必要性"
      checks:
        - preemptor_urgency_verified
        - no_alternative_resources
        
    - name: "识别可抢占目标"
      criteria:
        - lower_priority
        - flexible_resources
        - not_at_critical_phase
        
    - name: "通知被抢占方"
      content:
        - reason
        - duration
        - recovery_plan
        
    - name: "执行抢占"
      actions:
        - pause_target_tasks
        - transfer_resources
        - update_allocations
        
    - name: "监控与恢复"
      actions:
        - track_preemptor_progress
        - plan_resource_return
```

## 动态调整

### 调整触发
```yaml
adjustment_triggers:
  - new_project_added
  - project_deadline_changed
  - project_risk_changed
  - resource_availability_changed
  - dependency_status_changed
  - periodic_recalculation: "daily"
```

### 调整规则
```yaml
adjustment_rules:
  max_change_per_day: 10  # 单日最大调整幅度
  stability_buffer: 5     # 稳定缓冲，小幅波动不调整
  
  notification:
    on_priority_increase: true
    on_priority_decrease: true
    threshold: 10  # 变化超过10分通知
```

## 冲突解决

### 同优先级冲突
```yaml
same_priority_conflict:
  resolution_order:
    - earlier_deadline_first
    - higher_user_value_first
    - lower_resource_cost_first
    - earlier_created_first
```

### 资源竞争冲突
```yaml
resource_contention:
  resolution:
    - compare_priority_scores
    - apply_preemption_rules
    - request_additional_resources
    - escalate_if_unresolved
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 优先级分布 | 各级别项目数量 | P0>5 |
| 抢占频率 | 抢占次数/周 | >3 |
| 优先级波动 | 平均变化幅度 | >15分/周 |
| 低优先级积压 | P3/P4项目数 | >10 |

## 维护方式
- 调整权重: 更新维度权重配置
- 新增维度: 创建优先级维度
- 调整规则: 更新抢占规则

## 引用文件
- `portfolio/PORTFOLIO_SCHEMA.json` - 项目组合结构
- `resources/ALLOCATION_POLICY.md` - 资源分配策略
- `portfolio/PROJECT_QUEUE_POLICY.md` - 项目排队策略
