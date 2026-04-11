# SEGREGATION_OF_DUTIES.md - 职责分离规则

## 目的
定义职责分离规则，确保关键高风险流程不再由单点角色全包。

## 适用范围
- 权限分配
- 审批流程
- 系统操作
- 治理实施

## 核心规则

### 1. 权限分离矩阵

```yaml
permission_segregation:
  # 禁止同时拥有的权限组合
  forbidden_combinations:
    - role: "开发者"
      cannot_have: ["生产部署审批", "生产环境管理"]
    
    - role: "审批者"
      cannot_have: ["执行操作", "配置修改"]
    
    - role: "审计员"
      cannot_have: ["系统配置", "数据修改"]
    
    - role: "租户管理员"
      cannot_have: ["平台管理", "跨租户访问"]
    
    - role: "安全负责人"
      cannot_have: ["日常运维", "代码部署"]
```

### 2. 审批与执行分离

```yaml
approval_execution_segregation:
  # 必须分离的场景
  required_separation:
    - scenario: "系统配置变更"
      approver: "配置管理员"
      executor: "运维工程师"
      min_approvers: 1
    
    - scenario: "权限授予"
      approver: "安全负责人"
      executor: "系统管理员"
      min_approvers: 1
    
    - scenario: "数据导出"
      approver: "数据负责人"
      executor: "数据管理员"
      min_approvers: 1
    
    - scenario: "代码部署"
      approver: "发布经理"
      executor: "部署工程师"
      min_approvers: 1
    
    - scenario: "高风险操作"
      approver: "管理层"
      executor: "指定操作员"
      min_approvers: 2
```

### 3. 治理与实施分离

```yaml
governance_implementation_segregation:
  # 角色分离要求
  role_separation:
    governance_roles:
      - 治理委员会成员
      - AI 治理官
      - 合规负责人
      - 审计负责人
    
    implementation_roles:
      - 系统管理员
      - 开发工程师
      - 运维工程师
      - 业务操作员
    
    rules:
      - 治理角色不能同时担任实施角色
      - 治理决策者不能参与执行
      - 审计人员不能参与被审计工作
```

### 4. 关键流程职责分离

```yaml
critical_process_segregation:
  # 用户管理流程
  user_management:
    request: "业务经理"
    approval: "HR + IT安全"
    execution: "系统管理员"
    verification: "审计员"
  
  # 权限管理流程
  permission_management:
    request: "部门经理"
    approval: "安全负责人"
    execution: "权限管理员"
    verification: "审计员"
  
  # 变更管理流程
  change_management:
    request: "变更发起人"
    assessment: "技术负责人"
    approval: "变更委员会"
    execution: "变更执行人"
    verification: "质量保证"
  
  # 数据管理流程
  data_management:
    request: "数据使用者"
    approval: "数据负责人"
    execution: "数据管理员"
    verification: "合规负责人"
```

### 5. 例外审批要求

```yaml
exception_approval:
  # 例外场景
  scenarios:
    - scenario: "紧急修复"
      conditions:
        - 系统故障
        - 安全漏洞
        - 数据丢失风险
      approval: "值班经理 + 事后补批"
      documentation: "必须记录原因"
      review: "24小时内复审"
    
    - scenario: "单人值班"
      conditions:
        - 非工作时间
        - 人员不足
        - 低风险操作
      approval: "值班经理"
      documentation: "必须记录原因"
      review: "下一工作日复审"
    
    - scenario: "测试环境"
      conditions:
        - 非生产环境
        - 无真实数据
        - 无外部影响
      approval: "测试负责人"
      documentation: "测试记录"
      review: "月度抽查"
```

### 6. 检测与监控

```yaml
detection_monitoring:
  # 自动检测
  auto_detection:
    enabled: true
    checks:
      - 权限组合冲突检测
      - 审批执行同一人检测
      - 角色冲突检测
      - 异常操作检测
  
  # 告警规则
  alerts:
    - condition: "检测到禁止的权限组合"
      severity: "high"
      action: "立即通知安全负责人"
    
    - condition: "审批人与执行人相同"
      severity: "medium"
      action: "记录并通知审计"
    
    - condition: "治理角色执行操作"
      severity: "high"
      action: "阻止并通知管理层"
  
  # 定期审查
  periodic_review:
    frequency: "monthly"
    scope:
      - 权限分配审查
      - 角色分配审查
      - 例外记录审查
      - 冲突解决审查
```

## 异常处理

### 冲突发现
- 立即阻止操作
- 通知相关人员
- 记录冲突详情
- 提交解决方案

### 例外申请
- 说明例外原因
- 提出补偿措施
- 获得必要审批
- 设置有效期

### 违规处理
- 记录违规行为
- 评估影响范围
- 采取纠正措施
- 必要时升级处理

## 完成标准
- [x] 权限分离矩阵完整
- [x] 审批执行分离规则清晰
- [x] 治理实施分离明确
- [x] 关键流程职责分离完整
- [x] 例外审批要求明确
- [x] 检测监控规则完整
- [x] 关键高风险流程不再由单点角色全包

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
