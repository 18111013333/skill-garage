# AUTONOMY_EVAL.md - 自主能力评测方法

## 目的
定义自主能力评测方法，确保自主能力好坏可评测。

## 适用范围
所有自主执行能力的评测。

## 评测维度

| 维度 | 权重 | 说明 | 指标 |
|------|------|------|------|
| 计划质量 | 25% | 计划合理性 | 专家评分 |
| 执行稳定性 | 25% | 执行过程稳定性 | 成功率 |
| 审批命中率 | 15% | 审批通过率 | 通过/申请 |
| 异常处理 | 15% | 异常处理能力 | 处理成功率 |
| 回退成功率 | 10% | 回滚能力 | 成功/回滚 |
| 外部一致性 | 5% | 内外状态一致性 | 一致率 |
| 用户信任 | 5% | 用户满意度 | 反馈评分 |

## 评测方法

### 离线评测
```yaml
offline_evaluation:
  test_scenarios:
    - name: "标准场景"
      count: 100
      coverage: "常见任务类型"
      
    - name: "边界场景"
      count: 50
      coverage: "边界条件"
      
    - name: "异常场景"
      count: 30
      coverage: "异常处理"
      
  metrics:
    - plan_quality_score
    - execution_success_rate
    - approval_pass_rate
    - exception_handling_rate
    - rollback_success_rate
```

### 在线评测
```yaml
online_evaluation:
  methods:
    - shadow_mode:
        description: "影子模式运行"
        duration: "7d"
        
    - canary_release:
        description: "灰度发布"
        percentage: 5
        
  monitoring:
    - real_time_metrics
    - user_feedback
    - error_tracking
```

## 指标计算

### 计划质量评分
```javascript
function evaluatePlanQuality(plan) {
  const factors = {
    completeness: checkCompleteness(plan),
    feasibility: checkFeasibility(plan),
    risk_coverage: checkRiskCoverage(plan),
    rollback_plan: checkRollbackPlan(plan),
    approval_nodes: checkApprovalNodes(plan)
  };
  
  return weightedAverage(factors, {
    completeness: 0.25,
    feasibility: 0.25,
    risk_coverage: 0.2,
    rollback_plan: 0.15,
    approval_nodes: 0.15
  });
}
```

### 执行稳定性评分
```javascript
function evaluateExecutionStability(execution) {
  const metrics = {
    success_rate: execution.success / execution.total,
    error_rate: execution.errors / execution.total,
    timeout_rate: execution.timeouts / execution.total,
    retry_rate: execution.retries / execution.total
  };
  
  return (1 - metrics.error_rate) * 0.4 +
         (1 - metrics.timeout_rate) * 0.3 +
         (1 - metrics.retry_rate) * 0.3;
}
```

## 评测报告

### 报告结构
```yaml
evaluation_report:
  report_id: "EVAL-AUTO-2024-001"
  evaluation_date: "2024-01-31"
  
  summary:
    overall_score: 85
    grade: "B"
    recommendation: "可继续使用"
    
  dimension_scores:
    plan_quality: 88
    execution_stability: 82
    approval_hit_rate: 90
    exception_handling: 78
    rollback_success: 95
    external_consistency: 85
    user_trust: 80
    
  findings:
    strengths:
      - "回滚机制可靠"
      - "审批流程完善"
    weaknesses:
      - "异常处理需加强"
      
  recommendations:
    - "优化异常检测逻辑"
    - "增加异常场景测试"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 评测覆盖率 | 已评测/应评测 | <80% |
| 平均评分 | 综合评分 | <70 |
| 降级率 | 需降级/总评测 | >10% |

## 维护方式
- 新增维度: 创建评测维度
- 调整权重: 更新维度权重
- 新增方法: 创建评测方法

## 引用文件
- `autonomy/AUTONOMY_LEVELS.md` - 自主等级
- `autonomy/PLAN_GENERATION.md` - 计划生成
- `evaluation/QUALITY_METRICS.md` - 质量指标
