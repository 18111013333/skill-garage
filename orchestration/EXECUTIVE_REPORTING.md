# EXECUTIVE_REPORTING.md - 高层报表规范

## 目的
定义面向管理层的报表规范，提供可决策信息而非原始流水账。

## 适用范围
平台所有面向高管和管理层的报表场景。

## 与其他模块联动
| 模块 | 联动内容 |
|------|----------|
| reporting | 报表生成 |
| audit | 审计数据 |
| analytics | 分析数据 |
| performance_evolution | 性能数据 |

## 指标层次

### 层次定义
| 层次 | 说明 | 受众 |
|------|------|------|
| L1 执行层 | 原始数据 | 运营人员 |
| L2 管理层 | 汇总指标 | 部门经理 |
| L3 高管层 | 关键指标 | 高管 |
| L4 决策层 | 战略指标 | 董事会 |

### 指标分层
```yaml
metric_hierarchy:
  L1_operational:
    description: "执行层指标"
    examples:
      - 每日请求量
      - 错误日志详情
      - 用户操作记录
    aggregation: "none"
  
  L2_management:
    description: "管理层指标"
    examples:
      - 周度请求趋势
      - 错误率统计
      - 用户活跃度
    aggregation: "daily/weekly"
  
  L3_executive:
    description: "高管层指标"
    examples:
      - 月度健康度
      - 成本趋势
      - 风险摘要
    aggregation: "weekly/monthly"
  
  L4_strategic:
    description: "决策层指标"
    examples:
      - 季度战略指标
      - 年度趋势
      - 投资回报
    aggregation: "monthly/quarterly"
```

## 风险摘要

### 风险分类
| 类别 | 说明 | 报告频率 |
|------|------|----------|
| 安全风险 | 安全事件和威胁 | 实时+周报 |
| 合规风险 | 合规问题和风险 | 周报+月报 |
| 运营风险 | 运营稳定性风险 | 日报+周报 |
| 财务风险 | 成本和收益风险 | 周报+月报 |
| 声誉风险 | 用户满意度和投诉 | 周报+月报 |

### 风险摘要格式
```yaml
risk_summary:
  security:
    current_level: "低风险"
    trend: "稳定"
    key_issues: []
    recommendations: []
  
  compliance:
    current_level: "合规"
    trend: "稳定"
    key_issues: []
    recommendations: []
  
  operational:
    current_level: "健康"
    trend: "改善"
    key_issues: []
    recommendations: []
  
  financial:
    current_level: "可控"
    trend: "优化中"
    key_issues: []
    recommendations: []
  
  reputation:
    current_level: "良好"
    trend: "稳定"
    key_issues: []
    recommendations: []
```

## 成本摘要

### 成本分类
| 类别 | 说明 | 监控频率 |
|------|------|----------|
| Token成本 | AI模型调用成本 | 日度 |
| 计算成本 | 服务器和计算资源 | 周度 |
| 存储成本 | 数据存储成本 | 月度 |
| 人力成本 | 运维人力投入 | 月度 |
| 外部服务 | 第三方服务成本 | 月度 |

### 成本摘要格式
```yaml
cost_summary:
  total_monthly: "¥XX,XXX"
  breakdown:
    token_cost:
      amount: "¥XX,XXX"
      percentage: 60
      trend: "↓5%"
    
    compute_cost:
      amount: "¥X,XXX"
      percentage: 20
      trend: "→0%"
    
    storage_cost:
      amount: "¥X,XXX"
      percentage: 10
      trend: "↑2%"
    
    external_services:
      amount: "¥X,XXX"
      percentage: 10
      trend: "→0%"
  
  cost_per_request: "¥0.XX"
  cost_trend: "下降趋势"
  optimization_opportunities:
    - "模型路由优化可节省15%"
    - "缓存策略优化可节省10%"
```

## 可靠性摘要

### 可靠性指标
| 指标 | 说明 | 目标 |
|------|------|------|
| 可用性 | 系统可用时间比例 | > 99.9% |
| 响应时间 | 平均响应时间 | < 500ms |
| 错误率 | 请求失败率 | < 0.1% |
| 恢复时间 | 故障恢复时间 | < 5min |

### 可靠性摘要格式
```yaml
reliability_summary:
  availability:
    current: 99.95%
    target: 99.9%
    status: "达标"
  
  response_time:
    current: 350
    target: 500
    unit: "ms"
    status: "达标"
  
  error_rate:
    current: 0.05%
    target: 0.1%
    status: "达标"
  
  recovery_time:
    current: 2
    target: 5
    unit: "min"
    status: "达标"
  
  overall_health: "健康"
  incidents_this_month: 0
  major_incidents: 0
```

## 租户健康摘要

### 健康指标
| 指标 | 说明 | 权重 |
|------|------|------|
| 使用活跃度 | 租户使用频率 | 30% |
| 满意度 | 用户反馈评分 | 25% |
| 成长趋势 | 使用量增长 | 20% |
| 合规性 | 合规检查结果 | 15% |
| 成本效益 | 成本收益比 | 10% |

### 租户健康摘要格式
```yaml
tenant_health_summary:
  total_tenants: 50
  health_distribution:
    excellent: 20
    good: 25
    fair: 4
    poor: 1
  
  top_tenants:
    - tenant_id: "tenant_001"
      health_score: 98
      usage_trend: "↑"
      satisfaction: 4.8
    
    - tenant_id: "tenant_002"
      health_score: 95
      usage_trend: "→"
      satisfaction: 4.5
  
  attention_required:
    - tenant_id: "tenant_050"
      health_score: 60
      issues:
        - "使用量下降30%"
        - "投诉增加"
      recommendations:
        - "主动联系了解需求"
        - "提供培训支持"
```

## 关键异常与建议动作

### 异常分类
| 级别 | 说明 | 响应要求 |
|------|------|----------|
| P0 紧急 | 需立即处理 | 立即通知 |
| P1 重要 | 需尽快处理 | 24小时内 |
| P2 一般 | 需关注 | 周报汇总 |
| P3 提示 | 可优化 | 月报汇总 |

### 异常报告格式
```yaml
critical_issues:
  - issue_id: "ISS-001"
    level: "P1"
    category: "performance"
    description: "响应时间超过阈值"
    impact: "用户体验下降"
    detected_at: "2026-04-06T10:00:00+08:00"
    status: "处理中"
    owner: "ops_team"
    recommendations:
      - action: "扩容计算资源"
        priority: "高"
        estimated_impact: "响应时间降低50%"
      - action: "优化缓存策略"
        priority: "中"
        estimated_impact: "响应时间降低20%"
```

## 报表模板

### 高管日报模板
```yaml
executive_daily_report:
  sections:
    - name: "执行摘要"
      content:
        - 系统健康度
        - 关键指标概览
        - 今日异常
    
    - name: "风险状态"
      content:
        - 安全风险
        - 合规风险
        - 运营风险
    
    - name: "成本概览"
      content:
        - 今日成本
        - 成本趋势
    
    - name: "关键异常"
      content:
        - 异常列表
        - 建议动作
```

### 高管周报模板
```yaml
executive_weekly_report:
  sections:
    - name: "执行摘要"
      content:
        - 周度健康度
        - 关键指标趋势
        - 本周亮点
    
    - name: "风险摘要"
      content:
        - 各类风险状态
        - 风险趋势
        - 风险应对
    
    - name: "成本摘要"
      content:
        - 周度成本
        - 成本趋势
        - 优化建议
    
    - name: "可靠性摘要"
      content:
        - 可用性
        - 性能指标
        - 事件统计
    
    - name: "租户健康"
      content:
        - 健康分布
        - 关注租户
        - 成长趋势
    
    - name: "关键异常与建议"
      content:
        - 异常列表
        - 建议动作
        - 责任人
```

### 高管月报模板
```yaml
executive_monthly_report:
  sections:
    - name: "执行摘要"
      content:
        - 月度健康度
        - 战略指标达成
        - 月度亮点
    
    - name: "风险深度分析"
      content:
        - 风险趋势分析
        - 风险应对效果
        - 下月风险预测
    
    - name: "成本深度分析"
      content:
        - 月度成本分析
        - 成本优化成果
        - 下月成本预测
    
    - name: "可靠性深度分析"
      content:
        - 月度可用性
        - 事件复盘
        - 改进措施
    
    - name: "租户深度分析"
      content:
        - 租户健康分析
        - 流失风险
        - 增长机会
    
    - name: "战略建议"
      content:
        - 投资建议
        - 优化方向
        - 风险规避
```

## 引用文件
- `reporting/REPORT_SCHEMA.json` - 报表结构
- `reporting/SCHEDULED_REPORTS.md` - 定时报表
- `reporting/EXPORT_POLICY.md` - 导出规则
- `audit/AUDIT_POLICY.md` - 审计策略
