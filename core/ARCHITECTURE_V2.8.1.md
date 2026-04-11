# 小艺 Claw 终极星空鸽子王 - 完整架构 V2.8.1

## 架构概览

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        小艺 Claw 终极星空鸽子王 V2.8.1                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  L6: infrastructure - 基础设施与运维层                                       │
│  ├── path_resolver.py          # 统一路径解析                                │
│  ├── architecture_integrity_check.py  # 架构完整性检查                       │
│  ├── plugin_standard.py        # 插件标准（安全加固）                         │
│  ├── inventory/                # 技能注册表                                  │
│  ├── optimization/             # 性能优化                                    │
│  └── integration/              # 集成模块                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  L5: governance - 稳定性与治理层                                             │
│  ├── security/                 # 安全模块                                    │
│  │   ├── secret-vault/         # 密钥保险库                                  │
│  │   └── vmp-protect/          # VMP代码保护                                 │
│  ├── config/                   # 配置管理                                    │
│  │   └── permission_center.py  # 权限中心                                    │
│  └── compliance/               # 合规管理                                    │
│      └── trust_center.py       # 合规与信任中心                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  L4: execution - 能力执行层                                                  │
│  ├── skill_adapter_gateway.py  # 技能接入网关                                │
│  ├── skill_health_check.py     # 技能健康检查                                │
│  ├── capability_report.py      # 能力激活报告                                │
│  ├── result_validator.py       # 结果验证器                                  │
│  ├── task_quality.py           # 任务质量评估                                │
│  ├── product_center.py         # 产物中心                                    │
│  ├── task_reviewer.py          # 任务复盘器                                  │
│  ├── metrics_center.py         # 任务指标中心                                │
│  ├── feedback_learning.py      # 反馈学习闭环                                │
│  ├── workflow_ranker.py        # 工作流优选器                                │
│  └── guided_autonomy.py        # 可控半自动推进                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  L3: orchestration - 任务编排层                                              │
│  ├── router/                   # 路由器                                      │
│  │   └── SKILL_ROUTER.json     # 技能路由表                                  │
│  ├── workflows/                # 工作流包                                    │
│  │   ├── workflow_base.py      # 工作流基类                                  │
│  │   ├── ecommerce_product_analysis.py  # 电商选品分析                       │
│  │   ├── factory_comparison.py # 工厂筛选比价                                │
│  │   ├── partner_selection.py  # 主播/团长筛选                               │
│  │   ├── store_launch.py       # 店铺启动                                    │
│  │   ├── file_organization.py  # 文件整理                                    │
│  │   └── code_audit.py         # 代码审计                                    │
│  ├── project_state_machine.py  # 项目状态机                                  │
│  ├── goal_tracker.py           # 目标追踪器                                  │
│  └── multi_project_scheduler.py # 多项目调度器                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  L2: memory_context - 记忆与上下文层                                         │
│  ├── memory_quality.py         # 记忆质量治理                                │
│  ├── memory_summarizer.py      # 记忆总结器                                  │
│  ├── vector/                   # 向量存储                                    │
│  └── projects/                 # 项目记忆                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  L1: core - 核心认知层                                                       │
│  ├── ARCHITECTURE.md           # 架构唯一真源                                │
│  ├── LAYER_INTERFACES.md       # 层间接口                                    │
│  ├── DATA_FLOW.md              # 数据流程                                    │
│  ├── dynamic_prompt.py         # 动态提示词（安全加固）                       │
│  ├── prompt_integration.py     # 提示词集成                                  │
│  ├── layer_bridge/             # 层间桥接                                    │
│  └── guide/                    # 引导模块（每次对话加载）                     │
│      ├── assistant_guide.py    # 完整引导模块                                │
│      ├── bootstrap.py          # 启动脚本                                    │
│      └── guide_config.json     # 配置文件                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 扩展层架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              扩展层架构                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  E7: strategy - 战略目标层                                                   │
│  └── goal_engine.py            # 战略目标引擎（年度/阶段/项目/任务四级）      │
├─────────────────────────────────────────────────────────────────────────────┤
│  E6: autonomy - 自治治理层                                                   │
│  └── bounded_governor.py       # 受控自治治理器（按风险级别控制）            │
├─────────────────────────────────────────────────────────────────────────────┤
│  E5: collaboration - 组织协同层                                              │
│  └── org_orchestrator.py       # 组织协同编排（跨团队协作）                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  E4: portfolio - 资源组合层                                                  │
│  └── resource_scheduler.py     # 资源组合调度中心                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  E3: simulation - 决策模拟层                                                 │
│  └── decision_lab.py           # 决策模拟实验室                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  E2: reliability - 可靠性层                                                  │
│  └── resilience_center.py      # 企业级可靠性中心                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  E1: compliance - 合规信任层                                                 │
│  └── trust_center.py           # 合规与信任中心                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  E0: openapi - 开放接入层                                                    │
│  └── integration_contract.py   # 开放接入契约中心                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  X7: ecosystem - 生态伙伴层                                                  │
│  └── partner_manager.py        # 伙伴生态管理器                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  X6: standards - 标准资产层                                                  │
│  └── asset_registry.py         # 平台标准资产注册中心                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  X5: product - 产品封装层                                                    │
│  └── surface_manager.py        # 产品封装管理器                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  X4: tenant - 多租户层                                                       │
│  └── workspace_manager.py      # 多租户工作空间管理                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  X3: delivery - 多端交付层                                                   │
│  └── multi_surface_hub.py      # 多端交付中心                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  X2: billing - 成本核算层                                                    │
│  └── cost_center.py            # 成本核算中心                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  X1: business - 商业封装层                                                   │
│  └── packaging_manager.py      # 商业封装管理器                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  X0: release - 版本发布层                                                    │
│  └── release_manager.py        # 版本发布管理器                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  Y3: ops - 运维监控层                                                        │
│  └── dashboard.py              # 运维监控面板                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  Y2: extension - 扩展协议层                                                  │
│  └── contract_manager.py       # 扩展协议管理器                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  Y1: templates - 模板复制层                                                  │
│  └── replication_engine.py     # 模板复制引擎                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 完整层级体系

### 核心六层 (L1-L6)

| 层级 | 名称 | 核心模块 | 职责 |
|------|------|----------|------|
| **L1** | 核心认知层 | ARCHITECTURE.md, dynamic_prompt.py, guide/ | 架构真源、动态提示词、引导模块 |
| **L2** | 记忆上下文层 | memory_quality.py, memory_summarizer.py | 记忆管理、上下文治理 |
| **L3** | 任务编排层 | workflows/, goal_tracker.py | 工作流引擎、任务调度 |
| **L4** | 能力执行层 | skill_gateway.py, health_check.py | 技能网关、健康检查 |
| **L5** | 稳定治理层 | gatekeeper.py, security_boundary.py | 守门器、安全边界 |
| **L6** | 基础设施层 | path_resolver.py, plugin_standard.py | 路径解析、插件标准 |

### 扩展层 (E0-E7)

| 层级 | 名称 | 核心模块 | 职责 |
|------|------|----------|------|
| **E7** | 战略目标层 | goal_engine.py | 年度/阶段/项目/任务四级目标管理 |
| **E6** | 自治治理层 | bounded_governor.py | 按风险级别控制自动执行权限 |
| **E5** | 组织协同层 | org_orchestrator.py | 跨团队协作编排 |
| **E4** | 资源组合层 | resource_scheduler.py | 多资源优化调度 |
| **E3** | 决策模拟层 | decision_lab.py | 决策预演和风险评估 |
| **E2** | 可靠性层 | resilience_center.py | 企业级可靠性保障 |
| **E1** | 合规信任层 | trust_center.py | 合规性检查和信任管理 |
| **E0** | 开放接入层 | integration_contract.py | 外部系统接入标准 |

### 商业层 (X0-X7)

| 层级 | 名称 | 核心模块 | 职责 |
|------|------|----------|------|
| **X7** | 生态伙伴层 | partner_manager.py | 合作伙伴管理 |
| **X6** | 标准资产层 | asset_registry.py | 平台标准资产注册 |
| **X5** | 产品封装层 | surface_manager.py | 产品封装管理 |
| **X4** | 多租户层 | workspace_manager.py | 多租户工作空间管理 |
| **X3** | 多端交付层 | multi_surface_hub.py | Web/API/CLI/文件四端统一 |
| **X2** | 成本核算层 | cost_center.py | 资源使用和成本核算 |
| **X1** | 商业封装层 | packaging_manager.py | 商业化封装管理 |
| **X0** | 版本发布层 | release_manager.py | 版本发布和回滚管理 |

### 运维层 (Y1-Y3)

| 层级 | 名称 | 核心模块 | 职责 |
|------|------|----------|------|
| **Y3** | 运维监控层 | dashboard.py | 运维监控面板 |
| **Y2** | 扩展协议层 | contract_manager.py | 外部扩展协议管理 |
| **Y1** | 模板复制层 | replication_engine.py | 项目模板复制引擎 |

---

## 引导模块（核心组件）

### 架构位置
```
L1: core - 核心认知层
├── ARCHITECTURE.md
├── dynamic_prompt.py
├── guide/              ← 引导模块
│   ├── assistant_guide.py
│   ├── bootstrap.py
│   └── guide_config.json
└── layer_bridge/
```

### 功能
- 每次对话自动加载
- 智能意图识别（18种意图）
- 上下文相关引导
- 175个技能介绍
- 50+模块介绍
- 完整使用引导

### 触发词
| 触发词 | 响应 |
|--------|------|
| 帮助 | 快速参考 |
| 架构 | 架构功能 |
| 新增功能 | 新功能介绍 |
| 全部功能 | 功能大全 |
| 所有技能 | 技能列表(175个) |
| 所有模块 | 模块列表(50+) |
| 使用引导 | 使用教程 |

---

## 技能体系

### 技能统计
- **总数**: 175个技能
- **分类**: 15个类别
- **健康状态**: healthy/degraded/broken/orphaned 四级

### 技能分类
| 类别 | 技能示例 |
|------|----------|
| 文档处理 | docx, pdf, pptx, markitdown |
| 数据分析 | data-analysis, excel-analysis, sqlite, mysql |
| 搜索网络 | xiaoyi-web-search, web-browsing, web-scraping |
| 图片处理 | image-cog, xiaoyi-image-understanding, seedream-image-gen |
| 自动化 | cron, xiaoyi-gui-agent, playwright |
| 开发工具 | git, code-analysis, docker, ansible |
| 商业分析 | market-research, stock-price-query, crypto |
| 内容创作 | article-writer, copywriter, poetry, novel-generator |
| 多媒体 | audio-cog, video-cog, spotify-player |
| 社交平台 | xiaohongshu-all-in-one, bilibili-all-in-one, linkedin-api |
| 文件管理 | file-manager, baidu-netdisk-skills, huawei-drive |
| 实用工具 | weather, google-maps, imap-smtp-email |
| 系统工具 | find-skills, skill-creator, skill-safe-install |
| 专业领域 | senior-architect, senior-security, ceo-advisor |
| 工作流 | planning-with-files, post-job, today-task |

---

## 工作流体系

### 已建成工作流
| 工作流 | 说明 | 技能组合 |
|--------|------|----------|
| 电商选品分析 | 分析产品趋势，生成选品建议 | xiaoyi-web-search, data-analysis, docx |
| 工厂筛选比价 | 筛选供应商，对比价格质量 | xiaoyi-web-search, excel-analysis, docx |
| 主播/团长筛选 | 筛选合作主播团长 | xiaoyi-web-search, data-analysis |
| 店铺启动 | 新店铺启动指导 | docx, market-research |
| 代码审计 | 检查代码质量 | code-analysis, git |
| 市场分析报告 | 深度市场调研 | market-research, xiaoyi-web-search, docx |

---

## 服务包体系

| 服务包 | 适用场景 | 能力范围 |
|--------|----------|----------|
| **基础包** | 个人用户 | 基础技能、文档生成 |
| **标准包** | 小团队 | 数据分析、自动化 |
| **专业包** | 专业用户 | 市场研究、代码审计 |
| **企业包** | 中小企业 | 多租户、权限管理 |
| **旗舰包** | 大企业 | 全功能、专属支持 |
| **定制包** | 特殊需求 | 定制开发 |
| **试用包** | 体验用户 | 限时全功能 |

---

## 安全体系

### 安全加固措施
| 措施 | 说明 |
|------|------|
| **路径白名单** | 只允许访问指定目录 |
| **内容脱敏** | 敏感信息自动脱敏 |
| **沙箱执行** | 高风险操作隔离执行 |
| **权限声明** | 操作前声明所需权限 |
| **预注册机制** | 只执行预注册的代码 |

### 安全边界
| 风险级别 | 处理方式 |
|----------|----------|
| **低风险** | 自动执行 |
| **中风险** | 确认后执行 |
| **高风险** | 必须人工确认 |

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| V2.8.0 | 2026-04-10 | 十阶段架构升级完成 |
| V2.8.1 | 2026-04-11 | 安全加固 + 引导模块 |

---

## 架构统计

| 指标 | 数量 |
|------|------|
| 核心层级 | 6层 (L1-L6) |
| 扩展层级 | 8层 (E0-E7) |
| 商业层级 | 8层 (X0-X7) |
| 运维层级 | 3层 (Y1-Y3) |
| **总层级** | **25层** |
| 技能总数 | 175个 |
| 工作流 | 8个 |
| 服务包 | 7个 |
| 模板 | 7个 |
| 安全机制 | 5层防护 |
| 新增模块 | 50+ |
| 引导意图 | 18种 |

---

💡 **提示**: 完整架构已融合，所有扩展层已纳入体系！
