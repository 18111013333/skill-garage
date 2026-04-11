# STRATEGY_EVAL.md - 策略评测方法

## 目的
定义策略评测方法，确保策略好坏可量化。

## 适用范围
所有策略的效果评测。

## 评测维度

| 维度 | 权重 | 说明 | 指标 |
|------|------|------|------|
| 成功率 | 25% | 任务完成成功率 | success/total |
| 正确性 | 25% | 结果正确程度 | accuracy_score |
| 完整性 | 15% | 结果完整程度 | completeness_score |
| 成本 | 15% | 资源消耗 | cost_per_task |
| 时延 | 10% | 响应时间 | latency_p50/p99 |
| 追问修正率 | 5% | 需要修正的比例 | followup_rate |
| 用户满意度 | 5% | 用户反馈 | satisfaction_score |

## 评测方法

### 1. 离线评测
```yaml
offline_evaluation:
  setup:
    environment: "staging"
    data_source: "historical_logs"
    test_period: "last_30d"
    
  test_sets:
    - name: "standard"
      size: 1000
      sampling: "random"
      
    - name: "edge_cases"
      size: 200
      sampling: "curated"
      
    - name: "regression"
      size: 500
      sampling: "previous_failures"
      
  execution:
    parallel: true
    max_workers: 10
    timeout_per_task: "60s"
    
  metrics_collection:
    - task_level_metrics
    - aggregate_metrics
    - comparison_with_baseline
```

### 2. 在线评测
```yaml
online_evaluation:
  methods:
    - a_b_testing:
        control_group: "current_strategy"
        treatment_group: "new_strategy"
        traffic_split: "50/50"
        duration: "7d"
        
    - interleaved_testing:
        method: "mix_results"
        evaluation: "blind_judgment"
        
    - shadow_mode:
        method: "run_both_compare"
        user_sees: "current_only"
```

### 3. 用户反馈评测
```yaml
user_feedback_evaluation:
  collection:
    - explicit_feedback:
        - rating
        - thumbs_up_down
        - comment
        
    - implicit_feedback:
        - task_completion
        - followup_questions
        - rephrase_attempts
        - session_length
        
  analysis:
    - sentiment_analysis
    - topic_extraction
    - trend_identification
```

## 评测指标计算

### 成功率
```javascript
function calculateSuccessRate(results) {
  const successCount = results.filter(r => r.status === 'success').length;
  return successCount / results.length;
}
```

### 正确性
```javascript
function calculateAccuracy(results) {
  let totalScore = 0;
  
  for (const result of results) {
    // 有标准答案的对比
    if (result.ground_truth) {
      const similarity = calculateSimilarity(result.output, result.ground_truth);
      totalScore += similarity;
    }
    // 无标准答案的专家评分
    else if (result.expert_score) {
      totalScore += result.expert_score;
    }
  }
  
  return totalScore / results.length;
}
```

### 完整性
```javascript
function calculateCompleteness(results) {
  let totalScore = 0;
  
  for (const result of results) {
    const expectedPoints = result.expected_points || [];
    const coveredPoints = expectedPoints.filter(
      point => result.output.includes(point)
    );
    totalScore += coveredPoints.length / expectedPoints.length;
  }
  
  return totalScore / results.length;
}
```

### 成本效率
```javascript
function calculateCostEfficiency(results) {
  const totalCost = results.reduce((sum, r) => sum + r.cost, 0);
  const successCount = results.filter(r => r.status === 'success').length;
  
  return {
    total_cost: totalCost,
    cost_per_success: totalCost / successCount,
    cost_per_task: totalCost / results.length
  };
}
```

### 追问修正率
```javascript
function calculateFollowupRate(results) {
  const withFollowup = results.filter(
    r => r.followup_count > 0 || r.correction_requested
  ).length;
  
  return withFollowup / results.length;
}
```

## 分层评测

### 按任务类型
```yaml
by_task_type:
  - task_type: "query"
    metrics:
      - accuracy: 0.9
      - latency_p99: 3s
      
  - task_type: "generation"
    metrics:
      - completeness: 0.85
      - user_satisfaction: 0.8
      
  - task_type: "analysis"
    metrics:
      - accuracy: 0.85
      - completeness: 0.9
```

### 按风险等级
```yaml
by_risk_level:
  - risk: "low"
    threshold_multiplier: 1.0
    
  - risk: "medium"
    threshold_multiplier: 1.1  # 要求更高
    
  - risk: "high"
    threshold_multiplier: 1.2
    
  - risk: "critical"
    threshold_multiplier: 1.3
```

### 按环境
```yaml
by_environment:
  - environment: "development"
    sampling_rate: 0.1
    
  - environment: "staging"
    sampling_rate: 0.5
    
  - environment: "production"
    sampling_rate: 1.0
    full_metrics: true
```

## 评测报告

### 报告结构
```yaml
evaluation_report:
  metadata:
    - evaluation_id
    - strategy_id
    - evaluation_date
    - evaluator
    
  summary:
    - overall_score
    - pass_fail_status
    - key_findings
    
  detailed_metrics:
    - by_dimension
    - by_task_type
    - by_risk_level
    
  comparison:
    - vs_baseline
    - vs_previous_version
    - vs_competing_strategies
    
  recommendations:
    - keep
    - adjust
    - deprecate
    
  raw_data:
    - link_to_detailed_logs
```

### 报告频率
```yaml
report_frequency:
  - strategy_change: "immediate"
  - periodic: "weekly"
  - comprehensive: "monthly"
```

## 评测门禁

### 通过标准
```yaml
pass_criteria:
  overall_score: ">= 70"
  success_rate: ">= 90%"
  accuracy: ">= 85%"
  no_critical_regression: true
  
  by_risk_level:
    critical:
      accuracy: ">= 95%"
      success_rate: ">= 99%"
```

### 阻断条件
```yaml
block_conditions:
  - overall_score_drop: "> 10%"
  - critical_metric_regression: true
  - safety_violation: true
  - user_satisfaction_drop: "> 20%"
```

## 持续评测

### 自动评测
```yaml
continuous_evaluation:
  enabled: true
  frequency: "daily"
  sample_size: 100
  
  triggers:
    - strategy_change
    - performance_anomaly
    - user_feedback_spike
```

### 定期深度评测
```yaml
deep_evaluation:
  frequency: "monthly"
  scope: "all_strategies"
  methods:
    - full_test_suite
    - expert_review
    - user_survey
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 评测覆盖率 | 已评测/总策略 | <80% |
| 评测通过率 | 通过/总评测 | <70% |
| 评测延迟 | 评测完成时间 | >24h |
| 回归发现率 | 发现回归/总评测 | >5% |

## 维护方式
- 新增维度: 更新评测维度表
- 调整权重: 更新维度权重
- 新增方法: 创建评测方法

## 引用文件
- `strategy/STRATEGY_REGISTRY.json` - 策略注册表
- `strategy/STRATEGY_SELECTION.md` - 策略选择
- `evaluation/QUALITY_METRICS.md` - 质量指标
