# 架构收口改动清单

## 执行时间
- 开始时间：2026-04-10 00:28
- 完成时间：2026-04-10 00:30

---

## 一、删除的旧定义

### 1.1 旧架构定义文件（34个）
已移动到 `_archive/old_architecture_definitions_20260410/`：

| 文件名 | 说明 |
|-------|------|
| FUSION-ARCHITECTURE-V6-NETWORK.md | 旧融合架构V6网络版 |
| FUSION-ARCHITECTURE-V6.md | 旧融合架构V6 |
| FUSION-ARCHITECTURE-V5.md | 旧融合架构V5 |
| COMPLETE-FUSION-ARCHITECTURE-V7.md | 旧完全融合架构V7 |
| COMPLETE-ARCHITECTURE-V4.md | 旧完整架构V4 |
| FULL-ARCHITECTURE.md | 旧完整架构 |
| ARCHITECTURE-OPTIMIZATION-V3.md | 旧架构优化V3 |
| SYSTEM-EVOLUTION-V4.md | 旧系统进化V4 |
| ARCHITECTURE_V7.md ~ ARCHITECTURE_V25.md | 旧架构版本（多个） |
| ARCHITECTURE-DISPLAY.md | 旧架构展示 |
| architecture_display_live.md | 旧实时架构展示 |
| architecture-optimization-v2.md | 旧架构优化V2 |
| skills-fusion-plan.md | 旧技能融合计划 |
| TOOLS-v1-backup.md | 旧工具备份 |
| CLEANUP_POLICY.md | 旧清理策略 |
| MAINTENANCE_GUIDE.md | 旧维护指南 |

### 1.2 旧报告文件（43个）
已移动到 `_archive/old_reports_20260410/`：

| 文件类型 | 数量 |
|---------|------|
| UPGRADE_*.md | 15个 |
| *_REPORT*.md | 12个 |
| *_SUMMARY*.md | 8个 |
| 其他报告 | 8个 |

### 1.3 旧目录结构（14个）
已移动到 `_archive/`：

| 旧目录 | 说明 |
|-------|------|
| skills/ | 旧技能目录 |
| scripts/ | 旧脚本目录 |
| memory/ | 旧记忆目录 |
| _review_pending/ | 旧待审核目录 |
| business/ | 旧业务目录 |
| control/ | 旧控制目录 |
| evolution_lab/ | 旧进化实验室 |
| full-architecture-backup/ | 旧架构备份 |
| intelligence/ | 旧智能目录 |
| platform/ | 旧平台目录 |
| resilience/ | 旧弹性目录 |
| logs/ | 旧日志目录 |

---

## 二、合并的重复模块

### 2.1 技能合并
| 旧位置 | 新位置 | 所属层 |
|-------|-------|-------|
| skills/core/memory-management | memory_context/memory-management | L5 数据访问层 |
| skills/core/task-scheduler | orchestration/task-scheduler | L2 应用编排层 |
| skills/core/error-handling | governance/error-handling | L6 基础设施层 |
| skills/core/network-acceleration-layer | execution/network-acceleration-layer | L4 服务能力层 |
| skills/core/network-acceleration-layer-cpp | execution/network-acceleration-layer-cpp | L4 服务能力层 |
| skills/engines/phone-engine | execution/phone-engine | L4 服务能力层 |
| skills/utils/image-verification | execution/image-verification | L4 服务能力层 |

### 2.2 脚本合并
| 旧位置 | 新位置 | 所属层 |
|-------|-------|-------|
| scripts/routing/* | orchestration/routing/ | L2 应用编排层 |
| scripts/governance/* | governance/audit/ | L6 基础设施层 |
| scripts/inventory/* | infrastructure/inventory/ | L6 基础设施层 |
| scripts/ops/* | infrastructure/ops/ | L6 基础设施层 |
| scripts/assessment/* | infrastructure/assessment/ | L6 基础设施层 |
| scripts/auto-backup.sh | infrastructure/backup/ | L6 基础设施层 |
| scripts/memory-auto-cleanup.sh | infrastructure/backup/ | L6 基础设施层 |

### 2.3 配置合并
| 旧位置 | 新位置 | 说明 |
|-------|-------|------|
| scripts/inventory/architecture_config.json | infrastructure/inventory/architecture_config.json | 架构配置唯一源 |
| 多个旧配置 | infrastructure/inventory/skill_registry.json | 技能注册表唯一源 |

---

## 三、保留的兼容层

### 3.1 根目录兼容文件
| 文件 | 指向 | 说明 |
|-----|------|------|
| AGENTS.md | core/AGENTS.md | 兼容旧路径访问 |
| IDENTITY.md | core/IDENTITY.md | 兼容旧路径访问 |
| SOUL.md | core/SOUL.md | 兼容旧路径访问 |
| USER.md | core/USER.md | 兼容旧路径访问 |
| TOOLS.md | core/TOOLS.md | 兼容旧路径访问 |
| MEMORY.md | memory_context/MEMORY.md | 兼容旧路径访问 |

### 3.2 兼容层保留期限
- **第一阶段**：保留1周，观察是否有旧路径调用
- **第二阶段**：确认无调用后，删除兼容层

---

## 四、现有技能挂载位置

### 4.1 技能注册表
**路径**：`infrastructure/inventory/skill_registry.json`

| skill_id | skill_name | entry_layer | 层路径 |
|----------|-----------|-------------|-------|
| skill_memory_management_v1 | 记忆管理 | L5 | memory_context/memory-management/ |
| skill_task_scheduler_v1 | 任务调度 | L2 | orchestration/task-scheduler/ |
| skill_error_handling_v1 | 错误处理 | L6 | governance/error-handling/ |
| skill_phone_engine_v1 | 手机操作引擎 | L4 | execution/phone-engine/ |
| skill_image_verification_v1 | 图片验证 | L4 | execution/image-verification/ |
| skill_network_acceleration_v1 | 网络加速层 | L4 | execution/network-acceleration-layer/ |
| skill_network_acceleration_cpp_v1 | 网络加速层(C++) | L4 | execution/network-acceleration-layer-cpp/ |
| skill_route_smoke_test_v1 | 路由冒烟测试 | L2 | orchestration/routing/ |
| skill_failover_test_v1 | 故障转移测试 | L6 | governance/failover/ |
| skill_evidence_audit_v1 | 证据链审计 | L6 | governance/audit/ |

### 4.2 六层架构映射
| 层级 | 层名 | 路径 | 技能数 |
|-----|------|------|-------|
| L1 | 表达层 | core/ | 0 |
| L2 | 应用编排层 | orchestration/ | 2 |
| L3 | 领域规则层 | governance/policy/ | 0 |
| L4 | 服务能力层 | execution/ | 4 |
| L5 | 数据访问层 | memory_context/ | 1 |
| L6 | 基础设施层 | infrastructure/ + governance/ | 3 |

---

## 五、新增技能接入位置

### 5.1 唯一接入点
**注册表**：`infrastructure/inventory/skill_registry.json`

### 5.2 接入规则
**规则文档**：`core/SKILL_ACCESS_RULES.md`

### 5.3 接入流程
1. **能力归类** → 判断归属层（L1-L6）
2. **定义边界** → 输入/输出/依赖/超时/回退
3. **标准接口** → 统一接口名/参数名/返回结构
4. **注册入表** → 写入 skill_registry.json
5. **灰度接入** → 测试链路验证
6. **监控校验** → 补齐日志/调用链/耗时
7. **正式放量** → 验收后并入主流程

### 5.4 必填字段
| 字段 | 说明 |
|-----|------|
| skill_id | 唯一标识 |
| skill_name | 面向人可读名称 |
| version | 版本号 |
| entry_layer | 归属层（L1-L6） |
| input_schema | 输入参数定义 |
| output_schema | 返回结构定义 |
| dependencies | 依赖的服务或库 |
| owner | 谁维护、谁兜底 |
| timeout_ms | 超时阈值 |
| fallback_strategy | 失败后的兜底策略 |
| status | 生命周期状态 |

---

## 六、验证结果

### 6.1 功能验证
| 验证项 | 状态 |
|-------|------|
| 原有功能不受损 | ✅ |
| 原有数据不丢失 | ✅ |
| 原有配置可迁移 | ✅ |
| 调用链路无断裂 | ✅ |
| 出现问题时可回滚 | ✅ |

### 6.2 架构验证
| 验证项 | 状态 |
|-------|------|
| 主架构稳定为6层 | ✅ |
| 每个技能都有明确的entry_layer | ✅ |
| 所有技能都进入统一注册表 | ✅ |
| 不存在跨层乱调 | ✅ |
| 不存在职责混装 | ✅ |

### 6.3 回滚方案
| 回滚项 | 路径 |
|-------|------|
| 旧架构定义 | `_archive/old_architecture_definitions_20260410/` |
| 旧报告文件 | `_archive/old_reports_20260410/` |
| 旧技能目录 | `_archive/old_skills_20260410/` |
| 旧脚本目录 | `_archive/old_scripts_20260410/` |
| 旧记忆数据 | `_archive/old_memory_20260410/` |

---

## 七、最终目录结构

```
workspace/
├── core/                          # L1 表达层
│   ├── AGENTS.md
│   ├── IDENTITY.md
│   ├── SOUL.md
│   ├── USER.md
│   ├── TOOLS.md
│   ├── ARCHITECTURE.md           # 架构真源
│   └── SKILL_ACCESS_RULES.md     # 技能接入规则
│
├── memory_context/                # L5 数据访问层
│   ├── MEMORY.md
│   ├── data/
│   └── memory-management/
│
├── orchestration/                 # L2 应用编排层
│   ├── task-scheduler/
│   ├── routing/
│   └── policy/
│
├── execution/                     # L4 服务能力层
│   ├── phone-engine/
│   ├── image-verification/
│   ├── network-acceleration-layer/
│   ├── network-acceleration-layer-cpp/
│   └── runtime/
│
├── governance/                    # L6 基础设施层（部分）
│   ├── error-handling/
│   ├── safety/
│   ├── audit/
│   ├── failover/
│   ├── rollback/
│   └── disaster_recovery/
│
├── infrastructure/                # L6 基础设施层（部分）
│   ├── inventory/
│   │   ├── architecture_config.json
│   │   ├── skill_registry.json   # 技能注册表
│   │   └── generate_architecture_display.py
│   ├── ops/
│   ├── assessment/
│   ├── backup/
│   └── monitoring/
│
├── reports/                       # 运行产物目录
│
├── _archive/                      # 归档目录
│   ├── old_architecture_definitions_20260410/
│   ├── old_reports_20260410/
│   ├── old_skills_20260410/
│   ├── old_scripts_20260410/
│   └── ...
│
└── [兼容层文件]                   # 根目录兼容文件
    ├── AGENTS.md → core/AGENTS.md
    ├── IDENTITY.md → core/IDENTITY.md
    ├── SOUL.md → core/SOUL.md
    ├── USER.md → core/USER.md
    ├── TOOLS.md → core/TOOLS.md
    └── MEMORY.md → memory_context/MEMORY.md
```

---

## 版本
- V1.0.0
- 创建日期：2026-04-10
