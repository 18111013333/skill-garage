# AGENT_COMMUNICATION.md - 智能体通信协议

## 目的
定义多智能体系统中的通信协议和消息格式。

## 适用范围
所有智能体间通信、协作消息传递。

---

## 一、通信架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           智能体通信架构                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                   │
│  │  Agent A    │────▶│  Message    │────▶│  Agent B    │                   │
│  │             │     │  Broker     │     │             │                   │
│  └─────────────┘     └─────────────┘     └─────────────┘                   │
│         │                   │                   │                          │
│         │                   │                   │                          │
│         ▼                   ▼                   ▼                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Communication Bus                             │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │   │
│  │  │ Direct    │  │ Broadcast │  │ Pub/Sub   │  │ Request/  │        │   │
│  │  │ Message   │  │           │  │           │  │ Response  │        │   │
│  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 二、消息格式

### 2.1 标准消息结构
```json
{
  "message_id": "msg-uuid",
  "timestamp": "2026-04-07T15:00:00Z",
  "source": {
    "agent_id": "agent-001",
    "agent_type": "executor",
    "capability": "code_analysis"
  },
  "target": {
    "agent_id": "agent-002",
    "agent_type": "planner",
    "routing": "direct|broadcast|pubsub"
  },
  "message_type": "request|response|notification|error",
  "payload": {
    "action": "analyze_code",
    "data": {},
    "context": {}
  },
  "metadata": {
    "priority": "high|medium|low",
    "ttl": 60000,
    "correlation_id": "corr-uuid",
    "trace_id": "trace-uuid"
  }
}
```

### 2.2 消息类型
| 类型 | 说明 | 使用场景 |
|------|------|----------|
| request | 请求消息 | 请求其他智能体执行任务 |
| response | 响应消息 | 回复请求结果 |
| notification | 通知消息 | 状态变更通知 |
| error | 错误消息 | 错误报告 |
| heartbeat | 心跳消息 | 存活检测 |
| sync | 同步消息 | 状态同步 |

---

## 三、通信模式

### 3.1 直接通信
```
Agent A ────────▶ Agent B
         request
Agent A ◀──────── Agent B
         response
```

### 3.2 广播通信
```
                ┌─────────┐
                │ Agent B │
                └─────────┘
                     ▲
                     │
┌─────────┐     ┌─────────┐
│ Agent A │────▶│ Broadcast│
└─────────┘     │  Bus    │
                └─────────┘
                     │
                     ▼
                ┌─────────┐
                │ Agent C │
                └─────────┘
```

### 3.3 发布订阅
```
┌─────────┐     ┌─────────┐
│Publisher│────▶│  Topic  │────▶ ┌─────────┐
└─────────┘     │  Bus    │     │Subscriber│
                └─────────┘     └─────────┘
                     │
                     ▼
                ┌─────────┐
                │Subscriber│
                └─────────┘
```

### 3.4 请求响应
```
┌─────────┐  request   ┌─────────┐
│ Client  │───────────▶│ Server  │
│ Agent   │◀───────────│ Agent   │
└─────────┘  response  └─────────┘
```

---

## 四、通信协议

### 4.1 协议栈
```
┌─────────────────────────────────────┐
│         Application Layer           │  业务消息
├─────────────────────────────────────┤
│         Serialization Layer         │  JSON/Protobuf
├─────────────────────────────────────┤
│         Transport Layer             │  WebSocket/HTTP/gRPC
├─────────────────────────────────────┤
│         Network Layer               │  TCP/IP
└─────────────────────────────────────┘
```

### 4.2 序列化格式
| 格式 | 优点 | 缺点 | 使用场景 |
|------|------|------|----------|
| JSON | 可读性好 | 体积大 | 调试、日志 |
| Protobuf | 高效、小 | 不可读 | 生产环境 |
| MessagePack | 紧凑 | 兼容性 | 高性能场景 |

### 4.3 传输协议
| 协议 | 特点 | 使用场景 |
|------|------|----------|
| WebSocket | 双向、实时 | 实时协作 |
| HTTP/2 | 多路复用 | API调用 |
| gRPC | 高效、流式 | 微服务通信 |

---

## 五、消息路由

### 5.1 路由策略
```json
{
  "routing_rules": [
    {
      "rule_id": "route-001",
      "condition": {
        "message_type": "request",
        "target_capability": "code_analysis"
      },
      "action": {
        "route_to": "code-analyzer-agent",
        "load_balance": "round_robin"
      }
    },
    {
      "rule_id": "route-002",
      "condition": {
        "message_type": "notification",
        "topic": "status_update"
      },
      "action": {
        "route_to": "subscribers",
        "mode": "broadcast"
      }
    }
  ]
}
```

### 5.2 负载均衡
| 策略 | 说明 |
|------|------|
| round_robin | 轮询 |
| least_connections | 最少连接 |
| weighted | 加权 |
| capability_based | 基于能力 |

---

## 六、消息可靠性

### 6.1 可靠性保证
| 机制 | 说明 |
|------|------|
| 消息确认 | ACK机制 |
| 重试机制 | 失败重试 |
| 幂等性 | 重复处理 |
| 持久化 | 消息存储 |
| 死信队列 | 失败消息 |

### 6.2 消息确认流程
```
Sender                Receiver
  │                      │
  │──── message ────────▶│
  │                      │
  │◀──── ACK ────────────│
  │                      │
```

### 6.3 重试策略
```json
{
  "retry_policy": {
    "max_retries": 3,
    "backoff": "exponential",
    "initial_delay": 1000,
    "max_delay": 30000,
    "jitter": true
  }
}
```

---

## 七、安全机制

### 7.1 认证
| 方式 | 说明 |
|------|------|
| Token认证 | JWT Token |
| 证书认证 | mTLS |
| API Key | 密钥认证 |

### 7.2 授权
```json
{
  "authorization": {
    "agent_id": "agent-001",
    "permissions": [
      "send:code_analysis",
      "receive:analysis_result",
      "subscribe:status_update"
    ],
    "scope": ["project-001", "project-002"]
  }
}
```

### 7.3 加密
| 层级 | 加密方式 |
|------|----------|
| 传输层 | TLS 1.3 |
| 消息层 | AES-256-GCM |
| 端到端 | RSA-4096 |

---

## 八、监控与追踪

### 8.1 消息追踪
```json
{
  "trace": {
    "trace_id": "trace-uuid",
    "spans": [
      {
        "span_id": "span-001",
        "operation": "send_message",
        "start_time": "2026-04-07T15:00:00.000Z",
        "end_time": "2026-04-07T15:00:00.100Z",
        "status": "ok"
      },
      {
        "span_id": "span-002",
        "operation": "receive_message",
        "start_time": "2026-04-07T15:00:00.050Z",
        "end_time": "2026-04-07T15:00:00.150Z",
        "status": "ok"
      }
    ]
  }
}
```

### 8.2 监控指标
| 指标 | 说明 |
|------|------|
| message_rate | 消息速率 |
| latency | 延迟 |
| error_rate | 错误率 |
| queue_depth | 队列深度 |

---

## 版本
- 版本: V1.0.0
- 创建时间: 2026-04-07
- 适用: 终极鸽子王 V10.0
