# PROJECT_REVIEW_TEMPLATE.md - 项目复盘模板

## 目的
定义项目阶段复盘模板，实现结构化回顾。

## 适用范围
所有项目的周期性review和关键节点review。

## 复盘类型

| 类型 | 触发时机 | 频率 | 重点 |
|------|----------|------|------|
| 阶段复盘 | 阶段完成 | 按阶段 | 阶段目标达成 |
| 周期复盘 | 定期 | 周度/月度 | 进度和风险 |
| 里程碑复盘 | 里程碑完成 | 按里程碑 | 交付质量 |
| 项目总结 | 项目结束 | 一次 | 全项目回顾 |

## 复盘模板

### 标准复盘模板
```yaml
review_report:
  metadata:
    review_id: "REV-PROJ001-001"
    project_id: "PROJ-2024-001"
    review_type: "milestone"
    review_date: "2024-02-15"
    reviewer: "system"
    
  section_1_objective:
    title: "本阶段目标"
    content:
      planned_objectives:
        - objective_1
        - objective_2
      success_criteria:
        - criteria_1
        - criteria_2
        
  section_2_actual:
    title: "实际完成"
    content:
      completed_items:
        - item: "目标1"
          status: "completed"
          completion_rate: 100
        - item: "目标2"
          status: "partial"
          completion_rate: 70
      deliverables:
        - name: "交付物1"
          status: "completed"
          quality: "high"
          
  section_3_deviation:
    title: "偏差分析"
    content:
      schedule_deviation:
        planned: "2024-02-01"
        actual: "2024-02-10"
        deviation_days: 9
        reason: "资源调配延迟"
        
      scope_deviation:
        added: ["功能X"]
        removed: []
        modified: ["功能Y范围缩小"]
        
      quality_deviation:
        planned_quality: "A"
        actual_quality: "B"
        reason: "测试覆盖不足"
        
  section_4_root_cause:
    title: "偏差原因"
    content:
      internal_factors:
        - factor: "资源预估不足"
          impact: "high"
          controllable: true
        - factor: "技术难点低估"
          impact: "medium"
          controllable: true
          
      external_factors:
        - factor: "第三方API变更"
          impact: "medium"
          controllable: false
          
  section_5_issues:
    title: "遗留问题"
    content:
      open_issues:
        - issue_id: "ISS-001"
          description: "性能优化未完成"
          priority: "high"
          owner: "张三"
          due_date: "2024-02-20"
          
      resolved_issues:
        - issue_id: "ISS-002"
          description: "登录功能bug"
          resolution: "已修复"
          
  section_6_risks:
    title: "风险更新"
    content:
      new_risks:
        - risk: "性能可能不达标"
          probability: "medium"
          impact: "high"
          mitigation: "增加性能测试"
          
      changed_risks:
        - risk: "第三方依赖风险"
          change: "概率从low变为medium"
          reason: "供应商稳定性问题"
          
      closed_risks:
        - risk: "需求变更风险"
          close_reason: "需求已冻结"
          
  section_7_lessons:
    title: "经验教训"
    content:
      successes:
        - "敏捷迭代方式有效"
        - "每日站会提升沟通效率"
        
      failures:
        - "技术调研不充分"
        - "资源缓冲不足"
        
      improvements:
        - "增加技术预研阶段"
        - "预留20%资源缓冲"
        
  section_8_next_phase:
    title: "下一阶段建议"
    content:
      priorities:
        - priority: "完成性能优化"
          reason: "影响上线"
        - priority: "增加测试覆盖"
          reason: "质量保障"
          
      resource_needs:
        - role: "测试工程师"
          reason: "测试人力不足"
          
      risk_mitigations:
        - risk: "性能风险"
          action: "提前进行压力测试"
          
  section_9_metrics:
    title: "关键指标"
    content:
      schedule_adherence: 85
      quality_score: 82
      risk_management: 75
      team_velocity: 12
      defect_rate: 0.05
      
  approvals:
    - role: "项目经理"
      status: "approved"
      date: "2024-02-15"
    - role: "技术负责人"
      status: "approved"
      date: "2024-02-15"
```

## 复盘流程

### 执行流程
```yaml
review_flow:
  steps:
    - name: "数据收集"
      actions:
        - collect_project_metrics
        - gather_milestone_data
        - retrieve_decision_records
        - compile_issue_list
        
    - name: "偏差分析"
      actions:
        - compare_plan_vs_actual
        - identify_deviations
        - analyze_root_causes
        
    - name: "经验提取"
      actions:
        - identify_successes
        - identify_failures
        - extract_lessons
        
    - name: "报告生成"
      actions:
        - fill_template
        - calculate_metrics
        - generate_recommendations
        
    - name: "评审确认"
      actions:
        - present_to_stakeholders
        - collect_feedback
        - finalize_report
        
    - name: "归档应用"
      actions:
        - archive_report
        - update_project_plan
        - apply_lessons_learned
```

## 指标计算

### 进度指标
```javascript
function calculateScheduleAdherence(project) {
  const plannedMilestones = project.plannedMilestones;
  const actualMilestones = project.actualMilestones;
  
  let onTimeCount = 0;
  for (const milestone of plannedMilestones) {
    const actual = actualMilestones.find(m => m.id === milestone.id);
    if (actual && actual.date <= milestone.targetDate) {
      onTimeCount++;
    }
  }
  
  return (onTimeCount / plannedMilestones.length) * 100;
}
```

### 质量指标
```javascript
function calculateQualityScore(project) {
  const factors = {
    defectRate: 1 - project.defectCount / project.totalFeatures,
    testCoverage: project.testCoverage / 100,
    codeReviewPassRate: project.codeReviewPassRate,
    userAcceptanceRate: project.userAcceptanceRate
  };
  
  return weightedAverage(factors, {
    defectRate: 0.3,
    testCoverage: 0.25,
    codeReviewPassRate: 0.25,
    userAcceptanceRate: 0.2
  }) * 100;
}
```

## 复盘触发

### 自动触发
```yaml
auto_trigger:
  - condition: "milestone_completed"
    type: "milestone_review"
    
  - condition: "phase_completed"
    type: "phase_review"
    
  - condition: "project_status == 'completed'"
    type: "project_summary"
    
  - condition: "schedule: weekly"
    type: "periodic_review"
```

### 手动触发
```yaml
manual_trigger:
  allowed_roles: [owner, admin]
  reasons:
    - "重大问题发生"
    - "方向调整"
    - "用户请求"
```

## 报告存储

### 存储配置
```yaml
storage:
  path: "projects/reviews/"
  naming: "{project_id}/REV-{date}-{type}.yaml"
  retention: "project_lifetime + 1year"
  indexing:
    - project_id
    - review_type
    - review_date
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 复盘完成率 | 按时复盘/应复盘 | <90% |
| 问题闭环率 | 已解决/发现问题 | <80% |
| 经验应用率 | 已应用/提取经验 | <60% |
| 复盘质量分 | 复盘报告质量 | <70 |

## 维护方式
- 新增模板: 创建复盘模板
- 调整指标: 更新指标计算
- 新增类型: 更新复盘类型

## 引用文件
- `projects/PROJECT_SCHEMA.json` - 项目结构
- `projects/MILESTONE_POLICY.md` - 里程碑策略
- `evaluation/QUALITY_METRICS.md` - 质量指标
