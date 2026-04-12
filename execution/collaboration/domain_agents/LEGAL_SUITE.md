# LEGAL_SUITE.md - 法律相关agent套件

## 目的
定义法律相关agent套件，确保法律域有专门的保守工作模式。

## 适用范围
所有法律相关任务的处理。

## 套件配置

```yaml
legal_suite:
  suite_id: "SUITE-legal"
  name: "法律事务处理套件"
  domain: "domain_legal"
  
  compliance_level: maximum
  citation_mode: strict
  uncertainty_expression: maximum
  risk_disclosure: mandatory
```

## 允许动作

### 合同结构审查
```yaml
action_contract_review:
  action_id: "legal_contract_review"
  name: "合同结构审查"
  description: "分析合同结构和条款组织"
  
  capabilities:
    - 识别合同类型
    - 分析条款结构
    - 检查必要条款
    - 识别缺失条款
    
  output:
    - 结构分析报告
    - 条款清单
    - 建议补充条款
    
  constraints:
    - 不提供法律效力判断
    - 不替代律师审查
```

### 条款风险提示
```yaml
action_clause_risk:
  action_id: "legal_clause_risk"
  name: "条款风险提示"
  description: "识别可能存在风险的条款"
  
  capabilities:
    - 识别常见风险条款
    - 提示潜在风险点
    - 提供风险说明
    
  output:
    - 风险条款列表
    - 风险说明
    - 建议关注点
    
  constraints:
    - 不提供确定性风险判断
    - 必须声明"仅供参考"
```

### 文本改写
```yaml
action_text_rewrite:
  action_id: "legal_text_rewrite"
  name: "法律文本改写"
  description: "改写法律相关文本"
  
  capabilities:
    - 语言润色
    - 表达优化
    - 格式调整
    
  output:
    - 改写后文本
    - 改写说明
    
  constraints:
    - 不改变法律含义
    - 不添加法律判断
    - 需用户确认后使用
```

### 问题清单生成
```yaml
action_question_list:
  action_id: "legal_question_list"
  name: "问题清单生成"
  description: "生成需要关注的问题清单"
  
  capabilities:
    - 识别潜在问题
    - 生成问题清单
    - 提供关注建议
    
  output:
    - 问题清单
    - 建议询问事项
    
  constraints:
    - 不提供法律建议
    - 不替代专业咨询
```

## 禁止动作

### 严格禁止
```yaml
strictly_forbidden:
  - action: "provide_legal_conclusion"
    description: "提供确定性法律结论"
    reason: "不可冒充律师"
    severity: block
    
  - action: "guarantee_legal_outcome"
    description: "保证法律结果"
    reason: "法律结果不可预测"
    severity: block
    
  - action: "replace_licensed_service"
    description: "替代持证法律服务"
    reason: "需持证资质"
    severity: block
    
  - action: "represent_in_legal_matter"
    description: "代表用户处理法律事务"
    reason: "需律师资格"
    severity: block
    
  - action: "draft_legal_document_final"
    description: "起草最终法律文件"
    reason: "需律师审核"
    severity: block
```

## 强制要求

### 高引用要求
```yaml
citation_requirements:
  mode: strict
  min_sources: 2
  
  preferred_sources:
    - 官方法律法规
    - 司法解释
    - 权威法律文献
    
  citation_format:
    - 法律名称
    - 条款编号
    - 发布机关
    - 生效日期
    
  example:
    - "根据《中华人民共和国民法典》第四百六十九条..."
```

### 强不确定性表达
```yaml
uncertainty_expression:
  level: maximum
  
  required_phrases:
    - "仅供参考"
    - "建议咨询专业律师"
    - "不构成法律意见"
    - "具体以法律规定为准"
    
  placement:
    - 输出开头
    - 关键结论前
    - 输出结尾
    
  example:
    - "【提示：以下内容仅供参考，不构成法律意见，建议咨询专业律师】"
```

### 强风险提示
```yaml
risk_disclosure:
  mandatory: true
  
  disclosure_content:
    - "本服务不构成法律建议"
    - "法律问题具有复杂性"
    - "建议咨询持证律师"
    - "具体法律后果需专业判断"
    
  display:
    - 每次输出必显示
    - 突出显示
    - 不可关闭
```

## 验证要求

### 输出验证
```yaml
output_validation:
  pre_output:
    - check_no_legal_conclusion
    - check_citation_present
    - check_disclosure_present
    - check_uncertainty_expressed
    
  post_output:
    - verify_compliance
    - log_output
    - user_confirmation
```

### 质量检查
```yaml
quality_checks:
  - citation_accuracy
  - disclosure_completeness
  - uncertainty_clarity
  - boundary_compliance
```

## 审计要求

### 审计级别
```yaml
audit_level: comprehensive

  logged_items:
    - 所有交互记录
    - 所有输出内容
    - 用户确认记录
    - 风险提示展示
    
  retention: 7_years
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 禁止动作触发 | 触发禁止动作次数 | >0 |
| 引用完整率 | 完整引用/应引用 | <100% |
| 披露展示率 | 展示披露/应展示 | <100% |
| 用户投诉率 | 投诉/交互 | >1% |

## 维护方式
- 新增动作: 创建动作定义
- 调整要求: 更新强制要求
- 新增禁止: 更新禁止列表

## 引用文件
- `domain_agents/DOMAIN_REGISTRY.json` - 领域注册表
- `domain_agents/COMPLIANCE_MATRIX.md` - 合规矩阵
- `domain_agents/DOMAIN_ROUTING.md` - 领域路由
