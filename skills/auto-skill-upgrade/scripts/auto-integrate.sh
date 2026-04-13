#!/bin/bash
# 新技能自动整合脚本 - 当安装新技能时自动调用

# 参数：新技能路径
NEW_SKILL_PATH="$1"
SKILLS_DIR="$HOME/.openclaw/workspace/skills"
UPGRADE_DIR="$SKILLS_DIR/auto-skill-upgrade"

if [ -z "$NEW_SKILL_PATH" ]; then
    echo "用法: $0 <新技能路径>"
    exit 1
fi

NEW_SKILL_NAME=$(basename "$NEW_SKILL_PATH")
echo "🆕 检测到新技能: $NEW_SKILL_NAME"
echo ""

# 1. 安全检查（调用 skill-scope）
echo "1️⃣ 安全检查..."
if [ -f "$HOME/core_skills/skill-scope/scripts/scan-skill.sh" ]; then
    bash "$HOME/core_skills/skill-scope/scripts/scan-skill.sh" "$NEW_SKILL_PATH"
    if [ $? -ne 0 ]; then
        echo "❌ 安全检查未通过，拒绝整合"
        exit 1
    fi
else
    echo "⚠️ skill-scope 不可用，跳过安全检查"
fi
echo ""

# 2. 提取技能信息
echo "2️⃣ 提取技能信息..."
if [ -f "$NEW_SKILL_PATH/SKILL.md" ]; then
    description=$(head -1 "$NEW_SKILL_PATH/SKILL.md" | sed 's/^# //')
    echo "   描述: $description"
    
    # 检测类别
    category="other"
    case "$NEW_SKILL_NAME" in
        xiaoyi-*) category="xiaoyi" ;;
        *doc*|*pdf*|*pptx*|*excel*) category="document" ;;
        *image*|*video*|*audio*) category="multimedia" ;;
        *git*|*code*|*dev*) category="development" ;;
        *search*|*web*) category="search" ;;
        *memory*|*brain*) category="core" ;;
    esac
    echo "   类别: $category"
else
    echo "⚠️ 未找到 SKILL.md"
fi
echo ""

# 3. 检测冲突
echo "3️⃣ 检测潜在冲突..."
# 检查是否有同名或相似功能技能
similar=$(find "$SKILLS_DIR" -maxdepth 1 -type d -name "*$NEW_SKILL_NAME*" | grep -v "$NEW_SKILL_PATH" | head -1)
if [ -n "$similar" ]; then
    echo "⚠️ 发现相似技能: $(basename $similar)"
fi

# 检查功能重叠
if [ -f "$NEW_SKILL_PATH/SKILL.md" ]; then
    keywords=$(grep -oE "image|doc|pdf|search|web|video|audio" "$NEW_SKILL_PATH/SKILL.md" | sort -u)
    if [ -n "$keywords" ]; then
        echo "   关键词: $keywords"
        for kw in $keywords; do
            count=$(grep -l "$kw" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l)
            if [ "$count" -gt 0 ]; then
                echo "   ⚠️ '$kw' 相关技能: $count 个"
            fi
        done
    fi
fi
echo ""

# 4. 更新配置
echo "4️⃣ 更新技能配置..."
CONFIG_FILE="$UPGRADE_DIR/skills-config.json"
if [ -f "$CONFIG_FILE" ] && command -v jq &> /dev/null; then
    tmp=$(mktemp)
    jq ".categories.$category += [\"$NEW_SKILL_NAME\"] | .lastUpdate = \"$(date -Iseconds)\"" "$CONFIG_FILE" > "$tmp" && mv "$tmp" "$CONFIG_FILE"
    echo "✅ 配置已更新"
else
    echo "⚠️ jq 不可用或配置文件不存在"
fi
echo ""

# 5. 更新 MEMORY.md
echo "5️⃣ 更新记忆系统..."
MEMORY_FILE="$HOME/.openclaw/workspace/MEMORY.md"
if [ -f "$MEMORY_FILE" ]; then
    # 添加新技能记录
    echo "" >> "$MEMORY_FILE"
    echo "### 新增技能 - $(date '+%Y-%m-%d %H:%M')" >> "$MEMORY_FILE"
    echo "- **$NEW_SKILL_NAME**: $description" >> "$MEMORY_FILE"
    echo "  - 类别: $category" >> "$MEMORY_FILE"
    echo "✅ MEMORY.md 已更新"
fi
echo ""

# 6. 生成整合日志
INTEGRATE_LOG="$UPGRADE_DIR/integrate-log.md"
cat >> "$INTEGRATE_LOG" << EOF

---

## 新技能整合 - $(date '+%Y-%m-%d %H:%M:%S')

- **技能名称**: $NEW_SKILL_NAME
- **描述**: $description
- **类别**: $category
- **状态**: ✅ 已整合

EOF

echo "✅ 新技能整合完成"
echo "📄 整合日志: $INTEGRATE_LOG"
