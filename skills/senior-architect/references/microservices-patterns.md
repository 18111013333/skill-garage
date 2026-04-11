# 微服务架构模式库

## 目录

1. [服务拆分模式](#服务拆分模式)
2. [通信模式](#通信模式)
3. [数据管理模式](#数据管理模式)
4. [部署模式](#部署模式)
5. [弹性模式](#弹性模式)
6. [可观测性模式](#可观测性模式)
7. [安全模式](#安全模式)

---

## 服务拆分模式

### 1. 按业务能力拆分 (Decompose by Business Capability)

**定义**: 围绕业务能力组织服务，每个服务对应一个业务功能。

**适用场景**:
- 业务边界清晰
- 团队按业务线组织
- 需要独立部署的业务单元

**示例**:
```
电商系统拆分:
├── catalog-service      # 商品目录
├── order-service        # 订单管理
├── inventory-service    # 库存管理
├── payment-service      # 支付处理
├── shipping-service     # 物流配送
└── customer-service     # 客户管理
```

**优点**:
- 服务边界稳定
- 团队自治
- 业务理解直观

**缺点**:
- 初期识别业务能力困难
- 可能导致服务过大

---

### 2. 按子域拆分 (Decompose by Subdomain - DDD)

**定义**: 使用领域驱动设计(DDD)的限界上下文(Bounded Context)定义服务边界。

**适用场景**:
- 复杂业务领域
- 需要领域专家参与
- 长期演进系统

**示例**:
```
保险系统子域:
├── 核心域 (Core)
│   ├── policy-underwriting  # 保单核保
│   └── claims-processing    # 理赔处理
├── 支撑域 (Supporting)
│   ├── customer-management  # 客户管理
│   └── agent-management     # 代理人管理
└── 通用域 (Generic)
    ├── payment              # 支付
    └── notification         # 通知
```

**优点**:
- 边界清晰
- 领域语言统一
- 易于演进

**缺点**:
- 需要DDD专业知识
- 初期投入大

---

### 3. 绞杀者模式 (Strangler Fig Pattern)

**定义**: 逐步用新服务替换旧系统功能，最终完全替代。

**适用场景**:
- 遗留系统迁移
- 降低迁移风险
- 渐进式重构

**实施步骤**:
1. 识别要迁移的功能模块
2. 创建新服务实现该功能
3. 在旧系统前设置代理层
4. 逐步将流量路由到新服务
5. 移除旧系统代码

**示例架构**:
```
                    ┌─────────────────┐
                    │   API Gateway   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────────┐
        │ 新服务A  │  │ 新服务B  │  │  遗留系统    │
        │ (已迁移) │  │ (已迁移) │  │ (待迁移功能) │
        └──────────┘  └──────────┘  └──────────────┘
```

---

## 通信模式

### 1. 同步通信 - REST/HTTP

**适用场景**:
- 需要即时响应
- 简单查询操作
- 外部API暴露

**最佳实践**:
```yaml
# API设计规范
- 使用HTTP语义 (GET/POST/PUT/DELETE)
- 版本化: /api/v1/resource
- 分页: ?page=1&size=20
- 错误处理: 标准错误响应格式
- 超时设置: 连接5s, 读取30s
- 重试策略: 指数退避, 最大3次
```

**示例**:
```typescript
// 服务间调用
class OrderService {
  async getOrderWithUser(orderId: string) {
    const order = await this.orderRepo.findById(orderId);
    const user = await this.httpService.get(
      `${USER_SERVICE_URL}/api/v1/users/${order.userId}`,
      { timeout: 5000, retry: 3 }
    );
    return { ...order, user };
  }
}
```

---

### 2. 异步通信 - 消息队列

**适用场景**:
- 解耦服务
- 削峰填谷
- 最终一致性场景

**消息模式**:

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| 点对点 | 一对一消息 | 任务分发 |
| 发布订阅 | 一对多消息 | 事件广播 |
| 请求应答 | 双向通信 | 需要响应的异步调用 |

**常用消息中间件**:
- RabbitMQ: 可靠消息传递，复杂路由
- Kafka: 高吞吐，事件流
- Redis Pub/Sub: 简单场景，低延迟
- AWS SQS/SNS: 云原生，无运维

**示例**:
```typescript
// 事件发布
class OrderService {
  async createOrder(order: Order) {
    await this.orderRepo.save(order);
    await this.messageQueue.publish('order.created', {
      orderId: order.id,
      userId: order.userId,
      items: order.items,
      timestamp: Date.now()
    });
  }
}

// 事件消费
@Subscribe('order.created')
class InventoryService {
  async handle(event: OrderCreatedEvent) {
    for (const item of event.items) {
      await this.inventoryRepo.decrement(item.productId, item.quantity);
    }
  }
}
```

---

### 3. 服务网格 (Service Mesh)

**适用场景**:
- 大规模微服务
- 统一流量管理
- 高级可观测性

**核心功能**:
- 服务发现
- 负载均衡
- 熔断降级
- 金丝雀发布
- mTLS加密

**主流方案**:
- Istio: 功能全面，K8s原生
- Linkerd: 轻量级，易部署
- Consul Connect: HashiCorp生态

---

## 数据管理模式

### 1. 每服务一数据库 (Database per Service)

**定义**: 每个服务拥有独立的数据库，不共享数据存储。

**优点**:
- 服务独立部署
- 技术选型自由
- 故障隔离

**缺点**:
- 跨服务查询复杂
- 数据一致性挑战
- 运维成本增加

**示例**:
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Order Service  │  │  User Service   │  │ Catalog Service │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    ┌─────────┐          ┌─────────┐          ┌─────────┐
    │PostgreSQL│          │  MySQL  │          │ MongoDB │
    └─────────┘          └─────────┘          └─────────┘
```

---

### 2. Saga模式 (分布式事务)

**定义**: 通过一系列本地事务实现跨服务数据一致性。

**编排方式**:

#### 编排式 (Choreography)
```typescript
// 订单创建Saga - 事件驱动
Order Service: 创建订单 → 发布 OrderCreated
Inventory Service: 扣减库存 → 发布 InventoryReserved
Payment Service: 处理支付 → 发布 PaymentProcessed
Shipping Service: 创建配送 → 发布 ShippingCreated
Order Service: 更新状态 → 发布 OrderCompleted

// 补偿流程
Payment Service: 支付失败 → 发布 PaymentFailed
Inventory Service: 恢复库存 → 发布 InventoryRestored
Order Service: 取消订单 → 发布 OrderCancelled
```

#### 协调式 (Orchestration)
```typescript
class CreateOrderSaga {
  async execute(order: Order) {
    const sagaId = uuid();
    
    try {
      // 步骤1: 创建订单
      await this.orderService.create(order);
      
      // 步骤2: 预留库存
      await this.inventoryService.reserve(order.items);
      
      // 步骤3: 处理支付
      await this.paymentService.charge(order.payment);
      
      // 步骤4: 确认配送
      await this.shippingService.create(order.shipping);
      
      // 完成
      await this.orderService.confirm(order.id);
      
    } catch (error) {
      // 补偿
      await this.compensate(sagaId, order);
    }
  }
}
```

---

### 3. CQRS (命令查询职责分离)

**定义**: 分离读操作和写操作的数据模型。

**适用场景**:
- 读写比例差异大
- 复杂查询需求
- 高性能读取

**架构**:
```
         ┌──────────────────────────────────────┐
         │             Command Side             │
         │  ┌─────────┐    ┌─────────────────┐  │
Write ──▶│  │ Command │───▶│  Write Model    │  │
Request  │  │ Handler │    │  (主数据库)      │  │
         │  └─────────┘    └────────┬────────┘  │
         └──────────────────────────┼───────────┘
                                    │
                                    │ 事件同步
                                    ▼
         ┌──────────────────────────────────────┐
         │              Query Side              │
         │  ┌─────────────────┐  ┌───────────┐  │
Read ◀──│  │   Read Model    │◀─│  Event    │  │
Request │  │  (读优化视图)    │  │  Handler  │  │
         │  └─────────────────┘  └───────────┘  │
         └──────────────────────────────────────┘
```

---

## 部署模式

### 1. 容器化部署

**Docker最佳实践**:
```dockerfile
# 多阶段构建
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
USER node
CMD ["node", "dist/main.js"]
```

**健康检查**:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

---

### 2. Kubernetes部署

**Deployment配置**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    spec:
      containers:
      - name: order-service
        image: order-service:v1.2.0
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 3000
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 3000
```

---

### 3. 服务网格部署

**Istio配置示例**:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: order-service
spec:
  hosts:
  - order-service
  http:
  - route:
    - destination:
        host: order-service
        subset: v1
      weight: 90
    - destination:
        host: order-service
        subset: v2
      weight: 10  # 金丝雀发布
```

---

## 弹性模式

### 1. 熔断器 (Circuit Breaker)

**状态机**:
```
         失败率>阈值
    ┌─────────────────────▶
    │                      │
    ▼                      │
┌────────┐  半开成功  ┌────────┐
│  关闭  │◀──────────│  半开  │
│(正常)  │           │(探测)  │
└────────┘           └────────┘
    ▲                      │
    │      半开失败        │
    │  ┌───────────────────┘
    │  │
    │  ▼
┌────────┐  超时后  ┌────────┐
│  打开  │─────────▶│  半开  │
│(熔断)  │          │        │
└────────┘          └────────┘
```

**实现示例**:
```typescript
class CircuitBreaker {
  private state: 'closed' | 'open' | 'half-open' = 'closed';
  private failures = 0;
  private readonly threshold = 5;
  private readonly timeout = 60000; // 60秒

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      throw new Error('Circuit breaker is open');
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = 'closed';
  }

  private onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = 'open';
      setTimeout(() => this.state = 'half-open', this.timeout);
    }
  }
}
```

---

### 2. 重试模式

**策略**:
```typescript
const retryConfig = {
  maxAttempts: 3,
  backoff: 'exponential',  // linear, exponential, fixed
  baseDelay: 1000,         // 基础延迟(ms)
  maxDelay: 30000,         // 最大延迟(ms)
  retryableErrors: ['ECONNRESET', 'ETIMEDOUT', '5xx']
};

async function retry<T>(
  fn: () => Promise<T>,
  config: RetryConfig
): Promise<T> {
  let lastError: Error;
  
  for (let attempt = 1; attempt <= config.maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      if (!isRetryable(error, config.retryableErrors)) {
        throw error;
      }
      
      const delay = calculateDelay(attempt, config);
      await sleep(delay);
    }
  }
  
  throw lastError;
}
```

---

### 3. 舱壁模式 (Bulkhead)

**定义**: 隔离资源，防止故障蔓延。

**实现方式**:
- 线程池隔离
- 连接池隔离
- 信号量隔离

**示例**:
```typescript
class Bulkhead {
  private semaphore: Semaphore;
  
  constructor(maxConcurrent: number) {
    this.semaphore = new Semaphore(maxConcurrent);
  }

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    await this.semaphore.acquire();
    try {
      return await fn();
    } finally {
      this.semaphore.release();
    }
  }
}

// 使用
const orderServiceBulkhead = new Bulkhead(10); // 最多10个并发
await orderServiceBulkhead.execute(() => orderService.createOrder(order));
```

---

## 可观测性模式

### 1. 分布式追踪

**标准**: OpenTelemetry

**核心概念**:
- Trace: 完整请求链路
- Span: 单个操作
- Context: 传播上下文

**实现**:
```typescript
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('order-service');

async function createOrder(order: Order) {
  const span = tracer.startSpan('createOrder');
  
  try {
    span.setAttribute('orderId', order.id);
    span.setAttribute('userId', order.userId);
    
    await orderRepository.save(order);
    await inventoryService.reserve(order.items);
    
    span.setStatus({ code: SpanStatusCode.OK });
  } catch (error) {
    span.recordException(error);
    span.setStatus({ code: SpanStatusCode.ERROR });
    throw error;
  } finally {
    span.end();
  }
}
```

---

### 2. 日志聚合

**结构化日志**:
```typescript
const logger = {
  info: (message: string, context: LogContext) => {
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      level: 'INFO',
      service: 'order-service',
      traceId: context.traceId,
      spanId: context.spanId,
      message,
      ...context
    }));
  }
};

// 使用
logger.info('Order created', {
  orderId: '123',
  userId: '456',
  amount: 99.99,
  traceId: 'abc-123'
});
```

---

### 3. 指标监控

**关键指标**:
```yaml
# RED方法 (Rate, Errors, Duration)
- 请求速率 (requests/sec)
- 错误率 (errors/sec)
- 响应时间 (p50, p95, p99)

# USE方法 (Utilization, Saturation, Errors)
- CPU利用率
- 内存使用率
- 网络I/O
- 磁盘I/O

# 业务指标
- 订单创建数
- 支付成功率
- 库存周转率
```

**Prometheus示例**:
```typescript
import { Counter, Histogram, Registry } from 'prom-client';

const register = new Registry();

const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'path', 'status'],
  registers: [register]
});

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'path'],
  buckets: [0.1, 0.3, 0.5, 1, 3, 5, 10],
  registers: [register]
});
```

---

## 安全模式

### 1. API网关安全

**功能**:
- 认证授权
- 速率限制
- 请求验证
- SSL终止

**示例配置**:
```yaml
apiGateway:
  auth:
    type: JWT
    issuer: https://auth.example.com
    audience: api.example.com
    
  rateLimit:
    requests: 100
    window: 60s
    
  cors:
    origins: ["https://app.example.com"]
    methods: ["GET", "POST", "PUT", "DELETE"]
    
  ssl:
    enabled: true
    cert: /etc/ssl/cert.pem
    key: /etc/ssl/key.pem
```

---

### 2. 服务间认证

**mTLS (双向TLS)**:
```yaml
# Istio配置
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT  # 强制mTLS
```

---

### 3. 零信任架构

**原则**:
- 不信任网络
- 每个请求都验证
- 最小权限原则

**实现**:
```typescript
// 每个服务验证请求
async function validateRequest(req: Request): Promise<boolean> {
  // 1. 验证JWT
  const token = req.headers.authorization;
  const payload = await verifyJWT(token);
  
  // 2. 验证权限
  const hasPermission = await checkPermission(payload.userId, req.path, req.method);
  
  // 3. 验证请求来源
  const sourceValid = await validateSource(req.headers['x-source-service']);
  
  return hasPermission && sourceValid;
}
```

---

## 参考资料

- [Microservices Patterns](https://microservices.io/patterns/)
- [AWS Architecture Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Azure Cloud Design Patterns](https://docs.microsoft.com/en-us/azure/architecture/patterns/)
- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
