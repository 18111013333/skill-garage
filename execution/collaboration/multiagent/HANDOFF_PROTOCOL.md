# HANDOFF_PROTOCOL.md - Agent交接协议

## 目的
定义agent之间的交接协议，确保交接时不丢约束、不传脏信息。

## 适用范围
所有agent之间的任务交接。

## 交接协议结构

### 必需字段
| 字段 | 类型 | 说明 |
|------|------|------|
| task_id | string | 任务唯一标识 |
| subgoal | string | 子目标描述 |
| input_context | object | 输入上下文 |
| hard_constraints | array | 硬约束列表 |
| expected_output | object | 期望输出格式 |
| confidence_required | number | 要求的置信度 |
| deadline | datetime | 完成时限 |
| return_format | string | 返回格式 |

### 可选字段
| 字段 | 类型 | 说明 |
|------|------|------|
| soft_preferences | array | 软偏好列表 |
| reference_data | object | 参考数据 |
| previous_attempts | array | 之前尝试记录 |
| risk_notes | array | 风险提示 |

## 交接协议格式

```json
{
  "handoff_id": "ho_001",
  "timestamp": "2026-04-06T10:32:00+08:00",
  "from_agent": "orchestrator",
  "to_agent": "retriever",
  "task": {
    "task_id": "task_001",
    "subgoal": "检索AI最新进展相关信息",
    "input_context": {
      "user_query": "AI最新进展",
      "session_context": {
        "goal": "完成AI报告"
      }
    },
    "hard_constraints": [
      {
        "type": "freshness",
        "value": "24小时内"
      },
      {
        "type": "source_quality",
        "value": "可信度 >= 0.6"
      }
    ],
    "expected_output": {
      "format": "structured_list",
      "max_results": 10,
      "required_fields": ["title", "source", "date", "summary"]
    },
    "confidence_required": 0.7,
    "deadline": "2026-04-06T10:35:00+08:00",
    "return_format": "json"
  }
}
```

## 交接内容规范

### 输入上下文
| 内容 | 说明 |
|------|------|
| 用户原始请求 | 用户原始输入 |
| 会话上下文 | 当前会话相关上下文 |
| 已完成工作 | 之前已完成的工作 |
| 相关记忆 | 相关的长期记忆 |

### 硬约束传递
| 约束类型 | 传递规则 |
|----------|----------|
| 用户硬约束 | 必须完整传递 |
| 安全边界 | 必须传递 |
| 格式要求 | 必须传递 |
| 时效要求 | 必须传递 |

### 禁止传递内容
| 内容 | 原因 |
|------|------|
| 未验证的推断 | 可能不准确 |
| 低置信度结论 | 可能错误 |
| 冲突信息 | 可能误导 |
| 敏感信息 | 安全风险 |

## 交接流程

```
准备交接
    ↓
┌─────────────────────────────────────┐
│ 1. 提取子目标                        │
│    - 明确子目标范围                  │
│    - 确定完成标准                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 整理上下文                        │
│    - 提取相关上下文                  │
│    - 过滤无关信息                    │
│    - 验证信息准确性                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 传递约束                          │
│    - 整理硬约束                      │
│    - 标注约束来源                    │
│    - 确认约束完整                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 发送交接请求                      │
│    - 构建交接协议                    │
│    - 发送给目标agent                 │
└─────────────────────────────────────┘
    ↓
等待结果
```

## 返回协议

### 返回格式
```json
{
  "handoff_id": "ho_001",
  "timestamp": "2026-04-06T10:34:00+08:00",
  "from_agent": "retriever",
  "to_agent": "orchestrator",
  "status": "success",
  "result": {
    "output": [...],
    "confidence": 0.85,
    "issues": [],
    "resource_used": {
      "tokens": 500,
      "time_ms": 2000
    }
  }
}
```

### 返回状态
| 状态 | 说明 |
|------|------|
| success | 成功完成 |
| partial | 部分完成 |
| failed | 执行失败 |
| timeout | 执行超时 |
| rejected | 拒绝执行 |

## 交接验证

### 发送前验证
| 验证项 | 说明 |
|--------|------|
| 目标agent可用 | agent是否可用 |
| 任务范围明确 | 子目标是否明确 |
| 约束完整 | 约束是否完整 |
| 时限合理 | 时限是否合理 |

### 接收后验证
| 验证项 | 说明 |
|--------|------|
| 结果完整 | 结果是否完整 |
| 约束满足 | 约束是否满足 |
| 置信度达标 | 置信度是否达标 |
| 格式正确 | 格式是否正确 |

## 异常处理

| 异常 | 处理 |
|------|------|
| 交接失败 | 重试或换agent |
| 结果不合格 | 要求重试 |
| 时限超期 | 取消或降级 |

## 维护方式
- 新增交接字段: 添加到协议结构
- 调整传递规则: 更新传递规范
- 新增验证项: 更新验证表

## 引用文件
- `multiagent/AGENT_REGISTRY.json` - Agent注册表
- `multiagent/DELEGATION_POLICY.md` - 委派策略
- `multiagent/CONFLICT_RESOLUTION.md` - 冲突解决
