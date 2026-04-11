# TEAM_PROTOCOL.md - 团队协作协议

## 目的
定义团队协作基本规则，明确各角色职责边界，确保团队场景下职责清晰。

## 适用范围
- 多人协作场景
- 团队项目管理
- 任务分配与交接
- 审批流程

## 核心规则

### 1. 角色定义

| 角色 | 可发起任务 | 可接手任务 | 可审批 | 可查看 | 可关闭 | 可变更上下文 |
|------|-----------|-----------|--------|--------|--------|-------------|
| Owner | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Member | ✅ | ✅ | ❌ | ✅ | ✅* | ❌ |
| Observer | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |

*Member 只能关闭自己创建或接手的任务

### 2. 任务发起规则

```yaml
task_initiation:
  owner:
    can_create: true
    can_assign: true
    can_set_priority: true
    can_set_deadline: true
    require_approval: false
  
  admin:
    can_create: true
    can_assign: true
    can_set_priority: true
    can_set_deadline: true
    require_approval: false
  
  member:
    can_create: true
    can_assign: false  # 只能分配给自己
    can_set_priority: false
    can_set_deadline: true
    require_approval: true  # 需要审批
  
  observer:
    can_create: false
```

### 3. 任务接手规则

```yaml
task_assignment:
  rules:
    - 角色必须 >= Member
    - 任务状态必须为 open 或 reassigned
    - 接手者必须有对应技能或被明确指派
    - 接手后自动成为任务 owner
  
  auto_assign:
    enabled: true
    strategy: "skill_match"
    fallback: "round_robin"
  
  manual_assign:
    require_accept: true  # 被指派者需确认
    accept_timeout: 24h
    timeout_action: "escalate"
```

### 4. 审批规则

```yaml
approval:
  triggers:
    - 任务优先级变更
    - 任务截止时间变更
    - 任务范围扩大
    - 跨项目资源调用
    - 外部系统集成
  
  approval_levels:
    level_1:
      approvers: ["admin"]
      quorum: 1
      timeout: 4h
    
    level_2:
      approvers: ["owner"]
      quorum: 1
      timeout: 8h
    
    level_3:
      approvers: ["owner", "admin"]
      quorum: 2
      timeout: 24h
  
  escalation:
    enabled: true
    after: 2 * timeout
    escalate_to: "parent_workspace_owner"
```

### 5. 查看权限规则

```yaml
visibility:
  default: "team"  # 团队内可见
  
  by_role:
    owner: "all"
    admin: "all"
    member: "assigned + created"
    observer: "public_only"
  
  sensitive_content:
    require_role: "admin"
    audit_access: true
```

### 6. 任务关闭规则

```yaml
task_closure:
  who_can_close:
    - task_creator
    - task_assignee
    - admin
    - owner
  
  close_requirements:
    - 所有子任务完成
    - 无未解决评论
    - 完成报告已提交
  
  auto_close:
    enabled: false  # 禁止自动关闭
  
  archive_after: 30d
```

### 7. 共享上下文变更规则

```yaml
context_modification:
  who_can_modify:
    - owner
    - admin
  
  modification_types:
    add_context:
      require_approval: false
      audit: true
    
    remove_context:
      require_approval: true
      approver: "owner"
      audit: true
    
    change_visibility:
      require_approval: true
      approver: "owner"
      audit: true
  
  notification:
    on_change: true
    notify_who: "all_participants"
```

## 异常处理

### 角色冲突
- 同一人有多个角色时，取最高权限
- 权限冲突时，从严处理

### 审批超时
- 超时后自动升级
- 升级后仍未处理，暂停相关操作

### 任务争议
- 争议提交给 admin 仲裁
- admin 无法解决，提交给 owner
- 最终裁决由 owner 做出

## 完成标准
- [x] 角色职责明确定义
- [x] 任务生命周期权限清晰
- [x] 审批流程可追溯
- [x] 异常处理有明确路径
- [x] 系统能区分个人任务、双人协作、小团队协作

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
