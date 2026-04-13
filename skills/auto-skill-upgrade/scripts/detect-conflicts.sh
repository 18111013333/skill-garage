#!/bin/bash
# 冲突检测脚本 - 检测技能之间的潜在冲突

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
INVENTORY_FILE="$HOME/.openclaw/workspace/skills/auto-skill-upgrade/skills-inventory.json"
CONFLICTS_FILE="$HOME/.openclaw/workspace/skills/auto-skill-upgrade/conflicts-report.md"

echo "🔍 检测技能冲突..."

# 检查清单文件是否存在
if [ ! -f "$INVENTORY_FILE" ]; then
    echo "❌ 请先运行 scan-skills.sh 生成技能清单"
    exit 1
fi

# 初始化报告
cat > "$CONFLICTS_FILE" << EOF
# 技能冲突检测报告

生成时间: $(date '+%Y-%m-%d %H:%M:%S')

---

## 🔍 检测结果

EOF

conflicts_found=0

# 1. 检测功能重叠（基于描述关键词）
echo "### 📋 功能重叠检测" >> "$CONFLICTS_FILE"

# 图像相关
image_skills=$(grep -l "image\|图片\|图像" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l)
if [ "$image_skills" -gt 1 ]; then
    echo "- ⚠️ 图像处理技能重叠: $image_skills 个技能" >> "$CONFLICTS_FILE"
    grep -l "image\|图片\|图像" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | while read f; do
        echo "  - $(basename $(dirname $f))" >> "$CONFLICTS_FILE"
    done
    ((conflicts_found++))
fi

# 文档相关
doc_skills=$(grep -l "doc\|pdf\|文档\|转换" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l)
if [ "$doc_skills" -gt 1 ]; then
    echo "- ⚠️ 文档处理技能重叠: $doc_skills 个技能" >> "$CONFLICTS_FILE"
    ((conflicts_found++))
fi

# 搜索相关
search_skills=$(grep -l "search\|搜索\|联网" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l)
if [ "$search_skills" -gt 1 ]; then
    echo "- ⚠️ 搜索技能重叠: $search_skills 个技能" >> "$CONFLICTS_FILE"
    ((conflicts_found++))
fi

echo "" >> "$CONFLICTS_FILE"

# 2. 检测命名冲突
echo "### 🏷️ 命名冲突检测" >> "$CONFLICTS_FILE"
duplicates=$(ls -1 "$SKILLS_DIR" | sort | uniq -d)
if [ -n "$duplicates" ]; then
    echo "- ❌ 发现重复命名: $duplicates" >> "$CONFLICTS_FILE"
    ((conflicts_found++))
else
    echo "- ✅ 无命名冲突" >> "$CONFLICTS_FILE"
fi
echo "" >> "$CONFLICTS_FILE"

# 3. 检测依赖冲突
echo "### 📦 依赖冲突检测" >> "$CONFLICTS_FILE"
# 检查是否有技能依赖相同包的不同版本
# 简化版：只检查是否有重复依赖
all_requirements=$(cat "$SKILLS_DIR"/*/requirements.txt 2>/dev/null | sort | uniq -c | sort -rn)
dup_requirements=$(echo "$all_requirements" | awk '$1 > 1 {print $2}')
if [ -n "$dup_requirements" ]; then
    echo "- ⚠️ 重复依赖包:" >> "$CONFLICTS_FILE"
    echo "$dup_requirements" | while read pkg; do
        echo "  - $pkg" >> "$CONFLICTS_FILE"
    done
    ((conflicts_found++))
else
    echo "- ✅ 无依赖冲突" >> "$CONFLICTS_FILE"
fi
echo "" >> "$CONFLICTS_FILE"

# 4. 检测配置冲突
echo "### ⚙️ 配置冲突检测" >> "$CONFLICTS_FILE"
# 检查是否有技能修改相同的配置文件
config_modifiers=$(grep -r "config\|\.env\|settings" "$SKILLS_DIR"/*/scripts/*.sh 2>/dev/null | grep -v "^Binary" | cut -d: -f1 | sort -u)
if [ -n "$config_modifiers" ]; then
    echo "- ⚠️ 可能修改配置的技能:" >> "$CONFLICTS_FILE"
    echo "$config_modifiers" | while read f; do
        skill_name=$(basename $(dirname $(dirname $f)))
        echo "  - $skill_name: $(basename $f)" >> "$CONFLICTS_FILE"
    done
fi
echo "" >> "$CONFLICTS_FILE"

# 总结
echo "---" >> "$CONFLICTS_FILE"
echo "" >> "$CONFLICTS_FILE"
echo "## 📊 总结" >> "$CONFLICTS_FILE"
echo "" >> "$CONFLICTS_FILE"
if [ "$conflicts_found" -eq 0 ]; then
    echo "✅ 未检测到严重冲突" >> "$CONFLICTS_FILE"
else
    echo "⚠️ 发现 $conflicts_found 类潜在冲突，建议运行 merge-skills.sh 进行整合" >> "$CONFLICTS_FILE"
fi

echo ""
echo "📄 冲突报告已生成: $CONFLICTS_FILE"
cat "$CONFLICTS_FILE"
