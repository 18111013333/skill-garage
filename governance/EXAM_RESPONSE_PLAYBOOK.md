# EXAM_RESPONSE_PLAYBOOK.md - 监管检查响应手册

## 目的
定义面对监管检查/客户深审时的响应手册，确保有标准流程，不慌乱。

## 适用范围
- 监管机构检查
- 审计机构审计
- 大客户深审
- 第三方评估

## 响应流程

```
┌─────────────────────────────────────────────────────────────┐
│                    监管检查响应流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  收到请求 → 受理登记 → 角色分工 → 资料收集 → 内部审核 → 对外答复 │
│     ↓          ↓          ↓          ↓          ↓          ↓ │
│  验证身份    创建工单    指定负责人   按清单准备  合规审核    正式回复 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 1. 资料收集

```yaml
document_collection:
  # 标准资料清单
  standard_checklist:
    governance:
      - AI 治理政策文件
      - 风险评估报告
      - 用例审批记录
      - 培训记录
    
    compliance:
      - 合规政策文件
      - 合规评估报告
      - 整改记录
      - 审计报告
    
    security:
      - 安全政策文件
      - 安全评估报告
      - 漏洞扫描报告
      - 事件处理记录
    
    privacy:
      - 隐私政策文件
      - 数据处理记录
      - 同意管理记录
      - 隐私影响评估
    
    operations:
      - 系统架构文档
      - 变更管理记录
      - 监控报告
      - 备份恢复记录
  
  # 资料准备时限
  timeline:
    standard: "5 个工作日"
    urgent: "2 个工作日"
    emergency: "24 小时"
```

## 2. 角色分工

```yaml
role_assignment:
  # 总协调人
  coordinator:
    role: "合规负责人"
    responsibility:
      - 统筹协调
      - 进度跟踪
      - 质量把关
      - 对外沟通
  
  # 资料负责人
  document_owner:
    governance: "AI 治理官"
    compliance: "合规负责人"
    security: "安全负责人"
    privacy: "隐私负责人"
    operations: "运维负责人"
  
  # 审核负责人
  reviewer:
    legal: "法务负责人"
    compliance: "合规负责人"
    security: "安全负责人"
  
  # 对外接口人
  spokesperson:
    primary: "合规负责人"
    backup: "管理层代表"
```

## 3. 响应时限

```yaml
response_timeline:
  # 请求确认
  acknowledgment:
    standard: "1 个工作日"
    urgent: "4 小时"
  
  # 初步响应
  initial_response:
    standard: "3 个工作日"
    urgent: "1 个工作日"
  
  # 完整响应
  full_response:
    standard: "10 个工作日"
    urgent: "5 个工作日"
  
  # 补充材料
  supplementary:
    standard: "5 个工作日"
    urgent: "2 个工作日"
```

## 4. 升级机制

```yaml
escalation:
  # 升级触发条件
  triggers:
    - 请求超出常规范围
    - 涉及敏感信息
    - 时限无法满足
    - 内部意见分歧
    - 潜在法律风险
  
  # 升级路径
  path:
    level_1:
      to: "部门负责人"
      condition: "常规问题"
    
    level_2:
      to: "合规负责人"
      condition: "合规风险"
    
    level_3:
      to: "管理层"
      condition: "重大风险"
    
    level_4:
      to: "法务"
      condition: "法律风险"
  
  # 升级时限
  timeline:
    assessment: "4 小时"
    decision: "8 小时"
    action: "24 小时"
```

## 5. 对外答复口径

```yaml
communication_guidelines:
  # 答复原则
  principles:
    - 准确：基于事实和数据
    - 一致：口径统一
    - 适度：不主动扩大范围
    - 专业：使用规范术语
    - 谨慎：敏感信息需审批
  
  # 答复模板
  templates:
    acknowledgment: |
      尊敬的[机构名称]：
      
      我方已收到贵方于[日期]提出的[请求类型]请求。
      
      我方高度重视，已指定[负责人]负责此事，预计于[日期]前提供完整响应。
      
      如有任何问题，请联系[联系人]。
    
    full_response: |
      尊敬的[机构名称]：
      
      关于贵方[日期]提出的[请求类型]请求，现回复如下：
      
      1. [问题1]：[答复内容]
      2. [问题2]：[答复内容]
      ...
      
      相关证明材料请见附件。
      
      如需进一步信息，请联系[联系人]。
  
  # 敏感信息处理
  sensitive_handling:
    - 标记敏感内容
    - 法务审核
    - 管理层批准
    - 限制分发范围
```

## 6. 检查后跟进

```yaml
follow_up:
  # 问题整改
  remediation:
    - 记录检查发现
    - 制定整改计划
    - 分配整改责任
    - 跟踪整改进度
    - 验证整改效果
    - 报告整改结果
  
  # 经验总结
  lessons_learned:
    - 分析检查过程
    - 识别改进点
    - 更新响应手册
    - 组织培训分享
  
  # 关系维护
  relationship:
    - 感谢检查方
    - 保持沟通渠道
    - 主动报告改进
    - 建立长期信任
```

## 异常处理

### 请求超出范围
- 明确超出部分
- 说明无法提供原因
- 提供替代方案
- 记录沟通过程

### 时限无法满足
- 提前通知检查方
- 说明延迟原因
- 提供分阶段响应
- 争取额外时间

### 内部意见分歧
- 记录分歧点
- 升级决策
- 统一口径
- 对外一致

## 完成标准
- [x] 资料收集清单完整
- [x] 角色分工明确
- [x] 响应时限清晰
- [x] 升级机制完整
- [x] 对外答复口径规范
- [x] 检查后跟进规则清晰
- [x] 面对正式检查时有标准流程

## 版本
- 版本: 1.0.0
- 更新时间: 2026-04-07
