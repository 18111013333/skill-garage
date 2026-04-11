# 架构完整性规范

## V2.7.0 - 2026-04-10

确保技能、模块、组件要求一致，架构完整统一。

---

## 一、统一要求总表

| 要求项 | 技能 | 模块 | 组件 |
|--------|------|------|------|
| **必须注册** | ✅ skill_registry.json | ✅ COMPONENT_REGISTRY.json | ✅ COMPONENT_REGISTRY.json |
| **必须归属层** | ✅ entry_layer | ✅ layer | ✅ layer |
| **必须版本号** | ✅ version | ✅ version | ✅ version |
| **必须负责人** | ✅ owner | ✅ author | ✅ author |
| **必须接口规范** | ✅ input/output_schema | ✅ 接口定义 | ✅ 必须方法 |
| **必须性能达标** | ✅ timeout_ms | ✅ 延迟/QPS | ✅ 延迟/QPS |
| **必须监控接入** | ✅ 日志/调用链 | ✅ 指标暴露 | ✅ health_check |
| **必须文档完整** | ✅ README | ✅ README | ✅ 文档字符串 |

---

## 二、层级归属统一

### 2.1 六层架构定义

| 层级 | 名称 | 职责 | 技能类型 | 模块类型 | 组件类型 |
|------|------|------|----------|----------|----------|
| L1 | 表达层 | 对外展示、输入输出 | 页面、交互入口 | 核心模块 | 核心组件 |
| L2 | 编排层 | 流程编排、任务分发 | 工作流、路由 | 记忆模块 | 缓存组件 |
| L3 | 规则层 | 业务规则、判断逻辑 | 规则引擎、策略 | 编排模块 | 路由组件 |
| L4 | 能力层 | 技能、工具、API | 技能模块 | 执行模块 | 优化组件 |
| L5 | 数据层 | 数据读写、缓存 | 数据访问 | 治理模块 | 监控组件 |
| L6 | 基建层 | 日志、监控、配置 | 基础设施 | 基建模块 | 基建组件 |

### 2.2 归属判定规则

```
新内容 → 判断类型 → 选择层级 → 注册入表 → 接入验证
```

**判断流程**:
1. 是否涉及UI/交互？ → L1
2. 是否涉及流程编排？ → L2
3. 是否涉及业务规则？ → L3
4. 是否是可复用能力？ → L4
5. 是否涉及数据存取？ → L5
6. 是否是基础设施？ → L6

---

## 三、注册表统一

### 3.1 技能注册表
路径: `infrastructure/inventory/skill_registry.json`

```json
{
  "skill_id": "skill_xxx",
  "skill_name": "技能名称",
  "version": "1.0.0",
  "entry_layer": "L4",
  "owner": "负责人",
  "status": "prod",
  "input_schema": {...},
  "output_schema": {...},
  "dependencies": [...],
  "timeout_ms": 15000,
  "fallback_strategy": "retry->degrade"
}
```

### 3.2 模块/组件注册表
路径: `infrastructure/COMPONENT_REGISTRY.json`

```json
{
  "name": "module_xxx",
  "version": "2.7.0",
  "layer": 1,
  "type": "core",
  "entry": "path/to/module.py",
  "config": "path/to/config.json",
  "performance": {
    "avg_latency_ms": 0.005,
    "qps": 217523
  },
  "dependencies": [...],
  "status": "active",
  "description": "模块描述"
}
```

---

## 四、接口规范统一

### 4.1 技能接口

```python
def execute(input_data: dict) -> dict:
    """
    技能执行入口
    
    Args:
        input_data: 符合 input_schema 的输入
    
    Returns:
        符合 output_schema 的输出
    """
    return {
        "success": True,
        "data": {...},
        "error": None
    }
```

### 4.2 模块接口

```python
class Module:
    @property
    def name(self) -> str: ...
    @property
    def version(self) -> str: ...
    @property
    def layer(self) -> int: ...
    
    def init(self) -> bool: ...
    def shutdown(self) -> bool: ...
    def get_stats(self) -> dict: ...
```

### 4.3 组件接口

```python
class Component(ComponentBase):
    @property
    def name(self) -> str: ...
    @property
    def version(self) -> str: ...
    @property
    def layer(self) -> int: ...
    
    def _do_init(self) -> bool: ...
    def _do_shutdown(self) -> bool: ...
    def _do_health_check(self) -> dict: ...
```

---

## 五、性能要求统一

### 5.1 延迟分级

| 级别 | 延迟范围 | 技能要求 | 模块要求 | 组件要求 |
|------|----------|----------|----------|----------|
| P0 极速 | <0.01ms | - | L1/L2 | L1/L2 |
| P1 快速 | <0.1ms | - | L3 | L3 |
| P2 标准 | <1ms | 简单技能 | L4 | L4 |
| P3 普通 | <10ms | 普通技能 | L5 | L5 |
| P4 宽松 | <100ms | 复杂技能 | L6 | L6 |

### 5.2 QPS 要求

| 层级 | 技能QPS | 模块QPS | 组件QPS |
|------|---------|---------|---------|
| L1 | - | >100K | >100K |
| L2 | - | >100K | >100K |
| L3 | - | >50K | >50K |
| L4 | >1K | >10K | >10K |
| L5 | >100 | >1K | >1K |
| L6 | >1K | >10K | >10K |

### 5.3 资源限制统一

| 资源 | 技能限制 | 模块限制 | 组件限制 |
|------|----------|----------|----------|
| 内存 | <500MB | <100MB | <100MB |
| CPU | <50% | <10% | <10% |
| 超时 | 自定义 | <1s | <100ms |

---

## 六、监控要求统一

### 6.1 必须暴露指标

| 指标 | 技能 | 模块 | 组件 |
|------|------|------|------|
| calls_total | ✅ | ✅ | ✅ |
| calls_success | ✅ | ✅ | ✅ |
| calls_failed | ✅ | ✅ | ✅ |
| latency_ms | ✅ | ✅ | ✅ |
| memory_mb | ✅ | ✅ | ✅ |
| cpu_percent | ✅ | ✅ | ✅ |
| error_count | ✅ | ✅ | ✅ |

### 6.2 健康检查统一

```python
def health_check() -> dict:
    return {
        "healthy": True,
        "status": "active",
        "uptime_seconds": 3600,
        "checks": {
            "memory": {"status": "ok", "value": 50},
            "latency": {"status": "ok", "value": 0.005},
            "errors": {"status": "ok", "value": 0}
        }
    }
```

---

## 七、文档要求统一

### 7.1 必须文档

| 文档 | 技能 | 模块 | 组件 |
|------|------|------|------|
| README.md | ✅ | ✅ | ✅ |
| 配置文件 | ✅ | ✅ | ✅ |
| 接口文档 | ✅ | ✅ | ✅ |
| 示例代码 | ✅ | ✅ | ✅ |
| 变更日志 | ✅ | ✅ | ✅ |

### 7.2 README 必须包含

1. 概述
2. 快速开始
3. API 文档
4. 配置说明
5. 性能指标
6. 示例代码
7. 故障排查

---

## 八、验证流程统一

### 8.1 技能验证

```bash
python3 infrastructure/inventory/skill_validator.py
```

### 8.2 模块/组件验证

```bash
python3 infrastructure/component_validator.py
```

### 8.3 架构完整性验证

```bash
python3 infrastructure/architecture_integrity_check.py
```

---

## 九、约束规则统一

### 9.1 禁止事项

| 规则 | 技能 | 模块 | 组件 |
|------|------|------|------|
| 禁止跨层调用 | ✅ | ✅ | ✅ |
| 禁止职责混装 | ✅ | ✅ | ✅ |
| 禁止未注册上线 | ✅ | ✅ | ✅ |
| 禁止接口漂移 | ✅ | ✅ | ✅ |
| 禁止临时补丁 | ✅ | ✅ | ✅ |

### 9.2 必须执行

| 规则 | 技能 | 模块 | 组件 |
|------|------|------|------|
| 必须先注册 | ✅ | ✅ | ✅ |
| 必须灰度接入 | ✅ | ✅ | ✅ |
| 必须监控校验 | ✅ | ✅ | ✅ |
| 必须版本管理 | ✅ | ✅ | ✅ |
| 必须定期清理 | ✅ | ✅ | ✅ |

---

## 十、验收口径统一

### 10.1 架构健康指标

| 指标 | 目标 | 检查方式 |
|------|------|----------|
| 层级数量 | =6 | `find . -name "*.json" \| grep layer` |
| 注册完整率 | 100% | 验证脚本 |
| 接口规范率 | 100% | 验证脚本 |
| 性能达标率 | >95% | benchmark |
| 监控覆盖率 | 100% | health_check |
| 文档完整率 | >90% | 验证脚本 |

### 10.2 每月清理

- 合并重复技能/模块/组件
- 下线废弃能力
- 梳理高耦合点
- 更新注册表
- 归档旧版本

---

**版本**: V2.7.0
**作者**: @18816132863
