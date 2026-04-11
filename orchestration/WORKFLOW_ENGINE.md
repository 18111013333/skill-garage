# WORKFLOW_ENGINE.md - 工作流引擎规范

## 目的
定义工作流的设计、执行和管理规范。

## 适用范围
所有需要多步骤编排的复杂任务。

## 工作流类型

| 类型 | 说明 | 适用场景 | 特点 |
|------|------|----------|------|
| 顺序流 | 线性执行 | 简单流程 | 顺序依赖 |
| 并行流 | 并行执行 | 独立任务 | 提高效率 |
| 条件流 | 条件分支 | 业务逻辑 | 灵活决策 |
| 循环流 | 循环执行 | 批量处理 | 重复任务 |

## 工作流定义

### 基本结构
```yaml
workflow:
  id: user_onboarding
  name: "用户入职流程"
  version: "1.0"
  timeout: 3600
  
  variables:
    user_id: null
    department: null
  
  steps:
    - id: create_account
      name: "创建账号"
      action: create_user_account
      params:
        user_id: "${user_id}"
      retry: 3
      
    - id: assign_permissions
      name: "分配权限"
      action: assign_user_permissions
      params:
        user_id: "${user_id}"
        department: "${department}"
      depends_on: [create_account]
      
    - id: send_welcome
      name: "发送欢迎邮件"
      action: send_email
      params:
        to: "${user_id}@company.com"
        template: welcome
      depends_on: [create_account]
```

### 条件分支
```yaml
steps:
  - id: check_department
    name: "检查部门"
    action: get_department
    params:
      user_id: "${user_id}"
      
  - id: assign_tech_permissions
    name: "分配技术权限"
    condition: "${department == 'tech'}"
    action: assign_permissions
    params:
      role: developer
      
  - id: assign_sales_permissions
    name: "分配销售权限"
    condition: "${department == 'sales'}"
    action: assign_permissions
    params:
      role: sales
```

### 并行执行
```yaml
steps:
  - id: parallel_setup
    name: "并行设置"
    parallel:
      - id: setup_email
        action: create_email_account
      - id: setup_slack
        action: create_slack_account
      - id: setup_github
        action: create_github_account
    join:
      strategy: all
```

## 执行控制

### 状态管理
| 状态 | 说明 | 允许转换 |
|------|------|----------|
| pending | 待执行 | → running |
| running | 执行中 | → completed, failed, paused |
| completed | 已完成 | → archived |
| failed | 已失败 | → retry, cancelled |
| paused | 已暂停 | → running, cancelled |
| cancelled | 已取消 | → archived |

### 超时控制
```yaml
timeout:
  workflow: 3600
  step: 600
  action: 300
  on_timeout: fail
```

### 重试策略
```yaml
retry:
  max_attempts: 3
  backoff: exponential
  initial_delay: 10s
  max_delay: 300s
  retry_on:
    - timeout
    - temporary_error
```

## 错误处理

### 错误类型
| 错误类型 | 处理方式 | 说明 |
|----------|----------|------|
| 临时错误 | 重试 | 网络抖动等 |
| 业务错误 | 补偿 | 业务逻辑错误 |
| 系统错误 | 告警 | 系统异常 |
| 超时错误 | 重试/失败 | 执行超时 |

### 补偿事务
```yaml
compensation:
  enabled: true
  strategy: reverse
  steps:
    - trigger: create_account_failed
      compensation: delete_account
    - trigger: permissions_failed
      compensation: revoke_permissions
```

## 工作流模板

### 审批流程模板
```yaml
template: approval_workflow
  params:
    approvers: required
    timeout: default=86400
  steps:
    - id: submit
      action: create_request
    - id: approve
      action: wait_for_approval
      params:
        approvers: "${approvers}"
        timeout: "${timeout}"
    - id: execute
      condition: "${approved == true}"
      action: execute_request
    - id: reject
      condition: "${approved == false}"
      action: notify_rejection
```

### 数据处理流程模板
```yaml
template: etl_workflow
  params:
    source: required
    target: required
    transform: required
  steps:
    - id: extract
      action: extract_data
      params:
        source: "${source}"
    - id: transform
      action: transform_data
      params:
        rules: "${transform}"
    - id: load
      action: load_data
      params:
        target: "${target}"
    - id: verify
      action: verify_data
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 执行时间 | 工作流耗时 | >预期2倍 |
| 成功率 | 成功/总数 | <95% |
| 步骤失败率 | 失败步骤/总步骤 | >5% |
| 等待时间 | 步骤等待时间 | >60s |

## 可视化

### 流程图
```yaml
visualization:
  type: dag
  nodes:
    - id: step1
      label: "步骤1"
    - id: step2
      label: "步骤2"
  edges:
    - from: step1
      to: step2
```

### 执行追踪
```yaml
trace:
  enabled: true
  storage: jaeger
  sampling_rate: 0.1
  retention: 7d
```

## 维护方式
- 新增工作流: 创建工作流定义
- 新增模板: 创建工作流模板
- 调整策略: 更新执行控制配置

## 引用文件
- `automation/TASK_AUTOMATION.md` - 任务自动化
- `automation/SCHEDULE_MANAGER.md` - 调度管理
