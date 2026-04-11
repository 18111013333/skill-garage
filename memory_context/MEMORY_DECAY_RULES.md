# MEMORY_DECAY_RULES.md - 记忆衰减规则

## 目的
定义记忆衰减规则，确保旧记忆不会无限占据高权重。

## 适用范围
所有记忆条目的衰减管理。

## 记忆类型与衰减

| 类型 | 说明 | 衰减曲线 | 复活条件 | 淘汰条件 |
|------|------|----------|----------|----------|
| 稳定偏好 | 用户长期偏好 | 极慢衰减 | 使用即复活 | 用户明确修改 |
| 阶段性偏好 | 临时偏好 | 中等衰减 | 使用即复活 | 90天未用 |
| 项目事实 | 项目相关信息 | 项目周期内不衰减 | 项目活跃 | 项目归档后180天 |
| 时效性事实 | 有时效的信息 | 快速衰减 | 更新后复活 | 过期后30天 |
| 一次性约束 | 单次有效约束 | 立即衰减 | 不复活 | 任务完成后 |

## 衰减曲线

### 衰减公式
```javascript
function calculateDecay(memory) {
  const decayType = getDecayType(memory);
  const daysSinceUpdate = getDaysSinceUpdate(memory);
  
  const decayCurves = {
    // 稳定偏好：极慢衰减
    stable_preference: {
      formula: "1 - 0.001 * days",
      half_life: 500,  // 半衰期500天
      min_weight: 0.5
    },
    
    // 阶段性偏好：中等衰减
    temporary_preference: {
      formula: "exp(-0.01 * days)",
      half_life: 69,
      min_weight: 0.1
    },
    
    // 项目事实：项目周期内不衰减
    project_fact: {
      formula: "project_active ? 1.0 : exp(-0.005 * days_since_archive)",
      half_life: 138,
      min_weight: 0.3
    },
    
    // 时效性事实：快速衰减
    time_sensitive_fact: {
      formula: "max(0, 1 - days / expiry_days)",
      half_life: "expiry_days / 2",
      min_weight: 0
    },
    
    // 一次性约束：立即衰减
    one_time_constraint: {
      formula: "task_completed ? 0 : 1",
      half_life: 0,
      min_weight: 0
    }
  };
  
  const curve = decayCurves[decayType];
  const weight = eval(curve.formula);
  
  return Math.max(curve.min_weight, weight);
}
```

### 衰减曲线图
```
权重
1.0 ┤─────────────────────── 稳定偏好
    │ \
    │  \
0.8 ┤   \─────────────────── 项目事实(活跃)
    │    \
    │     \
0.6 ┤      \──────────────── 阶段性偏好
    │       \
    │        \
0.4 ┤         \───────────── 项目事实(归档)
    │          \
    │           \
0.2 ┤            \────────── 时效性事实
    │             \
    │              \
0.0 ┤───────────────\─────── 一次性约束
    └─────────────────────── 时间
      0   30  60  90  180  365 (天)
```

## 衰减触发

### 定期衰减
```yaml
periodic_decay:
  schedule: "daily"
  batch_size: 1000
  time_window: "02:00-04:00"  # 低峰期执行
```

### 事件触发衰减
```yaml
event_triggered_decay:
  events:
    - memory_not_accessed:
        threshold: "30d"
        action: "apply_decay"
        
    - project_archived:
        action: "switch_to_archive_decay"
        
    - task_completed:
        memory_type: "one_time_constraint"
        action: "immediate_decay"
        
    - fact_expired:
        action: "accelerate_decay"
```

## 复活机制

### 复活条件
```yaml
revival_conditions:
  access_revival:
    trigger: "memory_accessed"
    effect: "weight = min(1.0, weight + 0.3)"
    cooldown: "7d"
    
  update_revival:
    trigger: "memory_updated"
    effect: "weight = 1.0"
    reset_age: true
    
  confirmation_revival:
    trigger: "user_confirmed"
    effect: "weight = 1.0"
    reset_age: true
    
  project_revival:
    trigger: "project_reactivated"
    effect: "switch_to_active_decay"
```

### 复活限制
```yaml
revival_limits:
  max_revivals: 5
  revival_decay: "每次复活效果递减20%"
  min_weight_for_revival: 0.1
```

## 淘汰机制

### 淘汰条件
```yaml
elimination_conditions:
  weight_below_threshold:
    threshold: 0.1
    grace_period: "30d"
    
  expired_memory:
    condition: "expiry_date_passed"
    grace_period: "7d"
    
  conflicting_memory:
    condition: "superseded_by_newer"
    grace_period: "14d"
    
  user_deleted:
    condition: "user_marked_delete"
    grace_period: "0d"
```

### 淘汰流程
```yaml
elimination_flow:
  steps:
    - name: "标记淘汰"
      actions:
        - mark_for_elimination
        - set_grace_period_end
        
    - name: "等待期"
      actions:
        - allow_revival
        - monitor_access
        
    - name: "执行淘汰"
      conditions:
        - grace_period_ended
        - not_revived
      actions:
        - archive_or_delete
        - update_statistics
```

## 类型转换

### 自动类型转换
```yaml
type_conversion:
  temporary_to_stable:
    condition:
      - access_count > 10
      - age > 90d
      - weight > 0.7
    action: "convert_to_stable_preference"
    
  project_to_general:
    condition:
      - project_archived
      - high_reuse_value
    action: "convert_to_general_knowledge"
    
  time_sensitive_to_archive:
    condition:
      - expired
      - historical_value
    action: "archive_as_historical"
```

## 衰减配置

### 全局配置
```yaml
global_config:
  min_weight: 0.1
  max_weight: 1.0
  default_decay_rate: 0.01
  decay_check_interval: "daily"
  batch_size: 1000
```

### 类型配置
```yaml
type_config:
  stable_preference:
    decay_rate: 0.001
    min_weight: 0.5
    revival_boost: 0.1
    
  temporary_preference:
    decay_rate: 0.01
    min_weight: 0.1
    revival_boost: 0.3
    
  project_fact:
    decay_rate: 0.005
    min_weight: 0.3
    project_active_multiplier: 0
    
  time_sensitive_fact:
    decay_rate: 0.05
    min_weight: 0
    expiry_default: "30d"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 平均权重 | 所有记忆平均权重 | <0.5 |
| 淘汰率 | 淘汰/总记忆 | >5%/月 |
| 复活率 | 复活/淘汰候选 | <10% |
| 衰减延迟 | 衰减计算延迟 | >1小时 |

## 维护方式
- 新增衰减类型: 创建衰减曲线
- 调整参数: 更新衰减配置
- 新增复活条件: 更新复活规则

## 引用文件
- `memory_quality/MEMORY_SCORING.md` - 记忆评分
- `memory_quality/MEMORY_PROMOTION_POLICY.md` - 记忆晋升
- `MEMORY.md` - 记忆系统总索引
