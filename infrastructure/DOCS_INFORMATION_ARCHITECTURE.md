# DOCS_INFORMATION_ARCHITECTURE.md - 开发者文档信息架构

## 目的
定义开发者文档信息架构，确保开发者文档不再零散，形成完整导航。

## 适用范围
- 开发者文档
- API 文档
- SDK 文档
- 集成指南

## 核心规则

### 1. 文档结构

```
┌─────────────────────────────────────────────────────────────┐
│                    开发者文档架构                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 快速开始                                                │
│     ├── 概述                                                │
│     ├── 5分钟上手                                           │
│     ├── 第一个请求                                          │
│     └── 常见问题                                            │
│                                                             │
│  2. 认证授权                                                │
│     ├── 认证方式                                            │
│     ├── API Key 管理                                        │
│     ├── OAuth 流程                                          │
│     └── 权限范围                                            │
│                                                             │
│  3. SDK                                                     │
│     ├── SDK 概览                                            │
│     ├── 安装指南                                            │
│     ├── 语言支持                                            │
│     └── 版本历史                                            │
│                                                             │
│  4. API Reference                                           │
│     ├── API 概览                                            │
│     ├── 端点列表                                            │
│     ├── 请求格式                                            │
│     └── 响应格式                                            │
│                                                             │
│  5. Connectors                                              │
│     ├── 连接器列表                                          │
│     ├── 配置指南                                            │
│     └── 故障排除                                            │
│                                                             │
│  6. Events/Webhooks                                         │
│     ├── 事件类型                                            │
│     ├── Webhook 配置                                        │
│     └── 事件示例                                            │
│                                                             │
│  7. Limits/Quotas                                           │
│     ├── 速率限制                                            │
│     ├── 配额说明                                            │
│     └── 超限处理                                            │
│                                                             │
│  8. Troubleshooting                                         │
│     ├── 常见错误                                            │
│     ├── 调试指南                                            │
│     └── 支持渠道                                            │
│                                                             │
│  9. Migration Guides                                        │
│     ├── 版本迁移                                            │
│     ├── API 变更                                            │
│     └── 废弃公告                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 快速开始

```yaml
quick_start:
  # 概述
  overview:
    content:
      - 平台介绍
      - 核心能力
      - 适用场景
      - 技术栈
  
  # 5分钟上手
  five_minutes:
    steps:
      - 注册账号
      - 获取 API Key
      - 发送第一个请求
      - 查看结果
  
  # 第一个请求
  first_request:
    content:
      - 请求示例
      - 响应示例
      - 代码示例
    languages:
      - curl
      - Python
      - JavaScript
      - Java
```

### 3. 认证授权

```yaml
authentication:
  # 认证方式
  methods:
    api_key:
      description: "API Key 认证"
      usage: "Header: X-API-Key"
      security: "HTTPS 必需"
    
    oauth:
      description: "OAuth 2.0"
      flows:
        - authorization_code
        - client_credentials
      scopes:
        - read
        - write
        - admin
  
  # API Key 管理
  key_management:
    actions:
      - 创建 Key
      - 查看 Key
      - 撤销 Key
      - 设置权限
  
  # 权限范围
  scopes:
    read:
      description: "只读权限"
      endpoints: ["GET /*"]
    
    write:
      description: "读写权限"
      endpoints: ["GET /*", "POST /*", "PUT /*"]
    
    admin:
      description: "管理权限"
      endpoints: ["*"]
```

### 4. SDK

```yaml
sdk:
  # SDK 概览
  overview:
    content:
      - SDK 功能
      - 支持语言
      - 安装方式
      - 版本策略
  
  # 安装指南
  installation:
    python: "pip install xiaoyi-claw"
    javascript: "npm install xiaoyi-claw"
    java: "implementation 'com.xiaoyi:claw:1.0.0'"
    go: "go get github.com/xiaoyi/claw"
  
  # 语言支持
  language_support:
    - name: "Python"
      version: ">= 3.8"
      status: "stable"
    
    - name: "JavaScript"
      version: ">= Node 16"
      status: "stable"
    
    - name: "Java"
      version: ">= 11"
      status: "stable"
    
    - name: "Go"
      version: ">= 1.20"
      status: "beta"
```

### 5. API Reference

```yaml
api_reference:
  # API 概览
  overview:
    base_url: "https://api.xiaoyi-claw.com/v1"
    protocol: "HTTPS"
    format: "JSON"
  
  # 端点列表
  endpoints:
    - path: "/memory"
      methods: ["GET", "POST"]
      description: "记忆管理"
    
    - path: "/calendar"
      methods: ["GET", "POST", "PUT", "DELETE"]
      description: "日程管理"
    
    - path: "/contact"
      methods: ["GET"]
      description: "联系人搜索"
  
  # 请求格式
  request_format:
    headers:
      - "Content-Type: application/json"
      - "Authorization: Bearer {token}"
    
    body:
      format: "JSON"
      encoding: "UTF-8"
  
  # 响应格式
  response_format:
    success:
      status: "2xx"
      body: "JSON"
    
    error:
      status: "4xx, 5xx"
      body:
        code: "ERROR_CODE"
        message: "Error description"
        details: "Additional info"
```

### 6. Connectors

```yaml
connectors:
  # 连接器列表
  list:
    - name: "Slack"
      type: "messaging"
      status: "stable"
    
    - name: "Notion"
      type: "knowledge"
      status: "stable"
    
    - name: "GitHub"
      type: "development"
      status: "stable"
  
  # 配置指南
  configuration:
    steps:
      - 选择连接器
      - 获取凭证
      - 配置参数
      - 测试连接
      - 启用连接器
```

### 7. Events/Webhooks

```yaml
events:
  # 事件类型
  types:
    - name: "task.created"
      description: "任务创建"
      payload: "TaskObject"
    
    - name: "task.completed"
      description: "任务完成"
      payload: "TaskObject"
    
    - name: "memory.updated"
      description: "记忆更新"
      payload: "MemoryObject"
  
  # Webhook 配置
  webhook:
    setup:
      - 创建端点
      - 注册 URL
      - 验证签名
      - 测试事件
  
  # 事件示例
  examples:
    - event: "task.created"
      payload: |
        {
          "event": "task.created",
          "timestamp": "2026-04-07T12:00:00Z",
          "data": {...}
        }
```

### 8. Limits/Quotas

```yaml
limits:
  # 速率限制
  rate_limits:
    default:
      requests: 100
      period: "minute"
    
    authenticated:
      requests: 1000
      period: "minute"
  
  # 配额说明
  quotas:
    storage:
      free: "1GB"
      pro: "100GB"
      enterprise: "unlimited"
    
    api_calls:
      free: "10000/day"
      pro: "100000/day"
      enterprise: "unlimited"
  
  # 超限处理
  handling:
    response:
      status: 429
      headers:
        - "X-RateLimit-Limit"
        - "X-RateLimit-Remaining"
        - "X-RateLimit-Reset"
```

### 9. Troubleshooting

```yaml
troubleshooting:
  # 常见错误
  common_errors:
    - code: "AUTH_FAILED"
      cause: "认证失败"
      solution: "检查 API Key 是否正确"
    
    - code: "RATE_LIMIT"
      cause: "速率限制"
      solution: "等待重置或升级计划"
    
    - code: "INVALID_REQUEST"
      cause: "请求格式错误"
      solution: "检查请求参数"
  
  # 调试指南
  debugging:
    tools:
      - 日志查看
      - 请求追踪
      - 响应分析
  
  # 支持渠道
  support:
    - 文档中心
    - 社区论坛
    - 技术支持
    - GitHub Issues
```

### 10. Migration Guides

```yaml
migration:
  # 版本迁移
  version_migration:
    v1_to_v2:
      changes:
        - "端点路径变更"
        - "响应格式调整"
        - "认证方式升级"
      guide: "/docs/migration/v1-to-v2"
  
  # API 变更
  api_changes:
    deprecated:
      - endpoint: "/v1/old-api"
        replacement: "/v2/new-api"
        sunset: "2026-06-01"
  
  # 废弃公告
  deprecation:
    notice_period: "90 days"
    communication:
      - 文档公告
      - 邮件通知
      - API 响应头警告
```

## 完成标准
- [x] 文档结构完整
- [x] 快速开始内容清晰
- [x] 认证授权说明完整
- [x] SDK 文档完整
- [x] API Reference 完整
- [x] Connectors 文档完整
- [x] Events/Webhooks 文档完整
- [x] Limits/Quotas 说明清晰
- [x] Troubleshooting 完整
- [x] Migration Guides 完整
- [x] 开发者文档不再零散，形成完整导航

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
