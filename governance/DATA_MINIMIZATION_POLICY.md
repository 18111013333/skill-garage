# DATA_MINIMIZATION_POLICY.md - 数据最小化原则

## 目的
定义数据最小化原则，确保平台只收集和处理必要的数据。

## 适用范围
平台所有数据收集、存储、处理、传输场景。

## 与其他模块联动
| 模块 | 联动内容 |
|------|----------|
| data_governance | 数据分级与保留 |
| privacy | 隐私保护 |
| knowledge | 知识数据最小化 |
| audit | 最小化审计 |
| events | 事件数据最小化 |

## 最小化原则

### 核心原则
| 原则 | 说明 |
|------|------|
| 目的限定 | 只为明确目的收集数据 |
| 数量最小 | 只收集必要数量的数据 |
| 精度适当 | 数据精度不超过必要范围 |
| 期限最短 | 数据保留期限最短化 |
| 访问最小 | 数据访问范围最小化 |

### 最小化检查清单
```yaml
minimization_checklist:
  before_collection:
    - 是否有明确的收集目的？
    - 是否只收集必要的数据？
    - 是否可以用更少的数据达成目的？
    - 是否可以用匿名化数据？
    - 保留期限是否合理？
  
  during_processing:
    - 是否只处理必要的数据？
    - 是否只访问必要的字段？
    - 是否只保留必要的时间？
    - 是否及时删除临时数据？
  
  after_processing:
    - 是否删除了不需要的数据？
    - 是否匿名化了可匿名数据？
    - 是否清理了缓存和临时文件？
```

## 最少数据收集场景

### 强制最少收集场景
| 场景 | 允许收集 | 禁止收集 |
|------|----------|----------|
| 用户注册 | 账号、密码 | 真实姓名、身份证 |
| 登录认证 | 账号、密码 | 设备信息、位置 |
| 功能使用 | 功能必需数据 | 用户画像数据 |
| 问题反馈 | 问题描述 | 用户个人信息 |
| 性能监控 | 性能指标 | 用户行为详情 |

### 最少字段定义
```yaml
minimal_fields:
  user_authentication:
    required:
      - account_id
      - auth_token
    optional: []
    forbidden:
      - real_name
      - id_number
      - phone_number
  
  session_management:
    required:
      - session_id
      - start_time
    optional:
      - user_agent
    forbidden:
      - ip_address
      - device_id
  
  error_logging:
    required:
      - error_code
      - error_message
      - timestamp
    optional:
      - stack_trace
    forbidden:
      - user_input
      - session_content
  
  performance_monitoring:
    required:
      - metric_name
      - metric_value
      - timestamp
    optional: []
    forbidden:
      - user_id
      - request_content
```

## 禁止默认保存字段

### 禁止保存字段列表
| 字段类型 | 字段名称 | 例外条件 |
|----------|----------|----------|
| 身份信息 | 真实姓名 | 用户主动提供 |
| 身份信息 | 身份证号 | 法律要求 |
| 身份信息 | 护照号码 | 法律要求 |
| 生物特征 | 指纹数据 | 禁止 |
| 生物特征 | 人脸数据 | 禁止 |
| 位置信息 | 精确位置 | 用户明确同意 |
| 财务信息 | 银行账号 | 支付必需 |
| 通信内容 | 聊天原文 | 用户明确同意 |

### 例外审批流程
```yaml
exception_approval:
  trigger: "需要保存禁止字段"
  process:
    - submit_justification
    - legal_review
    - privacy_review
    - management_approval
  required_documents:
    - business_justification
    - legal_basis
    - risk_assessment
    - mitigation_measures
```

## 临时数据处理规则

### 临时数据定义
| 类型 | 说明 | 最大保留时间 |
|------|------|--------------|
| 会话缓存 | 会话期间缓存 | 会话结束即删除 |
| 处理中间结果 | 数据处理中间态 | 处理完成即删除 |
| 调试数据 | 调试过程数据 | 24小时 |
| 测试数据 | 测试过程数据 | 测试完成即删除 |
| 导出临时文件 | 导出过程文件 | 导出完成即删除 |

### 临时数据处理规则
```yaml
temporary_data_rules:
  session_cache:
    storage: "memory_only"
    encryption: "optional"
    cleanup: "on_session_end"
    max_size: "10MB"
  
  processing_intermediate:
    storage: "temp_directory"
    encryption: "required"
    cleanup: "on_process_complete"
    max_retention: "1_hour"
  
  debug_data:
    storage: "debug_directory"
    encryption: "required"
    cleanup: "scheduled_daily"
    max_retention: "24_hours"
  
  export_temp:
    storage: "export_temp"
    encryption: "required"
    cleanup: "on_download_complete"
    max_retention: "1_hour"
```

## 日志最小化

### 日志字段最小化
| 日志类型 | 必需字段 | 可选字段 | 禁止字段 |
|----------|----------|----------|----------|
| 访问日志 | 时间、操作、结果 | IP（脱敏） | 用户输入 |
| 错误日志 | 时间、错误码、消息 | 堆栈摘要 | 完整堆栈 |
| 审计日志 | 时间、操作者、操作 | 详情摘要 | 敏感数据 |
| 性能日志 | 时间、指标、值 | 标签 | 用户标识 |

### 日志脱敏规则
```yaml
log_masking:
  ip_address:
    method: "partial_mask"
    pattern: "keep_first_2_octets"
    example: "192.168.*.*"
  
  user_id:
    method: "hash"
    algorithm: "sha256"
    example: "user_abc123"
  
  session_id:
    method: "truncate"
    length: 8
    example: "sess_1234"
  
  error_message:
    method: "remove_pii"
    patterns: ["email", "phone", "id_number"]
```

## 缓存最小化

### 缓存规则
| 缓存类型 | 缓存内容限制 | 保留时间 | 清理策略 |
|----------|--------------|----------|----------|
| 响应缓存 | 非敏感响应 | 1小时 | 定时清理 |
| 查询缓存 | 查询结果摘要 | 30分钟 | LRU淘汰 |
| 会话缓存 | 会话状态 | 会话期间 | 会话结束 |
| 模型缓存 | 模型输出 | 10分钟 | 定时清理 |

### 缓存禁止内容
```yaml
cache_forbidden:
  - pii_data
  - sensitive_content
  - authentication_tokens
  - encryption_keys
  - user_passwords
  - session_content
```

## 回放最小化

### 回放数据限制
| 回放类型 | 允许内容 | 禁止内容 |
|----------|----------|----------|
| 问题回放 | 问题描述 | 用户信息 |
| 流程回放 | 流程步骤 | 输入内容 |
| 错误回放 | 错误信息 | 上下文数据 |
| 性能回放 | 性能指标 | 请求数据 |

### 回放数据脱敏
```yaml
replay_masking:
  user_input:
    method: "summarize"
    output: "intent_category"
  
  system_response:
    method: "template_match"
    output: "response_type"
  
  context_data:
    method: "aggregate"
    output: "context_summary"
```

## 导出最小化

### 导出内容限制
| 导出类型 | 允许导出 | 需脱敏 | 禁止导出 |
|----------|----------|--------|----------|
| 运营报表 | 聚合数据 | 用户统计 | 个体数据 |
| 审计报告 | 操作记录 | 操作者 | 敏感内容 |
| 用户数据 | 用户请求 | 部分字段 | 他人数据 |
| 系统日志 | 错误记录 | IP地址 | 用户输入 |

### 导出最小化检查
```yaml
export_minimization_check:
  before_export:
    - check_data_sensitivity
    - check_export_purpose
    - check_recipient_authorization
    - apply_minimization_rules
  
  during_export:
    - mask_sensitive_fields
    - remove_unnecessary_fields
    - aggregate_individual_data
    - verify_output_compliance
```

## 最小化审计

### 审计指标
| 指标 | 说明 | 目标 |
|------|------|------|
| 数据收集率 | 实际收集/计划收集 | < 100% |
| 字段使用率 | 实际使用/收集字段 | > 80% |
| 临时数据清理率 | 已清理/应清理 | 100% |
| 缓存命中率 | 命中/请求 | > 50% |

### 审计报告
```json
{
  "audit_id": "minimization_audit_001",
  "audit_period": "2026-04-01 to 2026-04-06",
  "metrics": {
    "data_collection_rate": 0.85,
    "field_usage_rate": 0.92,
    "temp_data_cleanup_rate": 1.0,
    "cache_hit_rate": 0.65
  },
  "findings": [
    {
      "area": "session_data",
      "issue": "部分会话数据保留超期",
      "recommendation": "加强自动清理机制"
    }
  ]
}
```

## 引用文件
- `data_governance/DATA_CLASSIFICATION.md` - 数据分级制度
- `data_governance/DATA_RETENTION_MATRIX.json` - 数据保留矩阵
- `privacy/PRIVACY_FRAMEWORK.md` - 隐私治理框架
