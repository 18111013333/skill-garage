# INGESTION_POLICY.md - 知识入库规则

## 目的
定义知识如何入库，确保知识进入平台前先治理。

## 适用范围
- 知识导入
- 系统同步
- 人工录入
- 会议沉淀
- 外部抓取

## 核心规则

### 1. 入库来源

```yaml
ingestion_sources:
  # 文档导入
  document_import:
    supported_formats:
      - pdf
      - docx
      - txt
      - md
      - html
    
    max_file_size: 50MB
    
    process:
      - 格式验证
      - 内容提取
      - 元数据解析
      - 质量检查
      - 入库存储
  
  # 系统同步
  system_sync:
    enabled: true
    
    sources:
      - project_documents
      - meeting_notes
      - task_descriptions
      - decision_records
    
    sync_frequency: "hourly"
  
  # 人工录入
  manual_entry:
    enabled: true
    
    validation:
      - 必填字段检查
      - 格式验证
      - 重复检测
      - 敏感内容检测
    
    approval:
      required: false
      auto_publish: false
  
  # 会议沉淀
  meeting_ingestion:
    enabled: true
    
    extract:
      - 会议纪要
      - 决策记录
      - 行动项
      - 待解决问题
    
    auto_link:
      - 关联项目
      - 关联任务
      - 关联参与者
  
  # 外部抓取
  external_crawl:
    enabled: true
    
    allowed_sources:
      - 官方文档
      - 公开知识库
      - 授权内容
    
    forbidden_sources:
      - 版权保护内容
      - 需登录内容
      - 敏感网站
```

### 2. 清洗规则

```yaml
cleaning:
  # 格式清洗
  format_cleaning:
    - 移除 HTML 标签
    - 统一换行符
    - 规范化空白字符
    - 修复编码问题
  
  # 内容清洗
  content_cleaning:
    - 移除页眉页脚
    - 移除水印
    - 移除广告内容
    - 移除导航元素
  
  # 质量清洗
  quality_cleaning:
    - 移除过短内容（< 50 字）
    - 移除无意义内容
    - 标记低质量内容
    - 检测并标记机器生成内容
```

### 3. 去重规则

```yaml
deduplication:
  # 精确去重
  exact_dedup:
    method: "hash"
    fields: ["title", "content_hash"]
    action: "skip"
  
  # 相似去重
  similarity_dedup:
    method: "semantic"
    threshold: 0.95
    action: "merge"
  
  # 去重流程
  process:
    - 计算内容哈希
    - 检查精确匹配
    - 计算语义相似度
    - 标记或合并重复项
    - 记录去重日志
```

### 4. 脱敏规则

```yaml
desensitization:
  # 自动脱敏
  auto_desensitize:
    patterns:
      - 手机号
      - 身份证号
      - 银行卡号
      - 邮箱地址
      - IP 地址
      - 密码/密钥
    
    action: "mask"
  
  # 标记脱敏
  mark_sensitive:
    keywords:
      - "机密"
      - "内部"
      - "保密"
      - "敏感"
    
    action: "mark_for_review"
  
  # 审核流程
  review:
    required_for: "marked_content"
    reviewer: "knowledge_curator"
    timeout: "24h"
```

### 5. 来源保留

```yaml
source_preservation:
  # 元数据保留
  metadata:
    - source_type
    - source_url
    - source_author
    - source_date
    - import_date
    - import_user
  
  # 原文保留
  original:
    enabled: true
    retention: "permanent"
    access: "admin_only"
  
  # 版本历史
  versioning:
    enabled: true
    max_versions: 10
    diff_tracking: true
```

### 6. 入库流程

```yaml
ingestion_flow:
  steps:
    - step: 1
      name: "来源验证"
      checks:
        - 来源是否允许
        - 格式是否支持
        - 大小是否合规
    
    - step: 2
      name: "内容提取"
      actions:
        - 解析文档
        - 提取文本
        - 提取元数据
    
    - step: 3
      name: "清洗处理"
      actions:
        - 格式清洗
        - 内容清洗
        - 质量检查
    
    - step: 4
      name: "脱敏处理"
      actions:
        - 检测敏感内容
        - 执行脱敏
        - 标记需审核内容
    
    - step: 5
      name: "去重检查"
      actions:
        - 计算哈希
        - 检查重复
        - 合并或跳过
    
    - step: 6
      name: "质量评估"
      actions:
        - 完整性检查
        - 准确性评估
        - 新鲜度评估
    
    - step: 7
      name: "入库存储"
      actions:
        - 存储内容
        - 建立索引
        - 关联元数据
    
    - step: 8
      name: "审核发布"
      actions:
        - 触发审核（如需要）
        - 发布或暂存
        - 通知相关人员
```

## 异常处理

### 入库失败
- 记录失败原因
- 通知提交者
- 提供修复建议

### 质量不达标
- 标记为待改进
- 通知负责人
- 定期复查

### 敏感内容
- 阻止自动发布
- 提交人工审核
- 记录审计日志

## 完成标准
- [x] 入库来源定义完整
- [x] 清洗规则明确
- [x] 去重规则清晰
- [x] 脱敏规则完整
- [x] 来源保留机制明确
- [x] 入库流程清晰
- [x] 知识进入平台前先治理

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
