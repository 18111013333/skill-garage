# TRY_IT_SANDBOX_POLICY.md - 开发者试用沙箱规则

## 目的
定义开发者试用沙箱规则，确保开发者可低风险试用平台能力。

## 适用范围
- 沙箱环境
- 试用功能
- 数据规则
- 迁移规则

## 核心规则

### 1. 沙箱能力范围

```yaml
sandbox_capabilities:
  # 可试用能力
  available:
    - 核心对话 API
    - 记忆管理 API
    - 日程查询 API
    - 联系人搜索 API
    - 基础搜索功能
  
  # 不可试用能力
  unavailable:
    - 生产数据访问
    - 外部集成
    - 批量操作
    - 敏感操作
    - 付费功能
  
  # 功能限制
  limitations:
    max_requests: 1000
    max_storage: 10MB
    max_concurrent: 5
    rate_limit: 10/minute
```

### 2. 假数据规则

```yaml
mock_data:
  # 数据类型
  types:
    user_data:
      source: "synthetic"
      privacy: "no_real_pii"
    
    memory_data:
      source: "generated"
      retention: "sandbox_only"
    
    calendar_data:
      source: "sample"
      scope: "demo_only"
  
  # 数据生成
  generation:
    method: "auto_generate"
    volume: "limited"
    variety: "representative"
  
  # 数据隔离
  isolation:
    from_production: true
    cross_sandbox: false
    export_allowed: false
```

### 3. 限流规则

```yaml
rate_limiting:
  # 请求限制
  requests:
    per_minute: 10
    per_hour: 100
    per_day: 1000
  
  # 并发限制
  concurrency:
    max_connections: 5
    max_websockets: 2
  
  # 存储限制
  storage:
    max_documents: 100
    max_size_mb: 10
  
  # 超限处理
  on_exceed:
    action: "reject"
    response:
      status: 429
      message: "Sandbox rate limit exceeded"
      retry_after: "60s"
```

### 4. 数据保留规则

```yaml
data_retention:
  # 保留期限
  retention:
    default: "7 days"
    max: "30 days"
  
  # 清理规则
  cleanup:
    frequency: "daily"
    action: "auto_delete"
    notification: "3 days before"
  
  # 导出限制
  export:
    allowed: false
    reason: "Sandbox data is temporary"
  
  # 备份
  backup:
    enabled: false
    reason: "Sandbox is for testing only"
```

### 5. 禁止动作

```yaml
prohibited_actions:
  # 严格禁止
  strict:
    - 访问生产数据
    - 执行真实外部调用
    - 发送真实消息
    - 修改真实配置
    - 创建真实用户
  
  # 需审批
  require_approval:
    - 批量数据导入
    - 自定义集成测试
    - 性能压力测试
  
  # 检测与处理
  enforcement:
    detection: "automatic"
    on_violation:
      - 阻止操作
      - 记录日志
      - 通知管理员
      - 可能暂停沙箱
```

### 6. 沙箱生命周期

```yaml
lifecycle:
  # 创建
  creation:
    trigger: "开发者注册"
    auto_provision: true
    setup_time: "< 5 minutes"
  
  # 激活
  activation:
    duration: "30 days"
    extendable: true
    max_extensions: 3
  
  # 暂停
  suspension:
    triggers:
      - 长期不活跃 (> 14 days)
      - 违规操作
      - 用户请求
    action: "disable_access"
  
  # 回收
  reclamation:
    triggers:
      - 试用期结束
      - 用户注销
      - 长期暂停
    action: "delete_all_data"
    notice: "7 days before"
```

### 7. 迁移到正式租户

```yaml
migration:
  # 迁移条件
  prerequisites:
    - 完成沙箱测试
    - 签署服务协议
    - 配置付费计划
    - 完成安全审核
  
  # 迁移流程
  process:
    steps:
      - 申请迁移
      - 审核批准
      - 创建正式租户
      - 配置生产环境
      - 迁移配置（非数据）
      - 验证功能
      - 关闭沙箱
  
  # 不可迁移内容
  non_migratable:
    - 沙箱数据
    - 测试记录
    - 临时配置
    - 假数据
  
  # 可迁移内容
  migratable:
    - 代码配置
    - 集成设置
    - API 调用逻辑
    - SDK 配置
```

### 8. 沙箱监控

```yaml
monitoring:
  # 使用监控
  usage:
    metrics:
      - API 调用量
      - 存储使用量
      - 活跃用户数
      - 错误率
  
  # 行为监控
  behavior:
    alerts:
      - 异常高频调用
      - 尝试访问生产
      - 可疑数据访问
  
  # 报告
  reporting:
    frequency: "weekly"
    content:
      - 使用统计
      - 异常事件
      - 即将到期提醒
```

## 异常处理

### 沙箱故障
- 通知用户
- 提供替代方案
- 记录故障日志

### 违规操作
- 立即阻止
- 记录详情
- 通知管理员
- 可能暂停沙箱

### 迁移失败
- 回滚操作
- 保留沙箱
- 通知用户
- 提供支持

## 完成标准
- [x] 沙箱能力范围明确
- [x] 假数据规则清晰
- [x] 限流规则完整
- [x] 数据保留规则明确
- [x] 禁止动作清晰
- [x] 沙箱生命周期完整
- [x] 迁移规则明确
- [x] 沙箱监控完整
- [x] 开发者可低风险试用平台能力

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
