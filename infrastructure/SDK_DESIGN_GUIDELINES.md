# SDK_DESIGN_GUIDELINES.md - SDK 设计规范

## 目的
定义 SDK 设计规范，确保不同语言 SDK 体验统一。

## 适用范围
所有官方和社区 SDK。

---

## 一、命名规范

### 1.1 包命名
| 语言 | 命名规范 | 示例 |
|------|----------|------|
| Python | 小写下划线 | `openclaw` |
| JavaScript | 小写连字符 | `@openclaw/sdk` |
| Java | 小写点分隔 | `ai.openclaw.sdk` |
| Go | 小写路径 | `github.com/openclaw/openclaw-go` |
| C# | PascalCase | `OpenClaw.SDK` |
| PHP | 小写连字符 | `openclaw/sdk` |
| Ruby | 小写 | `openclaw` |
| Rust | 小写连字符 | `openclaw` |

### 1.2 类命名
| 语言 | 命名规范 | 示例 |
|------|----------|------|
| Python | PascalCase | `OpenClawClient` |
| JavaScript | PascalCase | `OpenClawClient` |
| Java | PascalCase | `OpenClawClient` |
| Go | PascalCase | `Client` |
| C# | PascalCase | `OpenClawClient` |

### 1.3 方法命名
| 语言 | 命名规范 | 示例 |
|------|----------|------|
| Python | snake_case | `create_chat()` |
| JavaScript | camelCase | `createChat()` |
| Java | camelCase | `createChat()` |
| Go | PascalCase | `CreateChat()` |
| C# | PascalCase | `CreateChat()` |

---

## 二、异步/同步模式

### 2.1 同步方法
```python
# Python
response = client.chat.create(messages=[...])
```

### 2.2 异步方法
```python
# Python (asyncio)
response = await client.chat.create_async(messages=[...])
```

### 2.3 语言差异
| 语言 | 同步 | 异步 |
|------|------|------|
| Python | `method()` | `method_async()` |
| JavaScript | - | `method()` (Promise) |
| Java | `method()` | `methodAsync()` (CompletableFuture) |
| Go | `Method()` | `MethodAsync()` (goroutine) |
| C# | `Method()` | `MethodAsync()` (Task) |

---

## 三、分页处理

### 3.1 分页参数
```python
response = client.memory.list(
    page=1,
    page_size=20,
    cursor=None  # 或使用游标分页
)
```

### 3.2 分页响应
```python
class PaginatedResponse:
    items: List[Item]
    total: int
    page: int
    page_size: int
    has_more: bool
    next_cursor: Optional[str]
```

### 3.3 迭代器模式
```python
# 自动分页迭代
for item in client.memory.list_all():
    process(item)
```

---

## 四、重试机制

### 4.1 自动重试
| 错误类型 | 重试 | 最大次数 |
|----------|------|----------|
| 5xx 错误 | ✅ | 3 |
| 429 限流 | ✅ | 3 |
| 网络错误 | ✅ | 3 |
| 4xx 错误 | ❌ | 0 |

### 4.2 重试策略
```
指数退避: 1s → 2s → 4s
抖动: ±20% 随机
最大等待: 60s
```

### 4.3 重试配置
```python
client = OpenClawClient(
    max_retries=3,
    retry_delay=1.0,
    retry_max_delay=60.0
)
```

---

## 五、幂等性

### 5.1 幂等键
```python
response = client.execute(
    task="process_data",
    idempotency_key="unique-key-123"
)
```

### 5.2 幂等处理
```
相同 idempotency_key 的请求返回相同结果
有效期: 24 小时
```

---

## 六、超时设置

### 6.1 超时配置
```python
client = OpenClawClient(
    timeout=30.0,  # 默认超时
    connect_timeout=5.0,  # 连接超时
    read_timeout=30.0  # 读取超时
)
```

### 6.2 请求级超时
```python
response = client.chat.create(
    messages=[...],
    timeout=60.0  # 单次请求超时
)
```

### 6.3 超时错误
```python
try:
    response = client.chat.create(messages=[...])
except TimeoutError as e:
    handle_timeout(e)
```

---

## 七、认证处理

### 7.1 API Key 认证
```python
client = OpenClawClient(api_key="sk_xxx")
```

### 7.2 OAuth 认证
```python
client = OpenClawClient(
    oauth_token="access_token",
    refresh_token="refresh_token",
    token_refresh_callback=refresh_token
)
```

### 7.3 自动刷新
```
Token 过期时自动使用 refresh_token 刷新
刷新失败时抛出认证错误
```

---

## 八、错误封装

### 8.1 错误类型
```python
class OpenClawError(Exception):
    pass

class AuthenticationError(OpenClawError):
    pass

class PermissionError(OpenClawError):
    pass

class ValidationError(OpenClawError):
    pass

class RateLimitError(OpenClawError):
    pass

class ServerError(OpenClawError):
    pass
```

### 8.2 错误属性
```python
class OpenClawError(Exception):
    def __init__(self, code, message, details, request_id):
        self.code = code
        self.message = message
        self.details = details
        self.request_id = request_id
```

### 8.3 错误处理
```python
try:
    response = client.chat.create(messages=[...])
except AuthenticationError:
    refresh_auth()
except RateLimitError as e:
    wait_and_retry(e.retry_after)
except ValidationError as e:
    fix_request(e.details)
```

---

## 九、日志与脱敏

### 9.1 日志级别
| 级别 | 内容 |
|------|------|
| DEBUG | 请求/响应详情 |
| INFO | 请求摘要 |
| WARNING | 重试/降级 |
| ERROR | 错误信息 |

### 9.2 日志配置
```python
import logging

logging.basicConfig(level=logging.INFO)
client = OpenClawClient(log_level=logging.DEBUG)
```

### 9.3 脱敏规则
| 字段 | 处理 |
|------|------|
| api_key | `sk_***xxx` |
| token | `***` |
| password | `***` |
| pii | 脱敏或排除 |

---

## 十、SDK 结构

### 10.1 模块结构
```
openclaw/
├── __init__.py
├── client.py          # 主客户端
├── resources/
│   ├── chat.py        # 对话资源
│   ├── memory.py      # 记忆资源
│   ├── skills.py      # 技能资源
│   └── connectors.py  # 连接器资源
├── auth/
│   ├── api_key.py     # API Key 认证
│   └── oauth.py       # OAuth 认证
├── errors/
│   └── exceptions.py  # 错误定义
└── utils/
    ├── retry.py       # 重试工具
    └── logging.py     # 日志工具
```

### 10.2 初始化
```python
from openclaw import OpenClawClient

client = OpenClawClient(api_key="sk_xxx")
```

---

## 版本
- 版本: V9.0
- 更新时间: 2026-04-07
- 下次评审: 2026-07-07
