---
name: command-hook
description: "命令钩子技能 - 为所有下达的命令添加预处理和后处理钩子，支持命令验证、日志记录、结果处理等功能"
metadata:
  openclaw:
    emoji: "🪝"
    tags: ["hook", "command", "middleware", "interceptor"]
---

# 命令钩子技能

为所有下达的命令添加预处理和后处理钩子，实现命令的统一管理和增强。

## 功能特性

- **预处理钩子**：命令执行前的验证、转换、日志记录
- **后处理钩子**：命令执行后的结果处理、日志记录、通知
- **错误处理钩子**：命令失败时的统一处理
- **审计日志**：记录所有命令执行历史

## 钩子类型

### 1. 预处理钩子 (before)

在命令执行前触发，可用于：
- 参数验证
- 权限检查
- 命令转换
- 日志记录
- 性能计时开始

### 2. 后处理钩子 (after)

在命令执行后触发，可用于：
- 结果转换
- 日志记录
- 性能计时结束
- 通知发送
- 缓存更新

### 3. 错误钩子 (error)

在命令执行失败时触发，可用于：
- 错误日志记录
- 错误通知
- 重试逻辑
- 降级处理

## 使用方式

### 命令执行流程

```
用户命令 → 预处理钩子 → 命令执行 → 后处理钩子 → 返回结果
                                    ↓
                              错误钩子（如果失败）
```

### 钩子配置示例

```yaml
hooks:
  before:
    - name: validate_params
      enabled: true
    - name: log_command
      enabled: true
    - name: check_permission
      enabled: true

  after:
    - name: log_result
      enabled: true
    - name: notify_on_success
      enabled: false

  error:
    - name: log_error
      enabled: true
    - name: notify_on_error
      enabled: true
```

## 内置钩子

### 预处理钩子

| 钩子名称 | 功能 |
|----------|------|
| validate_params | 验证命令参数 |
| log_command | 记录命令日志 |
| check_permission | 检查执行权限 |
| rate_limit | 限流控制 |
| transform_command | 命令转换 |

### 后处理钩子

| 钩子名称 | 功能 |
|----------|------|
| log_result | 记录结果日志 |
| cache_result | 缓存结果 |
| notify_success | 成功通知 |
| transform_result | 结果转换 |
| update_metrics | 更新指标 |

### 错误钩子

| 钩子名称 | 功能 |
|----------|------|
| log_error | 记录错误日志 |
| notify_error | 错误通知 |
| retry_command | 重试命令 |
| fallback | 降级处理 |

## 审计日志格式

```json
{
  "timestamp": "2026-04-09T12:00:00.000Z",
  "command_id": "cmd_abc123",
  "command_type": "exec",
  "command": "npm install",
  "user": "user_001",
  "session": "session_xyz",
  "status": "success",
  "duration_ms": 1234,
  "hooks": {
    "before": ["validate_params", "log_command"],
    "after": ["log_result"]
  }
}
```

## 配置文件

详见 [config/hooks.yaml](config/hooks.yaml)

## 最佳实践

1. **钩子顺序**：预处理钩子按配置顺序执行，后处理钩子按逆序执行
2. **错误处理**：预处理钩子失败会阻止命令执行
3. **性能考虑**：避免在钩子中执行耗时操作
4. **幂等性**：钩子应该是幂等的，可以安全重试
