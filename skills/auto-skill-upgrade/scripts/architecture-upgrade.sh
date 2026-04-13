#!/bin/bash
# architecture-upgrade.sh - 架构升级脚本
# 检查和升级系统架构、技能架构、记忆架构

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$BASE_DIR")"
MEMORY_DIR="$WORKSPACE_DIR/memory"
SYSTEM_DIR="$MEMORY_DIR/system"

# 修正：如果 BASE_DIR 已经是 skills/auto-skill-upgrade，则 WORKSPACE_DIR 应该是上两级
if [[ "$BASE_DIR" == */skills/auto-skill-upgrade ]]; then
    WORKSPACE_DIR="$(dirname "$(dirname "$BASE_DIR")")"
fi

MEMORY_DIR="$WORKSPACE_DIR/memory"
SYSTEM_DIR="$MEMORY_DIR/system"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🏗️ 架构升级分析"
echo "=================="

# ============================================
# 1. 系统架构检查
# ============================================
echo ""
echo "### 1️⃣ 系统架构检查"

# 检查核心文件
CORE_FILES=(
    "AGENTS.md"
    "SOUL.md"
    "USER.md"
    "TOOLS.md"
    "MEMORY.md"
    "IDENTITY.md"
    "HEARTBEAT.md"
)

MISSING_FILES=()
for file in "${CORE_FILES[@]}"; do
    if [ -f "$WORKSPACE_DIR/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (缺失)"
        MISSING_FILES+=("$file")
    fi
done

# 检查目录结构
REQUIRED_DIRS=(
    "memory"
    "memory/system"
    "memory/scenarios"
    "memory/archive"
    "skills"
    ".learnings"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$WORKSPACE_DIR/$dir" ]; then
        echo "  ✅ $dir/"
    else
        echo "  ⚠️ $dir/ (不存在，将创建)"
        mkdir -p "$WORKSPACE_DIR/$dir"
    fi
done

# ============================================
# 2. 技能架构分析
# ============================================
echo ""
echo "### 2️⃣ 技能架构分析"

# 分析技能分类
SKILL_DIR="$WORKSPACE_DIR/skills"
TOTAL_SKILLS=$(ls -d "$SKILL_DIR"/*/ 2>/dev/null | wc -l)

# 统计各分类技能数
declare -A CATEGORIES
CATEGORIES["xiaoyi"]=0
CATEGORIES["core"]=0
CATEGORIES["integration"]=0
CATEGORIES["search"]=0
CATEGORIES["document"]=0
CATEGORIES["multimedia"]=0
CATEGORIES["development"]=0
CATEGORIES["finance"]=0
CATEGORIES["communication"]=0
CATEGORIES["content"]=0
CATEGORIES["productivity"]=0
CATEGORIES["marketing"]=0
CATEGORIES["business"]=0
CATEGORIES["automation"]=0
CATEGORIES["utility"]=0
CATEGORIES["other"]=0

# 从 skills-config.json 读取分类
if [ -f "$BASE_DIR/skills-config.json" ]; then
    echo "  📊 从 skills-config.json 读取分类..."
    # 使用 jq 或 grep 解析
    if command -v jq &> /dev/null; then
        for cat in "${!CATEGORIES[@]}"; do
            count=$(jq -r ".categories.$cat | length" "$BASE_DIR/skills-config.json" 2>/dev/null || echo "0")
            if [ "$count" != "null" ] && [ "$count" != "0" ]; then
                CATEGORIES[$cat]=$count
            fi
        done
    fi
fi

echo "  📊 技能分类统计:"
for cat in "${!CATEGORIES[@]}"; do
    if [ "${CATEGORIES[$cat]}" -gt 0 ]; then
        echo "     - $cat: ${CATEGORIES[$cat]}"
    fi
done

# 检查工作流链
echo ""
echo "  🔗 工作流链检查:"
if [ -f "$BASE_DIR/skills-config.json" ]; then
    if command -v jq &> /dev/null; then
        CHAINS=$(jq -r '.chains | keys[]' "$BASE_DIR/skills-config.json" 2>/dev/null)
        for chain in $CHAINS; do
            entry=$(jq -r ".chains.$chain.entry" "$BASE_DIR/skills-config.json" 2>/dev/null)
            priority=$(jq -r ".chains.$chain.priority" "$BASE_DIR/skills-config.json" 2>/dev/null)
            echo "     - $chain (入口: $entry, 优先级: $priority)"
        done
    fi
fi

# ============================================
# 3. 记忆架构分析
# ============================================
echo ""
echo "### 3️⃣ 记忆架构分析"

# 检查三层画像系统
echo "  🧠 三层画像系统:"

# L1 - 会话层
SESSION_FILES=$(find "$WORKSPACE_DIR" -name "*.jsonl" -type f 2>/dev/null | wc -l)
echo "     - L1 会话层: $SESSION_FILES 个会话文件"

# L2 - 场景层
if [ -d "$MEMORY_DIR/scenarios" ]; then
    SCENARIO_FILES=$(ls "$MEMORY_DIR/scenarios"/*.md 2>/dev/null | wc -l)
    echo "     - L2 场景层: $SCENARIO_FILES 个场景画像"
else
    echo "     - L2 场景层: ⚠️ 目录不存在"
fi

# L3 - 长期层
if [ -f "$WORKSPACE_DIR/USER.md" ]; then
    USER_SIZE=$(wc -c < "$WORKSPACE_DIR/USER.md")
    echo "     - L3 长期层: USER.md ($USER_SIZE bytes)"
fi
if [ -f "$WORKSPACE_DIR/MEMORY.md" ]; then
    MEMORY_SIZE=$(wc -c < "$WORKSPACE_DIR/MEMORY.md")
    echo "     - L3 长期层: MEMORY.md ($MEMORY_SIZE bytes)"
fi

# 检查 ontology
if [ -d "$MEMORY_DIR/ontology" ]; then
    ONTOLOGY_FILES=$(ls "$MEMORY_DIR/ontology"/* 2>/dev/null | wc -l)
    echo "     - 知识图谱: $ONTOLOGY_FILES 个文件"
fi

# ============================================
# 4. 架构健康度评估
# ============================================
echo ""
echo "### 4️⃣ 架构健康度评估"

HEALTH_SCORE=100
ISSUES=()

# 检查核心文件完整性
if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    HEALTH_SCORE=$((HEALTH_SCORE - 10 * ${#MISSING_FILES[@]}))
    ISSUES+=("缺失核心文件: ${MISSING_FILES[*]}")
fi

# 检查技能配置
if [ ! -f "$BASE_DIR/skills-config.json" ]; then
    HEALTH_SCORE=$((HEALTH_SCORE - 15))
    ISSUES+=("skills-config.json 不存在")
fi

# 检查记忆系统
if [ ! -d "$MEMORY_DIR/scenarios" ]; then
    HEALTH_SCORE=$((HEALTH_SCORE - 10))
    ISSUES+=("场景画像目录不存在")
fi

# 检查学习记录
if [ ! -d "$WORKSPACE_DIR/.learnings" ]; then
    HEALTH_SCORE=$((HEALTH_SCORE - 5))
    ISSUES+=(".learnings 目录不存在")
fi

# 输出健康度
if [ $HEALTH_SCORE -ge 90 ]; then
    echo "  ✅ 架构健康度: $HEALTH_SCORE/100 (优秀)"
elif [ $HEALTH_SCORE -ge 70 ]; then
    echo "  ⚠️ 架构健康度: $HEALTH_SCORE/100 (良好)"
else
    echo "  ❌ 架构健康度: $HEALTH_SCORE/100 (需要改进)"
fi

# 输出问题
if [ ${#ISSUES[@]} -gt 0 ]; then
    echo ""
    echo "  ⚠️ 发现问题:"
    for issue in "${ISSUES[@]}"; do
        echo "     - $issue"
    done
fi

# ============================================
# 5. 架构优化建议
# ============================================
echo ""
echo "### 5️⃣ 架构优化建议"

# 检查是否需要创建缺失文件
if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo "  💡 需要创建缺失的核心文件"
fi

# 检查技能链完整性
echo "  💡 建议定期检查工作流链的入口技能是否存在"

# 检查记忆归档
if [ -d "$MEMORY_DIR" ]; then
    OLD_FILES=$(find "$MEMORY_DIR" -name "*.md" -mtime +30 2>/dev/null | wc -l)
    if [ "$OLD_FILES" -gt 10 ]; then
        echo "  💡 建议归档 $OLD_FILES 个超过 30 天的记忆文件"
    fi
fi

# 检查技能冗余
if [ -f "$BASE_DIR/redundant-skills.txt" ]; then
    REDUNDANT=$(wc -l < "$BASE_DIR/redundant-skills.txt")
    if [ "$REDUNDANT" -gt 20 ]; then
        echo "  💡 建议清理 $REDUNDANT 个冗余技能"
    fi
fi

# ============================================
# 6. 生成架构报告
# ============================================
REPORT_FILE="$BASE_DIR/architecture-report.md"
cat > "$REPORT_FILE" << EOF
# 架构升级报告

生成时间: $(date '+%Y-%m-%d %H:%M:%S')

---

## 📊 系统概览

| 指标 | 数值 |
|------|------|
| 技能总数 | $TOTAL_SKILLS |
| 核心文件 | $((7 - ${#MISSING_FILES[@]}))/7 |
| 工作流链 | $(jq -r '.chains | keys | length' "$BASE_DIR/skills-config.json" 2>/dev/null || echo "0") |
| 健康度 | $HEALTH_SCORE/100 |

## 🏗️ 架构层次

### L1 会话层
- 会话文件: $SESSION_FILES

### L2 场景层
- 场景画像: $SCENARIO_FILES

### L3 长期层
- USER.md: $USER_SIZE bytes
- MEMORY.md: $MEMORY_SIZE bytes

## 📦 技能架构

### 分类统计
EOF

for cat in "${!CATEGORIES[@]}"; do
    if [ "${CATEGORIES[$cat]}" -gt 0 ]; then
        echo "- $cat: ${CATEGORIES[$cat]}" >> "$REPORT_FILE"
    fi
done

cat >> "$REPORT_FILE" << EOF

### 工作流链
EOF

if [ -f "$BASE_DIR/skills-config.json" ] && command -v jq &> /dev/null; then
    jq -r '.chains | to[] | "- \(.key): \(.value.entry) (优先级: \(.value.priority))"' "$BASE_DIR/skills-config.json" 2>/dev/null >> "$REPORT_FILE" || true
fi

if [ ${#ISSUES[@]} -gt 0 ]; then
    echo "" >> "$REPORT_FILE"
    echo "## ⚠️ 待解决问题" >> "$REPORT_FILE"
    for issue in "${ISSUES[@]}"; do
        echo "- $issue" >> "$REPORT_FILE"
    done
fi

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "*此报告由 auto-skill-upgrade 自动生成*" >> "$REPORT_FILE"

echo ""
echo "✅ 架构升级分析完成"
echo "📄 报告已生成: $REPORT_FILE"
