# CONSENSUS_POLICY.md - 共识策略

## 目的
定义何时需要多个agent交叉验证，确保多agent协作能形成可信共识。

## 适用范围
所有需要多agent交叉验证的场景。

## 需要共识验证的场景

### 高风险回答
| 场景 | 验证要求 | 参与agent |
|------|----------|------------|
| 医疗建议 | 至少2个agent验证 | retriever + validator |
| 法律咨询 | 至少2个agent验证 | retriever + validator |
| 财务决策 | 至少3个agent验证 | retriever + validator + auditor |
| 安全建议 | 至少3个agent验证 | retriever + validator + auditor |

### 来源冲突
| 场景 | 验证要求 | 参与agent |
|------|----------|------------|
| 多来源矛盾 | 必须共识验证 | retriever + validator |
| 官方与民间冲突 | 必须共识验证 | retriever + validator |
| 时间信息冲突 | 必须共识验证 | retriever + validator |

### 关键信息抽取
| 场景 | 验证要求 | 参与agent |
|------|----------|------------|
| 用户画像提取 | 至少2个agent验证 | retriever + validator |
| 约束条件提取 | 至少2个agent验证 | retriever + validator |
| 目标识别 | 至少2个agent验证 | retriever + validator |

### 事实密集型输出
| 场景 | 验证要求 | 参与agent |
|------|----------|------------|
| 数据报告 | 每个关键事实验证 | retriever + validator |
| 分析报告 | 核心结论验证 | retriever + validator |
| 对比分析 | 多源交叉验证 | retriever + validator |

### 结构化文档生成
| 场景 | 验证要求 | 参与agent |
|------|----------|------------|
| 合同文档 | 全文验证 | writer + validator + auditor |
| 正式报告 | 关键内容验证 | writer + validator |
| 技术文档 | 准确性验证 | writer + validator |

## 共识验证流程

```
触发共识验证
    ↓
┌─────────────────────────────────────┐
│ 1. 分配验证任务                      │
│    - 选择参与agent                   │
│    - 分配验证范围                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 并行验证                          │
│    - 各agent独立验证                 │
│    - 记录验证结果                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 汇总结果                          │
│    - 收集各agent结果                 │
│    - 比较验证结论                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 形成共识                          │
│    - 一致 → 合并结果                 │
│    - 不一致 → 冲突处理               │
└─────────────────────────────────────┘
    ↓
共识结果
```

## 一致时合并规则

### 完全一致
| 情况 | 处理 |
|------|------|
| 所有agent结论一致 | 直接采用，标注共识验证 |
| 置信度都高 | 采用最高置信度结果 |
| 置信度有差异 | 采用加权平均置信度 |

### 部分一致
| 情况 | 处理 |
|------|------|
| 多数一致 | 采用多数结论，标注少数异议 |
| 置信度差异大 | 采用高置信度结论 |
| 关键点一致 | 采用一致部分，标注争议点 |

## 不一致时升级规则

### 升级给校验agent
| 条件 | 处理 |
|------|------|
| 事实冲突 | 升级给validator裁决 |
| 来源可信度争议 | 升级给validator评估 |
| 时效性争议 | 升级给validator判断 |

### 升级给主控agent
| 条件 | 处理 |
|------|------|
| 无法形成共识 | 升级给orchestrator决策 |
| 影响核心目标 | 升级给orchestrator决策 |
| 用户需要知情 | 升级给orchestrator输出 |

### 升级给审计agent
| 条件 | 处理 |
|------|------|
| 涉及安全边界 | 升级给auditor审计 |
| 涉及合规问题 | 升级给auditor检查 |
| 涉及风险问题 | 升级给auditor评估 |

## 共识结果格式

```json
{
  "consensus_id": "cons_001",
  "timestamp": "2026-04-06T10:32:00+08:00",
  "task_id": "task_001",
  "participants": ["retriever", "validator"],
  "results": [
    {
      "agent": "retriever",
      "conclusion": "信息A正确",
      "confidence": 0.85
    },
    {
      "agent": "validator",
      "conclusion": "信息A正确",
      "confidence": 0.90
    }
  ],
  "consensus": {
    "conclusion": "信息A正确",
    "confidence": 0.875,
    "agreement": "full",
    "method": "weighted_average"
  }
}
```

## 异常处理

| 异常 | 处理 |
|------|------|
| agent不可用 | 减少验证人数或换agent |
| 验证超时 | 使用已完成验证 |
| 无法共识 | 升级给主控agent |

## 维护方式
- 新增验证场景: 添加到场景表
- 调整验证要求: 更新验证要求表
- 新增合并规则: 更新合并规则表

## 引用文件
- `multiagent/AGENT_REGISTRY.json` - Agent注册表
- `multiagent/CONFLICT_RESOLUTION.md` - 冲突解决
- `quality/FACT_CHECK_POLICY.md` - 事实校验策略
