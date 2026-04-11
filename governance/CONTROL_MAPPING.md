# CONTROL_MAPPING.md - 控制映射关系

## 目的
定义控制项与模块/风险/流程的映射关系。

## 适用范围
- 所有控制措施
- 所有系统模块
- 所有风险项

## 控制类型

```yaml
control_types:
  preventive:
    description: "预防型控制"
    purpose: "阻止风险发生"
    examples:
      - 访问控制
      - 输入验证
      - 权限分离
  
  detective:
    description: "检测型控制"
    purpose: "发现已发生问题"
    examples:
      - 日志监控
      - 异常检测
      - 定期审计
  
  corrective:
    description: "纠正型控制"
    purpose: "纠正已发现问题"
    examples:
      - 事件响应
      - 问题整改
      - 系统恢复
```

## 模块-控制映射

| 模块 | 关键控制 | 控制类型 | 覆盖风险 |
|------|----------|----------|----------|
| ai_governance | 用例审批 | 预防 | 合规风险 |
| ai_governance | 人工复核 | 预防 | 决策风险 |
| ai_governance | 性能监控 | 检测 | 运营风险 |
| controls | 职责分离 | 预防 | 欺诈风险 |
| controls | 控制测试 | 检测 | 控制失效 |
| data_governance | 数据分类 | 预防 | 数据泄露 |
| data_governance | 访问控制 | 预防 | 未授权访问 |
| privacy | 同意管理 | 预防 | 隐私违规 |
| privacy | DSAR 流程 | 纠正 | 合规风险 |
| security | 身份认证 | 预防 | 未授权访问 |
| security | 加密存储 | 预防 | 数据泄露 |
| security | 入侵检测 | 检测 | 攻击风险 |
| audit | 操作日志 | 检测 | 审计风险 |
| audit | 定期审计 | 检测 | 合规风险 |

## 风险-控制映射

```yaml
risk_control_mapping:
  data_breach:
    description: "数据泄露风险"
    controls:
      - C-001: 数据分类标记
      - C-002: 访问控制
      - C-003: 加密存储
      - C-004: 数据脱敏
      - C-005: 访问日志
  
  unauthorized_access:
    description: "未授权访问风险"
    controls:
      - C-006: 身份认证
      - C-007: 权限管理
      - C-008: 职责分离
      - C-009: 访问审批
  
  compliance_violation:
    description: "合规违规风险"
    controls:
      - C-010: 用例审批
      - C-011: 合规检查
      - C-012: 定期审计
      - C-013: 整改跟踪
  
  ai_decision_error:
    description: "AI 决策错误风险"
    controls:
      - C-014: 模型验证
      - C-015: 人工复核
      - C-016: 输出验证
      - C-017: 异常告警
```

## 流程-控制映射

```yaml
process_control_mapping:
  user_onboarding:
    controls:
      - 身份验证
      - 权限分配
      - 培训完成确认
  
  data_access:
    controls:
      - 访问申请
      - 权限审批
      - 访问日志
      - 定期审查
  
  ai_use_case_launch:
    controls:
      - 风险评估
      - 安全评审
      - 合规审批
      - 上线验证
  
  incident_response:
    controls:
      - 事件检测
      - 分级响应
      - 根因分析
      - 整改跟踪
```

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
