# STRATEGY_SELECTION.md - 策略选择规则

## 目的
定义策略选择规则，根据任务特征选择最合适的执行策略。

## 适用范围
所有需要策略选择的任务执行场景。

## 选择维度

| 维度 | 权重 | 说明 | 取值范围 |
|------|------|------|----------|
| 任务类型 | 30% | 任务的基本类型 | query/analysis/generation等 |
| 风险级别 | 25% | 任务的风险程度 | low/medium/high/critical |
| 时效要求 | 15% | 时间约束 | 紧急/正常/宽松 |
| 预算约束 | 15% | 成本敏感度 | 敏感/一般/不敏感 |
| 用户偏好 | 10% | 用户历史偏好 | 从用户画像获取 |
| 历史效果 | 5% | 类似任务历史表现 | 从评测数据获取 |

## 选择流程

```
任务输入
    ↓
┌─────────────────────────────────────┐
│ 1. 特征提取                          │
│    - 任务类型识别                    │
│    - 风险级别评估                    │
│    - 约束条件分析                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 候选策略筛选                      │
│    - 匹配适用任务类型                │
│    - 匹配触发条件                    │
│    - 过滤不兼容策略                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 策略评分排序                      │
│    - 计算匹配度分数                  │
│    - 考虑历史效果                    │
│    - 应用用户偏好                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 策略决策                          │
│    - 单策略选择 或 策略组合          │
│    - 验证兼容性                      │
│    - 确认回退策略                    │
└─────────────────────────────────────┘
```

## 选择规则

### 规则定义
```yaml
selection_rules:
  # 规则1：高风险任务强制使用保守策略
  - rule_id: rule_001
    name: "高风险保守"
    priority: 100
    conditions:
      - risk_level: [high, critical]
    actions:
      - require: STRAT_conservative_uncertainty
      - require: STRAT_strong_citation
    override: true
    
  # 规则2：紧急任务优先快速响应
  - rule_id: rule_002
    name: "紧急快速响应"
    priority: 90
    conditions:
      - time_constraint: urgent
      - risk_level: [low, medium]
    actions:
      - prefer: STRAT_answer_then_verify
      - fallback: STRAT_deep_search_first
      
  # 规则3：成本敏感任务
  - rule_id: rule_003
    name: "成本敏感"
    priority: 80
    conditions:
      - budget_constraint: sensitive
    actions:
      - prefer: STRAT_cost_saving
      - require_validation: true
      
  # 规则4：复杂分析任务
  - rule_id: rule_004
    name: "复杂分析"
    priority: 70
    conditions:
      - task_type: analysis
      - complexity: high
    actions:
      - prefer: STRAT_deep_search_first
      - combine: STRAT_strong_citation
```

### 规则优先级
| 优先级范围 | 规则类型 | 说明 |
|------------|----------|------|
| 90-100 | 强制规则 | 必须执行，不可覆盖 |
| 70-89 | 推荐规则 | 优先执行，可被覆盖 |
| 50-69 | 默认规则 | 无其他规则时执行 |
| 0-49 | 备选规则 | 作为备选项 |

## 单策略选择

### 选择算法
```javascript
function selectSingleStrategy(task, candidates) {
  let scores = [];
  
  for (const strategy of candidates) {
    let score = 0;
    
    // 任务类型匹配
    if (strategy.applicable_tasks.includes(task.type)) {
      score += 30;
    }
    
    // 风险级别匹配
    if (strategy.trigger_conditions.risk_levels?.includes(task.risk_level)) {
      score += 25;
    }
    
    // 时效要求匹配
    if (matchesTimeConstraint(strategy, task.time_constraint)) {
      score += 15;
    }
    
    // 预算约束匹配
    if (matchesBudgetConstraint(strategy, task.budget_constraint)) {
      score += 15;
    }
    
    // 用户偏好
    score += getUserPreferenceScore(task.user_id, strategy.strategy_id) * 10;
    
    // 历史效果
    score += getHistoricalPerformance(strategy.strategy_id, task.type) * 5;
    
    scores.push({ strategy, score });
  }
  
  // 按分数排序
  scores.sort((a, b) => b.score - a.score);
  
  return scores[0]?.strategy;
}
```

## 策略组合

### 组合条件
```yaml
combination_rules:
  - condition: "risk_level == high && task_type == analysis"
    strategies:
      - STRAT_conservative_uncertainty
      - STRAT_strong_citation
      - STRAT_deep_search_first
    execution_order: parallel
    
  - condition: "time_constraint == urgent && risk_level == low"
    strategies:
      - STRAT_answer_then_verify
    execution_order: sequential
    post_validation: true
```

### 组合验证
```javascript
function validateCombination(strategies) {
  // 检查兼容性
  for (let i = 0; i < strategies.length; i++) {
    for (let j = i + 1; j < strategies.length; j++) {
      if (strategies[i].incompatible_strategies?.includes(strategies[j].strategy_id)) {
        return { valid: false, reason: 'incompatible' };
      }
    }
  }
  
  // 检查必需验证器
  const allValidators = strategies.flatMap(s => s.required_validators || []);
  // 确保所有验证器可用
  
  return { valid: true };
}
```

## 回退策略

### 回退触发
| 触发条件 | 回退动作 |
|----------|----------|
| 策略执行失败 | 切换到fallback_strategy |
| 验证失败 | 回退到保守策略 |
| 超时 | 切换到快速策略 |
| 资源不足 | 切换到低成本策略 |

### 回退链
```yaml
fallback_chain:
  STRAT_answer_then_verify:
    fallback: STRAT_deep_search_first
    on: [validation_failed, timeout]
    
  STRAT_cost_saving:
    fallback: STRAT_deep_search_first
    on: [quality_below_threshold]
    
  STRAT_deep_search_first:
    fallback: STRAT_conservative_uncertainty
    on: [resource_exhausted]
```

## 动态调整

### 实时调整
```yaml
dynamic_adjustment:
  enabled: true
  triggers:
    - condition: "execution_time > expected * 1.5"
      action: switch_to_faster_strategy
    - condition: "error_rate > 5%"
      action: switch_to_conservative_strategy
    - condition: "user_feedback_negative"
      action: adjust_strategy_preference
```

### 学习调整
```yaml
learning_adjustment:
  enabled: true
  source: strategy_performance_metrics
  update_frequency: daily
  adjustment_range: ±10%
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 策略命中率 | 首选策略成功执行率 | <80% |
| 回退率 | 需要回退的比例 | >10% |
| 组合成功率 | 策略组合成功执行率 | <90% |
| 选择延迟 | 策略选择耗时 | >100ms |

## 维护方式
- 新增规则: 创建选择规则
- 调整权重: 更新维度权重
- 新增组合: 更新组合规则

## 引用文件
- `strategy/STRATEGY_REGISTRY.json` - 策略注册表
- `strategy/ADAPTATION_GUARDRAILS.md` - 自适应护栏
- `strategy/STRATEGY_EVAL.md` - 策略评测
