# CONNECTOR_PERMISSION_MODEL.md - 连接器权限模型

## 目的
定义连接器权限模型，实现细粒度权限控制。

## 适用范围
所有连接器的权限管理。

---

## 一、权限分类

### 1.1 读写权限
| 权限 | 说明 | 风险等级 |
|------|------|----------|
| read | 读取数据 | 低 |
| write | 写入数据 | 中 |
| delete | 删除数据 | 高 |
| admin | 管理权限 | 最高 |

### 1.2 权限组合
```
read-only = read
read-write = read + write
full-access = read + write + delete
admin = read + write + delete + admin
```

---

## 二、字段级访问

### 2.1 字段权限定义
```json
{
  "connector_id": "conn_slack",
  "field_permissions": {
    "message": {
      "read": ["content", "timestamp", "user_id"],
      "write": ["content"],
      "excluded": ["internal_metadata"]
    },
    "user": {
      "read": ["name", "email"],
      "write": [],
      "excluded": ["password_hash", "token"]
    }
  }
}
```

### 2.2 字段过滤
```
请求 → 权限检查 → 字段过滤 → 返回允许字段
```

### 2.3 敏感字段保护
| 字段类型 | 处理 |
|----------|------|
| 密码 | 永不返回 |
| Token | 永不返回 |
| PII | 需要额外权限 |
| 财务 | 需要额外权限 |

---

## 三、事件订阅权限

### 3.1 事件权限
| 事件类型 | 权限要求 |
|----------|----------|
| data.created | read |
| data.updated | read |
| data.deleted | read + delete |
| system.event | admin |

### 3.2 事件过滤
```
订阅请求 → 权限检查 → 事件过滤 → 推送允许事件
```

### 3.3 事件订阅配置
```json
{
  "subscription": {
    "events": ["message.created", "message.updated"],
    "filter": {
      "channel": "general"
    },
    "permissions": ["messages.read"]
  }
}
```

---

## 四、代用户访问

### 4.1 用户授权流程
```
用户请求 → 用户授权 → 获取 delegated token → 以用户身份访问
```

### 4.2 代用户权限
| 权限来源 | 说明 |
|----------|------|
| 用户权限 | 用户拥有的权限 |
| 连接器权限 | 连接器申请的权限 |
| 实际权限 = 用户权限 ∩ 连接器权限 |

### 4.3 用户授权记录
```json
{
  "user_id": "user_xxx",
  "connector_id": "conn_slack",
  "granted_scopes": ["messages.read", "messages.write"],
  "granted_at": "2026-04-07T12:00:00Z",
  "expires_at": "2027-04-07T12:00:00Z"
}
```

---

## 五、代租户访问

### 5.1 租户授权流程
```
租户管理员 → 启用连接器 → 配置权限 → 连接器以租户身份访问
```

### 5.2 代租户权限
| 权限来源 | 说明 |
|----------|------|
| 租户权限 | 租户拥有的权限 |
| 连接器权限 | 连接器申请的权限 |
| 实际权限 = 租户权限 ∩ 连接器权限 |

### 5.3 租户授权记录
```json
{
  "tenant_id": "tenant_xxx",
  "connector_id": "conn_google_drive",
  "granted_scopes": ["files.read", "files.write"],
  "granted_by": "admin_xxx",
  "granted_at": "2026-04-07T12:00:00Z"
}
```

---

## 六、受限对象访问

### 6.1 受限对象类型
| 类型 | 说明 | 访问要求 |
|------|------|----------|
| 敏感数据 | PII/财务等 | 额外审批 |
| 管理数据 | 系统配置 | 管理员权限 |
| 跨租户数据 | 其他租户 | 平台权限 |

### 6.2 受限对象检查
```
访问请求 → 对象分类 → 权限检查 → 额外审批（如需） → 允许/拒绝
```

### 6.3 受限对象配置
```json
{
  "restricted_objects": [
    {
      "type": "pii",
      "access_policy": "require_consent",
      "audit_level": "full"
    },
    {
      "type": "financial",
      "access_policy": "require_approval",
      "audit_level": "full"
    }
  ]
}
```

---

## 七、权限继承

### 7.1 继承规则
```
平台权限 → 租户权限 → 用户权限 → 连接器权限
    ↓           ↓           ↓           ↓
  最高       继承平台     继承租户    继承用户
```

### 7.2 权限限制
```
子级权限不能超过父级权限
```

---

## 八、权限审计

### 8.1 审计事件
| 事件 | 记录 |
|------|------|
| 权限授予 | ✅ |
| 权限撤销 | ✅ |
| 权限使用 | ✅ |
| 权限拒绝 | ✅ |

### 8.2 审计日志
```json
{
  "timestamp": "2026-04-07T12:00:00Z",
  "event": "permission.used",
  "connector_id": "conn_slack",
  "user_id": "user_xxx",
  "permission": "messages.read",
  "resource": "channel/general",
  "result": "allowed"
}
```

---

## 版本
- 版本: V9.0
- 更新时间: 2026-04-07
- 下次评审: 2026-07-07
