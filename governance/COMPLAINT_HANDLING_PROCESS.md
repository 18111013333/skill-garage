# COMPLAINT_HANDLING_PROCESS.md - 投诉处理流程

## 目的
建立监管投诉处理机制，确保投诉得到及时、公正的处理。

## 适用范围
- 所有监管相关投诉
- 所有客户投诉
- 所有员工举报

## 投诉分类

```yaml
complaint_classification:
  by_source:
    customer:
      description: "客户投诉"
      channel: ["客服", "邮件", "官网"]
      sla: "15 天内回复"
    
    regulator:
      description: "监管转办"
      channel: ["监管机构转办"]
      sla: "按监管要求"
    
    employee:
      description: "员工举报"
      channel: ["举报热线", "匿名信箱"]
      sla: "30 天内调查完成"
  
  by_severity:
    critical:
      description: "严重投诉"
      criteria: ["涉及违法", "重大损失", "媒体关注"]
      escalation: "立即上报管理层"
    
    high:
      description: "重要投诉"
      criteria: ["服务缺陷", "合规问题", "多次投诉"]
      escalation: "24 小时内上报"
    
    normal:
      description: "一般投诉"
      criteria: ["服务不满", "流程问题"]
      escalation: "按正常流程"
```

## 处理流程

```yaml
handling_process:
  step_1_receipt:
    action: "接收投诉"
    output: "投诉登记"
    timeline: "即时"
  
  step_2_classification:
    action: "分类定级"
    output: "投诉分类"
    timeline: "4 小时内"
  
  step_3_investigation:
    action: "调查核实"
    output: "调查报告"
    timeline: "根据严重程度"
  
  step_4_resolution:
    action: "处理解决"
    output: "处理方案"
    timeline: "SLA 期限内"
  
  step_5_response:
    action: "回复投诉人"
    output: "回复记录"
    timeline: "SLA 期限内"
  
  step_6_closure:
    action: "结案归档"
    output: "结案报告"
    timeline: "处理后 5 天"
```

## 记录要求

```yaml
record_requirements:
  complaint_register:
    fields:
      - 投诉编号
      - 投诉日期
      - 投诉来源
      - 投诉内容
      - 分类定级
      - 处理人
      - 处理状态
      - 处理结果
      - 结案日期
  
  retention: "5 年"
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
