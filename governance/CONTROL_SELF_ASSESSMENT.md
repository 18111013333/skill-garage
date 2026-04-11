# CONTROL_SELF_ASSESSMENT.md - 控制自评规范

## 目的
定义控制自评的要求和流程，确保控制所有者定期评估控制有效性。

## 适用范围
- 所有控制措施
- 所有控制所有者
- 所有流程负责人

## 自评周期

| 控制类型 | 自评频率 | 提交截止 |
|----------|----------|----------|
| 关键控制 | 季度 | 季末后 10 天 |
| 重要控制 | 半年 | 半年末后 15 天 |
| 一般控制 | 年度 | 年末后 20 天 |

## 自评内容

### 控制设计评估
```yaml
design_assessment:
  questions:
    - 控制目标是否明确？
    - 控制措施是否完整？
    - 控制逻辑是否正确？
    - 控制文档是否完备？
    - 控制是否覆盖所有风险？
  
  rating:
    effective: "设计合理完整"
    needs_improvement: "设计存在不足"
    ineffective: "设计存在重大缺陷"
```

### 控制运行评估
```yaml
operational_assessment:
  questions:
    - 控制是否持续执行？
    - 执行是否及时？
    - 执行是否完整？
    - 异常是否适当处理？
    - 证据是否充分保留？
  
  rating:
    effective: "运行一致有效"
    needs_improvement: "运行存在偏差"
    ineffective: "运行严重失效"
```

### 问题整改跟踪
```yaml
remediation_tracking:
  content:
    - 上期问题清单
    - 整改完成情况
    - 未完成原因
    - 新整改计划
    - 预计完成时间
```

## 自评流程

```yaml
self_assessment_process:
  step_1_preparation:
    action: "准备自评材料"
    content:
      - 控制文档
      - 运行证据
      - 上期问题
    timeline: "自评开始前"
  
  step_2_execution:
    action: "执行自评"
    content:
      - 回答评估问题
      - 收集支持证据
      - 识别问题
      - 制定整改计划
    timeline: "自评期间"
  
  step_3_review:
    action: "审核自评结果"
    reviewer: "流程负责人"
    content:
      - 验证自评准确性
      - 确认问题清单
      - 批准整改计划
    timeline: "自评完成后 5 天"
  
  step_4_submission:
    action: "提交自评报告"
    recipient: "合规部门"
    timeline: "截止日期前"
  
  step_5_follow_up:
    action: "跟踪整改"
    content:
      - 监控整改进度
      - 验证整改效果
      - 更新问题状态
    timeline: "持续"
```

## 自评报告

### 报告结构
```yaml
report_structure:
  sections:
    - 自评范围和方法
    - 控制评估结果汇总
    - 各控制详细评估
    - 问题清单和整改计划
    - 改进建议
    - 签字确认
```

### 评分标准
```yaml
scoring_criteria:
  effective:
    score: 3
    description: "控制有效，无问题"
  
  needs_improvement:
    score: 2
    description: "控制基本有效，存在改进空间"
  
  ineffective:
    score: 1
    description: "控制无效，需要重大改进"
  
  not_applicable:
    score: 0
    description: "本期不适用"
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
