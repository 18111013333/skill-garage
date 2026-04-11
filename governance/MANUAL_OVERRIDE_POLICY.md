# MANUAL_OVERRIDE_POLICY.md - 人工覆盖与兜底规则

## 目的
定义人工覆盖与人工兜底规则，确保人工干预可控可追溯。

## 适用范围
- 所有 AI 自动决策
- 所有系统自动执行
- 所有自动化流程

## 覆盖场景

### 允许覆盖
```yaml
allowed_override:
  scenarios:
    - 系统判断错误
    - 特殊情况处理
    - 紧急业务需求
    - 用户明确请求
    - 合规要求
  
  conditions:
    - 有明确业务理由
    - 不违反安全政策
    - 不违反合规要求
    - 记录覆盖原因
```

### 禁止覆盖
```yaml
prohibited_override:
  scenarios:
    - 绕过安全控制
    - 规避审计记录
    - 违反合规要求
    - 恶意目的
  
  action: "拒绝并报告"
```

## 覆盖权限

```yaml
override_authority:
  low_risk:
    approver: "操作人员"
    process: "自行决定 + 记录"
  
  medium_risk:
    approver: "主管"
    process: "申请 + 审批 + 记录"
  
  high_risk:
    approver: "部门负责人"
    process: "申请 + 审核 + 审批 + 记录"
  
  critical:
    approver: "管理层"
    process: "正式申请 + 多级审批 + 详细记录"
```

## 覆盖流程

```yaml
override_process:
  step_1_request:
    action: "提出覆盖请求"
    content:
      - 覆盖对象
      - 覆盖原因
      - 预期结果
      - 风险评估
  
  step_2_approval:
    action: "审批覆盖请求"
    output: "审批决定"
  
  step_3_execution:
    action: "执行覆盖"
    output: "执行记录"
  
  step_4_verification:
    action: "验证覆盖结果"
    output: "验证记录"
  
  step_5_review:
    action: "事后复核"
    output: "复核报告"
```

## 记录要求

```yaml
record_requirements:
  mandatory_fields:
    - 覆盖时间
    - 覆盖人员
    - 覆盖对象
    - 覆盖原因
    - 审批人
    - 执行结果
  
  retention: "5 年"
  audit: "纳入审计范围"
```

## 复核机制

```yaml
review_mechanism:
  frequency:
    high_risk: "即时复核"
    medium_risk: "24 小时内复核"
    low_risk: "周度抽样复核"
  
  content:
    - 覆盖是否合理
    - 流程是否合规
    - 记录是否完整
    - 是否需要改进
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
