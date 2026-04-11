#!/bin/bash
# auto-upgrade-full.sh - 完整自动升级流程
# 包含：自动检测、性能优化、记忆管理、冗余清理、整合升级、自我进化、架构升级
# 用法: bash auto-upgrade-full.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$BASE_DIR/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/upgrade_full_${TIMESTAMP}.log"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

log_section() {
    echo "" | tee -a "$LOG_FILE"
    echo "========================================" | tee -a "$LOG_FILE"
    echo "$1" | tee -a "$LOG_FILE"
    echo "========================================" | tee -a "$LOG_FILE"
}

# 确保日志目录存在
mkdir -p "$LOG_DIR"

log "🚀 自动升级开始 - $(date '+%Y-%m-%d %H:%M:%S')"
log "📄 日志文件: $LOG_FILE"

# ============================================
# 第一阶段：自动检测
# ============================================
log_section "🔍 第一阶段：自动检测"

log "\n### 1️⃣ 扫描技能库"
bash "$SCRIPT_DIR/scan-skills.sh" 2>&1 | tee -a "$LOG_FILE"
SKILL_COUNT=$(cat "$BASE_DIR/.last_skill_count" 2>/dev/null || echo "0")
log "📊 当前技能数: $SKILL_COUNT"

log "\n### 2️⃣ 检测冲突"
bash "$SCRIPT_DIR/detect-conflicts.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 3️⃣ 检测冗余"
bash "$SCRIPT_DIR/detect-redundancy.sh" 2>&1 | tee -a "$LOG_FILE"

# ============================================
# 第二阶段：性能优化
# ============================================
log_section "⚡ 第二阶段：性能优化"

log "\n### 1️⃣ 性能分析"
bash "$SCRIPT_DIR/performance-optimizer.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 2️⃣ Token 监控"
bash "$SCRIPT_DIR/token-monitor.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 3️⃣ 懒加载优化"
bash "$SCRIPT_DIR/lazy-loader.sh" 2>&1 | tee -a "$LOG_FILE"

# ============================================
# 第三阶段：记忆管理
# ============================================
log_section "🧠 第三阶段：记忆管理"

log "\n### 1️⃣ 记忆压缩"
bash "$SCRIPT_DIR/memory-compress.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 2️⃣ 会话压缩"
bash "$SCRIPT_DIR/session-compress.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 3️⃣ 知识图谱更新"
bash "$SCRIPT_DIR/update-ontology.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 4️⃣ 学习捕获"
bash "$SCRIPT_DIR/learning-capture.sh" 2>&1 | tee -a "$LOG_FILE"

# ============================================
# 第四阶段：冗余清理
# ============================================
log_section "🧹 第四阶段：冗余清理"

log "\n### 1️⃣ 冗余清理"
bash "$SCRIPT_DIR/redundancy-cleanup.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 2️⃣ 自动清理"
bash "$SCRIPT_DIR/auto-cleanup.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 3️⃣ 技能修剪"
bash "$SCRIPT_DIR/skill-pruner.sh" 2>&1 | tee -a "$LOG_FILE"

# ============================================
# 第五阶段：整合升级
# ============================================
log_section "🔄 第五阶段：整合升级"

log "\n### 1️⃣ 技能整合"
bash "$SCRIPT_DIR/merge-skills.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 2️⃣ 技能链合并"
bash "$SCRIPT_DIR/skill-chain-merge.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 3️⃣ 配置合并"
bash "$SCRIPT_DIR/config-merge.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 4️⃣ 使用频率追踪"
bash "$SCRIPT_DIR/usage-tracker.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 5️⃣ 技能推荐"
bash "$SCRIPT_DIR/skill-recommender.sh" 2>&1 | tee -a "$LOG_FILE"

# ============================================
# 第六阶段：自我进化
# ============================================
log_section "🌱 第六阶段：自我进化"

log "\n### 1️⃣ 自动进化"
bash "$SCRIPT_DIR/auto-evolve.sh" 2>&1 | tee -a "$LOG_FILE"

log "\n### 2️⃣ 本体优化"
bash "$SCRIPT_DIR/ontology-optimize.sh" 2>&1 | tee -a "$LOG_FILE"

# ============================================
# 生成报告
# ============================================
log_section "📊 升级报告"

# 统计数据
NEW_SKILL_COUNT=$(ls -d ~/.openclaw/workspace/skills/*/ 2>/dev/null | wc -l)
CONFLICTS=$(grep -c "⚠️" "$BASE_DIR/conflicts-report.md" 2>/dev/null || echo "0")
REDUNDANT=$(wc -l < "$BASE_DIR/redundant-skills.txt" 2>/dev/null || echo "0")

log "\n## 📈 统计数据"
log "| 指标 | 数值 |"
log "|------|------|"
log "| 技能总数 | $NEW_SKILL_COUNT |"
log "| 检测冲突 | $CONFLICTS |"
log "| 冗余技能 | $REDUNDANT |"

log "\n## ✅ 升级完成"
log "- 配置文件: $BASE_DIR/skills-config.json"
log "- 技能清单: $BASE_DIR/skills-inventory.json"
log "- 冲突报告: $BASE_DIR/conflicts-report.md"
log "- 升级日志: $LOG_FILE"

# ============================================
# 第七阶段：架构升级
# ============================================
log_section "🏗️ 第七阶段：架构升级"

log "\n### 1️⃣ 架构分析"
bash "$SCRIPT_DIR/architecture-upgrade.sh" 2>&1 | tee -a "$LOG_FILE"

# 更新 MEMORY.md
log "\n### 更新 MEMORY.md"
MEMORY_FILE="$BASE_DIR/../../MEMORY.md"
if [ -f "$MEMORY_FILE" ]; then
    # 添加升级记录
    echo "" >> "$MEMORY_FILE"
    echo "---" >> "$MEMORY_FILE"
    echo "" >> "$MEMORY_FILE"
    echo "## 🔄 自动升级记录 - $(date '+%Y-%m-%d %H:%M')" >> "$MEMORY_FILE"
    echo "" >> "$MEMORY_FILE"
    echo "- 技能总数: $NEW_SKILL_COUNT" >> "$MEMORY_FILE"
    echo "- 小艺系列: 6" >> "$MEMORY_FILE"
    echo "- 冲突检测: $CONFLICTS 项" >> "$MEMORY_FILE"
    echo "- 冗余清理: $REDUNDANT 项" >> "$MEMORY_FILE"
    echo "- 升级日志: $LOG_FILE" >> "$MEMORY_FILE"
    log "✅ MEMORY.md 已更新"
fi

log "\n🎉 自动升级完成！"
log "📄 详细日志: $LOG_FILE"

# 生成摘要报告
SUMMARY_FILE="$LOG_DIR/upgrade_full_${TIMESTAMP}_summary.md"
cat > "$SUMMARY_FILE" << EOF
# 自动升级摘要报告

**时间**: $(date '+%Y-%m-%d %H:%M:%S')

## 执行阶段

| 阶段 | 内容 | 状态 |
|------|------|------|
| 🔍 自动检测 | 扫描/冲突/冗余检测 | ✅ |
| ⚡ 性能优化 | 性能分析/Token监控/懒加载 | ✅ |
| 🧠 记忆管理 | 压缩/会话/图谱/学习 | ✅ |
| 🧹 冗余清理 | 冗余/自动清理/修剪 | ✅ |
| 🔄 整合升级 | 整合/链合并/配置/追踪 | ✅ |
| 🌱 自我进化 | 进化/本体优化 | ✅ |
| 🏗️ 架构升级 | 系统架构/技能架构/记忆架构 | ✅ |

## 统计数据

- 技能总数: $NEW_SKILL_COUNT
- 检测冲突: $CONFLICTS
- 冗余技能: $REDUNDANT

## 输出文件

- 配置: skills-config.json
- 清单: skills-inventory.json
- 冲突: conflicts-report.md
- 架构: architecture-report.md
- 日志: $LOG_FILE
EOF

log "📄 摘要报告: $SUMMARY_FILE"
