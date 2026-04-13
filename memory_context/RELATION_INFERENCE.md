# RELATION_INFERENCE.md - 关系推断规则

## 目的
定义关系推断规则，确保推断关系不冒充事实。

## 适用范围
所有知识图谱中的关系推断。

## 关系类型

| 类型 | 来源 | 置信度 | 标记 |
|------|------|--------|------|
| 显式关系 | 用户/系统直接创建 | 1.0 | explicit |
| 推断关系 | 系统推理得出 | 0.5-0.9 | inferred |
| 猜测关系 | 低置信度推断 | <0.5 | guessed |

## 推断条件

### 必须满足的条件
```yaml
inference_requirements:
  source_requirement:
    - 至少一个可靠来源
    - 来源时效性有效
    - 来源置信度 >= 0.6
    
  confidence_threshold:
    - 推断置信度 >= 0.5
    - 低于0.5不创建关系
    
  validation_requirement:
    - 推断逻辑可解释
    - 推断依据可追溯
```

### 推断规则
```yaml
inference_rules:
  # 规则1：传递性推断
  - rule_id: "transitive_inference"
    name: "传递性推断"
    pattern: "A depends_on B, B depends_on C => A depends_on C"
    confidence_formula: "min(conf_ab, conf_bc) * 0.9"
    applicable_relations:
      - depends_on
      - part_of
      - parent_of
      
  # 规则2：对称性推断
  - rule_id: "symmetric_inference"
    name: "对称性推断"
    pattern: "A collaborates_with B => B collaborates_with A"
    confidence_formula: "conf_ab * 1.0"
    applicable_relations:
      - collaborates_with
      - similar_to
      - relates_to
      
  # 规则3：逆向关系推断
  - rule_id: "inverse_inference"
    name: "逆向关系推断"
    pattern: "A created_by B => B created A"
    confidence_formula: "conf_ab * 1.0"
    relation_pairs:
      - [created_by, created]
      - [owns, owned_by]
      - [depends_on, depended_by]
      
  # 规则4：共现推断
  - rule_id: "cooccurrence_inference"
    name: "共现推断"
    pattern: "A and B frequently appear together => A relates_to B"
    confidence_formula: "cooccurrence_count / total_appearances * 0.7"
    min_cooccurrence: 3
    
  # 规则5：属性相似推断
  - rule_id: "attribute_similarity_inference"
    name: "属性相似推断"
    pattern: "A and B have similar attributes => A similar_to B"
    confidence_formula: "attribute_similarity * 0.8"
    min_similarity: 0.7
```

## 推断流程

```
推断触发
    ↓
┌─────────────────────────────────────┐
│ 1. 条件检查                          │
│    - 检查来源可靠性                  │
│    - 验证时效性                      │
│    - 确认置信度门槛                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 推断计算                          │
│    - 应用推断规则                    │
│    - 计算置信度                      │
│    - 生成推断依据                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 结果验证                          │
│    - 检查与现有关系冲突              │
│    - 验证逻辑合理性                  │
│    - 确认不违反约束                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 关系创建                          │
│    - 标记为推断关系                  │
│    - 记录推断依据                    │
│    - 设置置信度                      │
└─────────────────────────────────────┘
```

## 推断标记

### 标记内容
```yaml
inference_marking:
  required_fields:
    - is_inferred: true
    - inference_rule: "rule_id"
    - inference_basis: "推断依据描述"
    - confidence: 0.0-1.0
    - inferred_at: "timestamp"
    - source_relations: ["relation_ids"]
    
  optional_fields:
    - validation_status: "pending/verified/rejected"
    - user_feedback: "accepted/rejected"
    - decay_rate: "置信度衰减率"
```

### 标记示例
```json
{
  "relation_id": "rel_inferred_001",
  "from_entity": "task_001",
  "to_entity": "task_003",
  "relation_type": "depends_on",
  "is_inferred": true,
  "inference_rule": "transitive_inference",
  "inference_basis": "task_001 depends_on task_002, task_002 depends_on task_003",
  "confidence": 0.81,
  "source_relations": ["rel_001", "rel_002"],
  "inferred_at": "2024-01-15T10:00:00Z"
}
```

## 置信度计算

### 计算公式
```javascript
function calculateInferenceConfidence(rule, sourceRelations) {
  // 基础置信度
  let baseConfidence = rule.confidence_formula(sourceRelations);
  
  // 来源置信度因子
  const sourceFactor = Math.min(
    ...sourceRelations.map(r => r.confidence)
  );
  
  // 时效性因子
  const timelinessFactor = calculateTimeliness(sourceRelations);
  
  // 规则可靠性因子
  const ruleReliability = rule.historical_accuracy || 0.8;
  
  // 综合置信度
  const finalConfidence = 
    baseConfidence * 
    sourceFactor * 
    timelinessFactor * 
    ruleReliability;
    
  return Math.min(1.0, finalConfidence);
}
```

### 置信度衰减
```yaml
confidence_decay:
  enabled: true
  formula: "confidence * exp(-decay_rate * days_since_inference)"
  decay_rates:
    high_confidence: 0.001  # 高置信度衰减慢
    medium_confidence: 0.005
    low_confidence: 0.01  # 低置信度衰减快
    
  refresh_on:
    - user_confirmation
    - new_evidence
    - successful_usage
```

## 冲突处理

### 冲突检测
```yaml
conflict_detection:
  types:
    - name: "直接冲突"
      pattern: "推断关系与显式关系矛盾"
      action: "reject_inference"
      
    - name: "推断冲突"
      pattern: "多个推断结果矛盾"
      action: "use_highest_confidence"
      
    - name: "逻辑冲突"
      pattern: "推断违反关系约束"
      action: "reject_inference"
```

### 冲突解决
```yaml
conflict_resolution:
  priority:
    - explicit_relation
    - verified_inference
    - unverified_inference
    
  actions:
    - reject_lower_confidence
    - mark_conflict_for_review
    - request_user_clarification
```

## 推断验证

### 自动验证
```yaml
auto_validation:
  triggers:
    - new_evidence_available
    - user_interaction_with_relation
    - periodic_review
    
  checks:
    - consistency_with_new_data
    - usage_success_rate
    - user_feedback
```

### 人工验证
```yaml
manual_validation:
  triggers:
    - confidence_below: 0.6
    - conflict_detected
    - high_impact_relation
    
  process:
    - present_to_reviewer
    - collect_feedback
    - update_status
```

## 推断使用

### 使用限制
```yaml
usage_limits:
  - condition: "confidence < 0.5"
    action: "do_not_use"
    
  - condition: "confidence < 0.7"
    action: "use_with_uncertainty_statement"
    
  - condition: "validation_status == rejected"
    action: "do_not_use"
```

### 不确定性表达
```yaml
uncertainty_expression:
  templates:
    - "可能存在关系：{relation_type}"
    - "推断认为：{description}（置信度：{confidence}）"
    - "根据{basis}推断：{description}"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 推断准确率 | 验证正确/总推断 | <70% |
| 推断使用率 | 推断关系使用/总关系 | >50% |
| 冲突率 | 冲突/总推断 | >10% |
| 平均置信度 | 推断关系平均置信度 | <0.6 |

## 维护方式
- 新增规则: 创建推断规则
- 调整阈值: 更新置信度阈值
- 优化公式: 更新计算公式

## 引用文件
- `graph/GRAPH_SCHEMA.json` - 图谱结构
- `graph/GRAPH_REASONING.md` - 图谱推理
- `graph/GRAPH_HYGIENE.md` - 图谱清理
