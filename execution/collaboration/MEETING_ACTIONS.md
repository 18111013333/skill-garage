# MEETING_ACTIONS.md - 会议结论到行动项沉淀规则

## 目的
定义会议结论到行动项的沉淀规则，确保会议结果能稳定回写到项目、任务、状态机。

## 适用范围
- 会议纪要
- 决策记录
- 行动项提取
- 任务回写

## 核心规则

### 1. 会议结论提取

```yaml
extraction_types:
  # 决策
  decision:
    required_fields:
      - decision_id
      - decision_text
      - decision_maker
      - decision_time
      - rationale
    output: "decision_record"
  
  # 行动项
  action_item:
    required_fields:
      - action_id
      - action_text
      - owner
      - deadline
      - dependencies
    output: "task_record"
  
  # 待解决问题
  unresolved_question:
    required_fields:
      - question_id
      - question_text
      - context
      - proposed_owner
    output: "issue_record"
```

### 2. 决策提取规则

```yaml
decision_extraction:
  # 决策识别
  identification:
    keywords:
      - "决定"
      - "确定"
      - "同意"
      - "通过"
      - "批准"
      - "decided"
      - "agreed"
      - "approved"
    
    patterns:
      - "我们决定..."
      - "最终确定..."
      - "大家同意..."
  
  # 决策记录
  recording:
    format: |
      ## 决策 #{decision_id}
      - **内容**: {decision_text}
      - **决策人**: {decision_maker}
      - **时间**: {decision_time}
      - **依据**: {rationale}
      - **影响范围**: {impact_scope}
  
  # 决策回写
  writeback:
    - 更新项目决策日志
    - 通知相关干系人
    - 触发相关流程变更
```

### 3. 行动项提取规则

```yaml
action_item_extraction:
  # 行动项识别
  identification:
    keywords:
      - "需要"
      - "负责"
      - "跟进"
      - "完成"
      - "todo"
      - "action"
      - "follow-up"
    
    patterns:
      - "{owner} 负责..."
      - "需要 {owner} 完成..."
      - "{owner} 跟进..."
  
  # 行动项记录
  recording:
    format: |
      ## 行动项 #{action_id}
      - **内容**: {action_text}
      - **负责人**: {owner}
      - **截止日期**: {deadline}
      - **依赖项**: {dependencies}
      - **关联决策**: {related_decision}
  
  # 行动项回写
  writeback:
    - 创建任务记录
    - 分配给负责人
    - 设置截止日期提醒
    - 关联到相关项目
```

### 4. 待解决问题提取

```yaml
unresolved_extraction:
  # 问题识别
  identification:
    keywords:
      - "待定"
      - "待解决"
      - "需要讨论"
      - "pending"
      - "tbd"
      - "follow-up"
    
    patterns:
      - "需要进一步讨论..."
      - "待确定..."
      - "遗留问题..."
  
  # 问题记录
  recording:
    format: |
      ## 待解决问题 #{question_id}
      - **问题**: {question_text}
      - **背景**: {context}
      - **建议负责人**: {proposed_owner}
      - **优先级**: {priority}
  
  # 问题回写
  writeback:
    - 创建问题记录
    - 分配给建议负责人
    - 设置跟进提醒
    - 关联到相关项目
```

### 5. 依赖关系提取

```yaml
dependency_extraction:
  # 依赖识别
  identification:
    keywords:
      - "依赖"
      - "需要...先完成"
      - "等待"
      - "depends on"
      - "blocked by"
  
  # 依赖记录
  recording:
    format: |
      ## 依赖关系
      - **行动项**: {action_id}
      - **依赖**: {dependency}
      - **依赖类型**: {type}
      - **阻塞影响**: {impact}
  
  # 依赖回写
  writeback:
    - 更新任务依赖关系
    - 设置阻塞状态
    - 通知依赖方
```

### 6. 回写规则

```yaml
writeback_rules:
  # 回写到项目
  to_project:
    decisions: true
    action_items: true
    unresolved: true
  
  # 回写到任务
  to_task:
    action_items: true
    dependencies: true
  
  # 回写到状态机
  to_state_machine:
    decisions: true
    action_items: true
  
  # 回写时机
  timing:
    immediate: true
    batch: false
    retry_on_failure: true
```

### 7. 会议纪要模板

```yaml
meeting_minutes_template:
  structure:
    - 会议基本信息
    - 参会人员
    - 议程
    - 讨论摘要
    - 决策列表
    - 行动项列表
    - 待解决问题
    - 下次会议安排
  
  format: |
    # 会议纪要
    
    ## 基本信息
    - **会议主题**: {title}
    - **时间**: {time}
    - **地点**: {location}
    
    ## 参会人员
    {attendees}
    
    ## 决策
    {decisions}
    
    ## 行动项
    {action_items}
    
    ## 待解决问题
    {unresolved_questions}
    
    ## 下次会议
    - **时间**: {next_meeting}
```

## 异常处理

### 提取失败
- 标记待人工处理
- 通知会议记录人
- 保留原始记录

### 回写失败
- 重试机制
- 记录失败日志
- 通知管理员

### 责任人不明确
- 标记待分配
- 通知会议组织者
- 设置分配提醒

## 完成标准
- [x] 会议结论提取类型完整
- [x] 决策提取规则清晰
- [x] 行动项提取规则明确
- [x] 待解决问题提取规则完整
- [x] 依赖关系提取规则清晰
- [x] 回写规则明确
- [x] 会议纪要模板完整
- [x] 会议结果能稳定回写到项目、任务、状态机

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
