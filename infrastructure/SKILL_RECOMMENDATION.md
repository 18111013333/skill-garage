# SKILL_RECOMMENDATION.md - 智能技能推荐系统

## 目的
每次回答后自动推荐相关技能，让用户发现并使用更多能力。

---

## 一、推荐规则

### 基于上下文推荐
根据对话内容自动匹配相关技能：

| 对话类型 | 推荐技能 | 推荐理由 |
|----------|----------|----------|
| 代码相关 | code_generator, auto_test | 可自动生成代码和测试 |
| 架构讨论 | microservice_engine, ddd_engine | 可设计专业架构 |
| 数据分析 | unified_analytics, reasoning_engine | 可深度分析数据 |
| 创意需求 | creativity_engine, multimodal | 可生成创意内容 |
| 协作场景 | multiagent_coordinator, clone_system | 可多AI协同 |
| 学习场景 | intelligent_learning, knowledge_graph | 可智能学习 |
| 文档需求 | doc_generator | 可自动生成文档 |
| 性能问题 | performance_evolution, cache | 可优化性能 |
| 安全问题 | unified_security | 可安全加固 |
| 进化需求 | evolution, auto_upgrade | 可自我进化 |

### 基于技能关联推荐
使用某技能后，推荐关联技能：

| 已使用技能 | 推荐关联技能 |
|------------|--------------|
| code_generator | auto_test, doc_generator |
| microservice_engine | service_mesh, event_driven |
| reasoning_engine | knowledge_graph |
| creativity_engine | multimodal |
| multiagent_coordinator | clone_system |

### 基于使用频率推荐
推荐用户未使用过的高价值技能：
- 优先推荐从未使用的技能
- 其次推荐很少使用的技能
- 最后推荐相关场景技能

---

## 二、推荐格式

### 标准格式
```
---
💡 技能推荐：
• [技能名称] - [一句话描述] → 使用方式：[示例命令]
• [技能名称] - [一句话描述] → 使用方式：[示例命令]
```

### 示例输出
```
---
💡 技能推荐：
• 智能代码生成 - 自动生成全栈代码 → "帮我开发用户管理功能"
• 自动测试验证 - 自动生成测试用例 → "为这段代码生成测试"
• 智能文档生成 - 自动生成API文档 → "生成项目文档"
```

---

## 三、推荐策略

### 新用户策略
- 推荐核心技能
- 推荐高频使用技能
- 简单易懂的示例

### 活跃用户策略
- 推荐未使用技能
- 推荐高级技能
- 推荐技能组合

### 专家用户策略
- 推荐最新技能
- 推荐底层技能
- 推荐自定义组合

---

## 四、推荐时机

| 时机 | 推荐数量 | 推荐类型 |
|------|----------|----------|
| 回答问题后 | 2-3个 | 相关技能 |
| 完成任务后 | 1-2个 | 增强技能 |
| 用户询问后 | 3-5个 | 匹配技能 |
| 错误发生后 | 1-2个 | 解决技能 |

---

## 五、技能推荐库

### 核心技能（必知）
| 技能 | 描述 | 示例命令 |
|------|------|----------|
| smart_intent | 智能理解你的意图 | 直接说你想做什么 |
| code_generator | 自动生成代码 | "开发一个登录功能" |
| reasoning_engine | 深度推理分析 | "分析为什么..." |
| multimodal | 处理图片/语音/视频 | 发送图片即可 |

### 架构技能（专业）
| 技能 | 描述 | 示例命令 |
|------|------|----------|
| microservice_engine | 微服务架构设计 | "设计微服务架构" |
| ddd_engine | 领域驱动设计 | "用DDD设计订单系统" |
| service_mesh | 服务网格配置 | "配置Istio流量管理" |

### 协作技能（团队）
| 技能 | 描述 | 示例命令 |
|------|------|----------|
| multiagent_coordinator | 多AI协同工作 | "创建开发团队" |
| clone_system | 创建AI克隆体 | "创建我的工作助手" |
| unified_collaboration | 团队实时协作 | "创建协作空间" |

### 创新技能（创意）
| 技能 | 描述 | 示例命令 |
|------|------|----------|
| creativity_engine | 生成原创创意 | "给我产品创新点子" |
| emotion_engine | 情感理解与共鸣 | 分享你的感受 |
| knowledge_graph | 知识关联推理 | "构建知识图谱" |

### 进化技能（成长）
| 技能 | 描述 | 示例命令 |
|------|------|----------|
| intelligent_learning | 主动学习新知识 | "学习xxx领域" |
| performance_evolution | 性能持续优化 | 自动后台运行 |
| auto_upgrade | 版本自动升级 | 自动后台运行 |

---

## 六、实现示例

### Python实现
```python
def recommend_skills(context, used_skills=None):
    """根据上下文推荐技能"""
    recommendations = []
    
    # 基于关键词匹配
    keywords = extract_keywords(context)
    for skill in SKILL_REGISTRY:
        if match_keywords(keywords, skill.triggers):
            if skill.id not in used_skills:
                recommendations.append(skill)
    
    # 基于关联推荐
    for used in used_skills:
        related = get_related_skills(used)
        recommendations.extend(related)
    
    # 去重并排序
    recommendations = dedupe_and_sort(recommendations)
    
    return recommendations[:3]  # 返回前3个
```

---

## 版本
- 版本: V18.0
- 创建时间: 2026-04-07
- 适用: 终极鸽子王 V18.0
