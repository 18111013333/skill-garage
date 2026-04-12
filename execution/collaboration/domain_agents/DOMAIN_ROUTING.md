# DOMAIN_ROUTING.md - 行业场景识别与路由

## 目的
定义行业场景识别与路由规则，确保行业任务能进对入口。

## 适用范围
所有需要识别行业领域并进行路由的任务。

## 识别方法

### 关键词识别
```yaml
keyword_detection:
  domains:
    legal:
      keywords:
        - "合同", "条款", "法律", "法规", "诉讼", "仲裁"
        - "合同审查", "法律风险", "合规", "法务"
      weight: 1.0
      
    finance:
      keywords:
        - "投资", "理财", "股票", "基金", "收益", "风险"
        - "预算", "财务", "报表", "审计", "税务"
      weight: 1.0
      
    healthcare:
      keywords:
        - "医疗", "健康", "诊断", "治疗", "药物", "症状"
        - "医院", "医生", "病历", "处方"
      weight: 1.0
      
    operations:
      keywords:
        - "项目", "进度", "任务", "团队", "协作", "SOP"
        - "复盘", "里程碑", "交付", "运营"
      weight: 0.8
      
    research:
      keywords:
        - "研究", "分析", "论文", "文献", "数据", "实验"
        - "调研", "报告", "结论", "假设"
      weight: 0.8
```

### 语义识别
```yaml
semantic_detection:
  model: "domain_classifier"
  confidence_threshold: 0.7
  
  features:
    - task_description
    - user_context
    - historical_patterns
```

### 上下文识别
```yaml
context_detection:
  signals:
    - project_domain_tag
    - user_profile_domain
    - previous_task_domain
    - document_type
```

## 路由流程

```
任务输入
    ↓
┌─────────────────────────────────────┐
│ 1. 多维度识别                        │
│    - 关键词匹配                      │
│    - 语义分类                        │
│    - 上下文推断                      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 置信度计算                        │
│    - 综合各维度结果                  │
│    - 计算置信度分数                  │
│    - 识别多域混合                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 路由决策                          │
│    - 单域：直接路由                  │
│    - 多域：确定主域                  │
│    - 低置信：保守模式                │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 套件激活                          │
│    - 加载领域配置                    │
│    - 应用合规规则                    │
│    - 启用对应agent                   │
└─────────────────────────────────────┘
```

## 路由规则

### 单域路由
```yaml
single_domain_routing:
  condition: "max_confidence > 0.8"
  
  process:
    - select_domain: "highest_confidence"
    - load_domain_suite
    - apply_domain_rules
    
  example:
    input: "帮我审查这份合同的条款"
    detected: "legal"
    confidence: 0.95
    action: "route_to_legal_suite"
```

### 多域混合
```yaml
multi_domain_routing:
  condition: "multiple_domains_confidence > 0.6"
  
  process:
    - identify_primary_domain
    - identify_secondary_domains
    - apply_primary_rules
    - add_secondary_constraints
    
  primary_selection:
    - highest_confidence
    - highest_compliance_level
    - user_explicit_indication
    
  example:
    input: "分析这个投资项目的法律风险"
    detected:
      - finance: 0.75
      - legal: 0.70
    primary: "finance"
    secondary: ["legal"]
    action: "finance_suite_with_legal_constraints"
```

### 低置信处理
```yaml
low_confidence_handling:
  condition: "max_confidence < 0.6"
  
  actions:
    - use_conservative_mode
    - apply_strictest_rules
    - request_user_clarification
    
  conservative_mode:
    - highest_compliance_level
    - strictest_validation
    - maximum_uncertainty_expression
```

## 保守模式

### 触发条件
```yaml
conservative_mode_triggers:
  - domain_confidence < 0.6
  - multi_domain_conflict
  - high_risk_task
  - new_user
  - sensitive_topic
```

### 保守模式规则
```yaml
conservative_mode_rules:
  compliance_level: "maximum"
  citation_mode: "strict"
  uncertainty_expression: "maximum"
  validation: "comprehensive"
  approval_required: true
```

## 域切换

### 切换触发
```yaml
domain_switch_triggers:
  - new_domain_keywords_detected
  - user_explicit_request
  - task_phase_change
  - compliance_requirement_change
```

### 切换流程
```yaml
domain_switch_flow:
  steps:
    - detect_switch_need
    - save_current_context
    - load_new_domain_config
    - apply_transition_rules
    - notify_user
```

## 路由记录

### 记录内容
```yaml
routing_record:
  routing_id: "ROUTE-001"
  task_id: "TASK-001"
  
  detection:
    keyword_scores: {...}
    semantic_score: 0.85
    context_score: 0.90
    
  decision:
    primary_domain: "legal"
    secondary_domains: []
    confidence: 0.88
    mode: "standard"
    
  applied_rules:
    - compliance_level: "maximum"
    - citation_mode: "strict"
    
  timestamp: "2024-01-15T10:00:00Z"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 路由准确率 | 正确路由/总路由 | <85% |
| 平均置信度 | 路由置信度 | <0.7 |
| 多域比例 | 多域任务比例 | >30% |
| 保守模式率 | 保守模式使用率 | >20% |

## 维护方式
- 新增领域: 更新关键词和规则
- 调整权重: 更新识别权重
- 优化算法: 更新识别模型

## 引用文件
- `domain_agents/DOMAIN_REGISTRY.json` - 领域注册表
- `domain_agents/COMPLIANCE_MATRIX.md` - 合规矩阵
- `strategy/STRATEGY_SELECTION.md` - 策略选择
