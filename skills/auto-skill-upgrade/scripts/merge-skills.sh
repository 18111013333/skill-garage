#!/bin/bash
# 技能整合脚本 v2 - 自动整合相似或互补的技能

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
CONFIG_FILE="$SKILLS_DIR/auto-skill-upgrade/skills-config.json"
CONFLICTS_FILE="$SKILLS_DIR/auto-skill-upgrade/conflicts-report.md"
MERGE_LOG="$SKILLS_DIR/auto-skill-upgrade/merge-log.md"

echo "🔄 开始技能整合..."

# 初始化整合日志
cat > "$MERGE_LOG" << EOF
# 技能整合日志

时间: $(date '+%Y-%m-%d %H:%M:%S')

---

## 🔄 整合操作

EOF

# 1. 分类技能
echo "### 📂 技能分类" >> "$MERGE_LOG"

# 从配置文件读取分类
if [ -f "$CONFIG_FILE" ] && command -v jq &> /dev/null; then
    for category in $(jq -r '.categories | keys[]' "$CONFIG_FILE" 2>/dev/null); do
        skills=$(jq -r --arg cat "$category" '.categories[$cat][]' "$CONFIG_FILE" 2>/dev/null)
        count=$(echo "$skills" | wc -l)
        echo "- **$category**: $count 个技能" >> "$MERGE_LOG"
    done
else
    # 回退到简单分类
    for skill_dir in "$SKILLS_DIR"/*/; do
        if [ -f "$skill_dir/SKILL.md" ]; then
            skill_name=$(basename "$skill_dir")
            
            category="other"
            case "$skill_name" in
                xiaoyi-*) category="xiaoyi" ;;
                *doc*|*pdf*|*pptx*|*excel*|*markitdown*) category="document" ;;
                *image*|*video*|*audio*|*seedream*|*seedance*) category="multimedia" ;;
                *git*|*code*|*dev*|*webapp*) category="development" ;;
                *search*|*web*|*brain*) category="search" ;;
                *memory*|*ontology*|*self-improvement*) category="core" ;;
            esac
            
            echo "- $skill_name → $category" >> "$MERGE_LOG"
        fi
    done
fi

echo "" >> "$MERGE_LOG"

# 2. 建立技能链
echo "### 🔗 技能链建立" >> "$MERGE_LOG"

if [ -f "$CONFIG_FILE" ] && command -v jq &> /dev/null; then
    for chain in $(jq -r '.chains | keys[]' "$CONFIG_FILE" 2>/dev/null); do
        entry=$(jq -r --arg chain "$chain" '.chains[$chain].entry // empty' "$CONFIG_FILE" 2>/dev/null)
        skills=$(jq -r --arg chain "$chain" '.chains[$chain].skills | join(",")' "$CONFIG_FILE" 2>/dev/null)
        priority=$(jq -r --arg chain "$chain" '.chains[$chain].priority // 50' "$CONFIG_FILE" 2>/dev/null)
        
        if [ -n "$entry" ]; then
            echo "- **$chain**: $entry → [$skills] (优先级: $priority)" >> "$MERGE_LOG"
        fi
    done
else
    # 回退到默认链
    echo "- 📄 文档转换链: xiaoyi-file-upload,xiaoyi-doc-convert" >> "$MERGE_LOG"
    echo "- 🖼️ 图像处理链: xiaoyi-image-search,xiaoyi-image-understanding,seedream-image_gen" >> "$MERGE_LOG"
    echo "- 🔍 搜索链: xiaoyi-web-search,deep-search-and-insight-synthesize" >> "$MERGE_LOG"
fi

echo "" >> "$MERGE_LOG"

# 3. 检测并记录整合建议
echo "### 💡 整合建议" >> "$MERGE_LOG"

# 检查图像相关技能
image_skills=$(find "$SKILLS_DIR" -name "SKILL.md" -exec grep -l "image\|图片\|图像" {} \; 2>/dev/null | wc -l)
if [ "$image_skills" -gt 3 ]; then
    echo "- ⚠️ 图像技能建议整合为统一入口" >> "$MERGE_LOG"
    echo "  - 建立优先级: xiaoyi-image-understanding > image-search > seedream" >> "$MERGE_LOG"
fi

# 检查文档相关技能
doc_skills=$(find "$SKILLS_DIR" -name "SKILL.md" -exec grep -l "doc\|pdf\|文档" {} \; 2>/dev/null | wc -l)
if [ "$doc_skills" -gt 5 ]; then
    echo "- ⚠️ 文档技能建议建立调用链" >> "$MERGE_LOG"
    echo "  - xiaoyi-doc-convert 作为统一入口，内部调用 docx/pdf/pptx" >> "$MERGE_LOG"
fi

echo "" >> "$MERGE_LOG"

# 4. 更新统计
echo "### 📊 技能统计" >> "$MERGE_LOG"

total_count=$(find "$SKILLS_DIR" -maxdepth 1 -type d | tail -n +2 | wc -l)
xiaoyi_count=$(find "$SKILLS_DIR" -maxdepth 1 -type d -name "xiaoyi-*" | wc -l)

echo "- 总计: $total_count 个技能" >> "$MERGE_LOG"
echo "- 小艺系列: $xiaoyi_count 个" >> "$MERGE_LOG"

# 5. 完成报告
echo "" >> "$MERGE_LOG"
echo "---" >> "$MERGE_LOG"
echo "" >> "$MERGE_LOG"
echo "## ✅ 整合完成" >> "$MERGE_LOG"
echo "" >> "$MERGE_LOG"
echo "配置文件: $CONFIG_FILE" >> "$MERGE_LOG"
echo "整合日志: $MERGE_LOG" >> "$MERGE_LOG"

echo ""
echo "✅ 技能整合完成"
echo "📄 配置文件: $CONFIG_FILE"
echo "📄 整合日志: $MERGE_LOG"
