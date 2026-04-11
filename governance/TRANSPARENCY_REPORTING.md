# TRANSPARENCY_REPORTING.md - 透明度报告规则

## 目的
定义透明度报告规则，向外部展示平台可信度。

## 适用范围
- 所有对外透明度披露
- 所有公开报告
- 所有客户可见信息

## 披露指标

```yaml
disclosure_metrics:
  security:
    - 安全事件统计
    - 漏洞修复时效
    - 安全认证状态
    - 渗透测试频率
  
  availability:
    - 服务可用率
    - 计划内维护通知
    - 重大事件响应时间
  
  privacy:
    - 数据请求统计
    - DSAR 响应时效
    - 数据泄露事件
  
  compliance:
    - 合规认证状态
    - 审计发现统计
    - 整改完成率
  
  ai_governance:
    - AI 用例数量
    - 风险等级分布
    - 人工复核比例
```

## 更新频率

| 指标类型 | 更新频率 | 发布渠道 |
|----------|----------|----------|
| 服务状态 | 实时 | 状态页面 |
| 安全事件 | 事件后 72 小时 | 安全公告 |
| 月度指标 | 每月 | 信任中心 |
| 季度报告 | 每季度 | 透明度报告 |
| 年度报告 | 每年 | 年度报告 |

## 事件说明

```yaml
event_disclosure:
  security_incident:
    minor:
      disclosure: "季度报告汇总"
      detail: "影响范围和处置措施"
    
    major:
      disclosure: "72 小时内公告"
      detail: "事件概述、影响、响应措施"
      notification: "受影响客户单独通知"
  
  service_outage:
    minor:
      disclosure: "状态页面实时更新"
    
    major:
      disclosure: "即时公告 + 事后报告"
      detail: "原因、影响、改进措施"
```

## 不公开内容

```yaml
non_public_content:
  reasons:
    - 安全风险（披露会增加风险）
    - 客户隐私
    - 商业机密
    - 法律限制
  
  handling:
    - 提供概括性说明
    - 说明不能公开的原因
    - 提供替代信息渠道（如适用）
```

## 报告格式

```yaml
report_format:
  transparency_report:
    sections:
      - 执行摘要
      - 服务可用性
      - 安全状态
      - 隐私保护
      - 合规状态
      - AI 治理
      - 改进计划
    
    review: "法务 + 合规审核"
    approval: "管理层批准"
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
