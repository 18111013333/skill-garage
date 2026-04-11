# CONSENT_AND_PURPOSE_LIMITATION.md - 同意与用途限制规则

## 目的
定义数据收集的同意机制和用途限制规则，确保数据不被滥用。

## 适用范围
平台所有数据收集、使用、共享、变更场景。

## 与其他模块联动
| 模块 | 联动内容 |
|------|----------|
| privacy | 隐私治理框架 |
| data_governance | 数据分级管理 |
| audit | 同意审计 |
| compliance | 合规检查 |
| tenancy | 租户同意策略 |

## 同意机制

### 同意类型
| 类型 | 说明 | 适用场景 |
|------|------|----------|
| 明示同意 | 用户明确表达同意 | 敏感数据处理 |
| 默示同意 | 用户行为暗示同意 | 基本功能使用 |
| 选择性同意 | 用户可选择同意 | 可选功能 |
| 撤回同意 | 用户撤回同意 | 任何时间 |

### 同意获取方式
```yaml
consent_collection:
  explicit:
    method: "明确勾选或点击"
    requirements:
      - 单独展示
      - 明确说明
      - 易于理解
      - 可随时撤回
    examples:
      - "我同意收集我的位置信息用于..."
      - "我同意接收营销信息"
  
  implied:
    method: "用户行为推断"
    requirements:
      - 行为明确
      - 目的明显
      - 无其他解释
    examples:
      - 使用搜索功能 → 同意收集搜索词
      - 发送消息 → 同意处理消息内容
  
  optional:
    method: "可选功能单独同意"
    requirements:
      - 功能可选
      - 不影响核心功能
      - 明确说明
    examples:
      - 个性化推荐
      - 数据分析改进
```

## 同意记录

### 同意记录格式
```json
{
  "consent_id": "consent_001",
  "user_id": "user_001",
  "consent_type": "explicit",
  "consent_purpose": "location_based_service",
  "consent_scope": {
    "data_types": ["location"],
    "processing_types": ["service_delivery"],
    "retention_period": "session_only"
  },
  "consent_given_at": "2026-04-06T22:00:00+08:00",
  "consent_method": "checkbox",
  "consent_text": "我同意收集我的位置信息用于提供位置相关服务",
  "consent_version": "1.0",
  "withdrawal_supported": true,
  "withdrawn_at": null
}
```

### 同意版本管理
```yaml
consent_versioning:
  rules:
    - name: "版本变更通知"
      trigger: "consent_text_change"
      action: "notify_users"
    
    - name: "重新获取同意"
      trigger: "scope_expand"
      action: "require_new_consent"
    
    - name: "保留历史版本"
      trigger: "any_change"
      action: "archive_old_version"
```

## 用途限制

### 用途定义
| 用途类别 | 说明 | 数据范围 |
|----------|------|----------|
| 服务交付 | 提供核心服务 | 功能必需数据 |
| 安全保护 | 保护系统安全 | 安全相关数据 |
| 合规义务 | 履行法律义务 | 法定必需数据 |
| 服务改进 | 改进服务质量 | 使用数据 |
| 研究分析 | 数据分析研究 | 匿名化数据 |
| 营销推广 | 营销活动 | 需单独同意 |

### 用途限制规则
```yaml
purpose_limitations:
  service_delivery:
    allowed_data:
      - account_info
      - service_usage
    forbidden_data:
      - pii_unnecessary
    retention: "service_period"
  
  security_protection:
    allowed_data:
      - access_logs
      - security_events
    forbidden_data:
      - user_content
    retention: "90_days"
  
  compliance_obligation:
    allowed_data:
      - legal_required
    forbidden_data:
      - extra_data
    retention: "legal_requirement"
  
  service_improvement:
    allowed_data:
      - anonymized_usage
    forbidden_data:
      - identifiable_data
    retention: "1_year"
  
  marketing:
    allowed_data:
      - with_explicit_consent
    forbidden_data:
      - without_consent
    retention: "consent_period"
```

## 用途变更规则

### 变更类型
| 变更类型 | 说明 | 处理方式 |
|----------|------|----------|
| 范围扩大 | 用途范围扩大 | 需重新同意 |
| 目的改变 | 主要目的改变 | 需重新同意 |
| 数据增加 | 使用更多数据 | 需重新同意 |
| 期限延长 | 保留期限延长 | 需重新同意 |
| 共享增加 | 新增共享方 | 需重新同意 |

### 变更流程
```yaml
purpose_change_flow:
  steps:
    - name: "变更评估"
      actions:
        - assess_change_impact
        - identify_affected_users
        - evaluate_legal_basis
    
    - name: "用户通知"
      actions:
        - prepare_change_notice
        - send_notification
        - allow_opt_out
    
    - name: "同意获取"
      actions:
        - request_new_consent
        - record_consent_response
        - handle_non_consent
    
    - name: "变更执行"
      actions:
        - apply_new_purpose
        - update_records
        - audit_change
```

## 默认禁止用途

### 禁止用途列表
| 用途 | 说明 | 例外条件 |
|------|------|----------|
| 出售数据 | 出售用户数据 | 禁止 |
| 未经同意共享 | 向第三方共享 | 用户同意 |
| 跨用途使用 | 超出原定用途 | 用户同意 |
| 自动化决策 | 影响权益的自动决策 | 用户同意+人工复核 |
| 用户画像 | 建立用户画像 | 用户同意 |
| 行为追踪 | 跨站行为追踪 | 用户同意 |

### 自动化决策限制
```yaml
automated_decision_restrictions:
  prohibited_decisions:
    - name: "信用评估"
      condition: "影响金融服务"
      restriction: "禁止"
    
    - name: "就业决策"
      condition: "影响雇佣关系"
      restriction: "禁止"
    
    - name: "保险决策"
      condition: "影响保险服务"
      restriction: "需人工复核"
  
  allowed_decisions:
    - name: "内容推荐"
      condition: "用户可调整"
      restriction: "允许"
    
    - name: "服务优化"
      condition: "不影响权益"
      restriction: "允许"
```

## 合作伙伴访问

### 合作伙伴类型
| 类型 | 说明 | 访问条件 |
|------|------|----------|
| 服务提供商 | 协助提供服务 | 合同约束 |
| 业务伙伴 | 业务合作 | 用户同意 |
| 数据处理者 | 受托处理数据 | 处理协议 |
| 监管机构 | 监管检查 | 法律要求 |

### 合作伙伴访问规则
```yaml
partner_access_rules:
  service_provider:
    access_scope: "limited_to_service"
    data_retention: "service_period"
    security_requirements:
      - encryption
      - access_control
      - audit_logging
  
  business_partner:
    access_scope: "with_user_consent"
    data_retention: "consent_period"
    additional_requirements:
      - user_notification
      - consent_record
  
  data_processor:
    access_scope: "per_processing_agreement"
    data_retention: "agreement_period"
    security_requirements:
      - dpa_signed
      - security_audit
```

## 同意撤回

### 撤回权利
| 权利 | 说明 |
|------|------|
| 随时撤回 | 用户可随时撤回同意 |
| 无条件撤回 | 撤回无需理由 |
| 简便撤回 | 撤回方式简单 |
| 效果相同 | 撤回与拒绝效果相同 |

### 撤回处理流程
```yaml
withdrawal_flow:
  steps:
    - name: "接收撤回请求"
      actions:
        - verify_user_identity
        - record_withdrawal_request
    
    - name: "停止处理"
      actions:
        - stop_data_processing
        - notify_related_systems
    
    - name: "数据处置"
      actions:
        - delete_or_anonymize
        - verify_deletion
    
    - name: "通知相关方"
      actions:
        - notify_partners
        - update_records
    
    - name: "确认撤回"
      actions:
        - send_confirmation
        - audit_withdrawal
```

## 同意审计

### 审计内容
| 审计项 | 频率 | 说明 |
|--------|------|------|
| 同意有效性 | 实时 | 检查同意是否有效 |
| 用途合规性 | 日度 | 检查用途是否合规 |
| 撤回处理 | 实时 | 检查撤回是否及时 |
| 变更记录 | 周度 | 检查变更是否记录 |

## 引用文件
- `privacy/PRIVACY_FRAMEWORK.md` - 隐私治理框架
- `privacy/PII_HANDLING.md` - PII处理规则
- `privacy/DSAR_WORKFLOW.md` - 数据主体请求流程
- `data_governance/DATA_CLASSIFICATION.md` - 数据分级制度
