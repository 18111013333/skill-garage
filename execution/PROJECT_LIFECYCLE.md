# PROJECT_LIFECYCLE.md - 项目生命周期管理

## 目的
定义长期项目的生命周期阶段、转换规则和管理规范。

## 适用范围
所有跨会话长期项目的生命周期管理。

## 生命周期阶段

```
created → scoped → planned → in_progress → blocked → review → completed → archived
```

## 阶段定义

### 1. created（已创建）
| 属性 | 说明 |
|------|------|
| 进入条件 | 项目首次创建 |
| 允许操作 | 编辑基本信息、添加目标、分配负责人 |
| 退出条件 | 目标明确、负责人确认 |
| 回退条件 | 无 |

### 2. scoped（已界定）
| 属性 | 说明 |
|------|------|
| 进入条件 | 目标明确、范围界定完成 |
| 允许操作 | 定义范围边界、识别相关方、初步风险评估 |
| 退出条件 | 范围文档完成、相关方确认 |
| 回退条件 | 范围重大变更 → created |

### 3. planned（已规划）
| 属性 | 说明 |
|------|------|
| 进入条件 | 范围确认、里程碑定义完成 |
| 允许操作 | 拆解里程碑、定义依赖、分配资源、制定计划 |
| 退出条件 | 计划审批通过、资源就绪 |
| 回退条件 | 计划不可行 → scoped |

### 4. in_progress（进行中）
| 属性 | 说明 |
|------|------|
| 进入条件 | 计划确认、开始执行 |
| 允许操作 | 执行任务、更新进度、记录决策、处理问题 |
| 退出条件 | 所有里程碑完成 或 进入阻塞 或 进入评审 |
| 回退条件 | 重大变更 → planned |

### 5. blocked（已阻塞）
| 属性 | 说明 |
|------|------|
| 进入条件 | 遇到无法自行解决的阻塞 |
| 允许操作 | 记录阻塞原因、通知相关方、等待解除 |
| 退出条件 | 阻塞解除 → in_progress |
| 回退条件 | 阻塞无法解除 → review（异常终止） |

### 6. review（评审中）
| 属性 | 说明 |
|------|------|
| 进入条件 | 里程碑完成 或 阶段性节点 |
| 允许操作 | 验收交付物、评估偏差、记录经验教训 |
| 退出条件 | 评审通过 → completed 或 返工 → in_progress |
| 回退条件 | 评审不通过 → in_progress |

### 7. completed（已完成）
| 属性 | 说明 |
|------|------|
| 进入条件 | 所有成功标准达成、评审通过 |
| 允许操作 | 归档文档、总结经验、释放资源 |
| 退出条件 | 归档完成 → archived |
| 回退条件 | 发现重大问题 → in_progress（重新激活） |

### 8. archived（已归档）
| 属性 | 说明 |
|------|------|
| 进入条件 | 项目正式结束、文档归档 |
| 允许操作 | 查阅历史、提取经验 |
| 退出条件 | 无（终态） |
| 回退条件 | 无 |

## 状态转换矩阵

| 从\到 | created | scoped | planned | in_progress | blocked | review | completed | archived |
|-------|---------|--------|---------|-------------|---------|--------|-----------|----------|
| created | - | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| scoped | ✅ | - | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| planned | ❌ | ✅ | - | ✅ | ❌ | ❌ | ❌ | ✅ |
| in_progress | ❌ | ❌ | ✅ | - | ✅ | ✅ | ❌ | ❌ |
| blocked | ❌ | ❌ | ❌ | ✅ | - | ✅ | ❌ | ✅ |
| review | ❌ | ❌ | ❌ | ✅ | ❌ | - | ✅ | ❌ |
| completed | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | - | ✅ |
| archived | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | - |

## 转换规则

### 转换条件
```yaml
transitions:
  created_to_scoped:
    conditions:
      - objective_defined: true
      - owner_confirmed: true
    actions:
      - create_scope_document
      - notify_stakeholders
      
  scoped_to_planned:
    conditions:
      - scope_approved: true
      - stakeholders_identified: true
    actions:
      - create_milestones
      - identify_dependencies
      
  planned_to_in_progress:
    conditions:
      - plan_approved: true
      - resources_allocated: true
    actions:
      - start_execution
      - create_checkpoint
      
  in_progress_to_blocked:
    conditions:
      - blocker_identified: true
    actions:
      - record_blocker
      - notify_owner
      
  blocked_to_in_progress:
    conditions:
      - blocker_resolved: true
    actions:
      - resume_execution
      - update_status
      
  in_progress_to_review:
    conditions:
      - milestone_completed: true
    actions:
      - prepare_deliverables
      - schedule_review
      
  review_to_completed:
    conditions:
      - review_passed: true
      - success_criteria_met: true
    actions:
      - finalize_documentation
      - archive_project
      
  review_to_in_progress:
    conditions:
      - review_failed: true
    actions:
      - record_issues
      - create_rework_plan
```

## 异常处理

### 强制终止
```yaml
force_terminate:
  conditions:
    - owner_cancelled
    - objective_obsolete
    - resource_exhausted
  actions:
    - record_termination_reason
    - archive_partial_results
    - notify_stakeholders
  allowed_from: [created, scoped, planned, in_progress, blocked]
```

### 重新激活
```yaml
reactivate:
  conditions:
    - new_objective_defined
    - resources_available
  allowed_from: [completed, archived]
  actions:
    - create_new_version
    - reset_to_scoped
```

## 阶段检查点

### 检查点配置
```yaml
checkpoints:
  scoped:
    required:
      - scope_document
      - stakeholder_list
    optional:
      - initial_risk_assessment
      
  planned:
    required:
      - milestone_list
      - dependency_map
      - resource_plan
    optional:
      - contingency_plan
      
  in_progress:
    required:
      - progress_report
      - decision_log
    frequency: weekly
    
  review:
    required:
      - deliverables
      - metrics_report
      - lessons_learned
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 阶段停留时间 | 在某阶段时长 | 超预期50% |
| 阻塞次数 | 进入blocked次数 | >3次 |
| 回退次数 | 阶段回退次数 | >2次 |
| 里程碑延迟 | 延迟完成比例 | >20% |

## 维护方式
- 新增阶段: 更新阶段定义和转换矩阵
- 调整规则: 更新转换条件
- 新增检查点: 更新检查点配置

## 引用文件
- `projects/PROJECT_SCHEMA.json` - 项目结构
- `state/STATE_MACHINE.md` - 状态机
- `projects/MILESTONE_POLICY.md` - 里程碑策略
