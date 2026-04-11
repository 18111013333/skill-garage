# EVIDENCE_VAULT_POLICY.md - 证据仓规则

## 目的
定义证据仓规则，确保关键审计/监管证据不再临时拼凑。

## 适用范围
- 审计证据
- 监管证据
- 合规证据
- 事故证据

## 核心规则

### 1. 进入证据仓的证据类型

```yaml
evidence_types:
  # 治理证据
  governance:
    - AI 治理政策文件
    - 用例审批记录
    - 风险评估报告
    - 治理会议纪要
    - 培训认证记录
  
  # 合规证据
  compliance:
    - 合规评估报告
    - 整改跟踪记录
    - 控制测试记录
    - 审计报告
    - 监管响应记录
  
  # 安全证据
  security:
    - 安全评估报告
    - 漏洞扫描报告
    - 渗透测试报告
    - 安全事件记录
    - 访问审计日志
  
  # 隐私证据
  privacy:
    - 隐私影响评估
    - 数据处理记录
    - 同意管理记录
    - 数据主体请求记录
    - 跨境传输记录
  
  # 运营证据
  operations:
    - 变更管理记录
    - 事件处理记录
    - 备份恢复记录
    - 性能监控报告
    - SLA 达成报告
```

### 2. 保存格式

```yaml
storage_format:
  # 文档格式
  documents:
    preferred: "PDF/A"
    acceptable: ["PDF", "DOCX", "XLSX"]
    metadata:
      - 创建时间
      - 创建者
      - 版本号
      - 审批状态
  
  # 日志格式
  logs:
    format: "JSON"
    compression: "gzip"
    retention: "原始保留1年，压缩保留7年"
  
  # 数据格式
  data:
    format: "JSON/CSV"
    encryption: "AES-256"
    integrity: "SHA-256 哈希"
  
  # 签名格式
  signatures:
    type: "数字签名"
    algorithm: "RSA-2048"
    timestamp: "可信时间戳"
```

### 3. 完整性校验

```yaml
integrity_verification:
  # 校验方法
  methods:
    hash_verification:
      algorithm: "SHA-256"
      frequency: "每次访问"
    
    digital_signature:
      enabled: true
      verification: "每次访问"
    
    chain_of_custody:
      enabled: true
      tracking: "每次操作"
  
  # 校验频率
  frequency:
    on_access: true
    periodic: "每月"
    before_export: true
  
  # 校验失败处理
  on_failure:
    - 标记证据可疑
    - 通知证据管理员
    - 启动调查
    - 记录处理过程
```

### 4. 访问权限

```yaml
access_control:
  # 访问角色
  roles:
    evidence_admin:
      permissions: ["read", "write", "delete", "export"]
      scope: "所有证据"
    
    auditor:
      permissions: ["read", "export"]
      scope: "审计相关证据"
    
    compliance_officer:
      permissions: ["read", "export"]
      scope: "合规相关证据"
    
    investigator:
      permissions: ["read"]
      scope: "指定案件证据"
  
  # 访问审批
  approval:
    read:
      standard: "角色自动授权"
      sensitive: "证据管理员审批"
    
    export:
      all: "证据管理员 + 合规负责人审批"
    
    delete:
      all: "管理层 + 法务审批"
  
  # 访问日志
  logging:
    enabled: true
    retention: "7 年"
    content:
      - 访问者
      - 访问时间
      - 访问证据
      - 访问目的
      - 操作类型
```

### 5. 保留期

```yaml
retention_policy:
  # 按证据类型
  by_type:
    governance: "7 年"
    compliance: "7 年"
    security: "5 年"
    privacy: "7 年"
    operations: "3 年"
    incident: "10 年"
  
  # 按风险等级
  by_risk:
    critical: "永久"
    high: "10 年"
    medium: "7 年"
    low: "5 年"
  
  # 法律要求
  legal_requirements:
    - 遵守适用法律法规
    - 满足监管要求
    - 支持诉讼保全
  
  # 到期处理
  on_expiry:
    - 自动标记待删除
    - 通知证据管理员
    - 合规确认
    - 安全删除
    - 记录删除日志
```

### 6. 导出要求

```yaml
export_requirements:
  # 导出审批
  approval:
    internal_audit: "合规负责人"
    external_audit: "合规负责人 + 管理层"
    regulatory: "管理层 + 法务"
    legal: "法务 + 管理层"
  
  # 导出格式
  format:
    documents: "PDF/A"
    logs: "JSON/CSV"
    full_package: "ZIP + 清单"
  
  # 导出内容
  content:
    - 证据原件
    - 元数据
    - 完整性校验值
    - 访问历史
    - 导出记录
  
  # 导出记录
  logging:
    - 导出申请人
    - 导出时间
    - 导出内容清单
    - 导出目的
    - 接收方
    - 审批人
```

## 异常处理

### 证据损坏
- 记录损坏情况
- 尝试恢复
- 通知相关方
- 启动调查

### 访问违规
- 阻止访问
- 记录违规
- 通知管理员
- 必要时升级

### 导出风险
- 评估风险
- 限制范围
- 增加保护
- 跟踪使用

## 完成标准
- [x] 证据类型定义完整
- [x] 保存格式规范清晰
- [x] 完整性校验规则完整
- [x] 访问权限规则明确
- [x] 保留期规则清晰
- [x] 导出要求完整
- [x] 关键审计/监管证据不再临时拼凑

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
