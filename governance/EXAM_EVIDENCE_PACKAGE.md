# EXAM_EVIDENCE_PACKAGE.md - 检查证据包规范

## 目的
定义监管检查证据包的结构和准备规范，确保检查响应高效、完整。

## 适用范围
- 所有监管检查
- 所有审计活动
- 所有合规验证

## 证据包结构

### 标准结构
```yaml
evidence_package_structure:
  root:
    - README.md                    # 证据包说明
    - INDEX.json                   # 证据索引
    - SCOPE.md                     # 检查范围
  
  sections:
    governance:
      path: "01_governance/"
      content:
        - 组织架构图
        - 职责分工
        - 政策文件
        - 会议纪要
    
    policies:
      path: "02_policies/"
      content:
        - 政策清单
        - 政策原文
        - 版本历史
        - 审批记录
    
    controls:
      path: "03_controls/"
      content:
        - 控制矩阵
        - 控制文档
        - 测试结果
        - 问题整改
    
    operations:
      path: "04_operations/"
      content:
        - 运行记录
        - 日志摘要
        - 事件记录
        - 变更记录
    
    training:
      path: "05_training/"
      content:
        - 培训计划
        - 培训记录
        - 考核结果
        - 证书副本
    
    incidents:
      path: "06_incidents/"
      content:
        - 事件清单
        - 处理记录
        - 根因分析
        - 改进措施
    
    metrics:
      path: "07_metrics/"
      content:
        - KPI 报告
        - 趋势分析
        - 对比数据
        - 目标达成
```

## 证据类型

### 文档证据
```yaml
document_evidence:
  types:
    policy_document:
      description: "政策文件"
      requirements:
        - 最新版本
        - 审批签名
        - 生效日期
        - 版本历史
    
    process_document:
      description: "流程文件"
      requirements:
        - 流程图
        - 步骤说明
        - 角色职责
        - 例外处理
    
    report:
      description: "报告文件"
      requirements:
        - 报告日期
        - 编制人
        - 审核人
        - 数据来源
```

### 运行证据
```yaml
operational_evidence:
  types:
    log_record:
      description: "日志记录"
      requirements:
        - 时间戳
        - 操作人
        - 操作内容
        - 结果状态
    
    screenshot:
      description: "系统截图"
      requirements:
        - 截图时间
        - 系统标识
        - 关键信息高亮
        - 来源说明
    
    sample_data:
      description: "样本数据"
      requirements:
        - 数据脱敏
        - 样本说明
        - 选择依据
        - 完整性保证
```

### 人员证据
```yaml
personnel_evidence:
  types:
    interview_record:
      description: "访谈记录"
      requirements:
        - 访谈日期
        - 访谈对象
        - 访谈内容
        - 签字确认
    
    training_record:
      description: "培训记录"
      requirements:
        - 培训日期
        - 培训内容
        - 参加人员
        - 考核结果
    
    certificate:
      description: "证书"
      requirements:
        - 证书原件或副本
        - 有效期
        - 发证机构
```

## 证据准备流程

### 准备阶段
```yaml
preparation_phase:
  step_1_scope_confirmation:
    action: "确认检查范围"
    output: "检查范围文档"
    timeline: "检查前 30 天"
  
  step_2_evidence_mapping:
    action: "证据映射"
    output: "证据需求清单"
    timeline: "检查前 25 天"
  
  step_3_responsibility_assignment:
    action: "责任分配"
    output: "责任分配表"
    timeline: "检查前 20 天"
  
  step_4_evidence_collection:
    action: "证据收集"
    output: "原始证据文件"
    timeline: "检查前 15 天"
  
  step_5_evidence_review:
    action: "证据审核"
    output: "审核后的证据"
    timeline: "检查前 10 天"
  
  step_6_package_assembly:
    action: "证据包组装"
    output: "完整证据包"
    timeline: "检查前 5 天"
  
  step_7_final_review:
    action: "最终复核"
    output: "最终版本"
    timeline: "检查前 2 天"
```

### 质量检查
```yaml
quality_check:
  completeness:
    - 所有要求的证据都已包含
    - 证据覆盖所有检查范围
    - 时间范围符合要求
  
  accuracy:
    - 数据准确无误
    - 文档版本正确
    - 信息一致
  
  format:
    - 文件命名规范
    - 目录结构清晰
    - 索引完整准确
  
  compliance:
    - 敏感信息已脱敏
    - 访问控制已设置
    - 保密要求已满足
```

## 证据索引

### 索引结构
```json
{
  "package_info": {
    "package_id": "EP-2026-001",
    "exam_type": "年度合规检查",
    "exam_scope": "AI 治理",
    "preparation_date": "2026-04-07",
    "responsible": "合规负责人"
  },
  "evidence_index": [
    {
      "evidence_id": "EV-001",
      "category": "governance",
      "type": "policy_document",
      "title": "AI 治理政策",
      "file_path": "02_policies/AI_POLICY_FRAMEWORK.md",
      "version": "1.0.0",
      "effective_date": "2026-01-01",
      "related_requirement": "REQ-001"
    }
  ],
  "requirement_mapping": {
    "REQ-001": ["EV-001", "EV-002", "EV-003"],
    "REQ-002": ["EV-004", "EV-005"]
  }
}
```

## 证据提交

### 提交方式
```yaml
submission_methods:
  secure_portal:
    description: "安全门户提交"
    suitable_for: "电子证据"
    requirements:
      - 加密传输
      - 访问日志
      - 接收确认
  
  physical_delivery:
    description: "物理交付"
    suitable_for: "纸质证据"
    requirements:
      - 密封包装
      - 交接记录
      - 保管责任
  
  on_site_access:
    description: "现场访问"
    suitable_for: "系统演示"
    requirements:
      - 访问授权
      - 陪同人员
      - 操作记录
```

### 提交清单
```yaml
submission_checklist:
  before_submission:
    - [ ] 证据包完整性检查
    - [ ] 敏感信息脱敏确认
    - [ ] 索引与实际文件一致
    - [ ] 文件可正常打开
    - [ ] 内部审批完成
  
  at_submission:
    - [ ] 提交记录保存
    - [ ] 接收确认获取
    - [ ] 后续联系确认
  
  after_submission:
    - [ ] 补充材料准备
    - [ ] 答疑人员安排
    - [ ] 跟进进度监控
```

## 证据保管

### 保管要求
```yaml
retention_requirements:
  duration: "检查完成后 5 年"
  storage:
    - 安全存储环境
    - 访问控制
    - 备份机制
    - 完整性保护
  
  access:
    - 需授权访问
    - 访问日志记录
    - 保密义务确认
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
- 下次评审: 2027-04-07
