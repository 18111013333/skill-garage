# AGENT_METRICS.md - 智能体指标体系

## 目的
定义智能体系统的监控指标和评估体系。

## 适用范围
所有智能体的性能监控、健康评估、能力度量。

---

## 一、指标架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           智能体指标体系                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Metrics Collection                            │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │   │
│  │  │  Agent    │  │  Task     │  │ Resource  │  │  System   │        │   │
│  │  │  Metrics  │  │  Metrics  │  │  Metrics  │  │  Metrics  │        │   │
│  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Metrics Processing                            │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │   │
│  │  │  Aggregat │  │  Analyze  │  │  Alert    │  │  Report   │        │   │
│  │  │  ion      │  │           │  │           │  │           │        │   │
│  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 二、指标分类

### 2.1 智能体指标
| 指标 | 类型 | 说明 | 单位 |
|------|------|------|------|
| agent_status | gauge | 智能体状态 | 0-4 |
| agent_uptime | counter | 运行时间 | 秒 |
| agent_restart_count | counter | 重启次数 | 次 |
| agent_error_count | counter | 错误次数 | 次 |
| agent_health_score | gauge | 健康评分 | 0-100 |

### 2.2 任务指标
| 指标 | 类型 | 说明 | 单位 |
|------|------|------|------|
| task_total | counter | 任务总数 | 个 |
| task_completed | counter | 完成任务数 | 个 |
| task_failed | counter | 失败任务数 | 个 |
| task_pending | gauge | 待处理任务数 | 个 |
| task_processing | gauge | 处理中任务数 | 个 |
| task_duration | histogram | 任务耗时 | 毫秒 |
| task_queue_time | histogram | 排队时间 | 毫秒 |
| task_success_rate | gauge | 成功率 | % |

### 2.3 资源指标
| 指标 | 类型 | 说明 | 单位 |
|------|------|------|------|
| cpu_usage | gauge | CPU使用率 | % |
| memory_usage | gauge | 内存使用率 | % |
| memory_allocated | gauge | 分配内存 | 字节 |
| disk_usage | gauge | 磁盘使用率 | % |
| disk_io_read | counter | 磁盘读取 | 字节 |
| disk_io_write | counter | 磁盘写入 | 字节 |
| network_in | counter | 网络入流量 | 字节 |
| network_out | counter | 网络出流量 | 字节 |
| connection_count | gauge | 连接数 | 个 |

### 2.4 系统指标
| 指标 | 类型 | 说明 | 单位 |
|------|------|------|------|
| message_rate | gauge | 消息速率 | 条/秒 |
| message_latency | histogram | 消息延迟 | 毫秒 |
| message_queue_depth | gauge | 消息队列深度 | 条 |
| event_rate | gauge | 事件速率 | 个/秒 |
| error_rate | gauge | 错误率 | % |
| availability | gauge | 可用性 | % |

---

## 三、指标采集

### 3.1 采集配置
```json
{
  "metrics_collection": {
    "interval": 10000,
    "aggregation": {
      "window": 60000,
      "functions": ["avg", "max", "min", "p95", "p99"]
    },
    "labels": [
      "agent_id",
      "agent_type",
      "environment",
      "region"
    ],
    "storage": {
      "backend": "prometheus",
      "retention": "30d"
    }
  }
}
```

### 3.2 采集流程
```
指标采集
    │
    ▼
┌─────────────────┐
│  数据收集        │
│  - 系统指标      │
│  - 应用指标      │
│  - 自定义指标    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  数据处理        │
│  - 标准化        │
│  - 聚合          │
│  - 过滤          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  数据存储        │
│  - 时序存储      │
│  - 索引创建      │
└─────────────────┘
```

### 3.3 指标格式
```json
{
  "metric": {
    "name": "task_duration",
    "type": "histogram",
    "value": 1500,
    "unit": "ms",
    "labels": {
      "agent_id": "agent-001",
      "agent_type": "executor",
      "task_type": "code_analysis"
    },
    "timestamp": "2026-04-07T15:00:00Z"
  }
}
```

---

## 四、指标聚合

### 4.1 聚合函数
| 函数 | 说明 | 适用指标 |
|------|------|----------|
| avg | 平均值 | 延迟、使用率 |
| max | 最大值 | 峰值指标 |
| min | 最小值 | 最小值指标 |
| sum | 总和 | 计数器 |
| count | 计数 | 数量统计 |
| p50 | 50分位 | 延迟分布 |
| p95 | 95分位 | 延迟分布 |
| p99 | 99分位 | 延迟分布 |

### 4.2 聚合窗口
```json
{
  "aggregation_windows": [
    {
      "name": "realtime",
      "window": "1m",
      "step": "10s"
    },
    {
      "name": "short_term",
      "window": "5m",
      "step": "1m"
    },
    {
      "name": "medium_term",
      "window": "1h",
      "step": "5m"
    },
    {
      "name": "long_term",
      "window": "1d",
      "step": "1h"
    }
  ]
}
```

### 4.3 聚合规则
```json
{
  "aggregation_rules": [
    {
      "rule_id": "rule-001",
      "source_metric": "task_duration",
      "target_metric": "task_duration_avg",
      "function": "avg",
      "window": "5m",
      "group_by": ["agent_id", "task_type"]
    },
    {
      "rule_id": "rule-002",
      "source_metric": "task_total",
      "target_metric": "task_rate",
      "function": "rate",
      "window": "1m"
    }
  ]
}
```

---

## 五、告警规则

### 5.1 告警配置
```json
{
  "alert_rules": [
    {
      "alert_id": "alert-001",
      "name": "HighCPUUsage",
      "expr": "cpu_usage > 90",
      "duration": "5m",
      "severity": "warning",
      "labels": {
        "category": "resource"
      },
      "annotations": {
        "summary": "CPU使用率过高",
        "description": "智能体 {{agent_id}} CPU使用率超过90%"
      }
    },
    {
      "alert_id": "alert-002",
      "name": "HighErrorRate",
      "expr": "error_rate > 5",
      "duration": "1m",
      "severity": "critical",
      "labels": {
        "category": "error"
      }
    },
    {
      "alert_id": "alert-003",
      "name": "AgentDown",
      "expr": "agent_status == 0",
      "duration": "30s",
      "severity": "critical",
      "labels": {
        "category": "availability"
      }
    }
  ]
}
```

### 5.2 告警级别
| 级别 | 说明 | 响应时间 |
|------|------|----------|
| critical | 严重 | 立即 |
| warning | 警告 | 5分钟 |
| info | 信息 | 30分钟 |

### 5.3 告警处理
```
告警触发
    │
    ▼
┌─────────────────┐
│  告警评估        │
│  - 规则匹配      │
│  - 级别判断      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  告警通知        │
│  - 通道选择      │
│  - 内容生成      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  告警处理        │
│  - 确认          │
│  - 解决          │
│  - 归档          │
└─────────────────┘
```

---

## 六、仪表盘

### 6.1 智能体概览
```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Overview Dashboard                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Total: 100  │  │ Active: 95  │  │ Error: 5    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Agent Status Distribution               │   │
│  │  Running: ████████████████████████████████ 95%      │   │
│  │  Warning:  ████ 3%                                  │   │
│  │  Error:    ███ 2%                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Task Success Rate (24h)                 │   │
│  │  ████████████████████████████████████████ 98.5%     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 性能仪表盘
```
┌─────────────────────────────────────────────────────────────┐
│                    Performance Dashboard                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │   Task Duration     │  │   Message Latency   │          │
│  │   P50: 150ms        │  │   P50: 10ms         │          │
│  │   P95: 500ms        │  │   P95: 50ms         │          │
│  │   P99: 1000ms       │  │   P99: 100ms        │          │
│  └─────────────────────┘  └─────────────────────┘          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Throughput (requests/sec)               │   │
│  │  1000 ┤                                              │   │
│  │   800 ┤    ╭─╮                                       │   │
│  │   600 ┤   ╭╯ ╰╮    ╭─╮                              │   │
│  │   400 ┤  ╭╯   ╰───╯ ╰──╮                            │   │
│  │   200 ┤──╯                ╰──                        │   │
│  │       └───────────────────────────────────────────── │   │
│  │         00:00  04:00  08:00  12:00  16:00  20:00     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 七、报告生成

### 7.1 报告类型
| 类型 | 频率 | 内容 |
|------|------|------|
| 实时报告 | 实时 | 当前状态 |
| 日报 | 每日 | 24小时统计 |
| 周报 | 每周 | 7天趋势分析 |
| 月报 | 每月 | 月度总结 |

### 7.2 报告内容
```json
{
  "report": {
    "report_id": "report-001",
    "type": "daily",
    "period": {
      "start": "2026-04-06T00:00:00Z",
      "end": "2026-04-07T00:00:00Z"
    },
    "summary": {
      "total_agents": 100,
      "active_agents": 95,
      "total_tasks": 10000,
      "success_rate": 98.5,
      "avg_latency": 150
    },
    "trends": {
      "task_volume": "increasing",
      "success_rate": "stable",
      "latency": "decreasing"
    },
    "top_issues": [
      {
        "issue": "High CPU usage",
        "count": 15,
        "affected_agents": ["agent-001", "agent-002"]
      }
    ]
  }
}
```

---

## 八、指标查询

### 8.1 查询接口
```json
{
  "query": {
    "metric": "task_duration",
    "labels": {
      "agent_id": "agent-001"
    },
    "time_range": {
      "start": "2026-04-07T00:00:00Z",
      "end": "2026-04-07T15:00:00Z"
    },
    "aggregation": {
      "function": "avg",
      "window": "5m"
    }
  }
}
```

### 8.2 查询响应
```json
{
  "result": {
    "metric": "task_duration_avg",
    "labels": {
      "agent_id": "agent-001"
    },
    "data_points": [
      {
        "timestamp": "2026-04-07T00:00:00Z",
        "value": 145
      },
      {
        "timestamp": "2026-04-07T00:05:00Z",
        "value": 150
      }
    ]
  }
}
```

---

## 版本
- 版本: V1.0.0
- 创建时间: 2026-04-07
- 适用: 终极鸽子王 V10.0
