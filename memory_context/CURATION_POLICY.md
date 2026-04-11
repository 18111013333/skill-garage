# CURATION_POLICY.md - 知识整理与维护规则

## 目的
定义知识整理与维护规则，确保知识库能长期变干净、变有序。

## 适用范围
- 知识分类
- 内容整理
- 质量维护
- 过期清理

## 核心规则

### 1. 分类重整

```yaml
reclassification:
  # 分类体系
  taxonomy:
    levels:
      - level_1: "领域"
      - level_2: "主题"
      - level_3: "子主题"
      - level_4: "标签"
    
    domains:
      - 技术
      - 产品
      - 运营
      - 市场
      - 人事
      - 财务
      - 法务
  
  # 自动分类
  auto_classify:
    enabled: true
    method: "ml_classifier"
    confidence_threshold: 0.8
    fallback: "manual"
  
  # 分类审核
  review:
    frequency: "quarterly"
    reviewer: "knowledge_curator"
    action_on_misclassified: "reclassify"
```

### 2. 重复合并

```yaml
duplicate_merge:
  # 检测规则
  detection:
    exact_match:
      fields: ["title", "content_hash"]
      action: "auto_merge"
    
    near_duplicate:
      threshold: 0.90
      action: "mark_for_review"
    
    semantic_duplicate:
      threshold: 0.85
      action: "mark_for_review"
  
  # 合并策略
  merge_strategy:
    prefer: "most_complete"
    combine_metadata: true
    preserve_versions: true
    notify_owners: true
  
  # 合并流程
  process:
    - 检测重复项
    - 选择主文档
    - 合并内容
    - 合并元数据
    - 重定向引用
    - 归档副本
```

### 3. 冲突标记

```yaml
conflict_handling:
  # 冲突类型
  conflict_types:
    - 内容冲突（不同来源信息矛盾）
    - 版本冲突（多版本不一致）
    - 分类冲突（分类归属争议）
    - 权限冲突（访问权限争议）
  
  # 冲突检测
  detection:
    enabled: true
    frequency: "weekly"
    scope: "all_content"
  
  # 冲突标记
  marking:
    status: "conflict_detected"
    severity: ["low", "medium", "high"]
    assignee: "knowledge_curator"
  
  # 冲突解决
  resolution:
    low:
      resolver: "auto"
      strategy: "prefer_recent"
    
    medium:
      resolver: "curator"
      timeout: "7d"
    
    high:
      resolver: "expert_panel"
      timeout: "14d"
```

### 4. 陈旧清理

```yaml
stale_cleanup:
  # 陈旧判定
  staleness_criteria:
    age_threshold: 365  # 天
    access_threshold: 90  # 无访问天数
    accuracy_score: 0.6  # 准确性评分
  
  # 清理动作
  actions:
    mark_stale:
      condition: "age > 180d AND access < 30d"
      action: "mark_for_review"
    
    archive:
      condition: "age > 365d AND access < 90d"
      action: "move_to_archive"
    
    delete:
      condition: "age > 730d AND access < 180d AND accuracy < 0.5"
      action: "soft_delete"
      require_approval: true
  
  # 清理流程
  process:
    - 扫描陈旧内容
    - 生成清理建议
    - 通知内容负责人
    - 等待确认（7天）
    - 执行清理动作
    - 记录审计日志
```

### 5. 术语统一

```yaml
terminology_standardization:
  # 术语库
  glossary:
    enabled: true
    update_frequency: "monthly"
    approval_required: true
  
  # 自动标准化
  auto_standardize:
    enabled: true
    scope: ["technical_terms", "product_names", "abbreviations"]
    preserve_original: true
  
  # 术语冲突
  conflicts:
    detection: true
    resolution: "prefer_glossary"
    notify_on_change: true
```

### 6. 责任人管理

```yaml
ownership:
  # 责任人分配
  assignment:
    default_owner: "creator"
    allow_transfer: true
    require_acceptance: true
  
  # 责任人职责
  responsibilities:
    - 内容准确性维护
    - 及时更新内容
    - 处理反馈意见
    - 参与审核流程
  
  # 责任人变更
  transfer:
    trigger:
      - 责任人离职
      - 责任人申请
      - 长期无响应（30天）
    
    process:
      - 通知原责任人
      - 确认新责任人
      - 转移权限
      - 更新记录
```

### 7. 复查周期

```yaml
review_cycle:
  # 复查频率
  frequency:
    critical_content: "monthly"
    important_content: "quarterly"
    normal_content: "semiannually"
  
  # 复查内容
  review_items:
    - 内容准确性
    - 内容完整性
    - 分类正确性
    - 链接有效性
    - 权限设置
  
  # 复查流程
  process:
    - 生成复查清单
    - 通知责任人
    - 执行复查
    - 记录结果
    - 处理问题项
  
  # 复查报告
  reporting:
    frequency: "monthly"
    content:
      - 复查覆盖率
      - 问题发现率
      - 问题解决率
      - 质量趋势
```

## 异常处理

### 责任人缺失
- 自动分配给上级
- 通知管理员
- 记录异常

### 复查超期
- 自动升级
- 通知管理员
- 标记待处理

### 合并争议
- 暂停合并
- 提交仲裁
- 记录决策

## 完成标准
- [x] 分类重整规则完整
- [x] 重复合并规则清晰
- [x] 冲突标记机制明确
- [x] 陈旧清理规则完整
- [x] 术语统一规则清晰
- [x] 责任人管理规则明确
- [x] 复查周期定义清晰
- [x] 知识库能长期变干净、变有序

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
