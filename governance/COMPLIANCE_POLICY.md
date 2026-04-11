# COMPLIANCE_POLICY.md - 合规策略

## 目的
定义系统合规要求，确保系统行为符合法律法规、行业标准和用户期望。

## 适用范围
所有系统操作，特别是涉及敏感数据、外部交互、用户权益的场景。

## 合规框架

### 合规层级
| 层级 | 说明 | 来源 |
|------|------|------|
| L1 法律法规 | 国家法律法规要求 | 法律法规 |
| L2 行业标准 | 行业最佳实践 | 行业规范 |
| L3 平台规则 | 平台使用规则 | 平台政策 |
| L4 用户约定 | 用户明确约定 | 用户协议 |

## 合规领域

### 1. 数据合规
| 要求 | 说明 | 实现文件 |
|------|------|----------|
| 数据最小化 | 只收集必要数据 | MEMORY_POLICY.md |
| 数据加密 | 敏感数据加密存储 | SECRET_MANAGE.md |
| 数据脱敏 | 输出时脱敏处理 | OUTPUT_VALIDATOR.md |
| 数据删除 | 支持用户删除请求 | MEMORY_POLICY.md |

### 2. 隐私合规
| 要求 | 说明 | 实现文件 |
|------|------|----------|
| 隐私保护 | 不泄露用户隐私 | BOUNDARY.json |
| 访问控制 | 限制隐私数据访问 | TOOL_GUARDRAILS.json |
| 用户知情 | 用户知道数据用途 | USER.md |
| 用户控制 | 用户可控制数据 | MEMORY_POLICY.md |

### 3. 安全合规
| 要求 | 说明 | 实现文件 |
|------|------|----------|
| 访问控制 | 权限最小化 | RISK_POLICY.md |
| 操作审计 | 记录所有操作 | AUDIT_POLICY.md |
| 安全边界 | 禁止危险操作 | BOUNDARY.json |
| 异常检测 | 检测异常行为 | ALERT_POLICY.md |

### 4. 内容合规
| 要求 | 说明 | 实现文件 |
|------|------|----------|
| 内容安全 | 不生成有害内容 | REFUSAL_POLICY.md |
| 信息准确 | 不编造虚假信息 | UNCERTAINTY_POLICY.md |
| 来源标注 | 标注信息来源 | CITATION_POLICY.md |
| 版权尊重 | 尊重知识产权 | BOUNDARIES.md |

## 行业专属合规

### 金融领域
| 要求 | 说明 | 实现文件 |
|------|------|----------|
| 风险披露 | 投资建议需披露风险 | FINANCE_SUITE.md |
| 合规审查 | 金融操作需审查 | COMPLIANCE_MATRIX.md |
| 交易记录 | 记录所有交易 | AUDIT_POLICY.md |

### 法律领域
| 要求 | 说明 | 实现文件 |
|------|------|----------|
| 免责声明 | 法律建议需免责 | LEGAL_SUITE.md |
| 信息来源 | 标注法律依据 | CITATION_POLICY.md |
| 保密义务 | 保护客户信息 | BOUNDARY.json |

### 医疗领域
| 要求 | 说明 | 实现文件 |
|------|------|----------|
| 免责声明 | 医疗建议需免责 | DOMAIN_ROUTING.md |
| 专业建议 | 建议咨询专业人士 | REFUSAL_POLICY.md |
| 隐私保护 | 保护健康信息 | BOUNDARY.json |

## 合规检查

### 检查流程
```
操作请求
    ↓
┌─────────────────────────────────────┐
│ 1. 识别合规要求                      │
│    - 确定操作类型                    │
│    - 匹配合规规则                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 执行合规检查                      │
│    - 数据合规检查                    │
│    - 隐私合规检查                    │
│    - 安全合规检查                    │
│    - 内容合规检查                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 合规决策                          │
│    - 通过 → 执行操作                 │
│    - 不通过 → 拒绝或调整             │
└─────────────────────────────────────┘
    ↓
执行/拒绝
```

### 检查规则
```yaml
compliance_checks:
  data:
    - check: data_minimization
      rule: "只收集必要数据"
      action: reject_if_excessive
    
    - check: sensitive_data_handling
      rule: "敏感数据需加密"
      action: encrypt_before_store
  
  privacy:
    - check: user_consent
      rule: "用户已知情同意"
      action: verify_consent
    
    - check: access_control
      rule: "最小权限原则"
      action: enforce_least_privilege
  
  security:
    - check: dangerous_operation
      rule: "禁止危险操作"
      action: block_and_alert
    
    - check: audit_logging
      rule: "记录所有操作"
      action: log_all_operations
  
  content:
    - check: harmful_content
      rule: "不生成有害内容"
      action: filter_content
    
    - check: source_attribution
      rule: "标注信息来源"
      action: add_citations
```

## 合规报告

### 报告结构
```json
{
  "reportId": "compliance_report_001",
  "period": "2026-04",
  "summary": {
    "totalOperations": 10000,
    "compliantOperations": 9950,
    "nonCompliantOperations": 50,
    "complianceRate": 0.995
  },
  "byDomain": {
    "data": {"compliant": 2500, "nonCompliant": 10},
    "privacy": {"compliant": 2500, "nonCompliant": 15},
    "security": {"compliant": 2500, "nonCompliant": 5},
    "content": {"compliant": 2450, "nonCompliant": 20}
  },
  "issues": [
    {
      "type": "content_compliance",
      "description": "未标注信息来源",
      "count": 20,
      "resolution": "已添加引用标注"
    }
  ]
}
```

## 合规违规处理

### 违规分级
| 级别 | 说明 | 处理方式 |
|------|------|----------|
| 轻微 | 技术性违规 | 记录 + 提示 |
| 一般 | 影响用户体验 | 记录 + 修正 |
| 严重 | 影响用户权益 | 记录 + 告警 + 修正 |
| 重大 | 法律风险 | 记录 + 告警 + 上报 |

### 违规记录
```json
{
  "violationId": "viol_001",
  "timestamp": "2026-04-06T10:32:00+08:00",
  "type": "content_compliance",
  "severity": "minor",
  "description": "未标注信息来源",
  "context": {
    "operation": "web_search",
    "content": "..."
  },
  "resolution": {
    "action": "add_citation",
    "status": "resolved"
  }
}
```

## 合规培训

### 培训内容
| 内容 | 说明 | 频率 |
|------|------|------|
| 合规规则 | 学习合规规则 | 新规则发布时 |
| 案例分析 | 分析违规案例 | 每周 |
| 最佳实践 | 学习最佳实践 | 每月 |

### 培训记录
```yaml
training_records:
  - date: 2026-04-06
    topic: "数据合规最佳实践"
    participants: [system]
    outcome: "已更新数据最小化规则"
```

## 异常处理

| 异常 | 处理 |
|------|------|
| 合规规则冲突 | 按层级优先级处理 |
| 合规检查失败 | 拒绝操作 + 记录 |
| 合规报告失败 | 缓存 + 稍后重试 |

## 维护方式
- 新增合规要求: 添加到对应领域
- 调整合规规则: 更新检查规则
- 新增行业合规: 创建行业套件

## 引用文件
- `governance/GOVERNANCE_POLICY.md` - 治理总策略
- `safety/RISK_POLICY.md` - 风险策略
- `safety/BOUNDARY.json` - 安全边界
- `domain_agents/COMPLIANCE_MATRIX.md` - 合规矩阵
- `audit/AUDIT_POLICY.md` - 审计策略
