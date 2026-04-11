# AUDIT_LOG.md - 审计日志规范

## 目的
定义审计日志的格式、存储、查询和保留策略。

## 适用范围
所有需要审计的操作，包括高风险操作、系统配置变更、安全事件。

## 审计触发条件

| 触发条件 | 审计级别 |
|----------|----------|
| 风险等级 ≥ HIGH | 必须审计 |
| 累积风险 > 10 | 必须审计 |
| 用户拒绝确认 | 必须审计 |
| 操作失败 | 必须审计 |
| 安全边界违规 | 必须审计 |
| 系统配置变更 | 必须审计 |

## 日志格式

### 标准格式
```json
{
  "auditId": "audit_20260406_001",
  "timestamp": "2026-04-06T10:32:00+08:00",
  "sessionId": "session_001",
  "userId": "user_001",
  "operation": {
    "type": "file_delete",
    "target": "/path/to/file",
    "params": {}
  },
  "risk": {
    "level": "HIGH",
    "score": 3,
    "cumulativeScore": 8
  },
  "confirmation": {
    "required": true,
    "obtained": true,
    "method": "user_prompt",
    "responseTime": 5000
  },
  "result": {
    "status": "success",
    "message": "File deleted successfully"
  },
  "context": {
    "userAgent": "xiaoyi-channel",
    "ipAddress": "192.168.1.1",
    "requestId": "req_001"
  }
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| auditId | string | 是 | 唯一审计ID |
| timestamp | string | 是 | ISO 8601 时间戳 |
| sessionId | string | 是 | 会话ID |
| userId | string | 是 | 用户ID |
| operation.type | string | 是 | 操作类型 |
| operation.target | string | 是 | 操作目标 |
| risk.level | string | 是 | 风险等级 |
| confirmation.required | boolean | 是 | 是否需要确认 |
| result.status | string | 是 | 执行状态 |

## 存储策略

### 存储位置
```
~/.openclaw/audit/
├── current/           # 当前日志
│   └── audit-YYYY-MM.jsonl
├── archive/           # 归档日志
│   └── audit-YYYY-MM.tar.gz
└── index/             # 索引文件
    └── audit-index.json
```

### 存储配置
```json
{
  "maxFileSize": 104857600,
  "maxFilesPerMonth": 10,
  "compressionEnabled": true,
  "encryptionEnabled": true,
  "encryptionAlgorithm": "AES-256-GCM"
}
```

## 保留策略

| 日志类型 | 保留期限 | 归档策略 |
|----------|----------|----------|
| 高风险操作 | 1年 | 自动归档 |
| 安全事件 | 3年 | 永久保留 |
| 普通操作 | 90天 | 自动删除 |
| 失败操作 | 180天 | 自动归档 |

## 查询接口

### 查询参数
| 参数 | 类型 | 说明 |
|------|------|------|
| startTime | string | 开始时间 |
| endTime | string | 结束时间 |
| userId | string | 用户ID |
| operationType | string | 操作类型 |
| riskLevel | string | 风险等级 |
| status | string | 执行状态 |

### 查询示例
```json
{
  "query": {
    "startTime": "2026-04-01T00:00:00+08:00",
    "endTime": "2026-04-06T23:59:59+08:00",
    "riskLevel": "HIGH",
    "status": "failure"
  },
  "pagination": {
    "offset": 0,
    "limit": 100
  }
}
```

## 异常处理

| 异常 | 处理 |
|------|------|
| 日志写入失败 | 缓存到内存，稍后重试 |
| 存储空间不足 | 触发归档，清理旧日志 |
| 查询超时 | 返回部分结果，提示缩小范围 |

## 维护方式
- 调整保留期限: 修改保留策略表
- 新增审计触发: 更新触发条件表
- 调整存储配置: 修改存储配置

## 引用文件
- `safety/RISK_POLICY.md` - 风险策略
- `observability/LOG_FORMAT.md` - 日志格式
