# USE_CASE_APPROVAL_POLICY.md - AI 用例上线审批规则

## 目的
定义 AI 用例上线审批规则，确保 AI 应用符合组织治理要求。

## 适用范围
- 所有 AI 用例上线
- 所有 AI 用例变更
- 所有 AI 用例退役

## 审批分类

### 必须审批
```yaml
mandatory_approval:
  criteria:
    - 涉及自动化决策
    - 处理敏感数据
    - 影响客户权益
    - 涉及外部用户
    - 高风险模型
    - 新技术应用
  
  process:
    - 提交用例申请
    - 风险评估
    - 安全评审
    - 合规评审
    - 业务审批
    - 技术审批
    - 治理委员会终审（高风险）
```

### 快速通道
```yaml
fast_track:
  criteria:
    - 低风险用例
    - 内部辅助用途
    - 无敏感数据
    - 无自动化决策
    - 可逆操作
  
  process:
    - 提交简化申请
    - 自动风险评估
    - AI 治理官审批
    - 即时上线
  
  timeline: "3 个工作日"
```

### 增强评审
```yaml
enhanced_review:
  criteria:
    - 关键业务影响
    - 大规模用户影响
    - 法律合规风险
    - 不可逆决策
    - 高敏感数据
  
  additional_steps:
    - 法律部门评审
    - 隐私影响评估
    - 安全渗透测试
    - 外部专家咨询
    - 管理层审批
    - 董事会备案（极高风险）
  
  timeline: "30 个工作日"
```

### 禁止上线
```yaml
prohibited:
  criteria:
    - 违反法律法规
    - 侵犯用户权益
    - 无法解释的决策
    - 无人工监督的高风险决策
    - 监管明确禁止
  
  action: "拒绝申请并记录"
```

## 审批流程

```yaml
approval_process:
  step_1_submission:
    action: "提交用例申请"
    content:
      - 用例描述
      - 业务目标
      - 数据需求
      - 模型选择
      - 风险自评
      - 人工监督计划
  
  step_2_risk_assessment:
    action: "风险评估"
    output: "风险等级评定"
    reviewer: "AI 治理官"
  
  step_3_technical_review:
    action: "技术评审"
    content:
      - 模型验证
      - 安全评估
      - 性能测试
    reviewer: "技术负责人"
  
  step_4_compliance_review:
    action: "合规评审"
    content:
      - 合规检查
      - 隐私评估
      - 法律审核
    reviewer: "合规负责人"
  
  step_5_business_approval:
    action: "业务审批"
    reviewer: "业务负责人"
  
  step_6_final_approval:
    action: "终审"
    reviewer: "根据风险等级确定"
```

## 审批时限

| 风险等级 | 审批时限 | 审批人 |
|----------|----------|--------|
| 低 | 3 天 | AI 治理官 |
| 中 | 7 天 | 部门负责人 |
| 高 | 14 天 | 管理层 |
| 极高 | 30 天 | 治理委员会 |

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
