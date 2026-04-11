# HANDOFF_BETWEEN_HUMANS.md - 人与人任务交接规范

## 目的
定义人与人之间的任务交接规范，确保换人后任务不断档、不失真。

## 适用范围
- 任务交接
- 项目交接
- 职责转移
- 人员变动

## 核心规则

### 1. 交接文档结构

```yaml
handoff_document:
  required_sections:
    - 背景
    - 当前状态
    - 已完成内容
    - 未完成项
    - 风险点
    - 下一步建议
    - 资源清单
    - 联系人
```

### 2. 背景说明

```yaml
background:
  required_content:
    - 任务来源和目的
    - 相关项目背景
    - 业务上下文
    - 时间线概览
    - 关键决策历史
  
  format: |
    ## 背景
    - **任务来源**: [来源]
    - **任务目的**: [目的]
    - **相关项目**: [项目列表]
    - **时间线**: [关键时间点]
    - **关键决策**: [决策记录]
```

### 3. 当前状态

```yaml
current_status:
  required_content:
    - 整体进度百分比
    - 当前阶段
    - 阻塞项
    - 待决策项
    - 最近活动
  
  status_template:
    overall_progress: "XX%"
    current_phase: "[阶段名称]"
    blockers:
      - description: "[阻塞描述]"
        impact: "[影响范围]"
        owner: "[负责人]"
    pending_decisions:
      - decision: "[待决策项]"
        options: "[选项列表]"
        deadline: "[截止日期]"
    recent_activities:
      - date: "[日期]"
        activity: "[活动描述]"
```

### 4. 已完成内容

```yaml
completed_items:
  required_content:
    - 已交付成果
    - 已验证功能
    - 已关闭问题
    - 已完成里程碑
  
  template: |
    ## 已完成内容
    ### 已交付成果
    | 成果 | 交付时间 | 验收状态 |
    |------|----------|----------|
    | [成果1] | [时间] | [状态] |
    
    ### 已验证功能
    - [功能1]: [验证结果]
    
    ### 已关闭问题
    - [问题1]: [解决方案]
```

### 5. 未完成项

```yaml
pending_items:
  required_content:
    - 待办事项列表
    - 优先级排序
    - 预计工作量
    - 依赖关系
    - 截止日期
  
  template: |
    ## 未完成项
    | 事项 | 优先级 | 工作量 | 依赖 | 截止日期 |
    |------|--------|--------|------|----------|
    | [事项1] | P1 | 2d | [依赖] | [日期] |
    
    ### 详细说明
    #### [事项1]
    - **描述**: [详细描述]
    - **当前进度**: [进度]
    - **下一步**: [具体步骤]
```

### 6. 风险点

```yaml
risk_points:
  required_content:
    - 已知风险
    - 潜在风险
    - 风险应对措施
    - 需要关注的事项
  
  template: |
    ## 风险点
    | 风险 | 级别 | 影响 | 应对措施 | 状态 |
    |------|------|------|----------|------|
    | [风险1] | 高 | [影响] | [措施] | [状态] |
    
    ### 需要关注
    - [关注点1]: [原因和建议]
```

### 7. 下一步建议

```yaml
next_steps:
  required_content:
    - 立即行动项
    - 短期计划
    - 长期规划
    - 建议优先级
  
  template: |
    ## 下一步建议
    ### 立即行动（24h内）
    1. [行动1]
    2. [行动2]
    
    ### 短期计划（1周内）
    1. [计划1]
    
    ### 长期规划
    1. [规划1]
    
    ### 建议优先级
    1. [优先级排序及理由]
```

### 8. Owner 切换规则

```yaml
owner_switch:
  # 切换前
  before_switch:
    - 完成交接文档
    - 确认接收人
    - 获得审批（如需要）
    - 通知相关方
  
  # 切换中
  during_switch:
    - 正式转移权限
    - 更新任务 owner
    - 发送通知
    - 记录审计日志
  
  # 切换后
  after_switch:
    - 原 owner 保持 7 天咨询期
    - 新 owner 确认接收
    - 更新所有相关文档
    - 通知所有干系人
  
  # 紧急切换
  emergency_switch:
    allowed: true
    require_approval: "admin"
    documentation: "事后补齐"
    consultation_period: "延长至 14 天"
```

### 9. 审计要求

```yaml
audit_requirements:
  # 记录内容
  log_content:
    - 交接时间
    - 原负责人
    - 新负责人
    - 交接原因
    - 交接文档
    - 审批记录
    - 确认记录
  
  # 保留期限
  retention: "项目结束后 3 年"
  
  # 查询能力
  query:
    by_task: true
    by_user: true
    by_time: true
```

## 异常处理

### 交接拒绝
- 记录原因
- 通知管理员
- 寻找替代方案

### 交接中断
- 保存已完成部分
- 通知相关方
- 安排继续交接

### 紧急交接
- 启用紧急流程
- 事后补齐文档
- 延长咨询期

## 完成标准
- [x] 交接文档结构完整
- [x] 背景说明要求明确
- [x] 当前状态描述清晰
- [x] 已完成内容记录完整
- [x] 未完成项清单明确
- [x] 风险点识别清晰
- [x] 下一步建议具体
- [x] Owner 切换规则完整
- [x] 审计要求明确
- [x] 换人后任务不断档、不失真

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
