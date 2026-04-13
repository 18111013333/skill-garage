# 日志规范模板

## 一、日志格式标准

### JSON格式
```json
{
  "timestamp": "2026-04-09T12:00:00.000Z",
  "level": "INFO",
  "service": "api-gateway",
  "trace_id": "abc123def456",
  "span_id": "span789",
  "user_id": "user_001",
  "message": "Request processed successfully",
  "context": {
    "method": "GET",
    "path": "/api/users/123",
    "status_code": 200,
    "duration_ms": 45
  },
  "environment": "production",
  "host": "api-server-01",
  "version": "1.2.0"
}
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| timestamp | string | 是 | ISO 8601格式时间戳 |
| level | string | 是 | 日志级别 |
| service | string | 是 | 服务名称 |
| trace_id | string | 是 | 链路追踪ID |
| message | string | 是 | 日志消息 |
| context | object | 否 | 上下文信息 |
| environment | string | 是 | 环境标识 |
| host | string | 是 | 主机名 |
| version | string | 否 | 服务版本 |

## 二、日志级别规范

### 级别定义
| 级别 | 使用场景 | 示例 |
|------|----------|------|
| DEBUG | 开发调试 | 变量值、执行路径 |
| INFO | 正常业务流程 | 请求处理、状态变更 |
| WARN | 潜在问题 | 性能下降、资源不足 |
| ERROR | 错误但不影响服务 | 请求失败、异常捕获 |
| FATAL | 严重错误导致服务不可用 | 数据库连接失败、启动失败 |

### 使用原则
- 生产环境默认INFO级别
- 问题排查时临时开启DEBUG
- ERROR及以上必须告警
- 避免在循环中打印日志

## 三、日志分类

### 访问日志
```json
{
  "type": "access",
  "timestamp": "2026-04-09T12:00:00.000Z",
  "client_ip": "192.168.1.100",
  "method": "GET",
  "path": "/api/users/123",
  "query": "include=profile",
  "status_code": 200,
  "response_size": 1024,
  "duration_ms": 45,
  "user_agent": "Mozilla/5.0...",
  "user_id": "user_001"
}
```

### 错误日志
```json
{
  "type": "error",
  "timestamp": "2026-04-09T12:00:00.000Z",
  "error": {
    "name": "DatabaseError",
    "message": "Connection refused",
    "stack": "Error: Connection refused\n    at DB.connect...",
    "code": "ECONNREFUSED"
  },
  "context": {
    "operation": "getUserData",
    "user_id": "user_001"
  }
}
```

### 业务日志
```json
{
  "type": "business",
  "timestamp": "2026-04-09T12:00:00.000Z",
  "event": "order_created",
  "data": {
    "order_id": "order_123",
    "user_id": "user_001",
    "amount": 99.99,
    "items_count": 3
  }
}
```

## 四、敏感信息处理

### 脱敏规则
| 类型 | 原始值 | 脱敏后 |
|------|--------|--------|
| 手机号 | 13812345678 | 138****5678 |
| 身份证 | 110101199001011234 | 110101********1234 |
| 银行卡 | 6222021234567890123 | 6222************123 |
| 邮箱 | user@example.com | u***@example.com |
| 密码 | password123 | ****** |

### 禁止记录
- 密码明文
- 支付密钥
- Token完整值
- 证书私钥
- 个人敏感信息

## 五、日志库配置

### Node.js (Winston)
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'api-gateway',
    environment: process.env.NODE_ENV
  },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' })
  ]
});
```

### Python (structlog)
```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()
logger.info("request_processed", user_id="user_001", duration_ms=45)
```

## 六、日志存储策略

### 保留周期
| 日志类型 | 保留时间 | 存储位置 |
|----------|----------|----------|
| 访问日志 | 30天 | Elasticsearch |
| 错误日志 | 90天 | Elasticsearch |
| 业务日志 | 1年 | 数据仓库 |
| 审计日志 | 3年 | 归档存储 |

### 存储优化
- 热数据：SSD，快速查询
- 温数据：HDD，正常查询
- 冷数据：归档，按需恢复
