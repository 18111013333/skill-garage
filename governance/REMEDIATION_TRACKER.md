# REMEDIATION_TRACKER.md - 整改追踪规则

## 目的
定义监管发现问题后的整改追踪规则，确保问题持续跟踪直至关闭。

## 适用范围
- 所有监管检查发现
- 所有审计发现
- 所有客户审查发现

## 整改项登记

```yaml
remediation_register:
  required_fields:
    - 整改项编号
    - 来源（监管/审计/客户）
    - 问题描述
    - 风险等级
    - 责任人
    - 截止日期
    - 整改方案
    - 验证方式
    - 当前状态
```

## 风险等级与时限

| 风险等级 | 描述 | 整改时限 | 验证要求 |
|----------|------|----------|----------|
| 严重 | 重大合规风险 | 30 天 | 管理层验证 |
| 高 | 重要问题 | 60 天 | 部门验证 |
| 中 | 一般问题 | 90 天 | 控制所有者验证 |
| 低 | 改进建议 | 180 天 | 自行验证 |

## 整改流程

```yaml
remediation_process:
  step_1_registration:
    action: "登记整改项"
    output: "整改项记录"
  
  step_2_assignment:
    action: "分配责任人"
    output: "责任分配"
  
  step_3_planning:
    action: "制定整改方案"
    content:
      - 根因分析
      - 整改措施
      - 资源需求
      - 时间计划
    output: "整改方案"
  
  step_4_execution:
    action: "执行整改"
    output: "整改进展记录"
  
  step_5_verification:
    action: "验证整改效果"
    output: "验证报告"
  
  step_6_closure:
    action: "关闭整改项"
    output: "关闭记录"
```

## 进度跟踪

```yaml
progress_tracking:
  reporting:
    weekly:
      - 高风险整改进展
      - 即将到期项目
    
    monthly:
      - 全部整改进展
      - 逾期项目
      - 新增项目
    
    quarterly:
      - 整改趋势分析
      - 系统性问题识别
  
  metrics:
    - 整改完成率
    - 按时完成率
    - 逾期项目数
    - 平均整改周期
```

## 逾期处理

```yaml
overdue_handling:
  escalation:
    7_days_overdue:
      action: "提醒责任人"
      channel: "邮件"
    
    14_days_overdue:
      action: "升级主管"
      channel: "邮件 + 即时消息"
    
    30_days_overdue:
      action: "升级管理层"
      channel: "正式报告"
  
  consequences:
    - 纳入绩效考核
    - 限制新项目审批
    - 管理层约谈
```

## 验证标准

```yaml
verification_criteria:
  evidence_required:
    - 整改措施执行证据
    - 控制有效性证据
    - 测试验证结果
  
  verification_methods:
    - 文档审阅
    - 控制测试
    - 穿行测试
    - 系统验证
  
  approval:
    low: "控制所有者确认"
    medium: "流程负责人确认"
    high: "部门负责人确认"
    critical: "管理层确认 + 外部验证"
```

## 关闭标准

```yaml
closure_criteria:
  must_satisfy:
    - 整改措施已执行
    - 验证结果通过
    - 证据已归档
    - 相关方已确认
  
  documentation:
    - 整改完成报告
    - 验证报告
    - 证据材料
    - 关闭批准记录
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
