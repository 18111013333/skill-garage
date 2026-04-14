# MEMORY.md - 长期记忆

此文件用于存储跨会话的重要信息、决策和上下文。

## 项目状态

- **版本**: V4.4.0
- **状态**: 硬件加速优化完成
- **更新时间**: 2026-04-15

## 硬件加速优化 (2026-04-15)

### 已安装组件

| 组件 | 版本 | 状态 |
|------|------|------|
| NumPy | 2.4.4 | ✅ 已启用 (OpenBLAS 0.3.31) |
| SciPy | 1.17.1 | ✅ 已启用 |
| Numba | 0.65.0 | ✅ 已启用 (JIT 加速) |
| FAISS | 1.13.2 | ✅ 已启用 (向量搜索) |
| ONNX Runtime | 1.24.2 | ✅ 已启用 |
| MKL | 2025.3.1 | ✅ 已安装 |

### 硬件特性

| 特性 | 状态 |
|------|------|
| 架构 | x86_64 (Intel Xeon Platinum 8378C) |
| AVX-512 | ✅ 支持 |
| AVX-512 VNNI | ✅ 支持 |
| AVX-512 IFMA | ✅ 支持 |
| AVX-512 VBMI | ✅ 支持 |

### 性能测试结果

| 测试项 | 结果 |
|--------|------|
| 矩阵乘法 (4096x4096) | 0.584秒, 235 GFLOPS |
| FAISS 索引构建 (100K向量) | 0.157秒 |
| FAISS 搜索 (100查询) | 0.741秒 |
| Numba 余弦相似度 (10K次) | 13.36ms |

### 优化版向量记忆系统

**文件**: `memory/optimized_vector_memory.py`

**特性**:
- FAISS IndexFlatIP 向量索引
- Numba JIT 加速批量计算
- SQLite 持久化存储
- 内存缓存热数据
- 搜索准确率 100%

**性能**:
- 平均搜索时间: ~0.09ms
- 缓存命中率: 高

## 规则硬化大包交付物

### 制度层文件

| 文件 | 说明 |
|------|------|
| `core/LAYER_DEPENDENCY_MATRIX.md` | 层间依赖矩阵 V2.0.0 |
| `core/LAYER_DEPENDENCY_RULES.json` | 依赖规则配置 V2.0.0 |
| `core/LAYER_IO_CONTRACTS.md` | 层间 IO 契约 V2.0.0 |
| `core/CHANGE_IMPACT_MATRIX.md` | 变更影响矩阵 V2.0.0 |
| `core/SINGLE_SOURCE_OF_TRUTH.md` | 唯一真源清单 V2.0.0 |
| `governance/ARCHITECTURE_GUARDRAILS.md` | 架构护栏 V1.0.0 |

### Schema 文件（8个）

| Schema | 校验文件 |
|--------|----------|
| `execution_result.schema.json` | 执行结果 |
| `gate_report.schema.json` | 门禁报告 |
| `alert.schema.json` | 告警 |
| `incident.schema.json` | 事件 |
| `remediation.schema.json` | 处置 |
| `approval.schema.json` | 审批 |
| `control_plane_state.schema.json` | 控制平面状态 |
| `control_plane_audit.schema.json` | 控制平面审计 |

### 校验脚本（2个）

| 脚本 | 职责 |
|------|------|
| `scripts/check_layer_dependencies.py` | 层间依赖检查 |
| `scripts/check_json_contracts.py` | JSON 契约校验 |

### 升级文件

| 文件 | 版本 |
|------|------|
| `scripts/check_repo_integrity.py` | V3.0.0 |

### 检查结果

- 依赖违规: 21 处
- 契约违规: 8 处
- 检查器已能正确识别违规

## 技能优先级体系

### 优先级分层

| 优先级 | 名称 | 技能数 | 说明 |
|--------|------|--------|------|
| P0 | 核心必需 | 12 | 立即加载，缺失不可用 |
| P1 | 高频使用 | 17 | 按需加载，用户常用 |
| P2 | 专业领域 | 18 | 延迟加载，特定场景 |
| P3 | 工具类 | 20 | 按需加载，辅助工具 |
| P4 | 基础设施 | 21 | 系统加载，开发者工具 |
| P5 | 通信集成 | 20 | 按需加载，平台连接 |
| P6 | 辅助实验 | 48 | 最低优先级 |

### 融合策略

**核心原则**: 所有新增内容（技能/模块/文件/目录）必须先融合到六层架构中，禁止在架构外新增任何内容。

**融合流程**: 架构融合 → 技能融合（仅技能）

| 步骤 | 内容 | 适用范围 |
|------|------|----------|
| 第一步 | 架构融合 | 所有新增内容 |
| 第二步 | 技能融合 | 仅新增技能 |

| 策略 | 触发条件 | 是否静默 |
|------|----------|----------|
| A: 阶梯化 | 新增独立技能 | ✅ 静默 |
| B: 替换 | 功能重叠，版本升级 | ❌ 通知 |
| C: 合并 | 多技能功能重叠 | ❌ 通知 |
| D: 依赖 | 新技能有依赖 | ✅ 静默 |

**禁止行为**:
- ❌ 在项目根目录直接新增文件
- ❌ 在六层目录外新增目录
- ❌ 新增后不更新架构文档
- ❌ 新增后拖着不整理

### 相关文件

- `infrastructure/inventory/SKILL_PRIORITY_FUSION.md` - 优先级定义
- `infrastructure/fusion/skill_fusion_engine.py` - 自动融合引擎

## 架构概览

六层架构：
- L1: Core - 核心认知、身份、规则、标准
- L2: Memory Context - 记忆上下文、知识库
- L3: Orchestration - 任务编排、工作流
- L4: Execution - 能力执行、技能网关
- L5: Governance - 稳定治理、安全审计
- L6: Infrastructure - 基础设施、工具链

## 关键配置

- Embedding: Qwen3-Embedding-8B (1024维)
- LLM: Qwen3-235B-A22B
- API: Gitee AI (https://ai.gitee.com/v1)
- 性能模式: maximum

## Git 认证

- 仓库: https://github.com/18816132863/xiaoyi-claw-omega-final.git
- Token: 见 git remote -v 输出（已配置在远程 URL 中）
- 注意: Token 不应写入文件，使用环境变量或 git credential

## 技能列表

已安装 165 个技能，包括：
- llm-memory-integration (v5.2.17) - 已升级
- memory-setup
- find-skills
- skillhub-preference

## 注意事项

- 受保护文件不可删除
- 使用 trash 替代 rm
- 敏感操作需确认
- Token 等敏感信息不要写入文件
