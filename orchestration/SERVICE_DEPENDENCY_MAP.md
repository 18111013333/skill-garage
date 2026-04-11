# SERVICE_DEPENDENCY_MAP.md - 服务依赖映射规则

**版本: V27.0**

## 目的
定义服务依赖映射规则，确保关键服务的依赖链可视化、可追踪，实现"依赖可识别、影响可评估、变更可预测"。

## 适用范围
所有服务依赖映射场景，包括：
- 服务与模块依赖
- 服务与连接器依赖
- 服务与模型依赖
- 服务与区域依赖
- 服务与伙伴依赖
- 服务与数据存储依赖

---

## 一、依赖类型

| 类型 | 代码 | 说明 | 强度 |
|------|------|------|------|
| 强依赖 | STRONG | 必须依赖 | 高 |
| 弱依赖 | WEAK | 可选依赖 | 低 |
| 条件依赖 | CONDITIONAL | 条件依赖 | 中 |
| 替代依赖 | ALTERNATIVE | 可替代依赖 | 低 |

---

## 二、服务与模块依赖

### 2.1 依赖映射

| 服务 | 依赖模块 | 依赖类型 | 说明 |
|------|----------|----------|------|
| 记忆服务 | memory模块 | STRONG | 核心依赖 |
| 执行服务 | exec模块 | STRONG | 核心依赖 |
| 会话服务 | session模块 | STRONG | 核心依赖 |
| 搜索服务 | search模块 | STRONG | 核心依赖 |

### 2.2 依赖表达

```json
{
  "service_id": "svc_memory",
  "dependencies": {
    "modules": [
      {
        "module_id": "mod_memory_core",
        "dependency_type": "STRONG",
        "version": "1.0.0",
        "criticality": "critical"
      }
    ]
  }
}
```

---

## 三、服务与连接器依赖

### 3.1 依赖映射

| 服务 | 依赖连接器 | 依赖类型 | 说明 |
|------|------------|----------|------|
| 搜索服务 | web_search | STRONG | 搜索依赖 |
| 集成服务 | webhook | WEAK | 可选集成 |
| 通知服务 | email | WEAK | 可选通知 |

### 3.2 依赖表达

```json
{
  "service_id": "svc_search",
  "dependencies": {
    "connectors": [
      {
        "connector_id": "conn_web_search",
        "dependency_type": "STRONG",
        "fallback": "conn_local_search"
      }
    ]
  }
}
```

---

## 四、服务与模型依赖

### 4.1 依赖映射

| 服务 | 依赖模型 | 依赖类型 | 说明 |
|------|----------|----------|------|
| AI服务 | qwen-embedding | STRONG | 向量化依赖 |
| AI服务 | gpt-4 | WEAK | 可选模型 |
| 分析服务 | analysis-model | CONDITIONAL | 条件依赖 |

### 4.2 依赖表达

```json
{
  "service_id": "svc_ai",
  "dependencies": {
    "models": [
      {
        "model_id": "model_qwen_embedding",
        "dependency_type": "STRONG",
        "version": "8b",
        "fallback": "model_local_embedding"
      }
    ]
  }
}
```

---

## 五、服务与区域依赖

### 5.1 依赖映射

| 服务 | 依赖区域 | 依赖类型 | 说明 |
|------|----------|----------|------|
| 全局服务 | 所有区域 | STRONG | 全局部署 |
| 区域服务 | 特定区域 | STRONG | 区域部署 |
| 跨区服务 | 多区域 | CONDITIONAL | 跨区依赖 |

### 5.2 依赖表达

```json
{
  "service_id": "svc_global",
  "dependencies": {
    "regions": [
      {
        "region_id": "region_cn_east",
        "dependency_type": "STRONG"
      },
      {
        "region_id": "region_cn_south",
        "dependency_type": "STRONG"
      }
    ]
  }
}
```

---

## 六、服务与伙伴依赖

### 6.1 依赖映射

| 服务 | 依赖伙伴 | 依赖类型 | 说明 |
|------|----------|----------|------|
| 集成服务 | 第三方API | WEAK | 可选集成 |
| 支付服务 | 支付伙伴 | STRONG | 支付依赖 |
| 通知服务 | 短信伙伴 | WEAK | 可选通知 |

### 6.2 依赖表达

```json
{
  "service_id": "svc_payment",
  "dependencies": {
    "partners": [
      {
        "partner_id": "partner_payment_001",
        "dependency_type": "STRONG",
        "fallback": "partner_payment_002"
      }
    ]
  }
}
```

---

## 七、服务与数据存储依赖

### 7.1 依赖映射

| 服务 | 依赖存储 | 依赖类型 | 说明 |
|------|----------|----------|------|
| 记忆服务 | SQLite | STRONG | 数据存储 |
| 向量服务 | Qdrant | STRONG | 向量存储 |
| 缓存服务 | Redis | WEAK | 可选缓存 |

### 7.2 依赖表达

```json
{
  "service_id": "svc_memory",
  "dependencies": {
    "data_stores": [
      {
        "store_id": "store_sqlite",
        "dependency_type": "STRONG",
        "data_type": "structured"
      },
      {
        "store_id": "store_qdrant",
        "dependency_type": "STRONG",
        "data_type": "vector"
      }
    ]
  }
}
```

---

## 八、依赖可视化

### 8.1 依赖图

```
服务依赖图示例:

┌──────────┐
│ 记忆服务 │
└──────────┘
     │
     ├──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ memory   │ │ SQLite   │ │ Qdrant   │ │ 向量模型 │
│ 模块     │ │ 存储     │ │ 向量库   │ │          │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

### 8.2 依赖查询

| 查询类型 | 说明 |
|----------|------|
| 上游依赖 | 查询服务依赖的上游 |
| 下游依赖 | 查询依赖服务的下游 |
| 影响范围 | 查询服务变更影响范围 |
| 依赖路径 | 查询依赖路径 |

---

## 九、完成标准

| 标准 | 验证方式 |
|------|----------|
| 依赖完整 | 所有依赖已映射 |
| 类型正确 | 依赖类型正确 |
| 可视化有效 | 依赖图正确展示 |

---

## 引用文件

- `service_management/SERVICE_CATALOG.json` - 服务目录
- `platform_twin/PLATFORM_TOPOLOGY.md` - 平台拓扑
- `platform_twin/CONFIGURATION_GRAPH_SCHEMA.json` - 配置图谱

---

**版本**: 1.0.0
**更新时间**: 2026-04-08
**下次评审**: 2026-07-08
