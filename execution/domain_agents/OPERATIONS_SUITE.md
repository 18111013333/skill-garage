# OPERATIONS_SUITE.md - 运营/项目推进agent套件

## 目的
定义运营/项目推进类agent套件，形成高效率打法。

## 适用范围
所有运营和项目管理相关任务。

## 套件配置

```yaml
operations_suite:
  suite_id: "SUITE-operations"
  name: "运营项目推进套件"
  domain: "domain_operations"
  
  compliance_level: standard
  citation_mode: moderate
  
  linked_modules:
    - projects/
    - portfolio/
    - resources/
```

## 核心能力

### SOP生成
```yaml
capability_sop_generation:
  capability_id: "ops_sop_gen"
  name: "SOP生成"
  description: "生成标准操作流程"
  
  features:
    - 流程步骤拆解
    - 责任人分配
    - 时间节点设定
    - 检查点设置
    
  output:
    - SOP文档
    - 流程图
    - 检查清单
    
  integration:
    - 可关联项目里程碑
    - 可导入任务系统
```

### 项目节奏跟进
```yaml
capability_project_tracking:
  capability_id: "ops_project_track"
  name: "项目节奏跟进"
  description: "跟踪项目进度和节奏"
  
  features:
    - 进度监控
    - 偏差分析
    - 预警提示
    - 进度报告
    
  output:
    - 进度报告
    - 偏差分析
    - 预警通知
    
  integration:
    - 读取项目状态
    - 更新项目进度
    - 触发项目告警
```

### 待办拆解
```yaml
capability_task_breakdown:
  capability_id: "ops_task_break"
  name: "待办拆解"
  description: "将目标拆解为可执行任务"
  
  features:
    - 任务拆分
    - 优先级排序
    - 依赖分析
    - 资源匹配
    
  output:
    - 任务列表
    - 依赖关系图
    - 资源需求
    
  integration:
    - 创建项目任务
    - 关联项目里程碑
```

### 复盘分析
```yaml
capability_review:
  capability_id: "ops_review"
  name: "复盘分析"
  description: "项目或阶段复盘"
  
  features:
    - 数据收集
    - 偏差分析
    - 经验提取
    - 改进建议
    
  output:
    - 复盘报告
    - 经验总结
    - 改进建议
    
  integration:
    - 读取项目历史
    - 更新项目记录
    - 关联项目复盘模板
```

### 跨团队协作建议
```yaml
capability_collaboration:
  capability_id: "ops_collab"
  name: "跨团队协作建议"
  description: "提供协作优化建议"
  
  features:
    - 协作模式分析
    - 沟通优化建议
    - 流程改进建议
    
  output:
    - 协作建议
    - 流程优化方案
```

### 异常升级建议
```yaml
capability_escalation:
  capability_id: "ops_escalation"
  name: "异常升级建议"
  description: "识别异常并建议升级"
  
  features:
    - 异常检测
    - 影响评估
    - 升级建议
    
  output:
    - 异常报告
    - 升级建议
    - 处理方案
    
  integration:
    - 触发项目告警
    - 通知相关人员
```

## 模块联动

### 与projects模块联动
```yaml
projects_integration:
  read:
    - 项目状态
    - 里程碑信息
    - 任务列表
    
  write:
    - 更新进度
    - 创建任务
    - 记录复盘
    
  triggers:
    - 项目状态变更
    - 里程碑完成
    - 任务状态更新
```

### 与portfolio模块联动
```yaml
portfolio_integration:
  read:
    - 组合状态
    - 项目优先级
    - 资源分配
    
  write:
    - 进度报告
    - 风险更新
    
  triggers:
    - 组合复盘触发
    - 优先级调整
```

### 与resources模块联动
```yaml
resources_integration:
  read:
    - 资源状态
    - 资源可用性
    
  actions:
    - 资源申请
    - 资源释放
    
  triggers:
    - 资源紧张预警
```

## 工作模式

### 日常运营模式
```yaml
daily_operations:
  schedule:
    - 09:00: 检查项目状态
    - 12:00: 进度汇总
    - 18:00: 日报生成
    
  automation:
    - 自动进度跟踪
    - 自动预警检测
    - 自动报告生成
```

### 项目启动模式
```yaml
project_startup:
  steps:
    - 项目信息收集
    - SOP生成
    - 任务拆解
    - 资源规划
    - 启动检查
```

### 项目复盘模式
```yaml
project_review:
  steps:
    - 数据收集
    - 偏差分析
    - 经验提取
    - 报告生成
    - 改进跟踪
```

## 输出模板

### 进度报告模板
```yaml
progress_report:
  project_id: "PROJ-001"
  report_date: "2024-01-15"
  
  summary:
    overall_progress: 65%
    status: on_track
    
  milestones:
    - milestone: "M1"
      status: completed
    - milestone: "M2"
      status: in_progress
      progress: 80%
      
  risks:
    - risk: "资源紧张"
      level: medium
      
  next_actions:
    - action: "完成M2"
      due: "2024-01-20"
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 任务完成率 | 完成/计划 | <80% |
| 报告及时率 | 及时/应生成 | <90% |
| 预警准确率 | 准确/预警 | <70% |
| 协作满意度 | 用户反馈 | <80% |

## 维护方式
- 新增能力: 创建能力定义
- 调整联动: 更新模块联动
- 新增模板: 创建输出模板

## 引用文件
- `domain_agents/DOMAIN_REGISTRY.json` - 领域注册表
- `projects/PROJECT_SCHEMA.json` - 项目结构
- `portfolio/PORTFOLIO_SCHEMA.json` - 组合结构
