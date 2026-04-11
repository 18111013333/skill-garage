# COMMENT_RESOLUTION.md - 评论与分歧处理机制

## 目的
定义评论、批注、分歧处理机制，确保协作反馈可闭环。

## 适用范围
- 评论管理
- 批注处理
- 分歧解决
- 反馈闭环

## 核心规则

### 1. 评论状态定义

```yaml
comment_states:
  open:
    description: "新建评论，待处理"
    color: "blue"
    auto_action: "notify_assignee"
  
  acknowledged:
    description: "已确认收到，待处理"
    color: "yellow"
    auto_action: "start_timer"
  
  accepted:
    description: "已接受，将执行"
    color: "green"
    auto_action: "create_action_item"
  
  rejected:
    description: "已拒绝，说明原因"
    color: "red"
    auto_action: "notify_author"
  
  superseded:
    description: "已被新评论替代"
    color: "gray"
    auto_action: "link_to_new"
```

### 2. 评论绑定规则

```yaml
comment_binding:
  # 绑定到任务
  task_binding:
    allowed: true
    inherit_visibility: true
    affect_status: false
  
  # 绑定到项目
  project_binding:
    allowed: true
    inherit_visibility: true
    affect_status: false
  
  # 绑定到文档
  document_binding:
    allowed: true
    inherit_visibility: true
    affect_status: false
  
  # 绑定到审批节点
  approval_binding:
    allowed: true
    inherit_visibility: false
    affect_status: true  # 可影响审批状态
```

### 3. 评论处理流程

```yaml
resolution_flow:
  steps:
    - step: 1
      action: "创建评论"
      state: "open"
      notify: "assignee"
    
    - step: 2
      action: "确认收到"
      state: "acknowledged"
      timeout: "24h"
    
    - step: 3
      action: "评估处理"
      options:
        - accept: "接受并执行"
        - reject: "拒绝并说明"
        - escalate: "升级处理"
    
    - step: 4
      action: "执行或拒绝"
      state: "accepted / rejected"
    
    - step: 5
      action: "闭环确认"
      notify: "author"
```

### 4. 分歧处理机制

```yaml
disagreement_handling:
  # 分歧类型
  types:
    factual:
      description: "事实性分歧"
      resolution: "提供证据"
      escalation: "expert_review"
    
    opinion:
      description: "观点性分歧"
      resolution: "讨论协商"
      escalation: "vote_or_decide"
    
    priority:
      description: "优先级分歧"
      resolution: "评估影响"
      escalation: "owner_decide"
    
    approach:
      description: "方法性分歧"
      resolution: "对比分析"
      escalation: "team_discussion"
  
  # 分歧升级
  escalation:
    level_1:
      resolver: "直接负责人"
      timeout: "24h"
    
    level_2:
      resolver: "项目负责人"
      timeout: "48h"
    
    level_3:
      resolver: "团队投票"
      timeout: "72h"
    
    level_4:
      resolver: "最终裁决人"
      timeout: "24h"
```

### 5. 批注管理

```yaml
annotation_management:
  # 批注类型
  types:
    highlight:
      description: "高亮标注"
      action: "mark_for_attention"
    
    question:
      description: "疑问标注"
      action: "require_response"
    
    suggestion:
      description: "建议标注"
      action: "optional_adoption"
    
    correction:
      description: "修正标注"
      action: "require_action"
  
  # 批注处理
  processing:
    auto_notify: true
    track_status: true
    link_to_source: true
    preserve_history: true
```

### 6. 闭环规则

```yaml
closure_rules:
  # 自动闭环条件
  auto_close:
    conditions:
      - accepted_and_executed
      - rejected_and_acknowledged
      - superseded_by_newer
    
    action: "mark_resolved"
    notify: "all_participants"
  
  # 强制闭环
  force_close:
    allowed: true
    require_permission: "admin"
    require_reason: true
    audit: true
  
  # 闭环时效
  sla:
    open_to_acknowledged: "24h"
    acknowledged_to_resolved: "72h"
    total_resolution: "7d"
```

### 7. 评论统计与报告

```yaml
reporting:
  # 统计指标
  metrics:
    - total_comments
    - open_comments
    - avg_resolution_time
    - acceptance_rate
    - escalation_count
  
  # 报告周期
  frequency: "weekly"
  
  # 报告内容
  content:
    - 评论趋势
    - 处理效率
    - 分歧热点
    - 改进建议
```

## 异常处理

### 评论超时
- 自动升级
- 通知上级
- 记录超时日志

### 分歧僵持
- 触发投票机制
- 或提交最终裁决
- 记录决策过程

### 恶意评论
- 检测并标记
- 通知管理员
- 可隐藏或删除

## 完成标准
- [x] 评论状态定义完整
- [x] 评论绑定规则清晰
- [x] 评论处理流程明确
- [x] 分歧处理机制完整
- [x] 批注管理规则清晰
- [x] 闭环规则明确
- [x] 评论统计与报告完整
- [x] 协作反馈可闭环，不会散在聊天里

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
