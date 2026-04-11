# ALLOCATION_POLICY.md - 资源分配策略

## 目的
定义资源分配策略，确保资源分配有制度。

## 适用范围
所有资源的分配和占用管理。

## 分配类型

| 类型 | 说明 | 适用场景 | 特点 |
|------|------|----------|------|
| 固定配额 | 固定分配 | 核心项目 | 不受抢占 |
| 动态配额 | 按需分配 | 普通项目 | 可调整 |
| 优先级抢占 | 高优先级抢占 | 紧急任务 | 可抢占低优先级 |
| 保底资源 | 最小保障 | 所有项目 | 不可被抢占 |
| 应急资源池 | 应急使用 | 突发情况 | 需审批 |

## 分配流程

```
资源请求
    ↓
┌─────────────────────────────────────┐
│ 1. 请求验证                          │
│    - 验证请求者权限                  │
│    - 验证请求合理性                  │
│    - 检查资源可用性                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 分配策略选择                      │
│    - 确定分配类型                    │
│    - 计算分配量                      │
│    - 检查冲突                        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 执行分配                          │
│    - 预留资源                        │
│    - 更新使用记录                    │
│    - 通知相关方                      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 监控与回收                        │
│    - 监控使用情况                    │
│    - 超时自动回收                    │
│    - 主动释放处理                    │
└─────────────────────────────────────┘
```

## 分配规则

### 固定配额分配
```yaml
fixed_allocation:
  conditions:
    - project_priority: ">= P1"
    - resource_type: "critical"
    - approval: "required"
    
  process:
    - request_fixed_allocation
    - review_by_resource_owner
    - approve_or_reject
    - bind_to_project
    
  characteristics:
    - preemptable: false
    - adjustable: false
    - expires_with_project: true
```

### 动态配额分配
```yaml
dynamic_allocation:
  conditions:
    - resource_available: true
    - within_quota_limits: true
    
  process:
    - check_availability
    - calculate_allocation
    - allocate_immediately
    
  characteristics:
    - preemptable: true
    - adjustable: true
    - auto_expire: true
    
  formula: |
    allocation = min(
      requested,
      available * project_priority_factor,
      max_per_request
    )
```

### 优先级抢占分配
```yaml
preemption_allocation:
  conditions:
    - requester_priority: ">= P0"
    - target_priority: "< requester_priority"
    - no_fixed_allocation: true
    
  process:
    - identify_preemption_targets
    - notify_affected_projects
    - transfer_resources
    - update_allocations
    
  limits:
    - max_preemption_per_day: 3
    - min_notice_time: "5m"
    - recovery_guarantee: true
```

### 保底资源分配
```yaml
baseline_allocation:
  conditions:
    - all_active_projects: true
    
  process:
    - calculate_baseline
    - reserve_resources
    - guarantee_availability
    
  characteristics:
    - preemptable: false
    - guaranteed: true
    
  formula: |
    baseline = total_resources * 0.1 / active_project_count
    min_baseline = resource_type_specific_minimum
```

### 应急资源分配
```yaml
emergency_allocation:
  conditions:
    - emergency_declared: true
    - approval: "admin"
    
  process:
    - request_emergency_access
    - admin_approval
    - allocate_from_emergency_pool
    
  characteristics:
    - time_limited: true
    - requires_post_review: true
    - audit_level: "high"
```

## 申请流程

### 申请结构
```yaml
allocation_request:
  request_id: "REQ-001"
  requester:
    project_id: "PROJ-001"
    user_id: "user_001"
    
  resource:
    resource_id: "RES-model-0001"
    resource_type: "model_compute"
    requested_amount: 10000
    unit: "tokens"
    
  justification:
    reason: "完成里程碑MS-001"
    expected_duration: "2h"
    priority: "P1"
    
  constraints:
    max_wait_time: "30m"
    can_accept_less: true
    min_acceptable: 5000
```

### 审批规则
```yaml
approval_rules:
  auto_approve:
    conditions:
      - requested < available * 0.1
      - project_has_quota
      - no_conflict
      
  manual_approve:
    conditions:
      - requested > available * 0.3
      - new_project
      - emergency_request
      
  reject:
    conditions:
      - insufficient_resources
      - project_over_budget
      - policy_violation
```

## 资源回收

### 自动回收
```yaml
auto_reclaim:
  triggers:
    - allocation_timeout
    - task_completed
    - project_paused
    - project_completed
    
  process:
    - detect_trigger
    - notify_user
    - release_resources
    - update_availability
```

### 手动回收
```yaml
manual_reclaim:
  triggers:
    - admin_request
    - project_cancelled
    - policy_violation
    
  process:
    - verify_authority
    - notify_affected
    - force_release
    - audit_log
```

## 配额管理

### 配额设置
```yaml
quota_settings:
  by_project:
    - project_id: "PROJ-001"
      quotas:
        model_compute: 100000
        tool_calls: 5000
        storage: 10GB
        
  by_resource_type:
    - resource_type: "model_compute"
      default_quota: 50000
      max_quota: 500000
      
  by_priority:
    - priority: "P0"
      quota_multiplier: 2.0
    - priority: "P1"
      quota_multiplier: 1.5
```

### 配额监控
```yaml
quota_monitoring:
  alerts:
    - threshold: 80%
      action: "notify"
    - threshold: 95%
      action: "throttle"
    - threshold: 100%
      action: "block"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 资源利用率 | 已用/总量 | >85% |
| 分配成功率 | 成功/请求 | <90% |
| 平均等待时间 | 分配等待时长 | >5m |
| 抢占频率 | 抢占次数/天 | >5 |

## 维护方式
- 新增分配类型: 创建分配策略
- 调整规则: 更新分配规则
- 调整配额: 更新配额设置

## 引用文件
- `resources/RESOURCE_SCHEMA.json` - 资源结构
- `resources/CONTENTION_RESOLUTION.md` - 争用解决
- `portfolio/PRIORITIZATION_POLICY.md` - 优先级策略
