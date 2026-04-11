# WORKFLOW.md - 智能工作流系统

## 目的
实现自动化流程编排，让复杂任务一键执行。

## 核心能力

### 1. 可视化设计
- 拖拽式流程设计
- 实时预览
- 模板库

### 2. 条件分支
- 智能条件判断
- 多分支支持
- 嵌套逻辑

### 3. 循环执行
- 批量任务处理
- 迭代器支持
- 并行循环

### 4. 错误处理
- 自动重试
- 异常捕获
- 回滚机制

### 5. 定时调度
- Cron 表达式
- 时区支持
- 节假日处理

## 内置模板

| 模板 | 描述 |
|------|------|
| daily_report | 每日报告生成 |
| data_pipeline | 数据处理流水线 |
| notification_chain | 通知链 |
| approval_flow | 审批流程 |

## 使用示例

```bash
# 创建工作流
openclaw workflow create "每日报告"

# 添加步骤
openclaw workflow add "每日报告" --step "获取数据"
openclaw workflow add "每日报告" --step "生成报告"
openclaw workflow add "每日报告" --step "发送邮件"

# 执行工作流
openclaw workflow run "每日报告"

# 定时执行
openclaw workflow schedule "每日报告" --cron "0 9 * * *"
```

---
*V13.0 智能工作流系统*
