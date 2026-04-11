# COMPLIANCE_MATRIX.md - 行业合规矩阵

## 目的
建立行业合规矩阵，确保不同领域有不同合规模式。

## 适用范围
所有行业领域的合规要求管理。

## 合规维度

| 维度 | 说明 | 级别 |
|------|------|------|
| 允许动作 | 可执行的操作 | 按域定义 |
| 必须校验 | 强制校验项 | 按域定义 |
| 必须引用 | 强制引用要求 | 按域定义 |
| 必须审批 | 强制审批项 | 按域定义 |
| 禁止自动执行 | 禁止自动化的操作 | 按域定义 |
| 日志留存要求 | 审计日志要求 | 按域定义 |

## 合规矩阵

### 法律领域
```yaml
domain_legal:
  compliance_level: maximum
  
  allowed_actions:
    - 合同结构审查
    - 条款风险提示
    - 文本改写建议
    - 问题清单生成
    - 法律信息整理
    
  required_validations:
    - pre:
        - source_credibility_check
        - jurisdiction_check
    - during:
        - boundary_monitoring
    - post:
        - citation_verification
        - disclaimer_check
        - uncertainty_expression_check
        
  required_citations:
    mode: strict
    min_sources: 2
    format: "standard_legal"
    
  required_approvals:
    - 高风险结论
    - 批量合同审查
    - 外部发送
    
  forbidden_auto_actions:
    - 提供确定性法律结论
    - 替代持证法律服务
    - 代表用户签署
    - 法律文件最终定稿
    
  audit_requirements:
    log_level: comprehensive
    retention: 7_years
    include:
      - all_interactions
      - all_recommendations
      - user_disclaimers
      
  mandatory_disclosures:
    - "本服务不构成法律建议"
    - "建议咨询专业律师"
    - "结论仅供参考"
```

### 金融领域
```yaml
domain_finance:
  compliance_level: strict
  
  allowed_actions:
    - 信息整理分析
    - 指标解释说明
    - 风险对比分析
    - 预算测算辅助
    - 公开数据梳理
    
  required_validations:
    - pre:
        - data_source_verification
        - timeliness_check
    - during:
        - calculation_verification
    - post:
        - risk_disclosure_check
        
  required_citations:
    mode: strict
    min_sources: 1
    timeliness_required: true
    
  required_approvals:
    - 投资相关建议
    - 风险评估报告
    - 外部发布
    
  forbidden_auto_actions:
    - 提供投资建议
    - 保证收益承诺
    - 无依据荐股
    - 替代持牌投顾
    
  audit_requirements:
    log_level: detailed
    retention: 5_years
    
  mandatory_disclosures:
    - "不构成投资建议"
    - "投资有风险"
    - "过往业绩不代表未来"
```

### 医疗健康领域
```yaml
domain_healthcare:
  compliance_level: maximum
  
  allowed_actions:
    - 健康信息整理
    - 文献检索汇总
    - 生活方式建议
    - 医疗知识解释
    
  required_validations:
    - pre:
        - source_authority_check
    - post:
        - medical_disclaimer_check
        
  required_citations:
    mode: strict
    require_authoritative_source: true
    
  required_approvals:
    - 所有医疗相关输出
    
  forbidden_auto_actions:
    - 提供诊断
    - 开具处方
    - 治疗方案制定
    - 替代医疗建议
    
  audit_requirements:
    log_level: comprehensive
    retention: 10_years
    
  mandatory_disclosures:
    - "不能替代专业医疗建议"
    - "如有不适请就医"
    - "仅供参考"
```

### 运营领域
```yaml
domain_operations:
  compliance_level: standard
  
  allowed_actions:
    - SOP生成
    - 项目进度跟踪
    - 待办任务拆解
    - 复盘分析
    - 协作建议
    
  required_validations:
    - post:
        - output_quality_check
        
  required_citations:
    mode: moderate
    
  required_approvals:
    - 外部系统操作
    - 批量变更
    
  forbidden_auto_actions:
    - 无授权的外部操作
    - 越权审批
    
  audit_requirements:
    log_level: standard
    retention: 1_year
```

### 研究领域
```yaml
domain_research:
  compliance_level: high
  
  allowed_actions:
    - 文献综述
    - 数据分析
    - 报告生成
    - 假设验证
    
  required_validations:
    - pre:
        - source_credibility
    - post:
        - citation_check
        - methodology_review
        
  required_citations:
    mode: strict
    format: academic
    
  required_approvals:
    - 涉及敏感数据
    - 外部发布
    
  forbidden_auto_actions:
    - 数据造假
    - 引用伪造
    
  audit_requirements:
    log_level: detailed
    retention: 5_years
```

### 内容创作领域
```yaml
domain_content:
  compliance_level: standard
  
  allowed_actions:
    - 文本创作
    - 内容编辑
    - 翻译转换
    - 风格调整
    
  required_validations:
    - post:
        - plagiarism_check
        - content_quality
        
  required_citations:
    mode: relaxed
    
  required_approvals:
    - 商业发布
    - 涉及版权
    
  forbidden_auto_actions:
    - 侵犯版权
    - 抄袭内容
    
  audit_requirements:
    log_level: basic
    retention: 1_year
```

## 合规级别对比

| 级别 | 校验强度 | 引用要求 | 审批要求 | 日志级别 |
|------|----------|----------|----------|----------|
| standard | 基础 | 宽松 | 按需 | basic |
| high | 增强 | 中等 | 重要操作 | detailed |
| strict | 严格 | 严格 | 关键操作 | detailed |
| maximum | 最严 | 最严 | 全部操作 | comprehensive |

## 合规检查

### 检查流程
```yaml
compliance_check:
  steps:
    - identify_domain
    - load_compliance_rules
    - validate_allowed_actions
    - check_required_validations
    - verify_citations
    - confirm_approvals
    - check_forbidden_actions
    - apply_disclosures
```

### 检查结果
```yaml
check_result:
  status: pass | fail | warning
  violations: []
  warnings: []
  required_actions: []
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 合规违规次数 | 违规次数 | >0 |
| 审批通过率 | 通过/申请 | <80% |
| 披露完整性 | 披露完整/应披露 | <100% |
| 日志完整性 | 日志完整/应记录 | <100% |

## 维护方式
- 新增领域: 创建合规配置
- 调整规则: 更新合规矩阵
- 新增要求: 更新合规维度

## 引用文件
- `domain_agents/DOMAIN_REGISTRY.json` - 领域注册表
- `domain_agents/DOMAIN_ROUTING.md` - 领域路由
- `safety/RISK_POLICY.md` - 风险策略
