# 测试技能：文本摘要服务

## 基本信息

| 项目 | 内容 |
|-----|------|
| skill_id | skill_text_summary_v1 |
| skill_name | 文本摘要服务 |
| 所属层级 | L4 |
| 版本 | 1.0.0 |
| 负责人 | 系统管理员 |
| 状态 | draft |

## 功能说明

提供文本摘要功能，支持多种摘要算法和语言。

## 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| text | string | 是 | 待摘要的文本 |
| max_length | number | 否 | 最大摘要长度，默认200 |
| lang | string | 否 | 语言，默认auto |

## 输出结构

| 字段名 | 类型 | 说明 |
|-------|------|------|
| summary | string | 摘要结果 |
| original_length | number | 原文长度 |
| summary_length | number | 摘要长度 |
| algorithm | string | 使用的算法 |

## 使用示例

```python
from execution.text_summary import SkillInterface

config = {
    "skill_id": "skill_text_summary_v1",
    "timeout_ms": 5000
}

skill = SkillInterface(config)

input = SkillInput(
    request_id="req_001",
    skill_id="skill_text_summary_v1",
    params={
        "text": "这是一段很长的文本...",
        "max_length": 100
    },
    context=None,
    timeout_ms=5000,
    fallback=True
)

output = skill.execute(input)
print(output.data)
```

## 错误处理

| 错误码 | 说明 | 处理方式 |
|-------|------|---------|
| E001 | 输入参数错误 | 检查参数 |
| E002 | 文本过长 | 截断处理 |
| E003 | 处理超时 | 返回原文前N字 |

## 依赖关系

- 依赖服务：无
- 被依赖：无

## 变更历史

| 版本 | 日期 | 变更内容 |
|-----|------|---------|
| 1.0.0 | 2026-04-10 | 初始版本 |
