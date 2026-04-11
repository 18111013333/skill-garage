# CONTROL_EXCEPTION_TRACKING.md - 控制例外追踪规则

## 目的
定义控制例外追踪规则，确保例外有闭环管理。

## 适用范围
- 所有控制例外
- 所有例外申请人
- 所有例外审批人

## 例外生命周期

```yaml
exception_lifecycle:
  states:
    draft: "草稿"
    pending_approval: "待审批"
    active: "生效中"
    extended: "已延期"
    closed: "已关闭"
    expired: "已过期"
```

## 例外申请

```yaml
exception_request:
  required_info:
    - 例外类型
    - 涉及控制
    - 例外原因
    - 风险评估
    - 补偿控制
    - 申请期限
    - 责任人
  
  submission:
    method: "例外申请表单"
    timeline: "例外发生前或发生后 24 小时内"
```

## 审批流程

```yaml
approval_process:
  by_risk_level:
    low:
      approver: "控制所有者"
      timeline: "2 工作日"
    
    medium:
      approver: "流程负责人"
      timeline: "5 工作日"
      review: "合规会签"
    
    high:
      approver: "管理层"
      timeline: "10 工作日"
      review: "合规 + 风险会签"
    
    critical:
      approver: "治理委员会"
      timeline: "15 工作日"
      review: "多部门会签"
```

## 补偿控制

```yaml
compensating_control:
  requirements:
    - 必须能部分或完全替代原控制目标
    - 风险不得高于原控制
    - 必须可验证和审计
  
  types:
    - 人工控制替代
    - 替代控制措施
    - 增强监控
    - 事后审计
```

## 期限管理

```yaml
duration_management:
  max_duration:
    low_risk: "90 天"
    medium_risk: "60 天"
    high_risk: "30 天"
    critical: "15 天"
  
  extension:
    max_extensions: 2
    extension_approval: "原审批人或更高层级"
    requirement: "必须说明延期原因和进展"
```

## 定期审查

```yaml
periodic_review:
  frequency:
    critical: "每日"
    high: "每周"
    medium: "每月"
    low: "每季度"
  
  review_content:
    - 例外是否仍必要
    - 补偿控制是否有效
    - 是否有新风险
    - 是否可以关闭
```

## 关闭流程

```yaml
closure_process:
  conditions:
    - 例外原因已消除
    - 原控制已恢复
    - 期限到期且无延期
  
  steps:
    - 确认关闭条件
    - 验证原控制恢复
    - 评估例外期间影响
    - 记录经验教训
    - 更新例外登记簿
    - 通知相关方
```

## 例外登记簿

```yaml
exception_register:
  fields:
    - 例外编号
    - 例外描述
    - 涉及控制
    - 风险等级
    - 批准人
    - 批准日期
    - 有效期限
    - 补偿控制
    - 责任人
    - 状态
    - 关闭日期
  
  retention: "5 年"
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
