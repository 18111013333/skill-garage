# VENDOR_ASSESSMENT_POLICY.md - 供应商安全评估策略

## 目的
定义供应商安全评估的要求和流程，确保供应商符合组织安全标准。

## 适用范围
- 所有提供服务的第三方供应商
- 所有处理组织数据的供应商
- 所有接入组织系统的供应商

## 供应商分类

### 按风险等级分类
```yaml
vendor_classification:
  critical:
    description: "关键供应商"
    criteria:
      - 处理敏感数据
      - 接入核心系统
      - 业务连续性依赖
      - 不可替代服务
    assessment_frequency: "年度"
    assessment_depth: "全面评估"
  
  high:
    description: "高风险供应商"
    criteria:
      - 处理内部数据
      - 接入业务系统
      - 重要业务支持
    assessment_frequency: "年度"
    assessment_depth: "标准评估"
  
  medium:
    description: "中等风险供应商"
    criteria:
      - 有限数据接触
      - 非关键系统接入
      - 可替代服务
    assessment_frequency: "两年"
    assessment_depth: "简化评估"
  
  low:
    description: "低风险供应商"
    criteria:
      - 无数据接触
      - 无系统接入
      - 通用服务
    assessment_frequency: "三年"
    assessment_depth: "问卷评估"
```

## 评估内容

### 安全评估
```yaml
security_assessment:
  information_security:
    areas:
      - 安全管理体系
      - 安全策略和标准
      - 安全组织架构
      - 安全培训
    evidence:
      - ISO 27001 证书
      - 安全政策文件
      - 安全组织图
  
  technical_security:
    areas:
      - 访问控制
      - 加密措施
      - 网络安全
      - 终端安全
      - 漏洞管理
    evidence:
      - 技术架构文档
      - 安全配置标准
      - 渗透测试报告
  
  operational_security:
    areas:
      - 变更管理
      - 事件管理
      - 备份恢复
      - 业务连续性
    evidence:
      - 运维流程文档
      - 事件记录
      - 演练报告
```

### 隐私评估
```yaml
privacy_assessment:
  data_protection:
    areas:
      - 数据分类
      - 数据加密
      - 数据最小化
      - 数据保留
    evidence:
      - 数据保护政策
      - 数据处理记录
      - 技术措施说明
  
  privacy_compliance:
    areas:
      - 隐私政策
      - 同意管理
      - 数据主体权利
      - 跨境传输
    evidence:
      - 隐私政策
      - DPA 协议
      - 合规证明
```

### 合规评估
```yaml
compliance_assessment:
  regulatory_compliance:
    areas:
      - 适用法规识别
      - 合规状态
      - 监管历史
      - 整改情况
    evidence:
      - 合规声明
      - 审计报告
      - 整改记录
  
  contractual_compliance:
    areas:
      - 合同条款履行
      - SLA 达成情况
      - 违约历史
    evidence:
      - 合同副本
      - SLA 报告
      - 履约记录
```

## 评估方法

### 问卷评估
```yaml
questionnaire_assessment:
  description: "标准化问卷评估"
  suitable_for:
    - 低风险供应商
    - 初步筛选
    - 年度复评
  
  questionnaire_types:
    security_questionnaire:
      content: "安全控制问卷"
      questions: 50-100
      completion_time: "2-4 小时"
    
    privacy_questionnaire:
      content: "隐私保护问卷"
      questions: 30-50
      completion_time: "1-2 小时"
  
  scoring:
    pass_score: 80
    conditional_pass: 70-79
    fail: "< 70"
```

### 文档审阅
```yaml
document_review:
  description: "文档证据审阅"
  suitable_for:
    - 中高风险供应商
    - 深入评估
  
  document_types:
    required:
      - 安全政策
      - 组织架构
      - 认证证书
      - 审计报告
    
    optional:
      - 技术架构文档
      - 流程文档
      - 培训记录
      - 事件报告
  
  review_criteria:
    completeness: "文档是否完整"
    currency: "文档是否最新"
    adequacy: "内容是否充分"
```

### 现场评估
```yaml
on_site_assessment:
  description: "现场实地评估"
  suitable_for:
    - 关键供应商
    - 高风险场景
  
  activities:
    - 设施参观
    - 人员访谈
    - 系统演示
    - 控制验证
  
  duration: "1-3 天"
  team: "2-4 人"
  output: "现场评估报告"
```

### 第三方审计
```yaml
third_party_audit:
  description: "第三方审计报告"
  suitable_for:
    - 关键供应商
    - 替代现场评估
  
  accepted_reports:
    - SOC 2 Type II
    - ISO 27001 审计报告
    - CSA STAR 认证
  
  review_focus:
    - 审计范围匹配
    - 审计结果
    - 发现问题
    - 整改状态
```

## 评估流程

### 新供应商评估
```yaml
new_vendor_assessment:
  steps:
    step_1_classification:
      action: "供应商分类"
      output: "风险等级确定"
    
    step_2_questionnaire:
      action: "发送评估问卷"
      output: "问卷回复"
    
    step_3_review:
      action: "审阅回复和证据"
      output: "初步评估结果"
    
    step_4_deep_dive:
      action: "深入评估（如需要）"
      output: "详细评估报告"
    
    step_5_risk_decision:
      action: "风险决策"
      output: "批准/有条件批准/拒绝"
    
    step_6_contract:
      action: "合同安全条款"
      output: "签署合同"
```

### 年度复评
```yaml
annual_reassessment:
  triggers:
    - 到期复评
    - 重大变更
    - 事件触发
    - 风险变化
  
  process:
    - 发送更新问卷
    - 审阅变更情况
    - 评估风险变化
    - 更新风险等级
    - 记录评估结果
```

## 风险决策

### 决策标准
```yaml
risk_decision_criteria:
  approved:
    criteria:
      - 评估得分 >= 80
      - 无重大发现
      - 认证有效
    action: "正常合作"
  
  conditional_approval:
    criteria:
      - 评估得分 70-79
      - 存在可接受风险
      - 有整改计划
    action: "有条件合作"
    conditions:
      - 整改期限
      - 补偿控制
      - 加强监控
  
  rejected:
    criteria:
      - 评估得分 < 70
      - 存在重大风险
      - 无法接受
    action: "终止或拒绝合作"
```

## 持续监控

### 监控指标
```yaml
monitoring_metrics:
  security_metrics:
    - 安全事件数量
    - 漏洞修复时效
    - 认证状态
    - 审计发现
  
  performance_metrics:
    - SLA 达成率
    - 服务可用性
    - 响应时效
    - 问题解决率
  
  compliance_metrics:
    - 合规状态
    - 整改完成率
    - 监管变化响应
```

### 告警机制
```yaml
alert_mechanism:
  critical_alerts:
    - 安全事件
    - 认证失效
    - 重大违约
    - 监管处罚
    action: "立即响应"
  
  warning_alerts:
    - SLA 下降
    - 整改延期
    - 风险变化
    action: "48 小时内响应"
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
- 下次评审: 2027-04-07
