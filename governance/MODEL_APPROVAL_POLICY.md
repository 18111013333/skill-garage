# MODEL_APPROVAL_POLICY.md - 模型上线审批规则

## 目的
定义新模型引入、上线、变更的审批流程和规则。

## 适用范围
平台所有模型的引入、上线、变更、下线场景。

## 与其他模块联动
| 模块 | 联动内容 |
|------|----------|
| model_governance | 模型注册与风险分层 |
| tenancy | 租户模型权限 |
| access | 模型访问控制 |
| audit | 模型审批审计 |
| compliance | 模型合规检查 |
| console | 模型管理界面 |

## 审批流程

### 标准审批流程
```
模型引入申请
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. 技术评审                                                  │
│    - 技术可行性评估                                          │
│    - 性能指标验证                                            │
│    - 集成方案评审                                            │
└─────────────────────────────────────────────────────────────┘
    │ 通过
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. 安全评审                                                  │
│    - 安全风险评估                                            │
│    - 数据处理评估                                            │
│    - 漏洞扫描                                                │
└─────────────────────────────────────────────────────────────┘
    │ 通过
    ▼
┌─────────────────────────────────────────────────────────────
│ 3. 合规评审（高风险模型）                                    │
│    - 法律合规评估                                            │
│    - 隐私影响评估                                            │
│    - 监管要求检查                                            │
└─────────────────────────────────────────────────────────────
    │ 通过
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. 治理委员会审批                                            │
│    - 综合评估                                                │
│    - 风险决策                                                │
│    - 批准/拒绝                                               │
└─────────────────────────────────────────────────────────────┘
    │ 批准
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. 灰度部署                                                  │
│    - Canary测试                                              │
│    - 监控验证                                                │
│    - 逐步推广                                                │
└─────────────────────────────────────────────────────────────┘
    │ 验证通过
    ▼
正式上线
```

## 审批条件

### 新模型引入条件
| 条件 | 说明 | 验证方式 |
|------|------|----------|
| 技术可行性 | 技术方案可行 | 技术评审 |
| 性能达标 | 性能指标满足要求 | 性能测试 |
| 安全合规 | 无安全风险 | 安全评审 |
| 成本可控 | 成本在预算内 | 成本评估 |
| 用途明确 | 使用场景明确 | 需求文档 |

### 必须通过的测试
| 测试类型 | 测试内容 | 通过标准 |
|----------|----------|----------|
| 功能测试 | 核心功能验证 | 100% 通过 |
| 性能测试 | 响应时间、吞吐量 | 满足SLA |
| 安全测试 | 漏洞扫描、渗透测试 | 无高危漏洞 |
| 隐私测试 | PII处理验证 | 符合隐私策略 |
| 集成测试 | 系统集成验证 | 无兼容问题 |
| 回归测试 | 现有功能验证 | 无回归问题 |

### 租户/领域限制
```yaml
tenant_domain_restrictions:
  # 默认规则
  default:
    all_tenants: false        # 新模型默认不对所有租户开放
    all_domains: false        # 新模型默认不对所有领域开放
  
  # 限制场景
  restricted_scenarios:
    - name: "金融领域"
      condition: "模型风险等级 > 低风险"
      action: "需额外审批"
    
    - name: "医疗领域"
      condition: "模型涉及健康数据处理"
      action: "需合规审批"
    
    - name: "法律领域"
      condition: "模型提供法律建议"
      action: "禁止使用"
    
    - name: "儿童服务"
      condition: "目标用户包含未成年人"
      action: "需特殊审批"
```

## Canary部署规则

### Canary条件
| 条件 | 说明 |
|------|------|
| 标准风险模型 | 必须Canary |
| 高风险模型 | 必须Canary + 人工监督 |
| 低风险模型 | 可选Canary |

### Canary配置
```yaml
canary_config:
  # 流量分配
  traffic_allocation:
    initial: 1               # 初始1%流量
    increment: 5              # 每次增加5%
    max: 50                   # 最大50%
  
  # 观察周期
  observation_period:
    duration: 24h            # 每阶段观察24小时
    metrics:
      - error_rate
      - latency_p99
      - quality_score
      - user_feedback
  
  # 回滚条件
  rollback_conditions:
    - error_rate > 1%
    - latency_p99 > baseline * 2
    - quality_score < 0.8
    - user_complaints > threshold
```

### Canary阶段
| 阶段 | 流量 | 持续时间 | 验证内容 |
|------|------|----------|----------|
| 阶段1 | 1% | 24小时 | 基本功能 |
| 阶段2 | 5% | 24小时 | 性能指标 |
| 阶段3 | 10% | 24小时 | 稳定性 |
| 阶段4 | 25% | 48小时 | 全面验证 |
| 阶段5 | 50% | 48小时 | 最终确认 |

## 人工批准场景

### 必须人工批准
| 场景 | 说明 |
|------|------|
| 高风险模型 | 风险等级为高的模型 |
| 敏感领域 | 金融、医疗、法律领域 |
| 大规模影响 | 影响超过50%用户 |
| 成本超限 | 成本超过预算20% |
| 合规风险 | 存在合规风险 |

### 审批权限
| 审批类型 | 审批人 | 审批时限 |
|----------|--------|----------|
| 技术审批 | 技术负责人 | 3个工作日 |
| 安全审批 | 安全负责人 | 5个工作日 |
| 合规审批 | 合规负责人 | 7个工作日 |
| 委员会审批 | 治理委员会 | 10个工作日 |

## 审批记录

### 审批申请格式
```json
{
  "approval_id": "approval_001",
  "model_id": "model_new",
  "model_name": "NEW_MODEL_V1",
  "applicant": "user_001",
  "applicant_role": "developer",
  "request_type": "new_model_introduction",
  "risk_tier": "standard",
  "intended_use": ["general_qa", "content_generation"],
  "target_tenants": ["tenant_001", "tenant_002"],
  "target_domains": ["customer_service", "content"],
  "justification": "提升问答质量和内容生成能力",
  "technical_review": {
    "reviewer": "tech_lead",
    "status": "approved",
    "comments": "技术方案可行",
    "reviewed_at": "2026-04-06T10:00:00+08:00"
  },
  "security_review": {
    "reviewer": "security_lead",
    "status": "approved",
    "comments": "安全风险可控",
    "reviewed_at": "2026-04-06T12:00:00+08:00"
  },
  "board_approval": {
    "approver": "governance_board",
    "status": "pending",
    "meeting_date": "2026-04-07"
  }
}
```

## 快速审批通道

### 适用条件
| 条件 | 说明 |
|------|------|
| 低风险模型 | 风险等级为低 |
| 紧急修复 | 安全漏洞修复 |
| 小版本更新 | 仅minor版本变更 |
| 内部测试 | 仅限测试环境 |

### 快速审批流程
```yaml
fast_track:
  conditions:
    - risk_tier == "low"
    - change_type == "minor_update"
    - environment == "staging"
  
  process:
    - auto_technical_review
    - auto_security_scan
    - auto_approval
  
  timeline: "4小时"
```

## 异常处理

| 异常 | 处理 |
|------|------|
| 审批超时 | 自动升级处理 |
| 审批拒绝 | 记录原因，可申诉 |
| 测试失败 | 返回修复，重新审批 |
| Canary失败 | 自动回滚，分析原因 |

## 引用文件
- `model_governance/MODEL_REGISTRY.json` - 模型注册表
- `model_governance/MODEL_RISK_TIERING.md` - 模型风险分层
- `model_governance/MODEL_CHANGE_CONTROL.md` - 模型变更控制
- `audit/AUDIT_POLICY.md` - 审计策略
