# PROJECT_QUEUE_POLICY.md - 项目排队与切换规则

## 目的
定义项目排队与切换规则，确保多项目推进有队列秩序。

## 适用范围
所有项目组合中的项目排队和切换管理。

## 队列类型

| 类型 | 说明 | 并行度 | 适用场景 |
|------|------|--------|----------|
| 活跃队列 | 正在执行的项目 | 3-5 | 高优先级项目 |
| 等待队列 | 等待资源的项目 | 不限 | 等待资源 |
| 暂停队列 | 主动暂停的项目 | 不限 | 用户暂停 |
| 阻塞队列 | 被阻塞的项目 | 不限 | 依赖未满足 |

## 队列配置

### 并行规则
```yaml
parallel_rules:
  max_active_projects: 5
  
  by_priority:
    P0:
      max_concurrent: 2
      can_preempt: true
    P1:
      max_concurrent: 3
      can_preempt: true
    P2:
      max_concurrent: 5
      can_preempt: false
    P3:
      max_concurrent: 3
      can_preempt: false
      
  by_resource:
    - resource_type: "model_compute"
      max_projects: 3
    - resource_type: "human_confirmation"
      max_projects: 2
```

### 排队规则
```yaml
queue_rules:
  entry_criteria:
    - project_approved: true
    - resources_identified: true
    - dependencies_checked: true
    
  ordering:
    primary: "priority_score"
    secondary: "deadline"
    tertiary: "creation_time"
    
  bypass:
    - emergency_project
    - admin_override
```

## 项目切换

### 切换触发
```yaml
switch_triggers:
  planned:
    - phase_completed
    - milestone_reached
    - resource_time_slice_expired
    
  unplanned:
    - blocker_detected
    - user_request
    - priority_change
    - resource_conflict
    
  emergency:
    - critical_issue
    - security_concern
    - user_explicit_request
```

### 切换流程
```
切换触发
    ↓
┌─────────────────────────────────────┐
│ 1. 状态保存                          │
│    - 创建检查点                      │
│    - 保存执行上下文                  │
│    - 记录进度状态                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 资源释放                          │
│    - 释放动态资源                    │
│    - 保留固定资源                    │
│    - 更新资源状态                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 队列更新                          │
│    - 当前项目入等待队列              │
│    - 新项目从队列取出                │
│    - 更新队列顺序                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 新项目启动                        │
│    - 加载项目上下文                  │
│    - 分配资源                        │
│    - 恢复执行状态                    │
└─────────────────────────────────────┘
```

### 上下文保存
```yaml
context_preservation:
  required:
    - project_state
    - task_progress
    - checkpoint_data
    - decision_history
    - pending_actions
    
  optional:
    - intermediate_results
    - cached_data
    - user_preferences
    
  storage:
    location: "project_contexts/"
    format: "json"
    retention: "30d"
```

### 资源释放
```yaml
resource_release:
  release_immediately:
    - dynamic_allocations
    - temporary_resources
    - shared_resources
    
  retain:
    - fixed_allocations
    - reserved_resources
    - baseline_resources
    
  release_delay:
    - resources_in_use: "grace_period_5m"
    - pending_operations: "wait_or_cancel"
```

## 队列管理

### 入队规则
```yaml
enqueue_rules:
  validation:
    - project_valid: true
    - not_already_queued: true
    - dependencies_satisfied: true
    
  position_calculation:
    formula: "priority_score * 0.6 + deadline_urgency * 0.3 + wait_time_bonus * 0.1"
    
  notification:
    - notify_project_owner
    - update_portfolio_view
```

### 出队规则
```yaml
dequeue_rules:
  conditions:
    - resources_available: true
    - slot_available: true
    - no_higher_priority_waiting: true
    
  process:
    - select_highest_priority
    - verify_resources
    - allocate_resources
    - start_execution
```

### 队列调整
```yaml
queue_adjustment:
  priority_boost:
    - waiting_too_long: "+5 per day"
    - deadline_approaching: "+10 per day"
    
  priority_penalty:
    - repeatedly_blocked: "-5 per incident"
    - resource_waste: "-10 per incident"
```

## 上下文隔离

### 隔离原则
```yaml
isolation_principles:
  - 每个项目独立上下文
  - 切换不污染其他项目
  - 恢复时完整还原
  - 资源不交叉使用
```

### 隔离实现
```yaml
isolation_implementation:
  memory:
    - separate_memory_scope
    - clear_on_switch
    
  resources:
    - dedicated_allocations
    - no_shared_state
    
  state:
    - independent_state_machine
    - isolated_checkpoints
```

## 切换限制

### 切换频率限制
```yaml
switch_limits:
  max_switches_per_hour: 3
  min_execution_time: "15m"
  cooldown_between_switches: "5m"
```

### 切换成本
```yaml
switch_cost:
  time_cost: "2m"
  resource_cost: "context_memory"
  tracking: true
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 队列长度 | 等待队列项目数 | >20 |
| 平均等待时间 | 项目等待时长 | >4h |
| 切换频率 | 切换次数/小时 | >5 |
| 上下文丢失率 | 切换时上下文丢失 | >0 |

## 维护方式
- 调整并行度: 更新并行规则
- 新增队列类型: 创建队列定义
- 调整切换规则: 更新切换流程

## 引用文件
- `portfolio/PORTFOLIO_SCHEMA.json` - 项目组合结构
- `portfolio/PRIORITIZATION_POLICY.md` - 优先级策略
- `state/INTERRUPTION_HANDLING.md` - 中断处理
