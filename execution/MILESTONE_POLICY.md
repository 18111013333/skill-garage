# MILESTONE_POLICY.md - 里程碑策略

## 目的
定义里程碑拆解与验收规则，实现项目阶段化管理。

## 适用范围
所有长期项目的里程碑管理。

## 里程碑定义

### 里程碑结构
```yaml
milestone:
  milestone_id: "MS-PROJ001-001"
  name: "需求分析完成"
  description: "完成用户需求收集和分析"
  project_id: "PROJ-2024-001"
  
  objective:
    goal: "明确项目范围和核心需求"
    success_definition: "需求文档评审通过"
    
  target_date: "2024-02-01"
  actual_date: null
  
  status: "pending"  # pending, in_progress, completed, skipped
  
  deliverables:
    - name: "需求规格说明书"
      type: "document"
      verification_method: "评审通过"
      status: "pending"
    - name: "用户故事列表"
      type: "document"
      verification_method: "用户确认"
      status: "pending"
      
  risks:
    - risk_id: "R001"
      description: "用户需求不明确"
      probability: "medium"
      mitigation: "增加用户访谈"
      
  dependencies:
    - type: "information"
      item: "用户访谈安排"
      status: "pending"
      
  entry_criteria:
    - "项目范围已界定"
    - "相关方已确认"
    
  exit_criteria:
    - "需求文档完成"
    - "评审通过"
    - "用户确认"
    
  next_milestone: "MS-PROJ001-002"
```

## 里程碑拆解

### 拆解原则
| 原则 | 说明 | 检查方法 |
|------|------|----------|
| SMART | 具体、可衡量、可达成、相关、有时限 | 逐项检查 |
| 独立性 | 里程碑之间尽量独立 | 依赖分析 |
| 可验证 | 每个里程碑有明确验收标准 | 验收清单 |
| 粒度适中 | 不太大也不太小 | 时长1-4周 |

### 拆解流程
```
项目目标
    ↓
┌─────────────────────────────────────┐
│ 1. 阶段划分                          │
│    - 识别主要阶段                    │
│    - 定义阶段目标                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 里程碑定义                        │
│    - 每阶段拆解里程碑                │
│    - 定义交付物                      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 依赖梳理                          │
│    - 识别里程碑依赖                  │
│    - 排序和并行化                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 验收标准制定                      │
│    - 定义完成标准                    │
│    - 定义验收方法                    │
└─────────────────────────────────────┘
```

### 拆解模板
```yaml
templates:
  software_project:
    phases:
      - name: "需求阶段"
        milestones:
          - "需求收集完成"
          - "需求分析完成"
          - "需求评审通过"
      - name: "设计阶段"
        milestones:
          - "架构设计完成"
          - "详细设计完成"
          - "设计评审通过"
      - name: "开发阶段"
        milestones:
          - "核心功能开发完成"
          - "辅助功能开发完成"
          - "单元测试完成"
      - name: "测试阶段"
        milestones:
          - "集成测试完成"
          - "系统测试完成"
          - "验收测试通过"
      - name: "发布阶段"
        milestones:
          - "发布准备完成"
          - "正式发布完成"
          - "上线验证完成"
```

## 验收规则

### 验收标准
```yaml
acceptance_criteria:
  required:
    - all_deliverables_completed: true
    - exit_criteria_met: true
    - no_critical_issues: true
    - stakeholder_approval: true
    
  optional:
    - quality_metrics_met: true
    - documentation_complete: true
    - knowledge_transferred: true
```

### 验收流程
```yaml
acceptance_flow:
  steps:
    - name: "自检"
      actor: "执行者"
      actions:
        - check_deliverables
        - verify_exit_criteria
        - document_results
        
    - name: "评审"
      actor: "评审者"
      actions:
        - review_deliverables
        - verify_quality
        - provide_feedback
        
    - name: "确认"
      actor: "相关方"
      actions:
        - approve_or_reject
        - sign_off
        
    - name: "归档"
      actor: "系统"
      actions:
        - record_completion
        - archive_deliverables
        - update_project_status
```

### 验收结果
| 结果 | 说明 | 后续动作 |
|------|------|----------|
| 通过 | 所有标准满足 | 进入下一里程碑 |
| 有条件通过 | 存在次要问题 | 记录问题，进入下一里程碑 |
| 不通过 | 存在重大问题 | 返工，重新验收 |
| 延期 | 无法按期完成 | 调整计划，延期处理 |

## 里程碑状态

### 状态定义
| 状态 | 说明 | 允许转换 |
|------|------|----------|
| pending | 待开始 | → in_progress, skipped |
| in_progress | 进行中 | → completed, blocked, skipped |
| blocked | 已阻塞 | → in_progress, skipped |
| completed | 已完成 | → (终态) |
| skipped | 已跳过 | → (终态) |

### 状态转换规则
```yaml
transitions:
  pending_to_in_progress:
    conditions:
      - entry_criteria_met: true
      - dependencies_resolved: true
    actions:
      - start_tracking
      - notify_stakeholders
      
  in_progress_to_completed:
    conditions:
      - deliverables_done: true
      - acceptance_passed: true
    actions:
      - record_completion
      - trigger_next_milestone
      
  in_progress_to_blocked:
    conditions:
      - blocker_identified: true
    actions:
      - record_blocker
      - notify_owner
      
  any_to_skipped:
    conditions:
      - skip_approved: true
      - reason_documented: true
    actions:
      - record_skip_reason
      - adjust_plan
```

## 风险管理

### 风险识别
```yaml
risk_categories:
  - type: "依赖风险"
    indicators:
      - dependency_delayed
      - dependency_failed
  - type: "资源风险"
    indicators:
      - resource_unavailable
      - budget_exceeded
  - type: "技术风险"
    indicators:
      - technical_blocker
      - complexity_underestimated
  - type: "范围风险"
    indicators:
      - scope_creep
      - requirement_change
```

### 风险应对
```yaml
risk_response:
  mitigation:
    - identify_alternative_path
    - request_additional_resource
    - adjust_timeline
  escalation:
    trigger: "risk_probability == high && risk_impact == high"
    action: "escalate_to_project_owner"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 完成率 | 已完成/总数 | <计划值 |
| 延期率 | 延期/总数 | >20% |
| 阻塞时长 | 平均阻塞时间 | >3天 |
| 验收一次通过率 | 一次通过/总验收 | <80% |

## 维护方式
- 新增模板: 创建里程碑模板
- 调整规则: 更新验收规则
- 新增风险类型: 更新风险分类

## 引用文件
- `projects/PROJECT_SCHEMA.json` - 项目结构
- `projects/PROJECT_LIFECYCLE.md` - 项目生命周期
- `projects/DEPENDENCY_RULES.md` - 依赖规则
