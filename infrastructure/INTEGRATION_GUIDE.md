# 架构集成指南

## V2.7.0 - 2026-04-10

新功能与六层架构的融合说明。

---

## 一、集成架构

```
┌─────────────────────────────────────────────────────────────┐
│                    六层架构 + 新功能                         │
├─────────────────────────────────────────────────────────────┤
│  L1 Core        │ 提示词编排器 (prompt_integration.py)      │
├─────────────────────────────────────────────────────────────┤
│  L2 Memory      │ 记忆总结器 (memory_summarizer.py)         │
├─────────────────────────────────────────────────────────────┤
│  L3 Orchestration │ 任务引擎 (task_engine.py)               │
├─────────────────────────────────────────────────────────────┤
│  L4 Execution   │ 插件编排器 (plugin_integration.py)        │
├─────────────────────────────────────────────────────────────┤
│  L5 Governance  │ 权限中间件 (auth_integration.py)          │
├─────────────────────────────────────────────────────────────┤
│  L6 Infrastructure │ 统一入口 (integration.py)              │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、统一入口

```python
from infrastructure.integration import get_integration

# 初始化
integration = get_integration()

# 获取状态
status = integration.get_status()

# 调用插件
result = integration.call_plugin("beijing_time", {})

# 检查权限
allowed, reason = integration.check_permission("exec", "rm")

# 授权
session_id = integration.grant_auth(operations=["rm"], timeout=300)

# 撤销授权
integration.revoke_auth()
```

---

## 三、层级功能

### L1 核心层 - 提示词编排

```python
from core.prompt_integration import get_prompt_orchestrator

orchestrator = get_prompt_orchestrator()

# 加载最小提示词
prompt = orchestrator.load_minimal()

# 按层加载
layer_prompt = orchestrator.load_layer(1)

# Token 估算
tokens = orchestrator.get_token_estimate()
```

### L2 记忆层 - 记忆总结

```python
from memory_context.memory_summarizer import get_summarizer

summarizer = get_summarizer()

# 总结会话
summary = summarizer.summarize_session(log_content)

# 更新记忆
summarizer.update_short_memory(new_content)
summarizer.update_long_memory(important_content)
```

### L4 执行层 - 插件系统

```python
from execution.plugin_integration import get_plugin_orchestrator

orchestrator = get_plugin_orchestrator()

# 列出插件
plugins = orchestrator.list_plugins()

# 调用插件
result = orchestrator.call_plugin("web_reader", {"url": "https://..."})
```

### L5 治理层 - 权限控制

```python
from governance.security.auth_integration import get_auth_middleware

middleware = get_auth_middleware()

# 检查权限
allowed, reason = middleware.check_exec_permission("rm file")

# 授权
session = middleware.grant_temp_auth(operations=["rm"], timeout=300)

# 撤销
middleware.revoke_auth()
```

---

## 四、插件开发

### 标准结构

```
plugins/[插件名]/
├── main.py           # 主逻辑
├── description.yaml  # 描述
└── requirements.txt  # 依赖（可选）
```

### 标准接口

```python
def tool_main(arg: dict) -> str:
    """
    插件主函数
    
    Args:
        arg: 输入参数字典
    
    Returns:
        str: 执行结果
    """
    return "结果"
```

### description.yaml

```yaml
display_name: "插件名称"
description: "插件描述和调用方式"
version: "1.0.0"
author: "作者"
requires_auth: false
```

---

## 五、权限配置

`security_config.json`

```json
{
  "safe_paths": ["/home/user/workspace", "/tmp"],
  "dangerous_commands": ["rm", "sudo"],
  "dangerous_patterns": ["rm -rf /"],
  "auth_timeout": 3600
}
```

---

## 六、性能指标

| 指标 | 值 |
|------|-----|
| 启动 Token | ~1,500 |
| 插件数量 | 2 |
| 权限检查延迟 | <1ms |
| 插件调用延迟 | <10ms |

---

**版本**: V2.7.0
**作者**: @18816132863
