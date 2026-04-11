# CONTROL_TESTING_POLICY.md - 控制测试策略

## 目的
定义控制测试的策略和方法，确保控制措施有效运行。

## 适用范围
- 所有已实施的控制措施
- 所有控制所有者
- 所有审计活动

## 测试类型

### 设计有效性测试
```yaml
design_testing:
  purpose: "验证控制设计是否合理"
  scope:
    - 控制目标明确性
    - 控制措施完整性
    - 控制逻辑正确性
    - 控制文档完备性
  
  methods:
    - 文档审阅
    - 流程分析
    - 访谈确认
    - 案例推演
  
  frequency: "年度或控制变更时"
  evidence:
    - 控制设计文档
    - 测试工作底稿
    - 设计评估报告
```

### 运行有效性测试
```yaml
operational_testing:
  purpose: "验证控制是否持续有效运行"
  scope:
    - 控制执行一致性
    - 控制执行及时性
    - 控制执行完整性
    - 异常处理有效性
  
  methods:
    - 样本测试
    - 重新执行
    - 穿行测试
    - 系统日志分析
  
  frequency: "季度或月度"
  sample_size:
    manual_control: "25-60 样本"
    automated_control: "1-5 样本 + 系统验证"
    continuous_control: "全量日志分析"
```

### 穿行测试
```yaml
walkthrough_testing:
  purpose: "验证端到端流程控制"
  scope:
    - 流程完整性
    - 控制点覆盖
    - 信息流转
    - 职责分离
  
  methods:
    - 选择交易样本
    - 追踪完整流程
    - 验证各控制点
    - 记录测试结果
  
  frequency: "年度"
  coverage: "覆盖所有关键流程"
```

## 测试程序

### 测试计划
```yaml
test_planning:
  steps:
    - 确定测试范围
    - 识别测试对象
    - 选择测试方法
    - 确定样本量
    - 准备测试工具
    - 安排测试时间
    - 通知控制所有者
  
  timeline:
    planning: "测试前 2 周"
    execution: "测试周期 1-2 周"
    reporting: "测试后 1 周"
```

### 测试执行
```yaml
test_execution:
  steps:
    - 获取测试样本
    - 执行测试程序
    - 记录测试结果
    - 收集测试证据
    - 评估控制有效性
    - 记录异常发现
  
  documentation:
    - 测试日期和执行人
    - 测试方法和程序
    - 样本选择依据
    - 测试结果详情
    - 发现的问题
    - 支持性证据
```

### 结果评估
```yaml
result_evaluation:
  rating_criteria:
    effective:
      description: "控制有效"
      criteria:
        - 设计合理
        - 运行一致
        - 无重大例外
        - 文档完备
    
    needs_improvement:
      description: "需要改进"
      criteria:
        - 设计基本合理
        - 运行基本一致
        - 存在少量例外
        - 文档基本完备
    
    ineffective:
      description: "控制无效"
      criteria:
        - 设计存在缺陷
        - 运行不一致
        - 存在重大例外
        - 文档缺失
  
  exception_handling:
    minor: "记录并跟踪整改"
    major: "立即报告并制定补救措施"
    critical: "升级管理层并实施应急控制"
```

## 测试频率

| 控制类型 | 设计测试 | 运行测试 | 穿行测试 |
|----------|----------|----------|----------|
| 关键控制 | 年度 | 季度 | 年度 |
| 重要控制 | 年度 | 半年 | 年度 |
| 一般控制 | 年度 | 年度 | 两年 |

## 测试报告

### 报告内容
```yaml
test_report:
  sections:
    - 测试范围和目标
    - 测试方法和程序
    - 测试结果汇总
    - 控制有效性评估
    - 发现的问题
    - 改进建议
    - 后续跟踪计划
```

### 报告分发
```yaml
distribution:
  - 控制所有者
  - 流程负责人
  - 内部审计
  - 管理层（摘要版）
```

## 问题跟踪

### 问题分类
```yaml
issue_classification:
  design_deficiency:
    description: "设计缺陷"
    severity: "高"
    remediation: "重新设计控制"
  
  operational_failure:
    description: "运行失效"
    severity: "中"
    remediation: "加强执行监督"
  
  documentation_gap:
    description: "文档缺失"
    severity: "低"
    remediation: "补充完善文档"
```

### 整改跟踪
```yaml
remediation_tracking:
  process:
    - 记录问题详情
    - 分配整改责任人
    - 设定整改期限
    - 跟踪整改进度
    - 验证整改效果
    - 关闭问题
  
  escalation:
    overdue_30_days: "提醒责任人"
    overdue_60_days: "升级管理层"
    overdue_90_days: "列入审计重点"
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
- 下次评审: 2027-04-07
