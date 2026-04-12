# EXTERNAL_STATE_SYNC.md - 外部状态同步规则

## 目的
定义系统内部状态与外部系统状态同步规则。

## 适用范围
所有与外部系统交互的状态同步。

## 同步场景

| 场景 | 说明 | 同步方向 | 频率 |
|------|------|----------|------|
| 启动同步 | 系统启动时 | 外部→内部 | 启动时 |
| 定期同步 | 定期刷新 | 外部→内部 | 定时 |
| 事件同步 | 外部变更触发 | 外部→内部 | 实时 |
| 操作后同步 | 操作完成后 | 双向 | 操作后 |
| 冲突检测 | 检测不一致 | 双向 | 按需 |

## 同步规则

### 何时拉取外部状态
```yaml
pull_triggers:
  scheduled:
    - interval: "1h"
      resources: ["calendar", "documents"]
    - interval: "5m"
      resources: ["messages"]
      
  event_driven:
    - webhook_received: true
    - notification_received: true
    
  on_demand:
    - before_critical_operation: true
    - user_explicit_request: true
    - cache_miss: true
    
  on_startup:
    - enabled: true
    - priority_resources: ["permissions", "config"]
```

### 何时刷新本地缓存
```yaml
refresh_triggers:
  time_based:
    - max_age: "1h"
      action: "refresh_if_accessed"
      
  event_based:
    - external_update_detected: true
    - local_modification: true
    
  operation_based:
    - after_write_operation: true
    - after_failed_read: true
```

### 何时以外部为准
```yaml
external_authority:
  conditions:
    - local_data_stale: true
    - local_data_missing: true
    - conflict_detected: true
    - external_is_source_of_truth: true
    
  resources:
    - calendar_events: "external"
    - document_content: "external"
    - user_permissions: "external"
```

### 何时标记冲突
```yaml
conflict_marking:
  conditions:
    - local_and_external_differ: true
    - both_modified: true
    - timestamp_conflict: true
    
  actions:
    - mark_as_conflicted
    - preserve_both_versions
    - notify_user
    - await_resolution
```

## 同步流程

### 启动同步
```yaml
startup_sync:
  steps:
    - name: "识别需同步资源"
      action: "list_external_integrations"
      
    - name: "拉取外部状态"
      action: "fetch_external_state"
      
    - name: "与本地状态对比"
      action: "compare_states"
      
    - name: "处理差异"
      actions:
        - if_local_newer: "keep_local"
        - if_external_newer: "update_local"
        - if_conflict: "mark_conflict"
        
    - name: "更新本地缓存"
      action: "update_local_cache"
```

### 定期同步
```yaml
periodic_sync:
  schedule:
    - resources: ["calendar"]
      interval: "30m"
    - resources: ["documents"]
      interval: "1h"
      
  process:
    - fetch_external_state
    - detect_changes
    - apply_updates
    - log_sync_result
```

### 操作后同步
```yaml
post_operation_sync:
  triggers:
    - write_operation_completed
    - external_call_completed
    
  steps:
    - wait_for_external_confirmation
    - fetch_updated_state
    - verify_consistency
    - update_local_cache
```

## 冲突处理

### 冲突检测
```javascript
function detectConflict(local, external) {
  if (local.version === external.version) {
    return { hasConflict: false };
  }
  
  if (local.updated_at > external.updated_at) {
    return { 
      hasConflict: true, 
      winner: 'local',
      reason: 'local_newer' 
    };
  }
  
  if (external.updated_at > local.updated_at) {
    return { 
      hasConflict: true, 
      winner: 'external',
      reason: 'external_newer' 
    };
  }
  
  return { 
    hasConflict: true, 
    winner: 'unknown',
    reason: 'timestamp_conflict' 
  };
}
```

### 冲突解决
```yaml
conflict_resolution:
  strategies:
    - external_wins:
        condition: "external_is_authoritative"
        action: "use_external"
        
    - local_wins:
        condition: "local_is_authoritative"
        action: "use_local"
        
    - newer_wins:
        condition: "default"
        action: "use_newer"
        
    - merge:
        condition: "mergeable"
        action: "merge_changes"
        
    - manual:
        condition: "unresolvable"
        action: "request_user_decision"
```

## 状态验证

### 一致性检查
```yaml
consistency_check:
  frequency: "daily"
  
  checks:
    - compare_counts
    - compare_checksums
    - compare_timestamps
    
  on_inconsistency:
    - log_discrepancy
    - trigger_sync
    - notify_admin
```

### 验证点
```yaml
validation_points:
  - after_sync: true
  - before_critical_operation: true
  - on_user_request: true
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 同步成功率 | 成功/总同步 | <95% |
| 同步延迟 | 同步耗时 | >5m |
| 冲突率 | 冲突/总同步 | >5% |
| 一致性偏差 | 不一致项数 | >10 |

## 维护方式
- 新增同步场景: 创建同步规则
- 调整频率: 更新同步配置
- 新增冲突策略: 创建解决策略

## 引用文件
- `orchestration/INTEGRATION_REGISTRY.json` - 集成注册表
- `orchestration/ACTION_ORCHESTRATION.md` - 动作编排
- `orchestration/TRANSACTION_POLICY.md` - 事务策略
