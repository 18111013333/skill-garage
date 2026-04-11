# PORTFOLIO_REVIEW.md - 项目组合复盘机制

## 目的
定义项目组合级复盘机制，实现组合层面管理。

## 适用范围
所有项目组合的周期性复盘。

## 复盘类型

| 类型 | 频率 | 参与者 | 重点 |
|------|------|--------|------|
| 周度复盘 | 每周 | 组合负责人 | 进度和阻塞 |
| 月度复盘 | 每月 | 管理层 | 整体健康度 |
| 季度复盘 | 每季 | 高层 | 战略对齐 |
| 里程碑复盘 | 按需 | 相关方 | 关键节点 |

## 复盘模板

### 周度复盘模板
```yaml
weekly_review:
  review_id: "REV-W-2024-W03"
  portfolio_id: "PORT-2024-001"
  review_date: "2024-01-19"
  period: "2024-01-13 to 2024-01-19"
  
  section_1_progress:
    title: "本周期关键进展"
    content:
      projects_progress:
        - project_id: "PROJ-001"
          planned: "完成M1"
          actual: "完成M1"
          status: "on_track"
        - project_id: "PROJ-002"
          planned: "启动开发"
          actual: "延迟启动"
          status: "delayed"
          delay_reason: "资源未到位"
          
      key_achievements:
        - "完成核心模块设计"
        - "用户测试通过"
        
  section_2_priority:
    title: "优先级变化"
    content:
      changes:
        - project_id: "PROJ-003"
          from_priority: "P2"
          to_priority: "P1"
          reason: "客户紧急需求"
          
      new_priorities:
        - "PROJ-003 提升至P1"
        
  section_3_conflicts:
    title: "资源冲突"
    content:
      conflicts:
        - conflict_id: "CF-001"
          type: "resource_contention"
          projects: ["PROJ-001", "PROJ-002"]
          resource: "API配额"
          resolution: "PROJ-001优先"
          
  section_4_risks:
    title: "跨项目风险"
    content:
      new_risks:
        - risk: "PROJ-002延期可能影响PROJ-003"
          impact: "medium"
          mitigation: "调整PROJ-003启动时间"
          
      changed_risks:
        - risk: "资源不足"
          change: "风险等级从low变为medium"
          
  section_5_delays:
    title: "延期项"
    content:
      delayed_items:
        - project_id: "PROJ-002"
          item: "开发启动"
          planned_date: "2024-01-15"
          expected_date: "2024-01-22"
          impact: "影响PROJ-003"
          
  section_6_next_period:
    title: "下周期建议"
    content:
      priorities:
        - "优先完成PROJ-001的M2"
        - "解决PROJ-002资源问题"
        
      actions:
        - action: "申请额外API配额"
          owner: "admin"
          due: "2024-01-20"
```

### 月度复盘模板
```yaml
monthly_review:
  review_id: "REV-M-2024-01"
  portfolio_id: "PORT-2024-001"
  review_date: "2024-01-31"
  
  section_1_overview:
    title: "组合概览"
    content:
      total_projects: 5
      active_projects: 4
      completed_projects: 1
      on_track_rate: 75%
      
  section_2_metrics:
    title: "关键指标"
    content:
      schedule_adherence: 85%
      budget_utilization: 70%
      resource_efficiency: 82%
      risk_management_score: 75
      
  section_3_strategic_alignment:
    title: "战略对齐"
    content:
      alignment_score: 85
      gaps:
        - "PROJ-004与战略目标关联度较低"
        
  section_4_resource_analysis:
    title: "资源分析"
    content:
      utilization:
        - resource_type: "model_compute"
          utilization: 85%
        - resource_type: "human_slots"
          utilization: 90%
          
      bottlenecks:
        - "审批资源紧张"
        
  section_5_recommendations:
    title: "改进建议"
    content:
      - "增加审批资源配额"
      - "调整PROJ-004优先级"
      - "建立资源预警机制"
```

## 复盘流程

```
复盘触发
    ↓
┌─────────────────────────────────────┐
│ 1. 数据收集                          │
│    - 项目进度数据                    │
│    - 资源使用数据                    │
│    - 风险状态数据                    │
│    - 用户反馈数据                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 分析处理                          │
│    - 进度偏差分析                    │
│    - 资源效率分析                    │
│    - 风险趋势分析                    │
│    - 优先级影响分析                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 报告生成                          │
│    - 填充复盘模板                    │
│    - 生成可视化图表                  │
│    - 提炼关键发现                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 评审确认                          │
│    - 召开复盘会议                    │
│    - 讨论关键问题                    │
│    - 确认行动计划                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 5. 行动跟踪                          │
│    - 分配行动项                      │
│    - 设置截止日期                    │
│    - 跟踪执行情况                    │
└─────────────────────────────────────┘
```

## 指标计算

### 组合健康度
```javascript
function calculatePortfolioHealth(portfolio) {
  const factors = {
    scheduleAdherence: calculateScheduleAdherence(portfolio),
    resourceEfficiency: calculateResourceEfficiency(portfolio),
    riskManagement: calculateRiskScore(portfolio),
    strategicAlignment: calculateStrategicAlignment(portfolio)
  };
  
  const weights = {
    scheduleAdherence: 0.3,
    resourceEfficiency: 0.25,
    riskManagement: 0.25,
    strategicAlignment: 0.2
  };
  
  let health = 0;
  for (const [factor, weight] of Object.entries(weights)) {
    health += factors[factor] * weight;
  }
  
  return {
    score: Math.round(health),
    grade: getHealthGrade(health),
    factors: factors
  };
}
```

### 资源效率
```javascript
function calculateResourceEfficiency(portfolio) {
  const resources = portfolio.shared_resources;
  let totalEfficiency = 0;
  
  for (const resource of resources) {
    const utilization = resource.used / resource.capacity;
    const waste = Math.max(0, utilization - 0.8);  // 超过80%视为浪费
    const efficiency = Math.min(1, utilization) - waste * 0.5;
    totalEfficiency += efficiency;
  }
  
  return (totalEfficiency / resources.length) * 100;
}
```

## 行动项管理

### 行动项结构
```yaml
action_item:
  item_id: "ACT-001"
  review_id: "REV-W-2024-W03"
  
  description: "申请额外API配额"
  priority: "high"
  
  owner: "admin"
  due_date: "2024-01-20"
  
  status: "pending"
  progress: 0
  
  related_projects: ["PROJ-001", "PROJ-002"]
```

### 跟踪机制
```yaml
action_tracking:
  check_frequency: "daily"
  escalation:
    - overdue: "1d"
      action: "remind"
    - overdue: "3d"
      action: "escalate"
```

## 复盘报告存储

### 存储配置
```yaml
storage:
  path: "portfolio/reviews/"
  naming: "{portfolio_id}/REV-{type}-{date}.yaml"
  retention: "2_years"
  indexing:
    - portfolio_id
    - review_type
    - review_date
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 复盘完成率 | 按时复盘/应复盘 | <90% |
| 行动项完成率 | 完成/总行动项 | <80% |
| 组合健康度 | 综合健康评分 | <70 |
| 复盘延迟率 | 延迟复盘/总复盘 | >10% |

## 维护方式
- 新增模板: 创建复盘模板
- 调整指标: 更新指标计算
- 新增类型: 更新复盘类型

## 引用文件
- `portfolio/PORTFOLIO_SCHEMA.json` - 项目组合结构
- `portfolio/PORTFOLIO_RISK_MATRIX.md` - 风险矩阵
- `projects/PROJECT_REVIEW_TEMPLATE.md` - 项目复盘模板
