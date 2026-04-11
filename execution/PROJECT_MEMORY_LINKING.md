# PROJECT_MEMORY_LINKING.md - 项目记忆链接

## 目的
定义项目与记忆系统的链接机制，实现项目专属上下文。

## 适用范围
所有项目相关的记忆管理。

## 记忆分类

| 类型 | 作用域 | 示例 | 链接方式 |
|------|--------|------|----------|
| 项目核心记忆 | 项目专属 | 项目目标、里程碑决策 | 强链接 |
| 项目上下文记忆 | 项目关联 | 项目相关文档、任务 | 弱链接 |
| 用户偏好记忆 | 用户全局 | 用户沟通风格 | 无链接 |
| 通用知识记忆 | 系统全局 | 技术知识、最佳实践 | 无链接 |

## 链接机制

### 链接结构
```yaml
memory_project_link:
  memory_id: "MEM-001"
  project_id: "PROJ-2024-001"
  
  link_type: "core"  # core, context, reference
  
  link_strength: 1.0  # 0.0-1.0
  
  created_at: "2024-01-01T00:00:00Z"
  created_by: "system"
  
  context:
    phase: "planning"
    milestone: "MS-001"
    task: "TASK-001"
    
  access_control:
    project_members_only: false
    inherit_project_permissions: true
```

### 链接类型
```yaml
link_types:
  core:
    description: "项目核心记忆"
    strength: 1.0
    retention: "project_lifetime"
    access: "project_members"
    
  context:
    description: "项目上下文记忆"
    strength: 0.7
    retention: "project_lifetime"
    access: "project_members"
    
  reference:
    description: "项目参考记忆"
    strength: 0.3
    retention: "default"
    access: "inherit_from_memory"
```

## 链接创建

### 自动链接
```yaml
auto_linking:
  triggers:
    - condition: "memory_created_in_project_context"
      action: "link_as_context"
      
    - condition: "memory_about_project_milestone"
      action: "link_as_core"
      
    - condition: "memory_about_project_decision"
      action: "link_as_core"
      
    - condition: "memory_about_project_risk"
      action: "link_as_core"
```

### 手动链接
```yaml
manual_linking:
  allowed_roles: [owner, admin]
  process:
    - select_memory
    - select_project
    - choose_link_type
    - confirm_link
```

## 链接查询

### 项目记忆检索
```javascript
function getProjectMemories(projectId, options = {}) {
  const query = {
    project_id: projectId,
    link_type: options.linkType || ['core', 'context'],
    min_strength: options.minStrength || 0.5,
    include_context: options.includeContext || true
  };
  
  // 1. 获取项目直接链接的记忆
  const directMemories = queryMemoriesByLink(query);
  
  // 2. 获取项目上下文相关记忆
  const contextMemories = options.includeContext 
    ? queryMemoriesByContext(projectId)
    : [];
    
  // 3. 合并去重
  return mergeAndDeduplicate(directMemories, contextMemories);
}
```

### 跨项目检索
```yaml
cross_project_query:
  enabled: false  # 默认禁用
  conditions:
    - user_has_access_to_both_projects
    - projects_are_related
    
  scope:
    - shared_resources
    - common_patterns
    - reference_materials
```

## 链接维护

### 链接更新
```yaml
link_update:
  triggers:
    - memory_content_changed
    - project_phase_changed
    - link_type_upgrade_requested
    
  actions:
    - recalculate_link_strength
    - update_link_metadata
    - notify_affected_parties
```

### 链接清理
```yaml
link_cleanup:
  conditions:
    - project_archived:
        action: "convert_to_reference_link"
        
    - memory_expired:
        action: "remove_link"
        
    - link_strength_below_threshold:
        threshold: 0.1
        action: "downgrade_or_remove"
```

## 隔离机制

### 项目隔离
```yaml
project_isolation:
  principles:
    - 项目核心记忆不污染其他项目
    - 项目上下文记忆不进入全局检索
    - 项目间记忆默认不可见
    
  implementation:
    - scope_prefix: "project_{project_id}_"
    - access_control: "project_members_only"
    - retrieval_filter: "by_project_scope"
```

### 上下文切换
```yaml
context_switching:
  on_project_change:
    actions:
      - save_current_context
      - load_project_memories
      - update_retrieval_scope
      
  on_project_exit:
    actions:
      - save_project_state
      - clear_project_context
      - restore_global_context
```

## 记忆类型映射

### 项目事实
```yaml
project_facts:
  examples:
    - "项目目标是..."
    - "技术栈是..."
    - "团队规模是..."
  link_type: "core"
  retention: "permanent"
```

### 里程碑决策
```yaml
milestone_decisions:
  examples:
    - "选择方案A因为..."
    - "放弃功能B因为..."
    - "延期原因..."
  link_type: "core"
  retention: "permanent"
```

### 风险记录
```yaml
risk_records:
  examples:
    - "识别到风险X..."
    - "风险缓解措施..."
    - "风险状态更新..."
  link_type: "core"
  retention: "project_lifetime"
```

### 待办事项
```yaml
todo_items:
  examples:
    - "需要完成..."
    - "待确认..."
    - "后续跟进..."
  link_type: "context"
  retention: "until_completed"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 链接准确率 | 正确链接/总链接 | <90% |
| 项目记忆覆盖率 | 有记忆/总项目 | <80% |
| 隔离违规次数 | 跨项目泄露 | >0 |
| 链接查询延迟 | 查询耗时 | >500ms |

## 维护方式
- 新增链接类型: 更新链接类型定义
- 调整隔离规则: 更新隔离配置
- 优化查询: 更新检索逻辑

## 引用文件
- `projects/PROJECT_SCHEMA.json` - 项目结构
- `MEMORY.md` - 记忆系统总索引
- `memory_quality/MEMORY_SCORING.md` - 记忆评分
