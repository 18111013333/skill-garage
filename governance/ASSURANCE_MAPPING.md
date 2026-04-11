# ASSURANCE_MAPPING.md - 平台能力与外部要求映射

## 目的
定义平台能力与外部 assurance 要求的映射，快速响应合规问询。

## 适用范围
- 所有外部合规要求
- 所有客户安全问卷
- 所有监管问询

## 能力映射表

### 安全控制映射
```yaml
security_controls:
  access_control:
    requirement: "访问控制"
    platform_capabilities:
      - RBAC 权限管理
      - 多因素认证
      - 单点登录
      - 会话管理
    evidence:
      - access/RBAC_POLICY.md
      - access/PERMISSION_MATRIX.md
  
  data_protection:
    requirement: "数据保护"
    platform_capabilities:
      - 数据分类标记
      - 加密存储
      - 加密传输
      - 数据脱敏
    evidence:
      - data_governance/DATA_CLASSIFICATION.md
      - privacy/PII_HANDLING.md
  
  incident_response:
    requirement: "事件响应"
    platform_capabilities:
      - 事件检测
      - 分级响应
      - 根因分析
      - 恢复机制
    evidence:
      - incident/INCIDENT_SEVERITY.md
      - reliability/SLA_POLICY.md
```

### 隐私控制映射
```yaml
privacy_controls:
  consent_management:
    requirement: "同意管理"
    platform_capabilities:
      - 同意收集
      - 同意记录
      - 同意撤回
    evidence:
      - privacy/CONSENT_AND_PURPOSE_LIMITATION.md
  
  data_subject_rights:
    requirement: "数据主体权利"
    platform_capabilities:
      - DSAR 处理
      - 数据导出
      - 数据删除
    evidence:
      - privacy/DSAR_WORKFLOW.md
  
  cross_border_transfer:
    requirement: "跨境传输"
    platform_capabilities:
      - 传输审批
      - 标准合同条款
      - 传输记录
    evidence:
      - privacy/PRIVACY_FRAMEWORK.md
```

### 审计能力映射
```yaml
audit_capabilities:
  logging:
    requirement: "审计日志"
    platform_capabilities:
      - 操作日志
      - 访问日志
      - 变更日志
      - 日志保护
    evidence:
      - audit/AUDIT_LOG_POLICY.md
  
  reporting:
    requirement: "审计报告"
    platform_capabilities:
      - 合规报告
      - 安全报告
      - 自定义报告
    evidence:
      - reporting/REPORTING_SCHEMA.json
```

### 可靠性承诺映射
```yaml
reliability_commitments:
  availability:
    requirement: "可用性承诺"
    platform_capabilities:
      - 高可用架构
      - 故障转移
      - 灾难恢复
    evidence:
      - reliability/SLA_POLICY.md
      - reliability/SLO_DEFINITIONS.json
  
  business_continuity:
    requirement: "业务连续性"
    platform_capabilities:
      - 备份恢复
      - BCP 计划
      - 演练记录
    evidence:
      - resilience/BUSINESS_CONTINUITY_PLAN.md
```

### 证据链映射
```yaml
evidence_chain:
  traceability:
    requirement: "可追溯性"
    platform_capabilities:
      - 决策日志
      - 证据链记录
      - 来源追溯
    evidence:
      - evidence/EVIDENCE_CHAIN_POLICY.md
      - evidence/CLAIM_TO_SOURCE_MAPPING.md
```

### 数据治理映射
```yaml
data_governance:
  data_quality:
    requirement: "数据质量"
    platform_capabilities:
      - 数据验证
      - 数据清洗
      - 质量监控
    evidence:
      - data_governance/DATA_LINEAGE.md
  
  data_retention:
    requirement: "数据保留"
    platform_capabilities:
      - 保留策略
      - 自动清理
      - 保留记录
    evidence:
      - data_governance/DATA_RETENTION_MATRIX.json
```

## 快速响应模板

```yaml
response_template:
  for_requirement:
    structure:
      - 要求描述
      - 平台对应能力
      - 证据引用
      - 联系人
    timeline: "根据要求复杂度"
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
