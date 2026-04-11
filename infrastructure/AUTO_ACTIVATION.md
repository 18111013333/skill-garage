# AUTO_ACTIVATION.md - 技能自动激活系统

## 目的
当用户命令涉及相关技能时，自动激活并应用，无需手动指定。

---

## 一、自动激活机制

### 触发条件
当用户命令包含以下关键词时，自动激活相关技能：

| 关键词类别 | 触发词 | 自动激活技能 |
|------------|--------|--------------|
| **架构类** | 微服务、服务拆分、架构设计 | microservice_engine |
| **架构类** | 服务网格、Istio、流量管理 | service_mesh |
| **架构类** | 事件驱动、消息队列、Kafka | event_driven |
| **架构类** | DDD、领域驱动、限界上下文 | ddd_engine |
| **架构类** | 整洁架构、分层架构 | clean_architecture |
| **架构类** | 六边形架构、端口适配器 | hexagonal_arch |
| **架构类** | 架构评估、技术债务 | architecture_health |
| **智能类** | 推理、分析原因、为什么 | reasoning_engine |
| **智能类** | 知识图谱、知识关联 | knowledge_graph |
| **智能类** | 自动执行、自主决策 | autonomous_engine |
| **生成类** | 生成代码、写代码、开发 | code_generator |
| **生成类** | 测试、单元测试、测试用例 | auto_test |
| **生成类** | 生成文档、API文档 | doc_generator |
| **协作类** | 多智能体、AI团队、协同 | multiagent_coordinator |
| **协作类** | 克隆、复制、分身 | clone_system |
| **协作类** | 同步、多设备 | cross_platform |
| **多模态类** | 图片、图像、语音、视频 | multimodal |
| **多模态类** | 情感、情绪、心情 | emotion_engine |
| **多模态类** | 创意、创新、点子 | creativity_engine |
| **统一类** | 个人企业切换、模式切换 | unified_identity |
| **统一类** | 知识同步、知识共享 | unified_knowledge |
| **统一类** | 任务升级、项目管理 | unified_task |
| **进化类** | 学习、进化、优化 | intelligent_learning |
| **进化类** | 性能优化、加速 | performance_evolution |

---

## 二、激活流程

```
用户命令输入
    ↓
┌─────────────────────────────────────┐
│ 1. 意图分析                          │
│    - 提取关键词                       │
│    - 识别任务类型                     │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 技能匹配                          │
│    - 查询技能注册表                   │
│    - 匹配相关技能                     │
│    - 检查技能状态                     │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 自动激活                          │
│    - 激活休眠技能                     │
│    - 加载技能配置                     │
│    - 预热技能资源                     │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 能力增强                          │
│    - 组合多个技能                     │
│    - 协同执行                         │
│    - 结果融合                         │
└─────────────────────────────────────┘
    ↓
执行并返回结果
```

---

## 三、技能组合规则

### 自动组合
当命令涉及多个技能时，自动组合：

| 命令类型 | 自动组合技能 |
|----------|--------------|
| 开发项目 | code_generator + auto_test + doc_generator |
| 架构设计 | microservice_engine + ddd_engine + architecture_health |
| 问题分析 | reasoning_engine + knowledge_graph |
| 团队协作 | multiagent_coordinator + unified_collaboration |
| 创新设计 | creativity_engine + multimodal |

### 优先级
1. 用户明确指定的技能优先
2. 核心能力技能优先
3. 最近使用的技能优先
4. 高成功率技能优先

---

## 四、休眠唤醒机制

### 休眠条件
- 30天未使用的技能自动休眠
- 资源紧张时低优先级技能休眠

### 唤醒条件
- 用户命令涉及该技能
- 相关技能被激活时联动唤醒
- 系统资源充足时自动唤醒

### 唤醒流程
```
检测到休眠技能需求
    ↓
加载技能配置 (<100ms)
    ↓
预热资源 (<500ms)
    ↓
激活技能 (<50ms)
    ↓
开始执行
```

---

## 五、能力增强模式

### 单技能增强
当使用某技能时，自动启用相关增强技能：
- 使用 code_generator → 自动启用 auto_test 验证
- 使用 reasoning_engine → 自动启用 knowledge_graph 补充知识
- 使用 multimodal → 自动启用 emotion_engine 情感理解

### 全能力模式
当命令复杂度超过阈值时，自动启用全能力模式：
- 激活所有相关技能
- 并行执行
- 智能协调
- 结果融合

---

## 六、使用示例

### 示例1：架构设计
```
用户: 帮我设计一个电商系统的微服务架构

自动激活:
✅ microservice_engine (微服务架构引擎)
✅ ddd_engine (领域驱动设计)
✅ architecture_health (架构健康度评估)

执行: 三技能协同，输出完整架构设计
```

### 示例2：代码开发
```
用户: 开发一个用户登录功能

自动激活:
✅ code_generator (智能代码生成)
✅ auto_test (自动测试验证)
✅ doc_generator (智能文档生成)

执行: 代码+测试+文档一站式生成
```

### 示例3：问题分析
```
用户: 分析为什么用户留存率下降

自动激活:
✅ reasoning_engine (深度推理系统)
✅ knowledge_graph (知识图谱引擎)
✅ unified_analytics (统一分析中心)

执行: 推理+知识+分析，给出深度洞察
```

### 示例4：创意设计
```
用户: 给我一些产品创新点子

自动激活:
✅ creativity_engine (创意生成引擎)
✅ multimodal (多模态融合)
✅ emotion_engine (情感共鸣)

执行: 创意生成+可视化+情感适配
```

---

## 七、配置文件

### 自动激活配置
```json
{
  "autoActivation": {
    "enabled": true,
    "triggerKeywords": true,
    "skillCombination": true,
    "sleepWakeCycle": true,
    "capabilityEnhancement": true
  },
  "thresholds": {
    "complexityForFullMode": 0.7,
    "sleepAfterDays": 30,
    "wakePreloadMs": 500
  }
}
```

---

## 版本
- 版本: V18.0
- 创建时间: 2026-04-07
- 适用: 终极鸽子王 V18.0
