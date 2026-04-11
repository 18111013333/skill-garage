# PII_HANDLING.md - 个人敏感信息处理规则

## 目的
定义个人敏感信息（PII）的识别、标记、脱敏、存储、传输、删除规则。

## 适用范围
平台所有涉及个人身份信息和个人敏感信息的处理场景。

## 与其他模块联动
| 模块 | 联动内容 |
|------|----------|
| privacy | 隐私治理框架 |
| data_governance | PII数据分级 |
| access | PII访问控制 |
| audit | PII操作审计 |
| knowledge | PII知识处理 |
| events | PII事件记录 |

## PII定义与分类

### 个人身份信息（PII）
| 类别 | 字段 | 敏感级别 |
|------|------|----------|
| 基本身份 | 姓名、性别、出生日期 | L2 |
| 联系方式 | 手机号、邮箱、地址 | L2 |
| 证件信息 | 身份证、护照、驾照 | L3 |
| 生物特征 | 指纹、人脸、声纹 | L3 |
| 网络标识 | IP地址、设备ID、Cookie | L2 |

### 敏感个人信息
| 类别 | 字段 | 敏感级别 |
|------|------|----------|
| 财务信息 | 银行账户、信用卡、收入 | L3 |
| 健康信息 | 病历、诊断、用药记录 | L3 |
| 位置信息 | 实时位置、轨迹记录 | L2 |
| 通信内容 | 聊天记录、邮件内容 | L2 |
| 种族宗教 | 种族、民族、宗教信仰 | L3 |
| 政治观点 | 政治倾向、党派归属 | L3 |
| 性生活 | 性取向、性生活记录 | L3 |
| 刑事记录 | 犯罪记录、司法信息 | L3 |

## PII标记规则

### 标记格式
```json
{
  "field_name": "phone_number",
  "pii_type": "contact",
  "sensitivity": "L2",
  "masking_rule": "phone_mask",
  "storage_rule": "encrypted",
  "retention_rule": "consent_based",
  "audit_level": "full"
}
```

### 自动标记规则
```yaml
auto_marking:
  patterns:
    - name: "手机号"
      pattern: "1[3-9]\\d{9}"
      pii_type: "contact"
      sensitivity: "L2"
    
    - name: "身份证号"
      pattern: "\\d{17}[\\dXx]"
      pii_type: "id_document"
      sensitivity: "L3"
    
    - name: "邮箱"
      pattern: "[\\w.-]+@[\\w.-]+\\.\\w+"
      pii_type: "contact"
      sensitivity: "L2"
    
    - name: "银行卡号"
      pattern: "\\d{16,19}"
      pii_type: "financial"
      sensitivity: "L3"
    
    - name: "姓名"
      pattern: "姓名[：:]*\\s*[\\u4e00-\\u9fa5]{2,4}"
      pii_type: "identity"
      sensitivity: "L2"
```

## PII脱敏规则

### 脱敏方法
| 方法 | 适用场景 | 示例 |
|------|----------|------|
| 完全遮蔽 | 高敏感展示 | 138****1234 → ******* |
| 部分遮蔽 | 一般展示 | 13812345678 → 138****5678 |
| 哈希处理 | 唯一标识 | 张三 → a1b2c3d4 |
| 泛化处理 | 统计分析 | 25岁 → 20-30岁 |
| 假名化 | 数据分析 | 张三 → 用户A |

### 脱敏规则配置
```yaml
masking_rules:
  phone_mask:
    type: "partial"
    pattern: "keep_first_3_keep_last_4"
    example: "138****5678"
  
  id_card_mask:
    type: "partial"
    pattern: "keep_first_6_keep_last_4"
    example: "110101********1234"
  
  email_mask:
    type: "partial"
    pattern: "keep_first_3_domain"
    example: "abc***@example.com"
  
  name_mask:
    type: "partial"
    pattern: "keep_first_char"
    example: "张**"
  
  bank_card_mask:
    type: "partial"
    pattern: "keep_last_4"
    example: "************1234"
  
  address_mask:
    type: "generalize"
    pattern: "city_only"
    example: "北京市朝阳区***"
```

## PII存储规则

### 存储限制
| PII类型 | 存储要求 | 加密要求 | 访问限制 |
|---------|----------|----------|----------|
| L2 PII | 最小必要 | 传输加密 | 角色授权 |
| L3 PII | 禁止默认存储 | 强加密 | 特批访问 |
| 敏感PII | 需明确同意 | 最高加密 | 审批+审计 |

### 禁止存储场景
```yaml
forbidden_storage:
  scenarios:
    - name: "记忆系统"
      rule: "PII不得写入长期记忆"
      exception: "用户明确同意且必要"
    
    - name: "日志系统"
      rule: "PII不得写入普通日志"
      exception: "安全审计必需且脱敏"
    
    - name: "知识库"
      rule: "PII不得写入知识库"
      exception: "无"
    
    - name: "缓存系统"
      rule: "PII缓存需有时限"
      exception: "会话必需且会话结束清除"
    
    - name: "导出文件"
      rule: "PII导出需审批"
      exception: "用户本人请求"
```

## PII传输规则

### 传输安全
| 场景 | 安全要求 |
|------|----------|
| 内部传输 | TLS 1.2+ 加密 |
| 外部传输 | TLS 1.3 + 端到端加密 |
| API传输 | HTTPS + 签名验证 |
| 文件传输 | 加密压缩 + 安全通道 |

### 传输审计
```yaml
transmission_audit:
  required_fields:
    - source_system
    - target_system
    - pii_types
    - record_count
    - encryption_method
    - timestamp
    - operator
    - approval_id
```

## PII输出规则

### 输出隐藏规则
| 输出场景 | PII处理 |
|----------|----------|
| 用户界面 | 按权限脱敏显示 |
| API响应 | 按权限过滤 |
| 报表输出 | 脱敏或聚合 |
| 日志输出 | 禁止明文 |
| 调试输出 | 完全禁止 |

### 输出摘要化
```yaml
output_summarization:
  rules:
    - name: "用户列表"
      original: "姓名、手机号、邮箱"
      summarized: "用户数量、角色分布"
    
    - name: "操作记录"
      original: "操作者姓名、IP"
      summarized: "操作次数、时间分布"
    
    - name: "会话内容"
      original: "用户输入原文"
      summarized: "话题分类、意图统计"
```

## PII删除规则

### 删除触发条件
| 触发条件 | 删除范围 | 验证要求 |
|----------|----------|----------|
| 用户请求 | 用户所有PII | 身份验证 |
| 同意撤回 | 相关PII | 同意记录验证 |
| 保留期满 | 超期PII | 期限验证 |
| 法律要求 | 指定PII | 法律文件验证 |

### 删除流程
```yaml
deletion_flow:
  steps:
    - name: "请求验证"
      actions:
        - 验证请求者身份
        - 确认删除范围
        - 检查法律保留
    
    - name: "影响评估"
      actions:
        - 识别关联数据
        - 评估删除影响
        - 确认删除可行性
    
    - name: "执行删除"
      actions:
        - 标记删除状态
        - 执行物理删除
        - 清除备份副本
    
    - name: "验证确认"
      actions:
        - 验证删除完成
        - 更新审计记录
        - 通知请求者
```

## PII审计

### 审计内容
| 审计项 | 频率 | 保留期限 |
|--------|------|----------|
| PII访问 | 实时 | 3年 |
| PII处理 | 实时 | 3年 |
| PII传输 | 实时 | 3年 |
| PII删除 | 实时 | 5年 |
| PII导出 | 实时 | 5年 |

### 审计日志格式
```json
{
  "audit_id": "pii_audit_001",
  "timestamp": "2026-04-06T22:00:00+08:00",
  "pii_type": "phone_number",
  "operation": "read",
  "operator": "user_001",
  "operator_role": "analyst",
  "data_subject": "user_002",
  "purpose": "customer_service",
  "legal_basis": "consent",
  "result": "success",
  "masked": true,
  "tenant_id": "tenant_001"
}
```

## 异常处理

| 异常 | 处理 |
|------|------|
| PII泄露 | 立即响应+通知+审计 |
| 未授权访问 | 阻止+记录+调查 |
| 脱敏失败 | 禁止输出+告警 |
| 删除失败 | 重试+人工介入 |

## 引用文件
- `privacy/PRIVACY_FRAMEWORK.md` - 隐私治理框架
- `privacy/CONSENT_AND_PURPOSE_LIMITATION.md` - 同意与用途限制
- `data_governance/DATA_CLASSIFICATION.md` - 数据分级制度
- `audit/AUDIT_POLICY.md` - 审计策略
