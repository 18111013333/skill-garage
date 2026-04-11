# SHARED_CONTEXT_POLICY.md - 共享上下文边界

## 目的
定义共享上下文边界，确保协作信息能共享但不会过度暴露。

## 适用范围
- 多人协作场景
- 共享上下文管理
- 信息可见性控制
- 脱敏处理

## 核心规则

### 1. 共享内容分级

```yaml
content_classification:
  # 可完全共享
  fully_shareable:
    - 项目名称和描述
    - 任务标题和状态
    - 公开文档
    - 团队公告
    - 会议纪要（公开部分）
  
  # 限项目组共享
  project_team_only:
    - 任务详情
    - 项目配置
    - 内部文档
    - 进度报告
    - 风险清单
  
  # 限审批链共享
  approval_chain_only:
    - 审批意见
    - 决策依据
    - 敏感配置变更
    - 预算信息
  
  # 限发起人和执行者
  initiator_executor_only:
    - 个人备注
    - 私有记忆
    - 敏感凭证
    - 个人设置
  
  # 禁止共享
  never_share:
    - 密码和密钥
    - 个人身份信息
    - 支付信息
    - 合同细节
```

### 2. 共享前脱敏规则

```yaml
desensitization:
  # 自动脱敏
  auto_desensitize:
    enabled: true
    patterns:
      - pattern: "\\b\\d{11}\\b"  # 手机号
        action: "mask_middle"
        example: "138****1234"
      
      - pattern: "\\b[\\w.-]+@[\\w.-]+\\.\\w+\\b"  # 邮箱
        action: "mask_username"
        example: "a***@example.com"
      
      - pattern: "\\b\\d{16,19}\\b"  # 银行卡
        action: "mask_all"
        example: "****"
      
      - pattern: "\\b\\d{17}[\\dXx]\\b"  # 身份证
        action: "mask_all"
        example: "****"
  
  # 手动脱敏标记
  manual_marking:
    syntax: "[SENSITIVE:内容]"
    action: "replace_with_placeholder"
    placeholder: "[已脱敏]"
```

### 3. 可见性规则

```yaml
visibility_rules:
  # 按角色
  by_role:
    owner:
      can_see: "all"
      can_share: "all"
    
    admin:
      can_see: "all_except_private"
      can_share: "project_team_and_below"
    
    member:
      can_see: "project_team_and_below"
      can_share: "with_approval"
    
    observer:
      can_see: "public_only"
      can_share: "none"
  
  # 按内容类型
  by_content_type:
    task:
      default_visibility: "project_team"
      can_override: true
    
    document:
      default_visibility: "creator_choice"
      can_override: true
    
    memory:
      default_visibility: "private"
      can_share: "explicit_only"
    
    comment:
      default_visibility: "same_as_parent"
      can_override: false
```

### 4. 共享操作规则

```yaml
sharing_operations:
  # 主动共享
  proactive_sharing:
    require_permission: true
    audit: true
    notification:
      to: "all_affected"
      content: "共享范围和内容摘要"
  
  # 被动共享（继承）
  inherited_sharing:
    enabled: true
    rules:
      - 子任务继承父任务可见性
      - 评论继承所属对象可见性
      - 附件继承所属文档可见性
  
  # 共享撤销
  revoke_sharing:
    allowed: true
    require_permission: "owner_or_admin"
    notification: true
    audit: true
```

### 5. 跨项目共享

```yaml
cross_project_sharing:
  # 允许场景
  allowed_scenarios:
    - 同一租户下的关联项目
    - 有明确协作关系的项目
    - 经过审批的跨项目引用
  
  # 禁止场景
  forbidden_scenarios:
    - 跨租户共享（除非明确授权）
    - 敏感项目对外共享
    - 合规限制的数据共享
  
  # 审批流程
  approval:
    required: true
    approvers: ["source_owner", "target_owner"]
    timeout: "24h"
```

### 6. 共享审计

```yaml
sharing_audit:
  # 记录内容
  log_content:
    - 共享操作类型
    - 共享内容标识
    - 共享范围
    - 操作人
    - 操作时间
    - 审批记录
  
  # 审计查询
  query:
    by_content: true
    by_user: true
    by_time_range: true
    by_visibility_change: true
  
  # 异常检测
  anomaly_detection:
    enabled: true
    patterns:
      - 大范围共享变更
      - 敏感内容共享
      - 异常时间共享
```

## 异常处理

### 过度共享
- 检测并阻止
- 通知管理员
- 记录审计日志

### 脱敏失败
- 阻止共享
- 提示手动处理
- 记录异常

### 权限不足
- 拒绝操作
- 提示申请权限
- 记录尝试日志

## 完成标准
- [x] 共享内容分级明确
- [x] 脱敏规则清晰
- [x] 可见性规则完整
- [x] 共享操作规则明确
- [x] 跨项目共享规则清晰
- [x] 共享审计机制完整
- [x] 协作信息能共享，但不会过度暴露

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
