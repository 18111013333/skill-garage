# WORKFLOW_TEMPLATES.md - 工作流模板库

## 目的
提供常用工作流模板，加速任务执行、保证执行质量。

## 适用范围
所有需要多步骤执行的任务。

## 模板分类

### 按任务类型分类
| 类型 | 模板数 | 说明 |
|------|--------|------|
| 信息搜集 | 5 | 搜索、调研类 |
| 文档处理 | 8 | 文档创建、编辑类 |
| 内容创作 | 6 | 写作、生成类 |
| 数据分析 | 4 | 分析、报告类 |
| 系统操作 | 3 | 配置、维护类 |

## 信息搜集模板

### TPL-SEARCH-001: 基础搜索
```yaml
name: basic_search
description: 单一主题快速搜索
steps:
  - id: search
    skill: xiaoyi-web-search
    input: "${query}"
    output: search_results
  
  - id: summarize
    action: summarize
    input: search_results
    output: summary
  
  - id: cite
    action: add_citations
    input: summary
    output: final_result

estimated_time: 30s
max_steps: 3
```

### TPL-SEARCH-002: 深度调研
```yaml
name: deep_research
description: 多源深度调研
steps:
  - id: search_multiple
    skills:
      - xiaoyi-web-search
      - web-search-exa
      - deep-search-and-insight-synthesize
    parallel: true
    output: all_results
  
  - id: merge
    action: merge_results
    input: all_results
    output: merged_results
  
  - id: analyze
    skill: research-cog
    input: merged_results
    output: analysis
  
  - id: report
    skill: article-writer
    input: analysis
    output: final_report

estimated_time: 180s
max_steps: 10
```

### TPL-SEARCH-003: 对比分析
```yaml
name: compare_analysis
description: 多主题对比分析
steps:
  - id: search_a
    skill: xiaoyi-web-search
    input: "${topic_a}"
    output: results_a
  
  - id: search_b
    skill: xiaoyi-web-search
    input: "${topic_b}"
    output: results_b
  
  - id: compare
    action: compare_results
    input: [results_a, results_b]
    output: comparison
  
  - id: summarize
    action: create_comparison_table
    input: comparison
    output: final_result

estimated_time: 60s
max_steps: 5
```

## 文档处理模板

### TPL-DOC-001: 文档转换
```yaml
name: document_convert
description: 文档格式转换
steps:
  - id: upload
    skill: xiaoyi-file-upload
    input: "${file}"
    output: file_url
  
  - id: convert
    skill: xiaoyi-doc-convert
    input: file_url
    output: converted_file
  
  - id: validate
    action: validate_format
    input: converted_file
    output: final_result

estimated_time: 60s
max_steps: 5
fallback:
  - markitdown
  - pdf
  - docx
```

### TPL-DOC-002: 文档摘要
```yaml
name: document_summary
description: 长文档摘要生成
steps:
  - id: read
    action: read_document
    input: "${document}"
    output: content
  
  - id: chunk
    action: split_chunks
    input: content
    params:
      max_chunk_size: 5000
    output: chunks
  
  - id: summarize_chunks
    action: parallel_summarize
    input: chunks
    output: chunk_summaries
  
  - id: merge_summary
    action: merge_summaries
    input: chunk_summaries
    output: final_summary

estimated_time: 120s
max_steps: 8
```

### TPL-DOC-003: 文档翻译
```yaml
name: document_translate
description: 文档多语言翻译
steps:
  - id: extract_text
    action: extract_text
    input: "${document}"
    output: text
  
  - id: translate
    action: translate_text
    input: text
    params:
      target_lang: "${target_language}"
    output: translated_text
  
  - id: format
    action: preserve_format
    input: translated_text
    output: final_result

estimated_time: 90s
max_steps: 5
```

## 内容创作模板

### TPL-CREATE-001: 文章写作
```yaml
name: article_writing
description: 结构化文章创作
steps:
  - id: outline
    skill: article-writer
    input: "${topic}"
    action: generate_outline
    output: outline
  
  - id: research
    skill: xiaoyi-web-search
    input: outline
    output: research_data
  
  - id: write_sections
    skill: article-writer
    input: [outline, research_data]
    action: write_sections
    output: sections
  
  - id: assemble
    action: assemble_article
    input: sections
    output: article
  
  - id: polish
    action: polish_content
    input: article
    output: final_article

estimated_time: 300s
max_steps: 15
```

### TPL-CREATE-002: 报告生成
```yaml
name: report_generation
description: 专业报告生成
steps:
  - id: gather_data
    skills:
      - xiaoyi-web-search
      - data-analysis
    input: "${report_topic}"
    output: raw_data
  
  - id: analyze
    skill: data-analysis
    input: raw_data
    output: analysis
  
  - id: visualize
    skill: chart-image
    input: analysis
    output: charts
  
  - id: write_report
    skill: xiaoyi-report
    input: [analysis, charts]
    output: report
  
  - id: review
    action: quality_check
    input: report
    output: final_report

estimated_time: 240s
max_steps: 12
```

### TPL-CREATE-003: 邮件撰写
```yaml
name: email_composition
description: 专业邮件撰写
steps:
  - id: understand_context
    action: analyze_intent
    input: "${email_request}"
    output: context
  
  - id: draft
    action: compose_email
    input: context
    output: draft
  
  - id: tone_adjust
    action: adjust_tone
    input: draft
    params:
      tone: "${tone}"
    output: adjusted_draft
  
  - id: review
    action: grammar_check
    input: adjusted_draft
    output: final_email

estimated_time: 60s
max_steps: 5
```

## 数据分析模板

### TPL-DATA-001: 数据分析报告
```yaml
name: data_analysis_report
description: 数据分析报告生成
steps:
  - id: load_data
    action: load_data
    input: "${data_source}"
    output: data
  
  - id: clean
    action: clean_data
    input: data
    output: clean_data
  
  - id: analyze
    skill: data-analysis
    input: clean_data
    output: analysis
  
  - id: visualize
    skill: chart-image
    input: analysis
    output: visualizations
  
  - id: report
    action: generate_report
    input: [analysis, visualizations]
    output: final_report

estimated_time: 180s
max_steps: 10
```

### TPL-DATA-002: Excel 分析
```yaml
name: excel_analysis
description: Excel 数据分析
steps:
  - id: load
    skill: excel-analysis
    input: "${excel_file}"
    output: data
  
  - id: analyze
    skill: excel-analysis
    input: data
    action: analyze
    output: analysis
  
  - id: summarize
    action: create_summary
    input: analysis
    output: summary

estimated_time: 60s
max_steps: 5
```

## 系统操作模板

### TPL-SYS-001: 配置更新
```yaml
name: config_update
description: 安全配置更新
steps:
  - id: backup
    action: backup_config
    input: "${config_file}"
    output: backup_path
  
  - id: validate
    action: validate_config
    input: "${new_config}"
    output: validation_result
  
  - id: apply
    condition: validation_result.passed
    action: apply_config
    input: new_config
    output: apply_result
  
  - id: verify
    action: verify_config
    input: apply_result
    output: final_result
  
  - id: rollback
    condition: apply_result.failed
    action: rollback_config
    input: backup_path
    output: rollback_result

estimated_time: 30s
max_steps: 6
requires_confirmation: true
```

### TPL-SYS-002: 批量操作
```yaml
name: batch_operation
description: 安全批量操作
steps:
  - id: prepare
    action: prepare_batch
    input: "${items}"
    output: batch_plan
  
  - id: confirm
    action: request_confirmation
    input: batch_plan
    output: confirmation
  
  - id: execute
    condition: confirmation.approved
    action: execute_batch
    input: batch_plan
    params:
      batch_size: 5
      delay_between: 1000
    output: results
  
  - id: report
    action: generate_batch_report
    input: results
    output: final_report

estimated_time: 120s
max_steps: 10
requires_confirmation: true
```

## 模板使用规则

### 模板选择
```yaml
template_selection:
  by_task_type:
    qa: TPL-SEARCH-001
    research: TPL-SEARCH-002
    document_convert: TPL-DOC-001
    article: TPL-CREATE-001
    report: TPL-CREATE-002
    data_analysis: TPL-DATA-001
  
  by_complexity:
    simple: max_steps <= 5
    medium: max_steps 6-10
    complex: max_steps > 10
```

### 模板定制
```yaml
customization:
  allowed_params:
    - input_variables
    - output_format
    - timeout
    - fallback_skills
  
  not_allowed:
    - core_steps
    - safety_checks
    - audit_logging
```

## 模板管理

### 模板生命周期
| 阶段 | 说明 |
|------|------|
| 创建 | 新建模板 |
| 测试 | 测试模板效果 |
| 发布 | 发布到模板库 |
| 使用 | 用户使用模板 |
| 废弃 | 废弃旧模板 |

### 模板版本
```yaml
versioning:
  format: "v{major}.{minor}"
  compatibility: backward
  deprecation_period: 30d
```

## 异常处理

| 异常 | 处理 |
|------|------|
| 模板不存在 | 使用默认流程 |
| 步骤失败 | 执行 fallback |
| 超时 | 返回部分结果 |

## 维护方式
- 新增模板: 添加到对应分类
- 更新模板: 更新版本号
- 废弃模板: 标记 deprecated

## 引用文件
- `workflows/WORKFLOW_REGISTRY.json` - 工作流注册
- `workflows/MULTI_STEP_WORKFLOW.md` - 多步工作流
- `runtime/PLANNER.md` - 任务规划
