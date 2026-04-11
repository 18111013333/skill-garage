# DATA_LINEAGE.md - 数据血缘与流转追踪规则

## 目的
定义数据血缘追踪规则，确保关键数据可追溯来源和流向。

## 适用范围
平台所有关键数据的流转、处理、使用场景。

## 与其他模块联动
| 模块 | 联动内容 |
|------|----------|
| data_governance | 数据分级与保留 |
| audit | 数据流转审计 |
| knowledge | 知识数据血缘 |
| events | 事件数据血缘 |
| reporting | 报表数据血缘 |

## 数据血缘定义

### 血缘关系类型
| 关系类型 | 说明 | 示例 |
|----------|------|------|
| 来源关系 | 数据从哪里来 | 用户输入 → 会话数据 |
| 派生关系 | 数据如何产生 | 会话数据 → 记忆数据 |
| 使用关系 | 数据被谁使用 | 记忆数据 → 检索模块 |
| 引用关系 | 数据被谁引用 | 审计日志 → 合规报表 |

### 血缘追踪粒度
| 粒度 | 说明 | 适用场景 |
|------|------|----------|
| 数据集级 | 整个数据集的流转 | 数据仓库 |
| 记录级 | 单条记录的流转 | 敏感数据 |
| 字段级 | 单个字段的流转 | PII字段 |

## 数据来源追踪

### 来源类型
| 来源类型 | 说明 | 标记方式 |
|----------|------|----------|
| 用户输入 | 用户直接输入 | source:user_input |
| 系统生成 | 系统自动生成 | source:system_generated |
| 外部导入 | 从外部系统导入 | source:external_import |
| 模型输出 | AI模型生成 | source:model_output |
| 数据转换 | 数据处理转换 | source:transformation |

### 来源记录格式
```json
{
  "data_id": "data_001",
  "lineage": {
    "source": {
      "type": "user_input",
      "source_id": "session_001",
      "source_ref": "sessions://session_001/message_001",
      "collected_at": "2026-04-06T22:00:00+08:00",
      "collector": "chat_module",
      "consent_ref": "consent_001"
    }
  }
}
```

## 数据流转追踪

### 流转节点
| 节点类型 | 说明 | 记录内容 |
|----------|------|----------|
| 入口节点 | 数据进入系统 | 来源、时间、方式 |
| 处理节点 | 数据被处理 | 处理类型、参数、结果 |
| 存储节点 | 数据被存储 | 存储位置、格式、加密 |
| 输出节点 | 数据被输出 | 输出目标、格式、脱敏 |
| 删除节点 | 数据被删除 | 删除原因、方式、验证 |

### 流转记录格式
```json
{
  "data_id": "data_001",
  "lineage": {
    "flow": [
      {
        "node_id": "node_001",
        "node_type": "entry",
        "module": "chat_module",
        "action": "receive_input",
        "timestamp": "2026-04-06T22:00:00+08:00",
        "details": {
          "input_type": "text",
          "input_length": 100
        }
      },
      {
        "node_id": "node_002",
        "node_type": "processing",
        "module": "memory_module",
        "action": "extract_and_store",
        "timestamp": "2026-04-06T22:00:05+08:00",
        "details": {
          "extraction_method": "semantic",
          "storage_location": "memory/ontology/"
        }
      },
      {
        "node_id": "node_003",
        "node_type": "storage",
        "module": "storage_module",
        "action": "persist",
        "timestamp": "2026-04-06T22:00:10+08:00",
        "details": {
          "storage_path": "memory/2026-04-06.jsonl",
          "encryption": true
        }
      }
    ]
  }
}
```

## 数据使用追踪

### 使用场景
| 使用场景 | 说明 | 记录要求 |
|----------|------|----------|
| 检索查询 | 数据被检索 | 查询条件、结果 |
| 模型推理 | 数据用于推理 | 模型ID、输入输出 |
| 报表生成 | 数据用于报表 | 报表ID、字段 |
| 审计检查 | 数据用于审计 | 审计ID、范围 |
| 导出操作 | 数据被导出 | 导出ID、格式 |

### 使用记录格式
```json
{
  "data_id": "data_001",
  "lineage": {
    "usage": [
      {
        "usage_id": "usage_001",
        "usage_type": "retrieval",
        "module": "retrieval_module",
        "timestamp": "2026-04-06T23:00:00+08:00",
        "operator": "user_001",
        "purpose": "answer_question",
        "result_ref": "answer_001"
      }
    ]
  }
}
```

## 数据引用追踪

### 引用类型
| 引用类型 | 说明 | 示例 |
|----------|------|------|
| 直接引用 | 直接使用原始数据 | 报表引用原始日志 |
| 间接引用 | 使用派生数据 | 分析报告引用统计数据 |
| 聚合引用 | 使用聚合数据 | 摘要报告引用汇总数据 |
| 证据引用 | 作为证据使用 | 审计报告引用操作记录 |

### 引用记录格式
```json
{
  "data_id": "data_001",
  "lineage": {
    "references": [
      {
        "ref_id": "ref_001",
        "ref_type": "direct",
        "ref_target": "report_001",
        "ref_target_type": "report",
        "ref_fields": ["timestamp", "action", "result"],
        "ref_at": "2026-04-07T00:00:00+08:00"
      }
    ]
  }
}
```

## 数据状态变更追踪

### 状态类型
| 状态 | 说明 | 触发条件 |
|------|------|----------|
| 创建 | 数据首次创建 | 数据入库 |
| 更新 | 数据内容更新 | 数据修改 |
| 归档 | 数据移至归档 | 保留期满 |
| 删除 | 数据被删除 | 删除请求 |
| 匿名化 | 数据被匿名化 | 隐私处理 |

### 状态变更记录
```json
{
  "data_id": "data_001",
  "lineage": {
    "state_changes": [
      {
        "change_id": "change_001",
        "from_state": "active",
        "to_state": "archived",
        "trigger": "retention_policy",
        "timestamp": "2026-07-06T00:00:00+08:00",
        "operator": "system",
        "details": {
          "retention_days": 90,
          "archive_location": "archive/2026-04/"
        }
      }
    ]
  }
}
```

## 血缘查询

### 查询类型
| 查询类型 | 说明 | 用途 |
|----------|------|------|
| 上游追溯 | 查找数据来源 | 问题定位 |
| 下游追踪 | 查找数据去向 | 影响分析 |
| 全链追踪 | 完整血缘链 | 审计检查 |
| 影响分析 | 分析变更影响 | 变更评估 |

### 查询接口
```yaml
lineage_query:
  # 上游追溯
  upstream:
    params:
      - data_id
      - depth
    output:
      - source_chain
      - transformation_chain
  
  # 下游追踪
  downstream:
    params:
      - data_id
      - depth
    output:
      - usage_chain
      - reference_chain
  
  # 影响分析
  impact_analysis:
    params:
      - data_id
      - change_type
    output:
      - affected_systems
      - affected_reports
      - affected_users
```

## 血缘可视化

### 可视化格式
| 格式 | 说明 | 适用场景 |
|------|------|----------|
| 树状图 | 层级关系 | 来源追溯 |
| 流程图 | 流转过程 | 流程审计 |
| 关系图 | 关联关系 | 影响分析 |
| 时间线 | 时序关系 | 状态变更 |

## 血缘保留

### 保留规则
| 数据级别 | 血缘保留期限 | 说明 |
|----------|--------------|------|
| L0 公开 | 30天 | 基本追踪 |
| L1 内部 | 90天 | 标准追踪 |
| L2 敏感 | 180天 | 详细追踪 |
| L3 受限 | 365天 | 完整追踪 |

## 引用文件
- `data_governance/DATA_CLASSIFICATION.md` - 数据分级制度
- `data_governance/DATA_RETENTION_MATRIX.json` - 数据保留矩阵
- `audit/AUDIT_POLICY.md` - 审计策略
