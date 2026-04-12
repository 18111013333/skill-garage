# AUTONOMY_LEVELS.md - 自主等级定义

## 目的
定义自主能力的等级和边界，确保自主不是模糊概念。

## 适用范围
所有自主执行能力的分级管理。

## 自主等级

### L0 - 只建议不执行
```yaml
level_l0:
  name: "纯建议模式"
  description: "只提供建议和分析，不执行任何动作"
  
  allowed:
    - 分析问题
    - 提供建议
    - 生成方案
    - 风险评估
    - 信息整理
    
  forbidden:
    - 执行任何外部动作
    - 修改任何数据
    - 发送任何消息
    - 创建任何资源
    
  use_cases:
    - 高风险场景
    - 新用户场景
    - 探索性任务
```

### L1 - 可自动分析与草拟
```yaml
level_l1:
  name: "分析草拟模式"
  description: "可自动分析和生成草稿，但不提交"
  
  allowed:
    - L0所有能力
    - 生成文档草稿
    - 生成代码草稿
    - 生成消息草稿
    - 数据分析
    
  forbidden:
    - 提交/发送草稿
    - 执行外部动作
    - 修改生产数据
    
  output_handling:
    - 所有输出标记为"草稿"
    - 需用户确认才能使用
```

### L2 - 可执行低风险动作
```yaml
level_l2:
  name: "低风险执行模式"
  description: "可自动执行低风险动作"
  
  allowed:
    - L1所有能力
    - 读取外部数据
    - 查询操作
    - 生成只读报告
    - 创建临时资源
    
  forbidden:
    - 写入生产数据
    - 发送外部消息
    - 修改共享资源
    - 批量操作
    
  risk_threshold:
    max_risk_level: "low"
    requires_confirmation_for: ["medium"]
```

### L3 - 可串联多步动作但需审批节点
```yaml
level_l3:
  name: "审批链模式"
  description: "可执行多步动作，但关键节点需审批"
  
  allowed:
    - L2所有能力
    - 多步骤编排
    - 中等风险操作
    - 外部系统调用
    
  requires_approval:
    - 每个阶段开始前
    - 高风险动作前
    - 外部写入前
    - 批量操作前
    
  approval_chain:
    - phase_approval: true
    - action_approval: "by_risk_level"
    - result_approval: true
```

### L4 - 可按计划推进但全程审计和随时可中止
```yaml
level_l4:
  name: "强监管自主模式"
  description: "可按计划自主推进，但全程监控可中止"
  
  allowed:
    - L3所有能力
    - 完整计划执行
    - 高风险操作（有约束）
    - 批量操作（有约束）
    
  constraints:
    - 全程审计: true
    - 实时监控: true
    - 随时可中止: true
    - 阶段汇报: true
    
  monitoring:
    - 执行前校验
    - 执行中监测
    - 异常自动暂停
    - 定期汇报
    
  kill_switch:
    enabled: true
    triggers: ["异常", "越权", "用户请求"]
```

## 等级对比

| 能力 | L0 | L1 | L2 | L3 | L4 |
|------|----|----|----|----|----|
| 分析建议 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 生成草稿 | ❌ | ✅ | ✅ | ✅ | ✅ |
| 读取数据 | ❌ | ❌ | ✅ | ✅ | ✅ |
| 低风险执行 | ❌ | ❌ | ✅ | ✅ | ✅ |
| 多步编排 | ❌ | ❌ | ❌ | ✅ | ✅ |
| 高风险执行 | ❌ | ❌ | ❌ | 需审批 | 有约束 |
| 批量操作 | ❌ | ❌ | ❌ | 需审批 | 有约束 |
| 自主推进 | ❌ | ❌ | ❌ | ❌ | ✅ |

## 等级选择

### 选择规则
```yaml
level_selection:
  default: L0
  
  by_user:
    new_user: L0
    verified_user: L1
    trusted_user: L2
    admin: L3
    
  by_task:
    high_risk: L0
    medium_risk: L1
    low_risk: L2
    routine: L3
    approved_plan: L4
    
  by_domain:
    legal: L0
    finance: L0
    healthcare: L0
    operations: L2
    content: L2
```

### 动态调整
```yaml
dynamic_adjustment:
  downgrade_triggers:
    - error_rate_increase
    - user_negative_feedback
    - anomaly_detected
    - resource_constraint
    
  upgrade_conditions:
    - sustained_good_performance
    - user_explicit_approval
    - domain_verification
```

## 边界约束

### 跨等级约束
```yaml
cross_level_constraints:
  - never_bypass_approval: true
  - never_skip_audit: true
  - never_ignore_kill_switch: true
  - never_exceed_risk_limit: true
```

### 等级限制
```yaml
level_limits:
  L4:
    max_continuous_execution: "4h"
    max_actions_per_session: 100
    mandatory_break: "1h"
    report_frequency: "30m"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 等级分布 | 各等级使用比例 | L4>20% |
| 等级降级次数 | 自动降级次数 | >5/天 |
| 越权尝试次数 | 尝试越级执行 | >0 |
| 审批通过率 | 审批通过/申请 | <80% |

## 维护方式
- 新增等级: 创建等级定义
- 调整能力: 更新等级能力表
- 调整选择规则: 更新选择规则

## 引用文件
- `autonomy/PLAN_GENERATION.md` - 计划生成
- `autonomy/APPROVAL_CHAIN.md` - 审批链
- `autonomy/KILL_SWITCH.md` - 紧急停机
