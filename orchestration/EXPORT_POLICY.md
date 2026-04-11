# EXPORT_POLICY.md - 导出规则

## 目的
定义平台数据导出的规则，确保导出行为可控、可审计、可追溯。

## 适用范围
平台所有数据导出、下载、传输场景。

## 与其他模块联动
| 模块 | 联动内容 |
|------|----------|
| reporting | 报表导出 |
| data_governance | 数据分级导出 |
| privacy | 隐私数据导出 |
| audit | 导出审计 |
| compliance | 合规导出 |

## 导出分类

### 按数据类型分类
| 类型 | 说明 | 导出限制 |
|------|------|----------|
| 运营数据 | 日常运营数据 | 角色授权 |
| 财务数据 | 计费成本数据 | 需审批 |
| 审计数据 | 操作审计数据 | 需审批 |
| 用户数据 | 用户相关数据 | 用户本人或审批 |
| 系统数据 | 系统配置数据 | 管理员权限 |

### 按敏感级别分类
| 级别 | 说明 | 导出规则 |
|------|------|----------|
| L0 公开 | 无敏感风险 | 允许导出 |
| L1 内部 | 内部使用 | 角色授权导出 |
| L2 敏感 | 敏感信息 | 需审批+脱敏 |
| L3 受限 | 高敏感信息 | 禁止导出或特批 |

## 可导出报表

### 允许导出报表
| 报表类型 | 导出格式 | 审批要求 | 脱敏要求 |
|----------|----------|----------|----------|
| 运营日报 | CSV, JSON | 无 | 无 |
| 性能报表 | CSV, JSON | 无 | 无 |
| 使用统计 | CSV, JSON | 无 | 聚合数据 |
| 错误统计 | CSV, JSON | 无 | 无详情 |
| 审计摘要 | PDF | 需审批 | 脱敏 |
| 合规报告 | PDF | 需审批 | 按需 |

### 禁止导出数据
| 数据类型 | 说明 | 例外条件 |
|----------|------|----------|
| 原始日志 | 完整操作日志 | 合规审计需要 |
| 用户输入 | 用户原始输入 | 用户本人请求 |
| 会话内容 | 完整会话记录 | 法律要求 |
| PII数据 | 个人身份信息 | DSAR请求 |
| 认证信息 | 密码、密钥 | 禁止 |

## 角色导出权限

### 权限矩阵
| 角色 | 运营数据 | 财务数据 | 审计数据 | 用户数据 | 系统数据 |
|------|----------|----------|----------|----------|----------|
| 普通用户 | 无 | 无 | 无 | 本人 | 无 |
| 运营人员 | 授权范围 | 无 | 无 | 无 | 无 |
| 财务人员 | 无 | 授权范围 | 无 | 无 | 无 |
| 审计人员 | 无 | 无 | 授权范围 | 审批 | 无 |
| 管理员 | 全部 | 审批 | 审批 | 审批 | 全部 |

### 权限配置
```yaml
export_permissions:
  operator:
    allowed:
      - operational_reports
      - performance_reports
    restricted:
      - financial_reports
    forbidden:
      - user_data
      - audit_logs
  
  finance:
    allowed:
      - financial_reports
      - billing_reports
    restricted:
      - operational_reports
    forbidden:
      - user_data
      - audit_logs
  
  auditor:
    allowed:
      - audit_reports
      - compliance_reports
    restricted:
      - operational_reports
      - financial_reports
    forbidden: []
  
  admin:
    allowed:
      - all_reports
    restricted: []
    forbidden:
      - raw_pii_data
```

## 租户导出限制

### 租户差异化规则
```yaml
tenant_export_rules:
  # 基础租户
  basic_tenant:
    max_export_size: 10MB
    max_export_count: 10/day
    allowed_formats: [csv, json]
    approval_required: false
  
  # 标准租户
  standard_tenant:
    max_export_size: 100MB
    max_export_count: 50/day
    allowed_formats: [csv, json, pdf]
    approval_required: false
  
  # 高级租户
  premium_tenant:
    max_export_size: 1GB
    max_export_count: 100/day
    allowed_formats: [csv, json, pdf, xlsx]
    approval_required: false
  
  # 企业租户
  enterprise_tenant:
    max_export_size: unlimited
    max_export_count: unlimited
    allowed_formats: all
    approval_required: configurable
```

## 高敏导出审批

### 需审批场景
| 场景 | 说明 | 审批人 |
|------|------|--------|
| 敏感数据导出 | L2及以上数据 | 数据负责人 |
| 大批量导出 | 超过租户限制 | 租户管理员 |
| 跨租户导出 | 涉及其他租户 | 双方管理员 |
| 外部传输 | 导出到外部系统 | 安全负责人 |
| 历史数据 | 超过保留期数据 | 合规负责人 |

### 审批流程
```yaml
export_approval_flow:
  steps:
    - name: "提交申请"
      actions:
        - specify_export_scope
        - justify_purpose
        - select_format
    
    - name: "风险评估"
      actions:
        - assess_data_sensitivity
        - evaluate_export_risk
        - check_compliance
    
    - name: "审批决策"
      actions:
        - reviewer_approval
        - apply_conditions
        - set_expiry
    
    - name: "执行导出"
      actions:
        - apply_masking
        - generate_export
        - audit_record
```

## 导出格式规范

### 格式要求
| 格式 | 适用场景 | 安全要求 |
|------|----------|----------|
| JSON | 数据交换 | 结构化、可验证 |
| CSV | 表格数据 | 无公式、无宏 |
| PDF | 报告文档 | 只读、可签名 |
| XLSX | 复杂报表 | 无宏、无脚本 |
| HTML | 在线查看 | 无脚本 |

### 格式安全检查
```yaml
format_security:
  csv:
    checks:
      - no_formula_injection
      - no_macro_commands
    encoding: "utf-8"
  
  xlsx:
    checks:
      - no_vba_macros
      - no_external_links
    protection: "read_only"
  
  pdf:
    checks:
      - no_javascript
      - no_embedded_files
    security: "password_optional"
  
  json:
    checks:
      - valid_json_format
      - no_script_injection
    encoding: "utf-8"
```

## 导出审计

### 审计记录
```json
{
  "export_id": "export_001",
  "export_type": "report",
  "export_content": "operational_daily_report",
  "export_format": "csv",
  "export_size": "1.2MB",
  "exporter": "user_001",
  "exporter_role": "operator",
  "tenant_id": "tenant_001",
  "export_time": "2026-04-06T22:00:00+08:00",
  "approval_id": "approval_001",
  "data_sensitivity": "L1",
  "masking_applied": false,
  "download_time": "2026-04-06T22:05:00+08:00",
  "download_ip": "192.168.1.1"
}
```

### 审计要求
| 要求 | 说明 |
|------|------|
| 全量记录 | 所有导出必须记录 |
| 保留期限 | 审计记录保留3年 |
| 定期审查 | 月度审查导出行为 |
| 异常告警 | 异常导出实时告警 |

## 导出限制

### 技术限制
```yaml
export_limits:
  size_limits:
    single_file: 500MB
    total_daily: 2GB
    total_monthly: 50GB
  
  rate_limits:
    per_minute: 5
    per_hour: 20
    per_day: 100
  
  concurrent_limits:
    max_concurrent: 3
    queue_size: 10
```

### 内容限制
```yaml
content_restrictions:
  forbidden_content:
    - raw_passwords
    - encryption_keys
    - auth_tokens
    - biometric_data
  
  required_masking:
    - phone_numbers
    - email_addresses
    - id_numbers
    - ip_addresses
```

## 引用文件
- `reporting/REPORT_SCHEMA.json` - 报表结构
- `reporting/SCHEDULED_REPORTS.md` - 定时报表
- `data_governance/DATA_CLASSIFICATION.md` - 数据分级
- `audit/AUDIT_POLICY.md` - 审计策略
