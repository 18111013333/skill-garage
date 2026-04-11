# CONSOLE_AUDIT_REQUIREMENTS.md - 控制台操作审计要求

## 目的
定义控制台操作审计要求，确保控制台成为可审计的治理入口。

## 适用范围
所有控制台页面访问、按钮点击、配置改动、高风险操作。

## 审计级别分类

### 级别定义
| 级别 | 说明 | 记录内容 | 保留期限 |
|------|------|----------|----------|
| L1 - 基础 | 基础访问记录 | 页面访问 | 1 年 |
| L2 - 标准 | 标准操作记录 | 操作详情 | 3 年 |
| L3 - 增强 | 增强操作记录 | 操作详情 + 结果 | 5 年 |
| L4 - 强审计 | 强审计记录 | 完整上下文 | 7 年 |
| L5 - 最强审计 | 最高审计级别 | 全量记录 + 审批链 | 7 年 + 备份 |

## 页面访问审计

### 需记录访问的页面
| 页面类型 | 审计级别 | 记录内容 |
|----------|----------|----------|
| 概览页面 | L1 | 页面访问时间、用户 |
| 租户管理页面 | L2 | + 租户范围 |
| 配置管理页面 | L2 | + 配置类型 |
| 安全管理页面 | L3 | + 安全级别 |
| 合规管理页面 | L3 | + 合规级别 |
| 审计日志页面 | L2 | + 查询条件 |
| 系统管理页面 | L4 | + 系统范围 |

### 访问记录字段
```json
{
  "page_access_audit": {
    "audit_id": "audit-001",
    "audit_level": "L2",
    "user_id": "user-001",
    "user_role": "admin",
    "page_path": "/console/tenants/tenant-001",
    "page_name": "租户详情",
    "access_time": "2026-04-06T12:00:00Z",
    "session_id": "sess-001",
    "ip_address": "10.0.0.1",
    "user_agent": "Chrome/...",
    "tenant_context": "tenant-001"
  }
}
```

## 按钮点击审计

### 必须记录的按钮点击
| 按钮类型 | 审计级别 | 说明 |
|----------|----------|------|
| 保存按钮 | L2 | 配置保存 |
| 删除按钮 | L3 | 删除操作 |
| 提交按钮 | L2 | 表单提交 |
| 审批按钮 | L4 | 审批操作 |
| 执行按钮 | L3 | 操作执行 |
| 回滚按钮 | L4 | 回滚操作 |
| 禁用按钮 | L3 | 禁用操作 |
| 启用按钮 | L2 | 启用操作 |

### 点击记录字段
```json
{
  "button_click_audit": {
    "audit_id": "audit-002",
    "audit_level": "L3",
    "user_id": "user-001",
    "button_id": "btn-delete-tenant",
    "button_name": "删除租户",
    "page_path": "/console/tenants/tenant-001",
    "click_time": "2026-04-06T12:00:00Z",
    "confirmation_shown": true,
    "confirmation_response": "confirmed",
    "target_object": "tenant-001",
    "action_triggered": "delete_tenant"
  }
}
```

## 配置改动审计

### 必须记录前后差异的配置
| 配置类型 | 审计级别 | 说明 |
|----------|----------|------|
| 功能开关 | L2 | 功能启用/禁用 |
| 配额设置 | L3 | 配额调整 |
| 权限配置 | L4 | 权限变更 |
| 安全策略 | L4 | 安全策略变更 |
| 合规规则 | L4 | 合规规则变更 |
| 系统参数 | L4 | 系统参数变更 |
| 审批流程 | L4 | 审批流程变更 |

### 配置变更记录字段
```json
{
  "config_change_audit": {
    "audit_id": "audit-003",
    "audit_level": "L4",
    "user_id": "user-001",
    "config_type": "quota",
    "config_path": "tenant-001.quota.monthly_tokens",
    "change_time": "2026-04-06T12:00:00Z",
    "before_value": 1000000,
    "after_value": 2000000,
    "change_reason": "业务增长需要",
    "approval_id": "approval-001",
    "impact_assessment": "成本增加 ¥100/月"
  }
}
```

## 高风险控制台动作审计

### 强审计动作列表
| 动作 | 审计级别 | 说明 |
|------|----------|------|
| 删除租户 | L5 | 极高风险 |
| 禁用租户 | L4 | 高风险 |
| 回滚发布 | L5 | 极高风险 |
| 修改安全策略 | L5 | 极高风险 |
| 修改合规规则 | L5 | 极高风险 |
| 清除审计日志 | L5 | 极高风险 |
| 批量删除数据 | L5 | 极高风险 |
| 修改权限策略 | L4 | 高风险 |
| 禁用自治能力 | L4 | 高风险 |
| 清空死信队列 | L4 | 高风险 |

### 强审计记录字段
```json
{
  "high_risk_action_audit": {
    "audit_id": "audit-004",
    "audit_level": "L5",
    "action_type": "delete_tenant",
    "user_id": "user-001",
    "action_time": "2026-04-06T12:00:00Z",
    "target_object": "tenant-001",
    "action_params": {
      "tenant_id": "tenant-001",
      "delete_data": true
    },
    "approval_chain": [
      {
        "approver": "manager-001",
        "approved_at": "2026-04-06T11:00:00Z",
        "approval_level": "team_lead"
      },
      {
        "approver": "director-001",
        "approved_at": "2026-04-06T11:30:00Z",
        "approval_level": "department_head"
      }
    ],
    "execution_result": "success",
    "verification": {
      "verified_by": "admin-002",
      "verified_at": "2026-04-06T12:30:00Z"
    },
    "session_context": {
      "session_id": "sess-001",
      "ip_address": "10.0.0.1",
      "mfa_verified": true
    }
  }
}
```

## 审计日志存储

### 存储要求
| 审计级别 | 存储方式 | 冗余 | 加密 |
|----------|----------|------|------|
| L1 | 标准存储 | 单副本 | 传输加密 |
| L2 | 标准存储 | 双副本 | 传输加密 |
| L3 | 归档存储 | 双副本 | 全加密 |
| L4 | 归档存储 | 三副本 | 全加密 |
| L5 | 归档 + 备份 | 三副本 + 异地 | 全加密 |

### 访问控制
| 角色 | L1 | L2 | L3 | L4 | L5 |
|------|----|----|----|----|----|
| 普通用户 | 自身 | 自身 | - | - | - |
| 租户管理员 | 租户范围 | 租户范围 | 租户范围 | - | - |
| 运营人员 | 授权范围 | 授权范围 | 授权范围 | - | - |
| 审计人员 | 全部 | 全部 | 全部 | 全部 | 全部 |
| 安全人员 | 全部 | 全部 | 全部 | 全部 | 全部 |

## 审计报告

### 日报
| 内容 | 说明 |
|------|------|
| 访问统计 | 页面访问统计 |
| 操作统计 | 操作类型统计 |
| 异常事件 | 异常访问/操作 |
| 高风险操作 | 高风险操作列表 |

### 周报
| 内容 | 说明 |
|------|------|
| 访问趋势 | 访问趋势分析 |
| 操作趋势 | 操作趋势分析 |
| 风险分析 | 风险操作分析 |
| 合规检查 | 合规性检查 |

### 月报
| 内容 | 说明 |
|------|------|
| 审计全景 | 月度审计全景 |
| 风险评估 | 风险评估报告 |
| 改进建议 | 审计改进建议 |

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-06
