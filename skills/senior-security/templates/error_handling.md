# 错误处理最佳实践

## 一、错误处理原则

### 1. 快速失败 (Fail Fast)
- 尽早发现错误，尽早处理
- 不要让错误传播到系统深处
- 在边界处进行验证

### 2. 明确错误类型
- 区分业务错误和技术错误
- 区分可恢复错误和不可恢复错误
- 区分用户错误和系统错误

### 3. 提供有用信息
- 错误信息要具体
- 包含修复建议
- 记录上下文信息

## 二、错误分类

### 按来源分类
| 类型 | 示例 | 处理方式 |
|------|------|----------|
| 用户输入错误 | 邮箱格式不正确 | 返回友好提示 |
| 业务逻辑错误 | 余额不足 | 返回业务错误码 |
| 网络错误 | 连接超时 | 重试机制 |
| 系统错误 | 内存溢出 | 记录日志，告警 |
| 第三方错误 | API调用失败 | 降级处理 |

### 按严重程度分类
| 级别 | 描述 | 处理方式 |
|------|------|----------|
| Info | 信息提示 | 记录日志 |
| Warning | 警告 | 记录日志，监控 |
| Error | 错误 | 记录日志，通知 |
| Critical | 严重错误 | 告警，自动恢复 |

## 三、错误处理模式

### 1. Try-Catch-Finally
```javascript
try {
  // 可能出错的代码
  const result = await riskyOperation();
  return result;
} catch (error) {
  // 错误处理
  logger.error('Operation failed', { error, context });
  throw new BusinessError('操作失败，请稍后重试');
} finally {
  // 清理资源
  cleanup();
}
```

### 2. 错误边界 (Error Boundary)
```javascript
// React错误边界
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    logger.error('React Error', { error, info });
  }

  render() {
    if (this.state.hasError) {
      return <FallbackUI />;
    }
    return this.props.children;
  }
}
```

### 3. 断路器模式 (Circuit Breaker)
```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.failures = 0;
    this.threshold = threshold;
    this.timeout = timeout;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.lastFailure = null;
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailure > this.timeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit is open');
      }
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

  onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failures++;
    this.lastFailure = Date.now();
    if (this.failures >= this.threshold) {
      this.state = 'OPEN';
    }
  }
}
```

### 4. 重试模式 (Retry Pattern)
```javascript
async function retry(fn, maxRetries = 3, delay = 1000) {
  let lastError;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (i < maxRetries - 1) {
        await sleep(delay * Math.pow(2, i)); // 指数退避
      }
    }
  }

  throw lastError;
}
```

### 5. 降级模式 (Fallback)
```javascript
async function getDataWithFallback() {
  try {
    // 尝试主数据源
    return await fetchFromPrimary();
  } catch (error) {
    logger.warn('Primary source failed, using fallback');
    try {
      // 降级到备用数据源
      return await fetchFromSecondary();
    } catch (fallbackError) {
      // 返回缓存或默认值
      return getCachedData() || getDefaultData();
    }
  }
}
```

## 四、错误日志规范

### 日志格式
```json
{
  "timestamp": "2026-04-09T12:00:00.000Z",
  "level": "ERROR",
  "message": "Database connection failed",
  "error": {
    "name": "ConnectionError",
    "message": "ECONNREFUSED",
    "stack": "..."
  },
  "context": {
    "request_id": "req_abc123",
    "user_id": "user_123",
    "operation": "getUserData"
  },
  "environment": "production",
  "service": "api-gateway",
  "host": "api-server-01"
}
```

### 日志级别使用
| 级别 | 使用场景 |
|------|----------|
| DEBUG | 开发调试信息 |
| INFO | 正常业务流程 |
| WARN | 潜在问题，不影响运行 |
| ERROR | 错误，需要关注 |
| FATAL | 严重错误，服务不可用 |

## 五、错误监控告警

### 告警规则
```yaml
alerts:
  - name: high_error_rate
    condition: error_rate > 5%
    duration: 5m
    severity: critical
    channels: [slack, pagerduty]

  - name: repeated_errors
    condition: same_error_count > 100
    duration: 10m
    severity: warning
    channels: [slack]

  - name: service_down
    condition: health_check_failed
    duration: 1m
    severity: critical
    channels: [slack, pagerduty, sms]
```

### 告警内容模板
```
🚨 告警：{alert_name}
级别：{severity}
服务：{service}
时间：{timestamp}

详情：
{details}

处理建议：
{suggestions}

查看详情：{dashboard_url}
```

## 六、用户友好错误提示

### 错误提示原则
1. **不要暴露技术细节** - 用户不需要知道堆栈信息
2. **使用用户语言** - 避免技术术语
3. **提供解决方案** - 告诉用户该怎么做
4. **保持一致性** - 同类错误使用相同提示

### 错误提示模板
| 技术错误 | 用户提示 |
|----------|----------|
| ECONNREFUSED | 网络连接失败，请检查网络后重试 |
| ENOTFOUND | 服务暂时不可用，请稍后重试 |
| 401 Unauthorized | 登录已过期，请重新登录 |
| 403 Forbidden | 您没有权限执行此操作 |
| 404 Not Found | 您访问的内容不存在 |
| 500 Internal Error | 系统繁忙，请稍后重试 |
| 429 Too Many Requests | 操作过于频繁，请休息一下 |

## 七、错误处理检查清单

### 开发阶段
- [ ] 所有外部调用都有错误处理
- [ ] 错误信息不包含敏感信息
- [ ] 错误日志包含足够上下文
- [ ] 用户看到的错误提示友好
- [ ] 关键操作有重试机制
- [ ] 外部依赖有降级方案

### 测试阶段
- [ ] 错误路径有测试覆盖
- [ ] 边界条件有测试
- [ ] 异常场景有测试
- [ ] 错误日志格式正确

### 上线阶段
- [ ] 错误监控已配置
- [ ] 告警规则已设置
- [ ] 错误处理文档已更新
- [ ] 团队已知晓错误处理规范
