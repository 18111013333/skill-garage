# FINANCE_SUITE.md - 金融相关agent套件

## 目的
定义金融相关agent套件，确保金融域能力可用但守边界。

## 适用范围
所有金融相关任务的处理。

## 套件配置

```yaml
finance_suite:
  suite_id: "SUITE-finance"
  name: "金融事务处理套件"
  domain: "domain_finance"
  
  compliance_level: strict
  citation_mode: strict
  timeliness_required: true
  risk_disclosure: mandatory
```

## 允许动作

### 信息整理分析
```yaml
action_info_analysis:
  action_id: "finance_info_analysis"
  name: "金融信息整理分析"
  description: "整理和分析金融相关信息"
  
  capabilities:
    - 数据整理
    - 信息归纳
    - 趋势分析
    - 对比分析
    
  output:
    - 整理后的信息
    - 分析报告
    
  constraints:
    - 数据来源必须可靠
    - 时效性必须标注
```

### 指标解释说明
```yaml
action_metric_explain:
  action_id: "finance_metric_explain"
  name: "金融指标解释"
  description: "解释金融指标含义"
  
  capabilities:
    - 指标定义解释
    - 计算方法说明
    - 应用场景介绍
    
  output:
    - 指标解释
    - 计算示例
    
  constraints:
    - 不提供投资建议
    - 不预测指标走势
```

### 风险对比分析
```yaml
action_risk_compare:
  action_id: "finance_risk_compare"
  name: "风险对比分析"
  description: "对比不同选项的风险特征"
  
  capabilities:
    - 风险因素识别
    - 风险等级对比
    - 风险说明
    
  output:
    - 风险对比表
    - 风险说明
    
  constraints:
    - 不提供风险评级
    - 不推荐选择
    - 必须声明"仅供参考"
```

### 预算测算辅助
```yaml
action_budget_calc:
  action_id: "finance_budget_calc"
  name: "预算测算辅助"
  description: "辅助进行预算测算"
  
  capabilities:
    - 费用估算
    - 成本计算
    - 预算规划辅助
    
  output:
    - 测算结果
    - 假设说明
    
  constraints:
    - 明确假设条件
    - 声明估算性质
```

### 公开数据梳理
```yaml
action_public_data:
  action_id: "finance_public_data"
  name: "公开数据梳理"
  description: "梳理公开金融数据"
  
  capabilities:
    - 数据收集
    - 数据整理
    - 数据呈现
    
  output:
    - 数据汇总
    - 数据来源
    
  constraints:
    - 仅使用公开数据
    - 标注数据来源
    - 标注数据时效
```

## 禁止动作

### 严格禁止
```yaml
strictly_forbidden:
  - action: "provide_investment_advice"
    description: "提供投资建议"
    reason: "不可装成持牌投顾"
    severity: block
    
  - action: "guarantee_returns"
    description: "保证收益"
    reason: "收益不可保证"
    severity: block
    
  - action: "recommend_stocks"
    description: "无依据荐股"
    reason: "需投顾资质"
    severity: block
    
  - action: "predict_market"
    description: "预测市场走势"
    reason: "市场不可预测"
    severity: block
    
  - action: "replace_licensed_advisor"
    description: "替代持牌投顾"
    reason: "需持牌资质"
    severity: block
```

## 强制要求

### 时效性要求
```yaml
timeliness_requirements:
  data_freshness:
    - 市场数据: "实时或当日"
    - 财务数据: "最近报告期"
    - 政策信息: "最新版本"
    
  expiration_warning:
    - 数据过期必须提示
    - 时效性必须标注
    
  example:
    - "数据截至2024年1月15日，请注意时效性"
```

### 来源强度要求
```yaml
source_requirements:
  preferred_sources:
    - 官方发布
    - 监管机构
    - 权威财经媒体
    - 上市公司公告
    
  source_disclosure:
    - 必须标注来源
    - 必须标注时间
    - 必须标注可靠性
    
  example:
    - "数据来源：上海证券交易所，2024-01-15"
```

### 风险披露要求
```yaml
risk_disclosure:
  mandatory: true
  
  disclosure_content:
    - "不构成投资建议"
    - "投资有风险"
    - "过往业绩不代表未来"
    - "请独立判断决策"
    
  display:
    - 涉及投资话题必显示
    - 突出显示
```

## 验证要求

### 输出验证
```yaml
output_validation:
  checks:
    - no_investment_advice
    - source_disclosed
    - timeliness_labeled
    - risk_disclosure_present
```

### 数据验证
```yaml
data_validation:
  checks:
    - source_reliable
    - data_fresh
    - calculation_correct
```

## 审计要求

```yaml
audit_level: detailed

logged_items:
  - 所有金融相关交互
  - 数据来源记录
  - 风险提示展示
  
retention: 5_years
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 禁止动作触发 | 触发禁止动作次数 | >0 |
| 来源标注率 | 标注来源/应标注 | <100% |
| 时效标注率 | 标注时效/应标注 | <100% |
| 风险披露率 | 展示披露/应展示 | <100% |

## 维护方式
- 新增动作: 创建动作定义
- 调整要求: 更新强制要求
- 新增禁止: 更新禁止列表

## 引用文件
- `domain_agents/DOMAIN_REGISTRY.json` - 领域注册表
- `domain_agents/COMPLIANCE_MATRIX.md` - 合规矩阵
- `domain_agents/LEGAL_SUITE.md` - 法律套件
