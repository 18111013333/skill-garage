# API_ERROR_MODEL.md - 统一错误模型

## 目的
定义 API 统一错误格式，确保开发者能稳定处理错误。

## 适用范围
所有对外公开的 API 接口。

---

## 一、错误响应格式

### 1.1 标准错误格式
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "用户可见的错误描述",
    "details": {
      "field": "具体字段",
      "reason": "具体原因"
    },
    "request_id": "req_xxx",
    "documentation_url": "https://docs.openclaw.ai/errors/ERROR_CODE"
  }
}
```

### 1.2 字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| code | string | 错误码 |
| message | string | 用户可见描述 |
| details | object | 详细信息（可选） |
| request_id | string | 请求追踪 ID |
| documentation_url | string | 文档链接 |

---

## 二、错误码体系

### 2.1 错误码格式
```
CATEGORY_SUBCATEGORY_SPECIFIC

示例: AUTH_TOKEN_EXPIRED
```

### 2.2 错误分类
| 前缀 | 分类 | HTTP 状态码范围 |
|------|------|-----------------|
| AUTH | 认证错误 | 401 |
| PERM | 权限错误 | 403 |
| VALID | 验证错误 | 400 |
| NOT_FOUND | 资源不存在 | 404 |
| LIMIT | 限流错误 | 429 |
| QUOTA | 配额错误 | 402/403 |
| COMP | 合规错误 | 403 |
| INTERNAL | 内部错误 | 500 |
| SERVICE | 服务错误 | 502/503 |

---

## 三、用户可见错误

### 3.1 认证错误
| 错误码 | HTTP | 说明 |
|--------|------|------|
| AUTH_MISSING | 401 | 缺少认证信息 |
| AUTH_INVALID | 401 | 认证信息无效 |
| AUTH_TOKEN_EXPIRED | 401 | Token 已过期 |
| AUTH_TOKEN_REVOKED | 401 | Token 已撤销 |

### 3.2 权限错误
| 错误码 | HTTP | 说明 |
|--------|------|------|
| PERM_DENIED | 403 | 权限不足 |
| PERM_SCOPE_INSUFFICIENT | 403 | Scope 不足 |
| PERM_TENANT_DISABLED | 403 | 租户已禁用 |
| PERM_FEATURE_DISABLED | 403 | 功能未启用 |

### 3.3 验证错误
| 错误码 | HTTP | 说明 |
|--------|------|------|
| VALID_MISSING_FIELD | 400 | 缺少必填字段 |
| VALID_INVALID_FORMAT | 400 | 格式不正确 |
| VALID_INVALID_VALUE | 400 | 值不合法 |
| VALID_TOO_LONG | 400 | 内容过长 |

---

## 四、开发者可诊断错误

### 4.1 详细错误信息
```json
{
  "error": {
    "code": "VALID_INVALID_FORMAT",
    "message": "请求参数格式不正确",
    "details": {
      "field": "email",
      "expected": "email format",
      "received": "not-an-email",
      "location": "body"
    },
    "request_id": "req_xxx"
  }
}
```

### 4.2 调试信息
| 字段 | 说明 |
|------|------|
| field | 问题字段 |
| expected | 期望格式 |
| received | 实际值 |
| location | 位置（body/query/header） |

---

## 五、重试型错误

### 5.1 可重试错误
| 错误码 | HTTP | 说明 | 重试策略 |
|--------|------|------|----------|
| SERVICE_UNAVAILABLE | 503 | 服务暂时不可用 | 指数退避 |
| SERVICE_TIMEOUT | 504 | 服务超时 | 指数退避 |
| LIMIT_RATE_EXCEEDED | 429 | 限流 | 等待 Retry-After |
| INTERNAL_TEMPORARY | 500 | 临时错误 | 指数退避 |

### 5.2 重试响应头
```http
Retry-After: 60
X-Retry-Max: 3
```

### 5.3 重试策略
```
指数退避: 1s → 2s → 4s → 8s → 16s
最大重试: 5 次
最大等待: 60 秒
```

---

## 六、不可重试错误

### 6.1 不可重试错误
| 错误码 | HTTP | 说明 |
|--------|------|------|
| AUTH_INVALID | 401 | 认证无效 |
| PERM_DENIED | 403 | 权限不足 |
| VALID_INVALID_FORMAT | 400 | 格式错误 |
| NOT_FOUND_RESOURCE | 404 | 资源不存在 |
| COMP_VIOLATION | 403 | 合规违规 |

### 6.2 处理建议
```
不可重试错误需要修改请求或配置后重新发起
```

---

## 七、审批/权限/配额/合规错误

### 7.1 审批错误
| 错误码 | HTTP | 说明 |
|--------|------|------|
| APPROVAL_REQUIRED | 403 | 需要审批 |
| APPROVAL_PENDING | 403 | 审批中 |
| APPROVAL_REJECTED | 403 | 审批被拒绝 |

### 7.2 配额错误
| 错误码 | HTTP | 说明 |
|--------|------|------|
| QUOTA_EXCEEDED | 402 | 配额超限 |
| QUOTA_STORAGE_FULL | 402 | 存储配额满 |
| QUOTA_API_LIMIT | 429 | API 配额满 |
| QUOTA_SKILL_LIMIT | 403 | 技能数量限制 |

### 7.3 合规错误
| 错误码 | HTTP | 说明 |
|--------|------|------|
| COMP_DATA_RESIDENCY | 403 | 数据驻留违规 |
| COMP_PII_VIOLATION | 403 | PII 处理违规 |
| COMP_REGION_BLOCKED | 403 | 区域限制 |
| COMP_POLICY_VIOLATION | 403 | 策略违规 |

---

## 八、错误处理最佳实践

### 8.1 客户端处理
```python
def handle_error(response):
    error = response.json().get('error', {})
    code = error.get('code')
    
    if code.startswith('AUTH'):
        # 重新认证
        refresh_token()
    elif code.startswith('LIMIT'):
        # 等待重试
        wait_and_retry(response.headers.get('Retry-After'))
    elif code.startswith('VALID'):
        # 修正请求
        fix_request(error.get('details'))
    else:
        # 其他错误
        log_error(error)
```

### 8.2 错误日志
```
记录: request_id, error_code, timestamp, user_id
```

---

## 九、错误码完整列表

### 9.1 认证错误 (AUTH_*)
| 错误码 | HTTP | 说明 |
|--------|------|------|
| AUTH_MISSING | 401 | 缺少认证 |
| AUTH_INVALID | 401 | 认证无效 |
| AUTH_TOKEN_EXPIRED | 401 | Token 过期 |
| AUTH_TOKEN_REVOKED | 401 | Token 撤销 |
| AUTH_API_KEY_INVALID | 401 | API Key 无效 |

### 9.2 权限错误 (PERM_*)
| 错误码 | HTTP | 说明 |
|--------|------|------|
| PERM_DENIED | 403 | 权限不足 |
| PERM_SCOPE_INSUFFICIENT | 403 | Scope 不足 |
| PERM_TENANT_DISABLED | 403 | 租户禁用 |
| PERM_FEATURE_DISABLED | 403 | 功能禁用 |
| PERM_ROLE_INSUFFICIENT | 403 | 角色权限不足 |

### 9.3 验证错误 (VALID_*)
| 错误码 | HTTP | 说明 |
|--------|------|------|
| VALID_MISSING_FIELD | 400 | 缺少字段 |
| VALID_INVALID_FORMAT | 400 | 格式错误 |
| VALID_INVALID_VALUE | 400 | 值错误 |
| VALID_TOO_LONG | 400 | 过长 |
| VALID_TOO_SHORT | 400 | 过短 |

### 9.4 限流错误 (LIMIT_*)
| 错误码 | HTTP | 说明 |
|--------|------|------|
| LIMIT_RATE_EXCEEDED | 429 | 限流 |
| LIMIT_BURST_DETECTED | 429 | 爆量 |
| LIMIT_CONCURRENT | 429 | 并发限制 |

### 9.5 服务错误 (SERVICE_*)
| 错误码 | HTTP | 说明 |
|--------|------|------|
| SERVICE_UNAVAILABLE | 503 | 服务不可用 |
| SERVICE_TIMEOUT | 504 | 超时 |
| SERVICE_ERROR | 500 | 服务错误 |

---

## 版本
- 版本: V9.0
- 更新时间: 2026-04-07
- 下次评审: 2026-07-07
