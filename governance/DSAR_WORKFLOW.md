# DSAR_WORKFLOW.md - 数据主体请求流程

## 目的
定义数据主体请求（DSAR）的处理流程，确保用户权利得到保障。

## 适用范围
平台所有数据主体请求的处理场景。

## 与其他模块联动
| 模块 | 联动内容 |
|------|----------|
| privacy | 隐私治理框架 |
| data_governance | 数据管理 |
| audit | 请求审计 |
| compliance | 合规检查 |

## 请求类型

### 支持的请求类型
| 类型 | 说明 | 法律依据 |
|------|------|----------|
| 查询请求 | 查询个人数据 | 知情权 |
| 更正请求 | 更正不准确数据 | 更正权 |
| 删除请求 | 删除个人数据 | 删除权 |
| 导出请求 | 导出个人数据 | 携带权 |
| 限制处理请求 | 限制数据处理 | 限制处理权 |
| 反对处理请求 | 反对特定处理 | 反对权 |

### 请求定义
```yaml
request_types:
  access:
    name: "查询请求"
    description: "数据主体请求查询其个人数据"
    response_requirement: "提供数据副本"
    time_limit: 30_days
  
  rectification:
    name: "更正请求"
    description: "数据主体请求更正不准确的数据"
    response_requirement: "更正或说明拒绝原因"
    time_limit: 30_days
  
  erasure:
    name: "删除请求"
    description: "数据主体请求删除其个人数据"
    response_requirement: "删除或说明拒绝原因"
    time_limit: 30_days
  
  portability:
    name: "导出请求"
    description: "数据主体请求导出其个人数据"
    response_requirement: "提供结构化数据"
    time_limit: 30_days
  
  restriction:
    name: "限制处理请求"
    description: "数据主体请求限制数据处理"
    response_requirement: "限制处理或说明拒绝原因"
    time_limit: 30_days
  
  objection:
    name: "反对处理请求"
    description: "数据主体反对特定数据处理"
    response_requirement: "停止处理或说明理由"
    time_limit: 30_days
```

## 请求验证

### 身份验证
| 验证方式 | 说明 | 适用场景 |
|----------|------|----------|
| 账号登录 | 已登录用户 | 在线请求 |
| 邮箱验证 | 邮箱确认 | 离线请求 |
| 身份证明 | 身份证件 | 高敏感请求 |
| 多因素验证 | MFA验证 | 高风险请求 |

### 验证流程
```yaml
verification_flow:
  steps:
    - name: "接收请求"
      actions:
        - record_request
        - assign_request_id
        - send_acknowledgment
    
    - name: "身份验证"
      actions:
        - verify_identity
        - check_account_status
        - confirm_authorization
    
    - name: "请求验证"
      actions:
        - validate_request_type
        - check_request_scope
        - assess_feasibility
    
    - name: "验证结果"
      actions:
        - approve_or_reject
        - notify_requester
        - proceed_or_close
```

## 处理流程

### 标准处理流程
```
请求接收
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. 请求登记                                                  │
│    - 分配请求ID                                              │
│    - 记录请求信息                                            │
│    - 发送确认通知                                            │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. 身份验证                                                  │
│    - 验证请求者身份                                          │
│    - 确认请求权限                                            │
│    - 记录验证结果                                            │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. 请求评估                                                  │
│    - 评估请求范围                                            │
│    - 识别相关数据                                            │
│    - 检查法律例外                                            │
└─────────────────────────────────────────────────────────────┐
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. 请求执行                                                  │
│    - 收集相关数据                                            │
│    - 执行请求操作                                            │
│    - 验证执行结果                                            │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. 响应发送                                                  │
│    - 准备响应内容                                            │
│    - 发送给请求者                                            │
│    - 记录响应日志                                            │
└─────────────────────────────────────────────────────────────┘
```

### 各类型处理细则

#### 查询请求处理
```yaml
access_request_handling:
  steps:
    - name: "数据收集"
      actions:
        - search_all_systems
        - collect_personal_data
        - identify_third_party_sharing
    
    - name: "数据整理"
      actions:
        - organize_by_category
        - format_for_readability
        - apply_appropriate_masking
    
    - name: "响应准备"
      actions:
        - prepare_data_summary
        - include_data_categories
        - explain_data_usage
```

#### 删除请求处理
```yaml
erasure_request_handling:
  steps:
    - name: "影响评估"
      actions:
        - identify_all_data
        - assess_deletion_impact
        - check_legal_exceptions
    
    - name: "例外检查"
      exceptions:
        - legal_obligation
        - legal_claims
        - public_interest
        - legitimate_interest
    
    - name: "执行删除"
      actions:
        - delete_primary_data
        - delete_backups
        - notify_third_parties
        - verify_deletion
```

#### 导出请求处理
```yaml
portability_request_handling:
  steps:
    - name: "数据收集"
      actions:
        - collect_provided_data
        - exclude_derived_data
        - format_structured_output
    
    - name: "格式准备"
      formats:
        - json
        - csv
        - xml
    
    - name: "安全传输"
      actions:
        - encrypt_data
        - secure_delivery
        - verify_receipt
```

## 处理时限

### 时限要求
| 阶段 | 时限 | 说明 |
|------|------|------|
| 确认接收 | 3天 | 确认收到请求 |
| 身份验证 | 7天 | 完成身份验证 |
| 请求处理 | 30天 | 完成请求处理 |
| 响应发送 | 2天 | 发送处理结果 |

### 时限延长
```yaml
deadline_extension:
  conditions:
    - complex_request
    - high_volume_requests
    - verification_difficulties
  
  max_extension: 60_days
  notification_required: true
  justification_required: true
```

## 审计记录

### 审计内容
```json
{
  "request_id": "dsar_001",
  "request_type": "access",
  "requester": {
    "user_id": "user_001",
    "verified_identity": true,
    "verification_method": "account_login"
  },
  "request_details": {
    "submitted_at": "2026-04-01T10:00:00+08:00",
    "request_scope": "all_personal_data",
    "preferred_format": "json"
  },
  "processing": {
    "assigned_to": "privacy_team",
    "started_at": "2026-04-02T09:00:00+08:00",
    "completed_at": "2026-04-10T17:00:00+08:00",
    "actions_taken": [
      "data_collection",
      "data_organization",
      "response_preparation"
    ]
  },
  "response": {
    "sent_at": "2026-04-11T10:00:00+08:00",
    "response_type": "fullfilled",
    "delivery_method": "secure_download",
    "data_categories_included": 5,
    "records_included": 150
  },
  "audit": {
    "total_processing_days": 10,
    "within_deadline": true,
    "compliance_verified": true
  }
}
```

## 拒绝处理

### 拒绝理由
| 理由 | 说明 |
|------|------|
| 身份无法验证 | 无法确认请求者身份 |
| 请求范围不清 | 请求范围不明确 |
| 法律例外 | 法律规定不得处理 |
| 侵犯他人权利 | 可能侵犯第三方权利 |
| 技术不可行 | 技术上无法实现 |

### 拒绝通知
```yaml
rejection_notification:
  required_content:
    - rejection_reason
    - legal_basis
    - appeal_rights
    - complaint_options
  
  format:
    - clear_explanation
    - reference_to_law
    - next_steps_guidance
```

## 投诉处理

### 投诉渠道
| 渠道 | 说明 |
|------|------|
| 内部投诉 | 向隐私团队投诉 |
| 监管投诉 | 向监管机构投诉 |
| 司法途径 | 通过法院解决 |

### 投诉记录
```yaml
complaint_recording:
  required:
    - complaint_content
    - complaint_date
    - handling_process
    - resolution_result
  
  retention: 5_years
```

## 引用文件
- `privacy/PRIVACY_FRAMEWORK.md` - 隐私治理框架
- `privacy/PII_HANDLING.md` - PII处理规则
- `data_governance/DATA_RETENTION_MATRIX.json` - 数据保留矩阵
- `audit/AUDIT_POLICY.md` - 审计策略
