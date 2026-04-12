# FALLBACK_STRATEGY.md - 回退策略

## 目的
定义系统回退策略，确保在降级、失败、异常时有明确的回退路径。

## 适用范围
所有需要回退的场景，包括技能回退、工具回退、策略回退。

## 回退层级

### 回退层级定义
| 层级 | 说明 | 触发条件 |
|------|------|----------|
| L0 | 正常执行 | 无异常 |
| L1 | 备选方案 | 主方案失败 |
| L2 | 降级方案 | 备选失败 |
| L3 | 最小方案 | 降级失败 |
| L4 | 安全模式 | 全部失败 |

## 技能回退

### 技能回退链
```yaml
skill_fallback:
  xiaoyi-web-search:
    primary: xiaoyi-web-search
    fallback_1: deep-search-and-insight-synthesize
    fallback_2: web-search-exa
    fallback_3: web-search-plus
    minimal: memory_search
  
  xiaoyi-image-understanding:
    primary: xiaoyi-image-understanding
    fallback_1: image-cog
    fallback_2: ocr-local
    minimal: basic_description
  
  xiaoyi-doc-convert:
    primary: xiaoyi-doc-convert
    fallback_1: markitdown
    fallback_2: pdf + docx
    minimal: text_extraction
```

### 技能回退流程
```
技能调用
    ↓
┌─────────────────────────────────────┐
│ 1. 尝试主技能                        │
│    - 成功 → 返回结果                 │
│    - 失败 → 继续回退                 │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 尝试备选技能                      │
│    - 成功 → 返回结果                 │
│    - 失败 → 继续回退                 │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 尝试降级方案                      │
│    - 成功 → 返回结果                 │
│    - 失败 → 继续回退                 │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 最小方案                          │
│    - 返回基础结果                    │
│    - 标注限制                        │
└─────────────────────────────────────┘
```

## 工具回退

### 工具回退链
| 工具 | 备选 | 降级 | 最小 |
|------|------|------|------|
| web_fetch | browser | memory_search | 缓存 |
| memory_search | memory_get | 直接读取 | 空结果 |
| exec | 内置命令 | 脚本 | 拒绝 |
| browser | web_fetch | 缓存 | 拒绝 |

### 工具回退规则
```yaml
tool_fallback_rules:
  on_timeout:
    action: fallback
    max_retries: 2
  
  on_error:
    action: fallback
    log_error: true
  
  on_permission_denied:
    action: reject
    notify_user: true
  
  on_not_found:
    action: fallback
    try_alternative: true
```

## 策略回退

### 策略回退场景
| 场景 | 主策略 | 回退策略 |
|------|--------|----------|
| 复杂规划 | 详细规划 | 简化规划 |
| 并行执行 | 并行 | 顺序 |
| 深度分析 | 深度 | 浅层 |
| 多步任务 | 多步 | 单步 |

### 策略回退配置
```yaml
strategy_fallback:
  planning:
    complex:
      fallback: simple
      trigger: planning_timeout
  
  execution:
    parallel:
      fallback: sequential
      trigger: resource_constraint
  
  analysis:
    deep:
      fallback: shallow
      trigger: time_constraint
```

## 数据回退

### 数据源回退
| 主数据源 | 备选数据源 | 降级数据源 |
|----------|------------|------------|
| 外部API | 内部缓存 | 默认值 |
| 实时数据 | 近期数据 | 历史数据 |
| 详细数据 | 摘要数据 | 元数据 |

### 数据回退规则
```yaml
data_fallback:
  on_unavailable:
    - try_cache
    - try_backup
    - use_default
  
  on_stale:
    - use_with_warning
    - try_refresh
    - use_cached
```

## 回退日志

### 日志格式
```json
{
  "fallbackId": "fb_001",
  "timestamp": "2026-04-06T10:32:00+08:00",
  "type": "skill_fallback",
  "original": {
    "name": "xiaoyi-web-search",
    "error": "timeout"
  },
  "fallback": {
    "name": "deep-search",
    "result": "success"
  },
  "level": 1
}
```

## 回退统计

### 统计指标
| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| 回退触发率 | 回退次数/总调用 | > 20% |
| L1回退成功率 | L1成功/L1触发 | < 80% |
| 最终失败率 | 全部失败/总调用 | > 5% |
| 平均回退层级 | 平均回退深度 | > 2 |

## 异常处理

| 异常 | 处理 |
|------|------|
| 回退链为空 | 进入安全模式 |
| 所有回退失败 | 返回错误 + 建议 |
| 回退循环 | 终止 + 记录 |

## 维护方式
- 新增回退链: 添加到技能/工具配置
- 调整回退顺序: 更新回退链配置
- 新增回退场景: 添加到回退场景表

## 引用文件
- `runtime/FAILOVER.md` - 故障恢复
- `runtime/DEGRADATION_RULES.md` - 降级规则
- `runtime/EXECUTION_POLICY.md` - 执行策略
