# CROSS_PROJECT_DEPENDENCIES.md - 跨项目依赖治理

## 目的
定义跨项目依赖治理规则，确保系统能识别项目间联动。

## 适用范围
所有项目组合中的跨项目依赖管理。

## 依赖类型

| 类型 | 说明 | 示例 | 影响 |
|------|------|------|------|
| 共享里程碑依赖 | 里程碑相互关联 | 项目A的M1依赖项目B的M2 | 延期传导 |
| 共享资源依赖 | 共用同一资源 | 多项目共用API配额 | 资源竞争 |
| 共享知识依赖 | 知识/数据共享 | 项目A需要项目B的分析结果 | 信息依赖 |
| 审批依赖 | 审批流程关联 | 项目A需等项目B审批通过 | 流程阻塞 |
| 交付顺序依赖 | 交付先后关系 | 项目A必须在项目B之前上线 | 顺序约束 |

## 依赖定义

### 依赖结构
```yaml
cross_project_dependency:
  dependency_id: "XDEP-001"
  type: "milestone"  # milestone, resource, knowledge, approval, delivery_sequence
  
  from:
    project_id: "PROJ-001"
    entity_type: "milestone"
    entity_id: "MS-001"
    
  to:
    project_id: "PROJ-002"
    entity_type: "milestone"
    entity_id: "MS-002"
    
  relationship: "depends_on"  # depends_on, blocks, enables, requires
  
  status: "pending"  # pending, satisfied, blocked, failed
  
  impact:
    if_delayed:
      affected_projects: ["PROJ-001"]
      delay_propagation: "7d"
      
  mitigation:
    alternative_path: "可替代方案"
    buffer_time: "3d"
```

## 依赖检测

### 自动检测
```yaml
auto_detection:
  triggers:
    - new_milestone_created
    - resource_binding_changed
    - knowledge_reference_added
    - approval_flow_updated
    
  detection_rules:
    - same_resource_binding:
        type: "resource"
        auto_create: true
        
    - milestone_reference:
        type: "milestone"
        auto_create: true
        
    - knowledge_cross_reference:
        type: "knowledge"
        auto_create: true
```

### 手动声明
```yaml
manual_declaration:
  allowed_roles: [owner, admin]
  process:
    - identify_dependency
    - specify_impact
    - define_mitigation
    - get_acknowledgment
```

## 影响分析

### 延期传导分析
```javascript
function analyzeDelayPropagation(dependency, delayDays) {
  const affectedProjects = [];
  
  // 直接影响
  const directImpact = {
    project_id: dependency.from.project_id,
    delay: delayDays,
    reason: `依赖${dependency.to.project_id}延期`
  };
  affectedProjects.push(directImpact);
  
  // 间接影响（传递依赖）
  const transitiveDeps = findTransitiveDependencies(dependency.from.project_id);
  for (const dep of transitiveDeps) {
    affectedProjects.push({
      project_id: dep.project_id,
      delay: delayDays + dep.buffer,
      reason: `传递依赖延期`
    });
  }
  
  return affectedProjects;
}
```

### 影响矩阵
```yaml
impact_matrix:
  dimensions:
    - dependency_strength: [weak, medium, strong, critical]
    - project_priority: [P0, P1, P2, P3, P4]
    - timeline_sensitivity: [low, medium, high]
    
  scoring:
    critical_strong_P0_high: 100
    strong_P1_high: 80
    medium_P2_medium: 50
    weak_P3_low: 20
```

## 依赖管理

### 依赖状态管理
```yaml
status_management:
  states:
    - pending: "等待满足"
    - in_progress: "正在满足"
    - satisfied: "已满足"
    - blocked: "被阻塞"
    - failed: "无法满足"
    
  transitions:
    pending_to_in_progress:
      trigger: "dependency_work_started"
    in_progress_to_satisfied:
      trigger: "dependency_completed"
    any_to_blocked:
      trigger: "blocking_issue_detected"
    blocked_to_failed:
      trigger: "unresolvable_issue"
```

### 依赖冲突检测
```yaml
conflict_detection:
  types:
    - circular_dependency:
        detection: "cycle_in_dependency_graph"
        resolution: "break_cycle"
        
    - conflicting_requirements:
        detection: "incompatible_constraints"
        resolution: "negotiate_or_prioritize"
        
    - resource_contention:
        detection: "overlapping_resource_needs"
        resolution: "schedule_or_allocate"
```

## 延期处理

### 延期通知
```yaml
delay_notification:
  triggers:
    - milestone_delay_detected
    - resource_unavailable
    - dependency_blocked
    
  notification:
    to:
      - affected_project_owners
      - portfolio_manager
    content:
      - delay_reason
      - affected_projects
      - estimated_impact
      - proposed_actions
```

### 延期缓解
```yaml
delay_mitigation:
  strategies:
    - buffer_consumption:
        description: "使用缓冲时间"
        condition: "buffer_available"
        
    - resource_reallocation:
        description: "重新分配资源"
        condition: "alternative_resources"
        
    - scope_adjustment:
        description: "调整范围"
        condition: "negotiable_scope"
        
    - parallel_execution:
        description: "并行执行"
        condition: "independent_paths"
        
    - alternative_path:
        description: "替代路径"
        condition: "alternative_available"
```

## 依赖可视化

### 依赖图
```yaml
dependency_graph:
  nodes:
    - type: "project"
      id: "PROJ-001"
    - type: "milestone"
      id: "MS-001"
      
  edges:
    - from: "PROJ-001:MS-001"
      to: "PROJ-002:MS-002"
      type: "depends_on"
      status: "pending"
```

### 关键路径
```yaml
critical_path:
  calculation: "longest_dependency_chain"
  update: "on_dependency_change"
  highlight:
    - zero_buffer_dependencies
    - high_impact_dependencies
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 依赖数量 | 跨项目依赖总数 | >50 |
| 循环依赖数 | 检测到的循环 | >0 |
| 阻塞依赖数 | 被阻塞的依赖 | >5 |
| 延期传导率 | 延期传导/总延期 | >30% |

## 维护方式
- 新增依赖类型: 更新依赖类型表
- 调整检测规则: 更新检测配置
- 优化缓解策略: 更新缓解策略

## 引用文件
- `portfolio/PORTFOLIO_SCHEMA.json` - 项目组合结构
- `portfolio/PRIORITIZATION_POLICY.md` - 优先级策略
- `projects/DEPENDENCY_RULES.md` - 项目依赖规则
