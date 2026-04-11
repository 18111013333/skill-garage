# EVENT_ROUTING.md - 事件路由规则

**版本: V27.0**

## 目的
定义事件路由规则，确保事件能进入正确模块和工作流，实现"精准路由、高效处理、不丢不漏"。

## 适用范围
所有事件路由场景，包括：
- 事件类型路由
- 租户路由
- 领域路由
- 敏感级别路由
- 优先级路由

---

## 一、路由维度

| 维度 | 说明 | 路由依据 |
|------|------|----------|
| 事件类型 | 按事件类型路由 | event_type |
| 租户 | 按租户路由 | tenant_id |
| 领域 | 按业务领域路由 | domain |
| 敏感级别 | 按敏感级别路由 | sensitivity |
| 优先级 | 按优先级路由 | priority |

---

## 二、按事件类型路由

### 2.1 路由规则

| 事件类别 | 目标模块 | 目标队列 | 说明 |
|----------|----------|----------|------|
| lifecycle | runtime | q_lifecycle | 生命周期事件 |
| operation | runtime | q_operation | 操作事件 |
| governance | governance_center | q_governance | 治理事件 |
| security | safety | q_security | 安全事件 |
| integration | connectors | q_integration | 集成事件 |
| evolution | evolution | q_evolution | 进化事件 |
| alert | observability | q_alert | 告警事件 |

### 2.2 事件类型映射

```
事件类型格式: {category}.{entity}.{action}

示例:
- lifecycle.project.created → q_lifecycle
- operation.task.completed → q_operation
- governance.policy.violated → q_governance
- security.auth.failed → q_security
- integration.webhook.received → q_integration
- evolution.model.upgraded → q_evolution
- alert.threshold.exceeded → q_alert
```

---

## 三、按租户路由

### 3.1 路由规则

| 租户类型 | 路由策略 | 说明 |
|----------|----------|------|
| 企业租户 | 独立队列 | 高优先级、独立处理 |
| 普通租户 | 共享队列 | 标准处理 |
| 试用租户 | 共享队列 | 低优先级 |
| 合作伙伴 | 独立队列 | 特殊处理 |

### 3.2 租户队列命名

```
队列命名格式: q_{category}_{tenant_type}_{tenant_id}

示例:
- q_operation_enterprise_tenant_abc123
- q_governance_standard_tenant_xyz789
- q_security_partner_tenant_def456
```

### 3.3 租户隔离

| 隔离级别 | 说明 | 适用租户 |
|----------|------|----------|
| 完全隔离 | 独立队列、独立处理 | 企业租户 |
| 队列隔离 | 独立队列、共享处理 | 合作伙伴 |
| 逻辑隔离 | 共享队列、逻辑隔离 | 普通租户 |
| 无隔离 | 完全共享 | 试用租户 |

---

## 四、按领域路由

### 4.1 领域定义

| 领域 | 代码 | 说明 | 目标模块 |
|------|------|------|----------|
| 记忆 | memory | 记忆相关 | memory |
| 知识 | knowledge | 知识相关 | knowledge |
| 任务 | task | 任务相关 | runtime |
| 技能 | skill | 技能相关 | skills |
| 审计 | audit | 审计相关 | audit |
| 安全 | security | 安全相关 | safety |
| 配置 | config | 配置相关 | runtime |
| 集成 | integration | 集成相关 | connectors |

### 4.2 领域路由规则

```
领域识别方式:
1. 从事件类型提取: {category}.{domain}.{action}
2. 从事件 payload 提取: payload.domain
3. 从事件元数据提取: metadata.domain

路由优先级: 事件类型 > payload > metadata
```

### 4.3 领域处理器

| 领域 | 处理器 | 说明 |
|------|--------|------|
| memory | MemoryEventHandler | 记忆事件处理 |
| knowledge | KnowledgeEventHandler | 知识事件处理 |
| task | TaskEventHandler | 任务事件处理 |
| skill | SkillEventHandler | 技能事件处理 |
| audit | AuditEventHandler | 审计事件处理 |
| security | SecurityEventHandler | 安全事件处理 |
| config | ConfigEventHandler | 配置事件处理 |
| integration | IntegrationEventHandler | 集成事件处理 |

---

## 五、按敏感级别路由

### 5.1 敏感级别定义

| 级别 | 代码 | 说明 | 路由策略 |
|------|------|------|----------|
| 公开 | public | 公开信息 | 标准路由 |
| 内部 | internal | 内部信息 | 标准路由 |
| 机密 | confidential | 机密信息 | 加密队列 |
| 受限 | restricted | 受限信息 | 安全队列 |
| 关键 | critical | 关键信息 | 安全队列 + 审计 |

### 5.2 敏感级别路由规则

| 敏感级别 | 目标队列 | 加密要求 | 审计要求 |
|----------|----------|----------|----------|
| public | q_standard | 无 | 无 |
| internal | q_standard | 无 | 标准 |
| confidential | q_encrypted | 传输加密 | 标准 |
| restricted | q_secure | 全程加密 | 增强 |
| critical | q_secure_critical | 全程加密 | 实时 |

### 5.3 敏感数据处理

| 处理项 | 说明 |
|--------|------|
| 传输加密 | HTTPS/TLS |
| 存储加密 | AES-256 |
| 访问控制 | RBAC |
| 审计记录 | 完整审计 |
| 保留期限 | 按级别配置 |

---

## 六、按优先级路由

### 6.1 优先级定义

| 优先级 | 代码 | 说明 | 处理时限 |
|--------|------|------|----------|
| 关键 | critical | 关键事件 | 立即 |
| 高 | high | 高优先级 | 5 分钟 |
| 普通 | normal | 普通优先级 | 30 分钟 |
| 低 | low | 低优先级 | 4 小时 |

### 6.2 优先级队列

| 优先级 | 队列 | 处理线程数 | 说明 |
|--------|------|------------|------|
| critical | q_critical | 10 | 最高优先级 |
| high | q_high | 5 | 高优先级 |
| normal | q_normal | 3 | 普通优先级 |
| low | q_low | 1 | 低优先级 |

### 6.3 优先级提升

| 提升条件 | 提升到 | 说明 |
|----------|--------|------|
| 超时未处理 | +1 级 | 自动提升 |
| 相关事故 | critical | 事故关联 |
| 用户投诉 | high | 用户反馈 |
| 重复发生 | +1 级 | 重复事件 |

---

## 七、死信/隔离队列

### 7.1 死信队列

| 队列 | 说明 | 触发条件 |
|------|------|----------|
| dlq_processing | 处理失败 | 处理重试耗尽 |
| dlq_routing | 路由失败 | 无法路由 |
| dlq_validation | 验证失败 | 格式/权限错误 |
| dlq_timeout | 超时 | 处理超时 |

### 7.2 隔离队列

| 队列 | 说明 | 触发条件 |
|------|------|----------|
| quarantine_suspicious | 可疑事件 | 安全检测异常 |
| quarantine_malformed | 格式异常 | 格式严重错误 |
| quarantine_oversized | 超大事件 | 超过大小限制 |
| quarantine_rate_limited | 限流 | 触发限流 |

### 7.3 死信处理

```
死信处理流程:
1. 死信入队
2. 告警通知
3. 人工审核
4. 重试/丢弃/修复
5. 记录处理结果
```

---

## 八、路由流程

```
事件产生
    ↓
┌─────────────────────────────────────┐
│ 1. 事件验证                          │
│    - 格式验证                        │
│    - 权限验证                        │
│    - 大小验证                        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 路由决策                          │
│    - 事件类型路由                    │
│    - 租户路由                        │
│    - 领域路由                        │
│    - 敏感级别路由                    │
│    - 优先级路由                      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 队列选择                          │
│    - 选择目标队列                    │
│    - 检查队列状态                    │
│    - 应用限流策略                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 事件投递                          │
│    - 投递到目标队列                  │
│    - 记录路由日志                    │
│    - 返回投递结果                    │
└─────────────────────────────────────┘
```

---

## 九、路由监控

### 9.1 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 路由延迟 | 路由决策延迟 | > 100ms |
| 队列深度 | 队列待处理数量 | > 10000 |
| 死信率 | 死信事件比例 | > 1% |
| 路由错误率 | 路由失败比例 | > 0.1% |

### 9.2 路由报告

| 报告类型 | 频率 | 内容 |
|----------|------|------|
| 路由统计 | 每小时 | 各队列事件统计 |
| 死信报告 | 每日 | 死信事件分析 |
| 路由异常 | 实时 | 路由异常告警 |
| 容量报告 | 每日 | 队列容量分析 |

---

## 十、异常处理

| 异常类型 | 处理方式 |
|----------|----------|
| 路由失败 | 进入死信队列 + 告警 |
| 队列满 | 进入隔离队列 + 告警 |
| 格式错误 | 进入死信队列 + 通知 |
| 权限不足 | 拒绝 + 审计 |
| 超大事件 | 进入隔离队列 + 告警 |

---

## 十一、完成标准

| 标准 | 验证方式 |
|------|----------|
| 路由准确 | 事件进入正确队列 |
| 不丢不漏 | 无事件丢失 |
| 死信可查 | 死信可查询处理 |
| 监控有效 | 异常及时告警 |

---

## 引用文件

- `events/EVENT_SCHEMA.json` - 事件数据结构
- `events/TRIGGER_POLICY.md` - 事件触发规则
- `tenancy/TENANT_ISOLATION.md` - 租户隔离规则

---

**版本**: 1.0.0
**更新时间**: 2026-04-08
**下次评审**: 2026-07-08
