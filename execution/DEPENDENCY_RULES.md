# DEPENDENCY_RULES.md - 项目依赖规则

## 目的
定义项目依赖关系规则，确保前置条件满足后再推进。

## 适用范围
所有项目和任务的依赖管理。

## 依赖类型

| 类型 | 说明 | 示例 | 检测方式 |
|------|------|------|----------|
| 任务依赖 | 任务间的前后关系 | A任务完成才能开始B | 任务状态检查 |
| 信息依赖 | 需要的信息输入 | 需要用户提供需求文档 | 输入检查 |
| 审批依赖 | 需要的审批确认 | 需要主管批准方案 | 审批状态检查 |
| 工具依赖 | 需要的工具可用性 | 需要数据库访问权限 | 工具可用性检查 |
| 时间依赖 | 时间约束条件 | 需要等待特定时间点 | 时间检查 |
| 外部条件依赖 | 外部系统/条件 | 需要第三方API可用 | 外部状态检查 |

## 依赖定义

### 依赖结构
```yaml
dependency:
  dependency_id: "DEP-001"
  type: "task"  # task, information, approval, tool, time, external
  
  from:
    entity_type: "task"
    entity_id: "TASK-001"
    
  to:
    entity_type: "task"
    entity_id: "TASK-002"
    
  relationship: "requires"  # requires, blocks, enables, triggers
  
  status: "pending"  # pending, satisfied, failed, waived
  
  satisfaction_criteria:
    condition: "TASK-001.status == 'completed'"
    verified_at: null
    
  timeout:
    duration: "7d"
    action: "escalate"
    
  alternative_path:
    enabled: true
    condition: "timeout_exceeded"
    action: "use_cached_result"
    
  created_at: "2024-01-01T00:00:00Z"
  updated_at: "2024-01-01T00:00:00Z"
```

## 依赖检测

### 检测规则
```yaml
detection_rules:
  task_dependency:
    check: "dependency.from.status == 'completed'"
    on_change: true
    periodic: false
    
  information_dependency:
    check: "required_input in received_inputs"
    on_input: true
    timeout: "30m"
    
  approval_dependency:
    check: "approval.status == 'approved'"
    on_approval: true
    timeout: "24h"
    
  tool_dependency:
    check: "tool.availability == true"
    on_start: true
    periodic: "5m"
    
  time_dependency:
    check: "current_time >= target_time"
    periodic: "1m"
    
  external_dependency:
    check: "external_system.status == 'available'"
    on_start: true
    periodic: "1m"
```

### 检测流程
```
依赖检查触发
    ↓
┌─────────────────────────────────────┐
│ 1. 收集依赖状态                      │
│    - 查询所有依赖项状态              │
│    - 评估满足条件                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 分类依赖                          │
│    - 已满足                          │
│    - 待满足                          │
│    - 无法满足                        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 决策处理                          │
│    - 全部满足 → 继续                 │
│    - 部分不满足 → 标记blocked        │
│    - 无法满足 → 触发替代路径         │
└─────────────────────────────────────┘
```

## 阻塞处理

### 阻塞标记
```yaml
blocker_marking:
  conditions:
    - dependency_status == "pending"
    - timeout_not_exceeded
    
  actions:
    - set_task_state: "blocked"
    - record_blocker:
        type: "dependency_incomplete"
        dependency_id: "${dependency_id}"
        reason: "${unsatisfied_condition}"
    - notify_owner
```

### 阻塞恢复
```yaml
blocker_recovery:
  on_dependency_satisfied:
    actions:
      - update_dependency_status: "satisfied"
      - check_all_dependencies
      - if_all_satisfied:
          - set_task_state: "ready"
          - notify_owner
          
  on_timeout:
    actions:
      - check_alternative_path
      - if_alternative_available:
          - execute_alternative
      - else:
          - escalate
```

## 替代路径

### 替代策略
| 策略 | 适用场景 | 说明 |
|------|----------|------|
| 跳过依赖 | 非关键依赖 | 标记为waived，继续执行 |
| 使用缓存 | 信息依赖 | 使用缓存数据替代 |
| 降级方案 | 工具依赖 | 使用替代工具 |
| 等待恢复 | 外部依赖 | 等待外部恢复 |
| 取消任务 | 关键依赖 | 无法满足时取消 |

### 替代配置
```yaml
alternative_paths:
  - dependency_type: "information"
    condition: "timeout > 30m"
    alternatives:
      - type: "use_cached"
        priority: 1
      - type: "use_default"
        priority: 2
      - type: "skip_task"
        priority: 3
        
  - dependency_type: "tool"
    condition: "tool_unavailable"
    alternatives:
      - type: "use_alternative_tool"
        tool_id: "backup_tool"
      - type: "queue_for_later"
        
  - dependency_type: "external"
    condition: "external_unavailable"
    alternatives:
      - type: "use_cached_result"
      - type: "graceful_degradation"
```

## 等待策略

### 等待配置
```yaml
waiting_strategy:
  active_waiting:
    # 主动等待，定期检查
    check_interval: "5m"
    max_wait: "24h"
    actions:
      - periodic_check
      - notify_progress
      
  passive_waiting:
    # 被动等待，事件触发
    trigger: "dependency_change_event"
    timeout: "7d"
    actions:
      - wait_for_event
      - on_timeout: escalate
      
  hybrid_waiting:
    # 混合策略
    initial_passive: "1h"
    then_active: "6h"
    final_escalation: "24h"
```

## 依赖可视化

### 依赖图
```yaml
dependency_graph:
  nodes:
    - id: "TASK-001"
      type: "task"
      status: "completed"
    - id: "TASK-002"
      type: "task"
      status: "in_progress"
    - id: "TASK-003"
      type: "task"
      status: "blocked"
      
  edges:
    - from: "TASK-001"
      to: "TASK-002"
      type: "requires"
      status: "satisfied"
    - from: "TASK-002"
      to: "TASK-003"
      type: "requires"
      status: "pending"
```

### 关键路径
```yaml
critical_path:
  calculation: "longest_path"
  update: "on_dependency_change"
  alert:
    - path_delay > 10%
    - critical_task_blocked
```

## 循环依赖检测

### 检测算法
```javascript
function detectCircularDependency(dependencies) {
  const visited = new Set();
  const recursionStack = new Set();
  
  function dfs(node) {
    visited.add(node);
    recursionStack.add(node);
    
    const neighbors = getDependencies(node);
    for (const neighbor of neighbors) {
      if (!visited.has(neighbor)) {
        if (dfs(neighbor)) return true;
      } else if (recursionStack.has(neighbor)) {
        return true;  // 发现循环
      }
    }
    
    recursionStack.delete(node);
    return false;
  }
  
  for (const node of getAllNodes()) {
    if (!visited.has(node)) {
      if (dfs(node)) {
        return { hasCycle: true, nodes: [...recursionStack] };
      }
    }
  }
  
  return { hasCycle: false };
}
```

### 循环处理
```yaml
cycle_handling:
  detection: "on_dependency_add"
  action: "reject_with_warning"
  resolution:
    - break_cycle_by_splitting_task
    - introduce_intermediate_task
    - convert_to_parallel_execution
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 依赖满足率 | 已满足/总数 | <80% |
| 平均等待时间 | 等待依赖时长 | >预期50% |
| 阻塞任务数 | 被阻塞任务数 | >10 |
| 循环依赖数 | 检测到的循环 | >0 |

## 维护方式
- 新增依赖类型: 更新依赖类型表
- 调整策略: 更新替代路径配置
- 新增检测规则: 更新检测规则

## 引用文件
- `projects/PROJECT_SCHEMA.json` - 项目结构
- `state/BLOCKER_POLICY.md` - 阻塞策略
- `graph/GRAPH_REASONING.md` - 图谱推理
