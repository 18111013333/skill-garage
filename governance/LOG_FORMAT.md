# LOG_FORMAT.md - 日志格式规范

## 目的
定义统一的日志格式，确保日志可解析、可检索、可分析。

## 适用范围
所有系统组件的日志输出。

## 日志格式

### 标准格式
```json
{
  "timestamp": "2026-04-06T10:32:00.123+08:00",
  "level": "INFO",
  "logger": "orchestrator",
  "message": "Task classified successfully",
  "context": {
    "sessionId": "session_001",
    "taskId": "task_001",
    "requestId": "req_001"
  },
  "data": {
    "taskType": "qa",
    "confidence": 0.95
  },
  "trace": {
    "traceId": "trace_001",
    "spanId": "span_001",
    "parentSpanId": null
  },
  "extra": {}
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| timestamp | string | 是 | ISO 8601 时间戳 |
| level | string | 是 | 日志级别 |
| logger | string | 是 | 日志来源 |
| message | string | 是 | 日志消息 |
| context | object | 否 | 上下文信息 |
| data | object | 否 | 业务数据 |
| trace | object | 否 | 追踪信息 |
| extra | object | 否 | 扩展信息 |

## 日志级别

| 级别 | 值 | 说明 | 使用场景 |
|------|-----|------|----------|
| DEBUG | 10 | 调试 | 开发调试 |
| INFO | 20 | 信息 | 正常流程 |
| WARNING | 30 | 警告 | 异常但不影响运行 |
| ERROR | 40 | 错误 | 影响功能 |
| CRITICAL | 50 | 严重 | 系统不可用 |

## 日志分类

### 按来源分类
| logger | 说明 |
|--------|------|
| orchestrator | 总调度 |
| classifier | 任务分类 |
| planner | 任务规划 |
| router | 技能路由 |
| executor | 执行器 |
| tool | 工具调用 |
| skill | 技能执行 |
| memory | 记忆系统 |
| validator | 输出校验 |

### 按类型分类
| 类型 | 说明 | 示例 |
|------|------|------|
| request | 请求日志 | 请求进入/退出 |
| execution | 执行日志 | 任务执行过程 |
| tool | 工具日志 | 工具调用 |
| error | 错误日志 | 错误信息 |
| audit | 审计日志 | 审计记录 |
| metric | 指标日志 | 指标数据 |

## 日志输出

### 输出目标
| 目标 | 说明 | 配置 |
|------|------|------|
| console | 控制台 | 开发环境 |
| file | 文件 | 生产环境 |
| syslog | 系统日志 | 服务器 |
| remote | 远程服务 | 集中日志 |

### 输出配置
```json
{
  "outputs": [
    {
      "type": "console",
      "enabled": true,
      "level": "DEBUG",
      "format": "pretty"
    },
    {
      "type": "file",
      "enabled": true,
      "level": "INFO",
      "format": "json",
      "path": "~/.openclaw/logs/app.log",
      "rotation": {
        "maxSize": 10485760,
        "maxFiles": 10,
        "compress": true
      }
    }
  ]
}
```

## 日志追踪

### TraceContext格式
```json
{
  "traceId": "trace_001",
  "spanId": "span_001",
  "parentSpanId": "span_000",
  "sampled": true
}
```

### 追踪规则
1. 每个请求生成唯一 traceId
2. 每个操作生成唯一 spanId
3. 子操作继承 parentSpanId
4. 关联日志通过 traceId 关联

## 日志采样

### 采样策略
| 策略 | 说明 | 配置 |
|------|------|------|
| 全量 | 记录所有日志 | sampled: true |
| 随机 | 随机采样 | sampleRate: 0.1 |
| 错误优先 | 错误必记录 | errorSampled: true |
| 动态 | 根据负载调整 | dynamicSampling: true |

### 采样配置
```json
{
  "sampling": {
    "enabled": true,
    "defaultRate": 1.0,
    "errorRate": 1.0,
    "warningRate": 0.5,
    "infoRate": 0.1,
    "debugRate": 0.01
  }
}
```

## 日志清理

### 清理规则
| 规则 | 条件 | 动作 |
|------|------|------|
| 按时间 | 超过保留期 | 删除 |
| 按大小 | 超过大小限制 | 压缩归档 |
| 按级别 | DEBUG日志 | 优先清理 |

### 清理配置
```json
{
  "cleanup": {
    "enabled": true,
    "retentionDays": {
      "DEBUG": 7,
      "INFO": 30,
      "WARNING": 90,
      "ERROR": 180,
      "CRITICAL": 365
    },
    "maxTotalSize": 1073741824,
    "compressAfterDays": 30
  }
}
```

## 异常处理

| 异常 | 处理 |
|------|------|
| 写入失败 | 缓存到内存 |
| 磁盘满 | 触发清理 |
| 格式错误 | 使用默认格式 |

## 维护方式
- 新增日志类型: 添加到分类表
- 调整输出: 修改输出配置
- 调整采样: 修改采样配置

## 引用文件
- `observability/ERROR_TAXONOMY.md` - 错误分类
- `governance/AUDIT_LOG.md` - 审计日志
