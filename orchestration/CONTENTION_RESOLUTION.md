# CONTENTION_RESOLUTION.md - 资源争用冲突解决

## 目的
定义资源争用冲突解决规则，确保冲突时有统一裁决。

## 适用范围
所有资源争用和冲突场景。

## 争用场景

| 场景 | 说明 | 典型案例 |
|------|------|----------|
| 同时申请 | 多方同时申请同一资源 | 多项目同时申请API配额 |
| 配额超限 | 总需求超过可用配额 | 资源总量不足 |
| 优先级冲突 | 同优先级项目竞争 | 两个P1项目争抢 |
| 预留冲突 | 预留资源被请求 | 预留资源被紧急请求 |
| 时间冲突 | 时间窗口重叠 | 同一时段资源需求 |

## 仲裁维度

| 维度 | 权重 | 说明 | 评分范围 |
|------|------|------|----------|
| 项目优先级 | 30% | 项目整体优先级 | 1-100 |
| 任务风险 | 20% | 任务风险等级 | 1-100 |
| 截止时间 | 20% | 时间紧迫程度 | 1-100 |
| 预留配额 | 15% | 是否有预留 | 0/100 |
| 最小可交付 | 15% | 最小保障需求 | 1-100 |

## 仲裁流程

```
争用检测
    ↓
┌─────────────────────────────────────┐
│ 1. 争用识别                          │
│    - 识别争用方                      │
│    - 评估争用资源                    │
│    - 确定争用类型                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 评分计算                          │
│    - 计算各方得分                    │
│    - 考虑历史因素                    │
│    - 应用调整因子                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 裁决决策                          │
│    - 比较得分                        │
│    - 应用特殊规则                    │
│    - 生成裁决结果                    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 执行裁决                          │
│    - 分配资源给胜出方                │
│    - 通知其他方                      │
│    - 记录裁决日志                    │
└─────────────────────────────────────┘
```

## 仲裁规则

### 基础仲裁
```javascript
function arbitrateContention(contenders, resource) {
  const scores = [];
  
  for (const contender of contenders) {
    let score = 0;
    
    // 项目优先级
    score += contender.projectPriority * 0.30;
    
    // 任务风险
    score += scoreRisk(contender.task) * 0.20;
    
    // 截止时间
    score += scoreDeadline(contender.deadline) * 0.20;
    
    // 预留配额
    if (contender.hasReservation) {
      score += 100 * 0.15;
    }
    
    // 最小可交付保障
    score += scoreMinDelivery(contender) * 0.15;
    
    scores.push({ contender, score });
  }
  
  // 排序
  scores.sort((a, b) => b.score - a.score);
  
  return {
    winner: scores[0].contender,
    scores: scores,
    reasoning: generateReasoning(scores)
  };
}
```

### 特殊规则

#### 紧急优先
```yaml
emergency_priority:
  condition: "contender.isEmergency == true"
  action: "grant_immediately"
  override_priority: 100
  requires_approval: true
```

#### 预留保护
```yaml
reservation_protection:
  condition: "contender.hasReservation == true"
  action: "honor_reservation"
  exception:
    - emergency_override
    - reservation_expired
```

#### 公平轮转
```yaml
fair_rotation:
  condition: "scores_difference < 5"
  action: "rotate_among_contenders"
  rotation_interval: "1h"
```

## 冲突类型处理

### 同时申请
```yaml
simultaneous_request:
  detection:
    - requests_within: "1s"
    - same_resource: true
    
  resolution:
    - calculate_scores
    - award_to_highest
    - queue_others
    
  notification:
    - notify_winner
    - notify_queued
    - provide_eta
```

### 配额超限
```yaml
quota_exceeded:
  detection:
    - total_demand > available
    
  resolution:
    - prioritize_by_score
    - allocate_proportionally
    - defer_low_priority
    
  alternatives:
    - request_additional_quota
    - enable_burst_capacity
    - schedule_for_later
```

### 同优先级冲突
```yaml
same_priority_conflict:
  detection:
    - priority_equal: true
    
  resolution_order:
    - earlier_deadline_first
    - smaller_request_first
    - earlier_created_first
    - fair_rotation
```

## 最小可交付保障

### 保障规则
```yaml
min_delivery_guarantee:
  principle: "每个项目获得最小资源保障"
  
  calculation:
    - total_available: "resource.capacity"
    - active_projects: "count(active)"
    - min_per_project: "total_available * 0.1"
    
  enforcement:
    - never_preempt_min_allocation
    - always_reserve_min_capacity
```

### 保障实现
```yaml
guarantee_implementation:
  reserved_pool:
    - size: "total * 0.2"
    - purpose: "minimum_guarantee"
    - allocation: "per_project_min"
    
  protection:
    - no_preemption: true
    - no_reallocation: true
```

## 裁决记录

### 记录内容
```yaml
arbitration_record:
  arbitration_id: "ARB-001"
  timestamp: "2024-01-15T10:00:00Z"
  
  contenders:
    - project_id: "PROJ-001"
      score: 85
      outcome: "winner"
    - project_id: "PROJ-002"
      score: 72
      outcome: "queued"
      
  resource:
    resource_id: "RES-001"
    amount_requested: 100
    amount_awarded: 100
    
  reasoning:
    - "PROJ-001优先级更高"
    - "PROJ-001截止时间更紧迫"
    
  appeals:
    allowed: true
    deadline: "24h"
```

## 申诉机制

### 申诉流程
```yaml
appeal_process:
  allowed_within: "24h"
  
  grounds:
    - scoring_error
    - new_information
    - special_circumstances
    
  process:
    - submit_appeal
    - admin_review
    - final_decision
    
  outcomes:
    - uphold_original
    - modify_decision
    - emergency_override
```

## 监控指标

| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 争用频率 | 争用次数/小时 | >10 |
| 仲裁延迟 | 仲裁耗时 | >5s |
| 申诉率 | 申诉/裁决 | >5% |
| 公平性评分 | 轮转公平度 | <80 |

## 维护方式
- 调整权重: 更新仲裁维度权重
- 新增规则: 创建特殊规则
- 优化算法: 更新评分算法

## 引用文件
- `resources/RESOURCE_SCHEMA.json` - 资源结构
- `resources/ALLOCATION_POLICY.md` - 分配策略
- `portfolio/PRIORITIZATION_POLICY.md` - 优先级策略
