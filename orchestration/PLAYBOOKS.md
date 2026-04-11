# PLAYBOOKS.md - 策略手册

## 目的
把高频高价值场景沉淀成可复用的策略手册。

## 适用范围
所有需要标准化处理的常见场景。

## 手册结构

```yaml
playbook:
  id: "PB-001"
  name: "场景名称"
  description: "场景描述"
  
  applicable_conditions:
    - 条件1
    - 条件2
    
  default_strategy:
    strategy_id: "STRAT-xxx"
    params: {}
    
  exceptions:
    - condition: "异常条件"
      strategy: "替代策略"
      
  validation_steps:
    - step1
    - step2
    
  stop_conditions:
    - 停止条件1
    - 停止条件2
```

## 手册列表

### 1. 事实查询
```yaml
playbook:
  id: "PB-fact-query"
  name: "事实查询"
  description: "用户询问具体事实或数据"
  
  applicable_conditions:
    - query_type: "fact"
    - expected_answer: "specific_value"
    
  default_strategy:
    strategy_id: "STRAT-deep_search_first"
    steps:
      - name: "检索"
        action: "search_knowledge_base"
        params:
          sources: ["verified", "official"]
          min_confidence: 0.8
          
      - name: "验证"
        action: "cross_validate"
        params:
          min_sources: 2
          
      - name: "回答"
        action: "generate_answer_with_citation"
        
  exceptions:
    - condition: "time_sensitive"
      strategy: "STRAT-answer_then_verify"
      params:
        verification_delay: "10s"
        
    - condition: "low_confidence_result"
      strategy: "STRAT_conservative_uncertainty"
      action: "state_uncertainty_clearly"
      
  validation_steps:
    - "检查来源可信度"
    - "验证数据时效性"
    - "确认无冲突信息"
    
  stop_conditions:
    - "找到高置信度答案"
    - "用户确认满意"
    - "无法找到可靠来源"
```

### 2. 文档重写
```yaml
playbook:
  id: "PB-doc-rewrite"
  name: "文档重写"
  description: "用户要求重写或优化文档"
  
  applicable_conditions:
    - task_type: "rewrite"
    - input: "document_content"
    
  default_strategy:
    strategy_id: "STRAT-strong_citation"
    steps:
      - name: "分析"
        action: "analyze_document"
        params:
          aspects: ["structure", "style", "content"]
          
      - name: "规划"
        action: "plan_rewrite"
        params:
          preserve: ["key_facts", "citations"]
          improve: ["clarity", "structure"]
          
      - name: "执行"
        action: "execute_rewrite"
        
      - name: "验证"
        action: "validate_rewrite"
        params:
          check: ["accuracy", "completeness"]
          
  exceptions:
    - condition: "technical_document"
      strategy: "preserve_technical_accuracy"
      params:
        verify_technical_terms: true
        
    - condition: "legal_document"
      strategy: "conservative_rewrite"
      params:
        preserve_exact_wording: true
        
  validation_steps:
    - "对比原文关键信息"
    - "验证引用完整性"
    - "检查风格一致性"
    
  stop_conditions:
    - "用户确认满意"
    - "达到最大迭代次数"
    - "质量检查通过"
```

### 3. 复杂规划
```yaml
playbook:
  id: "PB-complex-planning"
  name: "复杂规划"
  description: "需要多步骤规划的复杂任务"
  
  applicable_conditions:
    - task_complexity: "high"
    - requires_planning: true
    
  default_strategy:
    strategy_id: "STRAT-deep_search_first"
    steps:
      - name: "需求分析"
        action: "analyze_requirements"
        params:
          identify_constraints: true
          identify_dependencies: true
          
      - name: "信息收集"
        action: "gather_information"
        params:
          sources: ["memory", "external", "user"]
          
      - name: "方案设计"
        action: "design_plan"
        params:
          generate_alternatives: true
          evaluate_risks: true
          
      - name: "方案验证"
        action: "validate_plan"
        params:
          check_feasibility: true
          check_dependencies: true
          
      - name: "输出方案"
        action: "present_plan"
        params:
          include_alternatives: true
          include_risks: true
          
  exceptions:
    - condition: "time_critical"
      strategy: "rapid_planning"
      params:
        skip_alternatives: true
        focus_critical_path: true
        
    - condition: "high_risk"
      strategy: "conservative_planning"
      params:
        require_validation: true
        include_contingency: true
        
  validation_steps:
    - "检查依赖完整性"
    - "验证资源可用性"
    - "评估风险可控性"
    
  stop_conditions:
    - "用户批准方案"
    - "发现不可行因素"
    - "资源约束无法满足"
```

### 4. 长任务推进
```yaml
playbook:
  id: "PB-long-task"
  name: "长任务推进"
  description: "跨会话的长期任务执行"
  
  applicable_conditions:
    - task_duration: "multi_session"
    - has_project_context: true
    
  default_strategy:
    strategy_id: "checkpoint_driven"
    steps:
      - name: "状态恢复"
        action: "restore_task_state"
        params:
          load_checkpoint: true
          verify_context: true
          
      - name: "进度评估"
        action: "assess_progress"
        params:
          check_milestones: true
          identify_blockers: true
          
      - name: "下一步规划"
        action: "plan_next_steps"
        params:
          prioritize_blocked: false
          
      - name: "执行推进"
        action: "execute_steps"
        params:
          create_checkpoints: true
          
      - name: "状态保存"
        action: "save_state"
        params:
          update_progress: true
          record_decisions: true
          
  exceptions:
    - condition: "blocked_task"
      strategy: "blocker_resolution"
      params:
        identify_alternatives: true
        escalate_if_needed: true
        
    - condition: "context_changed"
      strategy: "context_revalidation"
      params:
        recheck_assumptions: true
        adjust_plan: true
        
  validation_steps:
    - "验证状态一致性"
    - "检查依赖状态"
    - "确认资源可用"
    
  stop_conditions:
    - "任务完成"
    - "用户取消"
    - "发现重大阻塞"
```

### 5. 项目复盘
```yaml
playbook:
  id: "PB-project-review"
  name: "项目复盘"
  description: "项目阶段或完成后的复盘"
  
  applicable_conditions:
    - trigger: "milestone_complete"
    - or: "project_complete"
    
  default_strategy:
    steps:
      - name: "数据收集"
        action: "collect_project_data"
        params:
          include:
            - milestones
            - decisions
            - issues
            - metrics
            
      - name: "偏差分析"
        action: "analyze_deviation"
        params:
          compare_plan_actual: true
          identify_root_causes: true
          
      - name: "经验提取"
        action: "extract_lessons"
        params:
          categorize: ["success", "failure", "improvement"]
          
      - name: "建议生成"
        action: "generate_recommendations"
        params:
          for_future: true
          actionable: true
          
      - name: "报告输出"
        action: "generate_report"
        params:
          template: "review_template"
          
  exceptions:
    - condition: "failed_project"
      strategy: "blameless_review"
      params:
        focus_systemic_issues: true
        avoid_personal_blame: true
        
  validation_steps:
    - "验证数据完整性"
    - "检查分析客观性"
    - "确认建议可行性"
    
  stop_conditions:
    - "报告完成"
    - "用户确认"
```

### 6. 冲突信息处理
```yaml
playbook:
  id: "PB-conflict-handling"
  name: "冲突信息处理"
  description: "遇到相互矛盾的信息"
  
  applicable_conditions:
    - conflict_detected: true
    
  default_strategy:
    strategy_id: "STRAT_conservative_uncertainty"
    steps:
      - name: "冲突识别"
        action: "identify_conflicts"
        params:
          sources: ["memory", "external", "user_input"]
          
      - name: "来源评估"
        action: "evaluate_sources"
        params:
          criteria: ["credibility", "timeliness", "verification"]
          
      - name: "冲突分析"
        action: "analyze_conflict"
        params:
          determine_type: true  # factual, opinion, temporal
          identify_resolution_path: true
          
      - name: "用户确认"
        action: "request_clarification"
        params:
          present_options: true
          explain_conflict: true
          
      - name: "记录决策"
        action: "record_resolution"
        params:
          update_memory: true
          mark_conflict_resolved: true
          
  exceptions:
    - condition: "critical_conflict"
      strategy: "escalate"
      params:
        require_human_decision: true
        
    - condition: "temporal_conflict"
      strategy: "use_latest"
      params:
        verify_timestamp: true
        
  validation_steps:
    - "确认冲突类型正确"
    - "验证来源评估合理"
    - "检查用户确认完整"
    
  stop_conditions:
    - "冲突解决"
    - "用户确认处理方式"
```

### 7. 高风险回答
```yaml
playbook:
  id: "PB-high-risk-answer"
  name: "高风险回答"
  description: "涉及敏感或高风险内容的回答"
  
  applicable_conditions:
    - risk_level: "high"
    - or: "critical"
    
  default_strategy:
    strategy_id: "STRAT_conservative_uncertainty"
    steps:
      - name: "风险评估"
        action: "assess_risk"
        params:
          dimensions: ["safety", "accuracy", "privacy", "legal"]
          
      - name: "安全检查"
        action: "safety_check"
        params:
          check_policies: true
          check_boundaries: true
          
      - name: "内容准备"
        action: "prepare_content"
        params:
          require_citations: true
          state_limitations: true
          include_disclaimers: true
          
      - name: "审核确认"
        action: "review_content"
        params:
          auto_check: true
          human_review_if_needed: true
          
      - name: "输出回答"
        action: "deliver_answer"
        params:
          include_uncertainty: true
          provide_alternatives: true
          
  exceptions:
    - condition: "safety_violation"
      strategy: "refuse_answer"
      params:
        explain_reason: true
        suggest_alternatives: true
        
  validation_steps:
    - "安全检查通过"
    - "引用验证完整"
    - "免责声明包含"
    
  stop_conditions:
    - "安全检查失败"
    - "无法满足安全要求"
    - "用户确认接受风险"
```

### 8. 资料检索
```yaml
playbook:
  id: "PB-resource-search"
  name: "资料检索"
  description: "用户需要查找特定资料或文档"
  
  applicable_conditions:
    - task_type: "search"
    - target: "document_or_resource"
    
  default_strategy:
    strategy_id: "STRAT-deep_search_first"
    steps:
      - name: "需求理解"
        action: "understand_requirement"
        params:
          clarify_scope: true
          identify_keywords: true
          
      - name: "多源检索"
        action: "multi_source_search"
        params:
          sources: ["local", "memory", "external"]
          parallel: true
          
      - name: "结果整合"
        action: "integrate_results"
        params:
          deduplicate: true
          rank_by_relevance: true
          
      - name: "结果呈现"
        action: "present_results"
        params:
          summarize: true
          provide_access: true
          
  exceptions:
    - condition: "no_results"
      strategy: "suggest_alternatives"
      params:
        broaden_search: true
        suggest_related: true
        
    - condition: "too_many_results"
      strategy: "refine_search"
      params:
        add_filters: true
        cluster_results: true
        
  validation_steps:
    - "验证结果相关性"
    - "检查来源可访问性"
    - "确认无敏感信息泄露"
    
  stop_conditions:
    - "用户找到目标"
    - "用户确认无更多需求"
    - "资源不可访问"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 手册命中率 | 使用手册/总任务 | <50% |
| 手册成功率 | 成功/使用手册 | <85% |
| 异常触发率 | 触发异常/使用手册 | >20% |
| 用户满意度 | 手册场景满意度 | <80% |

## 维护方式
- 新增手册: 创建手册定义
- 更新手册: 根据反馈优化
- 废弃手册: 标记为deprecated

## 引用文件
- `strategy/STRATEGY_REGISTRY.json` - 策略注册表
- `strategy/STRATEGY_SELECTION.md` - 策略选择
- `strategy/STRATEGY_EVAL.md` - 策略评测
