# MODEL_RISK_TIERING.md - 模型风险分层

## 目的
定义模型风险分层规则，确保不同风险级别的模型得到相应的管理和控制。

## 适用范围
平台所有模型的风险评估、分层、管理场景。

## 与其他模块联动
| 模块 | 联动内容 |
|------|----------|
| model_governance | 模型注册与审批 |
| tenancy | 租户模型权限 |
| access | 模型访问控制 |
| audit | 模型风险审计 |
| compliance | 模型合规检查 |

## 风险分层定义

### 风险等级
| 等级 | 名称 | 说明 | 风险特征 |
|------|------|------|----------|
| T1 | 低风险 | 无生成能力或影响有限 | 辅助功能、无敏感数据 |
| T2 | 标准风险 | 有生成能力，影响可控 | 核心功能、可能处理敏感数据 |
| T3 | 高风险 | 影响重大决策或处理高度敏感数据 | 决策影响、敏感数据处理 |

### 风险评估维度
| 维度 | 权重 | 评估内容 |
|------|------|----------|
| 能力风险 | 30% | 模型能力带来的潜在风险 |
| 数据风险 | 25% | 处理数据的敏感程度 |
| 决策风险 | 25% | 对决策的影响程度 |
| 影响范围 | 20% | 影响的用户和业务范围 |

## 低风险模型 (T1)

### 定义特征
```yaml
tier1_characteristics:
  capabilities:
    - 无生成能力或生成能力有限
    - 仅用于辅助功能
    - 输出可预测可控
  
  data_handling:
    - 不处理敏感数据
    - 不处理PII
    - 数据不持久化
  
  decision_impact:
    - 不影响重大决策
    - 不影响用户权益
    - 可随时替代或停用
```

### 典型模型
| 模型类型 | 说明 | 风险点 |
|----------|------|--------|
| 嵌入模型 | 文本向量化 | 低 |
| 分类模型 | 内容分类 | 低 |
| 检测模型 | 异常检测 | 低 |
| 排序模型 | 结果排序 | 低 |

### 使用规则
```yaml
tier1_usage_rules:
  allowed_tasks:
    - 辅助检索
    - 内容分类
    - 质量检测
    - 性能优化
  
  allowed_tenants:
    - all
  
  allowed_domains:
    - all
  
  approval_requirements:
    technical_review: true
    security_review: false
    legal_review: false
    board_approval: false
  
  deployment_rules:
    canary_required: false
    gradual_rollout: false
    monitoring_level: standard
```

## 标准风险模型 (T2)

### 定义特征
```yaml
tier2_characteristics:
  capabilities:
    - 有生成能力
    - 用于核心功能
    - 输出需审核
  
  data_handling:
    - 可能处理敏感数据
    - 可能处理部分PII
    - 数据有保留期限
  
  decision_impact:
    - 可能影响业务决策
    - 可能影响用户体验
    - 需要人工监督
```

### 典型模型
| 模型类型 | 说明 | 风险点 |
|----------|------|--------|
| 大语言模型 | 文本生成 | 中 |
| 视觉模型 | 图像理解 | 中 |
| 语音模型 | 语音处理 | 中 |
| 翻译模型 | 语言翻译 | 中 |

### 使用规则
```yaml
tier2_usage_rules:
  allowed_tasks:
    - 问答服务
    - 内容生成
    - 信息分析
    - 辅助决策
  
  restricted_tasks:
    - financial_advice
    - medical_diagnosis
    - legal_advice
  
  allowed_tenants:
    - all
  excluded_tenants: []
  
  allowed_domains:
    - customer_service
    - content_creation
    - data_analysis
  restricted_domains:
    - finance
    - healthcare
    - legal
  
  approval_requirements:
    technical_review: true
    security_review: true
    legal_review: false
    board_approval: true
  
  deployment_rules:
    canary_required: true
    gradual_rollout: true
    monitoring_level: enhanced
```

## 高风险模型 (T3)

### 定义特征
```yaml
tier3_characteristics:
  capabilities:
    - 影响重大决策
    - 自动化决策能力
    - 难以预测输出
  
  data_handling:
    - 处理高度敏感数据
    - 处理完整PII
    - 数据长期保留
  
  decision_impact:
    - 直接影响用户权益
    - 影响重大业务决策
    - 需要人工复核
```

### 典型模型
| 模型类型 | 说明 | 风险点 |
|----------|------|--------|
| 决策模型 | 自动决策 | 高 |
| 风险评估模型 | 风险判断 | 高 |
| 信用评估模型 | 信用评分 | 高 |
| 人脸识别模型 | 身份识别 | 高 |

### 使用规则
```yaml
tier3_usage_rules:
  allowed_tasks:
    - risk_assessment
    - fraud_detection
    - compliance_check
  restricted_tasks:
    - credit_scoring
    - employment_decision
    - insurance_decision
  
  allowed_tenants:
    - approved_list_only
  excluded_tenants:
    - all_others
  
  allowed_domains:
    - risk_management
    - security
  restricted_domains:
    - finance
    - healthcare
    - employment
  
  approval_requirements:
    technical_review: true
    security_review: true
    legal_review: true
    board_approval: true
    external_audit: true
  
  deployment_rules:
    canary_required: true
    gradual_rollout: true
    monitoring_level: maximum
    human_oversight: true
```

## 额外控制要求

### 高风险模型额外要求
```yaml
tier3_additional_controls:
  # 引用要求
  citation_requirements:
    - 每次使用必须记录
    - 输出必须标注模型来源
    - 用户必须被告知使用AI
  
  # 审批要求
  approval_requirements:
    - 每次使用需审批
    - 审批有效期有限
    - 定期重新审批
  
  # 校验要求
  validation_requirements:
    - 定期准确性验证
    - 偏见检测
    - 公平性评估
  
  # 审计要求
  audit_requirements:
    - 全量使用记录
    - 定期审计报告
    - 外部审计支持
```

## 风险等级调整

### 升级条件
| 条件 | 说明 |
|------|------|
| 能力扩展 | 模型能力显著增强 |
| 数据范围扩大 | 处理更敏感数据 |
| 用途变更 | 用于更高风险场景 |
| 事件触发 | 发生风险事件 |

### 降级条件
| 条件 | 说明 |
|------|------|
| 能力限制 | 增加能力限制 |
| 数据范围缩小 | 不再处理敏感数据 |
| 用途限制 | 仅用于低风险场景 |
| 长期稳定 | 长期无风险事件 |

## 风险评估流程

### 评估步骤
```yaml
risk_assessment_flow:
  steps:
    - name: "能力评估"
      actions:
        - analyze_model_capabilities
        - identify_potential_risks
        - score_capability_risk
    
    - name: "数据评估"
      actions:
        - analyze_data_types
        - assess_sensitivity
        - score_data_risk
    
    - name: "决策评估"
      actions:
        - analyze_decision_impact
        - assess_user_impact
        - score_decision_risk
    
    - name: "范围评估"
      actions:
        - analyze_user_scope
        - assess_business_impact
        - score_scope_risk
    
    - name: "综合评定"
      actions:
        - calculate_total_score
        - determine_risk_tier
        - document_assessment
```

## 引用文件
- `model_governance/MODEL_REGISTRY.json` - 模型注册表
- `model_governance/MODEL_APPROVAL_POLICY.md` - 模型审批规则
- `model_governance/MODEL_CHANGE_CONTROL.md` - 模型变更控制
- `data_governance/DATA_CLASSIFICATION.md` - 数据分级制度
