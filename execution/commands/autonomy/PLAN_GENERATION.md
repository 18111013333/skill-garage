# PLAN_GENERATION.md - 自主计划生成规则

## 目的
定义自主计划生成规则，确保计划可监管。

## 适用范围
所有自主执行的计划生成。

## 计划结构

```yaml
plan:
  plan_id: "PLAN-2024-001"
  name: "计划名称"
  description: "计划描述"
  
  objective:
    goal: "计划目标"
    success_criteria:
      - criterion_1
      - criterion_2
    constraints:
      - constraint_1
      - constraint_2
      
  prerequisites:
    - condition: "前置条件1"
      verification: "验证方法"
    - condition: "前置条件2"
      verification: "验证方法"
      
  phases:
    - phase_id: "PHASE-001"
      name: "阶段名称"
      objective: "阶段目标"
      steps:
        - step_id: "STEP-001"
          action: "动作描述"
          risk_level: "low"
          resources_needed: []
          approval_required: false
          rollback_action: "回滚动作"
          
      entry_criteria:
        - 条件1
      exit_criteria:
        - 条件1
      approval_gate: true
      
  risks:
    - risk_id: "RISK-001"
      description: "风险描述"
      probability: "medium"
      impact: "high"
      mitigation: "缓解措施"
      
  resources:
    - resource_id: "RES-001"
      amount: 100
      duration: "2h"
      
  approval_nodes:
    - node_id: "APPR-001"
      phase: "PHASE-001"
      approvers: ["admin"]
      timeout: "4h"
      
  stop_conditions:
    - condition: "停止条件1"
      action: "暂停并通知"
    - condition: "停止条件2"
      action: "终止并回滚"
      
  rollback_plan:
    strategy: "reverse_order"
    steps:
      - step: "回滚步骤1"
      - step: "回滚步骤2"
    verification: "验证回滚完成"
    
  monitoring:
    checkpoints:
      - checkpoint_1
      - checkpoint_2
    report_frequency: "30m"
    metrics:
      - metric_1
      - metric_2
```

## 生成流程

```
目标输入
    ↓
┌─────────────────────────────────────┐
│ 1. 目标分析                          │
│    - 解析目标                        │
│    - 识别约束                        │
│    - 评估可行性                      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 阶段拆分                          │
│    - 划分执行阶段                    │
│    - 定义阶段目标                    │
│    - 设置审批节点                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 步骤细化                          │
│    - 细化每阶段步骤                  │
│    - 评估每步风险                    │
│    - 设计回滚方案                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 风险评估                          │
│    - 识别风险点                      │
│    - 设计缓解措施                    │
│    - 设置停止条件                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 5. 计划验证                          │
│    - 逻辑一致性检查                  │
│    - 资源可行性检查                  │
│    - 合规性检查                      │
└─────────────────────────────────────┘
```

## 生成规则

### 阶段拆分规则
```yaml
phase_rules:
  max_phases: 10
  min_phases: 2
  
  phase_criteria:
    - 每阶段有明确目标
    - 每阶段可独立验证
    - 阶段间有审批节点
    - 每阶段可回滚
    
  complexity_handling:
    - complex_task: "拆分为多个阶段"
    - simple_task: "合并为单阶段"
```

### 步骤细化规则
```yaml
step_rules:
  max_steps_per_phase: 20
  
  step_requirements:
    - 明确的动作描述
    - 风险等级评估
    - 资源需求说明
    - 回滚方案设计
    
  approval_placement:
    - high_risk_step: "前置审批"
    - external_write: "前置审批"
    - batch_operation: "前置审批"
    - phase_boundary: "阶段审批"
```

### 风险评估规则
```yaml
risk_assessment:
  risk_factors:
    - data_modification
    - external_interaction
    - resource_intensity
    - dependency_complexity
    - time_sensitivity
    
  risk_levels:
    low:
      auto_execute: true
    medium:
      requires_approval: true
    high:
      requires_approval: true
      requires_rollback_plan: true
    critical:
      requires_manual_execution: true
```

## 计划约束

### 禁止规则
```yaml
forbidden_patterns:
  - one_click_full_execution:
      description: "禁止一键全跑到底"
      reason: "必须有阶段审批"
      
  - no_rollback_plan:
      description: "禁止无回滚方案"
      reason: "必须可回滚"
      
  - unlimited_execution:
      description: "禁止无限执行"
      reason: "必须有停止条件"
      
  - bypass_approval:
      description: "禁止绕过审批"
      reason: "必须走审批链"
```

### 强制要求
```yaml
mandatory_requirements:
  - 阶段化执行: true
  - 审批节点: true
  - 回滚方案: true
  - 停止条件: true
  - 监控检查点: true
  - 资源预算: true
```

## 计划验证

### 验证项
```yaml
validation_checks:
  logic:
    - 步骤顺序合理
    - 依赖关系正确
    - 无循环依赖
    
  feasibility:
    - 资源可用
    - 时间合理
    - 能力匹配
    
  compliance:
    - 符合安全规则
    - 符合权限要求
    - 符合审计要求
    
  safety:
    - 有回滚方案
    - 有停止条件
    - 有风险缓解
```

### 验证流程
```yaml
validation_flow:
  - auto_validation:
      checks: [logic, feasibility]
      pass: "继续"
      fail: "修改计划"
      
  - compliance_validation:
      checks: [compliance, safety]
      pass: "提交审批"
      fail: "拒绝计划"
```

## 计划审批

### 审批要求
```yaml
approval_requirements:
  plan_level:
    - complexity: "high"
      approvers: ["admin", "owner"]
    - complexity: "medium"
      approvers: ["owner"]
    - complexity: "low"
      approvers: ["auto"]
      
  content_review:
    - 目标合理性
    - 风险可控性
    - 资源充足性
    - 回滚可行性
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 计划生成成功率 | 成功/请求 | <80% |
| 计划平均阶段数 | 平均阶段数 | >10 |
| 验证通过率 | 通过/验证 | <70% |
| 审批通过率 | 通过/审批 | <60% |

## 维护方式
- 新增规则: 创建生成规则
- 调整约束: 更新约束配置
- 新增验证: 更新验证项

## 引用文件
- `autonomy/AUTONOMY_LEVELS.md` - 自主等级
- `autonomy/APPROVAL_CHAIN.md` - 审批链
- `autonomy/SUPERVISED_EXECUTION.md` - 强监管执行
