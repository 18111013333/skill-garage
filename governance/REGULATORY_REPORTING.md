# REGULATORY_REPORTING.md - 监管报告规则

## 目的
定义面向监管或强审计客户的定期报告规则。

## 适用范围
- 所有监管要求报告
- 所有客户合规报告
- 所有内部治理报告

## 报告类型

```yaml
report_types:
  periodic:
    monthly:
      - 运营状态报告
      - 事件统计报告
      - SLA 达成报告
    
    quarterly:
      - 合规状态报告
      - 风险评估报告
      - 控制有效性报告
    
    annual:
      - 年度治理报告
      - 审计报告
      - 安全评估报告
  
  event_driven:
    - 重大事件报告
    - 安全事件通知
    - 合规变更报告
  
  on_demand:
    - 监管问询响应
    - 客户审计支持
    - 尽职调查报告
```

## 报告内容

### 合规状态报告
```yaml
compliance_status_report:
  frequency: "季度"
  audience: "管理层 + 监管（如要求）"
  content:
    - 合规义务清单
    - 合规状态评估
    - 差距分析
    - 整改进展
    - 风险变化
    - 下期计划
  approval: "合规负责人"
```

### AI 治理报告
```yaml
ai_governance_report:
  frequency: "季度"
  audience: "治理委员会"
  content:
    - 用例状态汇总
    - 风险等级分布
    - 人工监督统计
    - 事件和异常
    - 模型性能趋势
    - 改进建议
  approval: "AI 治理官"
```

### 安全状态报告
```yaml
security_status_report:
  frequency: "月度"
  audience: "管理层"
  content:
    - 安全事件统计
    - 漏洞修复状态
    - 安全控制状态
    - 威胁情报摘要
    - 改进进展
  approval: "安全负责人"
```

## 数据来源

```yaml
data_sources:
  automated:
    - 系统日志
    - 监控指标
    - 审计记录
    - 事件管理系统
  
  manual:
    - 评估结果
    - 整改状态
    - 人工复核记录
    - 培训记录
```

## 审批流程

```yaml
approval_process:
  internal_report:
    drafter: "报告负责人"
    reviewer: "部门负责人"
    approver: "分管领导"
  
  external_report:
    drafter: "报告负责人"
    reviewer: "部门负责人 + 合规"
    approver: "管理层"
    legal_review: "法务审核（如需要）"
```

## 敏感内容处理

```yaml
sensitive_content_handling:
  classification:
    - 识别敏感内容
    - 标记敏感级别
    - 评估披露风险
  
  protection:
    - 数据脱敏
    - 聚合统计
    - 访问限制
    - 加密传输
  
  approval:
    sensitive_content: "合规 + 法务审批"
    highly_sensitive: "管理层审批"
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
