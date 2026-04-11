#!/bin/bash
# 冗余检测与清理脚本

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
CONFIG_FILE="$SKILLS_DIR/auto-skill-upgrade/skills-config.json"
REPORT_FILE="$SKILLS_DIR/auto-skill-upgrade/redundancy-report.md"

echo "# 冗余检测报告" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "生成时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 1. 检测功能重叠
echo "## 功能重叠检测" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 图像处理
echo "### 图像处理技能" >> "$REPORT_FILE"
image_skills=$(grep -l "image\|图片\|图像\|vision" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | xargs -I {} basename $(dirname {}))
if [ -n "$image_skills" ]; then
  echo "$image_skills" | while read s; do
    echo "- $s" >> "$REPORT_FILE"
  done
  echo "" >> "$REPORT_FILE"
  echo "**建议**: 使用 xiaoyi-image-understanding 作为统一入口" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 文档处理
echo "### 文档处理技能" >> "$REPORT_FILE"
doc_skills=$(grep -l "doc\|pdf\|pptx\|excel\|文档" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | xargs -I {} basename $(dirname {}))
if [ -n "$doc_skills" ]; then
  echo "$doc_skills" | while read s; do
    echo "- $s" >> "$REPORT_FILE"
  done
  echo "" >> "$REPORT_FILE"
  echo "**建议**: 使用 xiaoyi-doc-convert 作为统一入口" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 搜索
echo "### 搜索技能" >> "$REPORT_FILE"
search_skills=$(grep -l "search\|搜索\|联网" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | xargs -I {} basename $(dirname {}))
if [ -n "$search_skills" ]; then
  echo "$search_skills" | while read s; do
    echo "- $s" >> "$REPORT_FILE"
  done
  echo "" >> "$REPORT_FILE"
  echo "**建议**: 使用 deep-search-and-insight-synthesize 作为统一入口" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 2. 检测未使用技能
echo "## 低使用率技能检测" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "需要手动检查使用日志..." >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 3. 检测依赖冲突
echo "## 依赖冲突检测" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 检查重复依赖
all_requirements=$(cat "$SKILLS_DIR"/*/requirements.txt 2>/dev/null | sort | uniq -c | sort -rn)
dup_deps=$(echo "$all_requirements" | awk '$1 > 1 {print $2}')
if [ -n "$dup_deps" ]; then
  echo "重复依赖包:" >> "$REPORT_FILE"
  echo "$dup_deps" | while read dep; do
    echo "- $dep" >> "$REPORT_FILE"
  done
else
  echo "✅ 无依赖冲突" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 4. 生成清理建议
echo "## 清理建议" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "1. 建立技能调用链，避免重复调用" >> "$REPORT_FILE"
echo "2. 使用统一入口技能" >> "$REPORT_FILE"
echo "3. 定期检查低使用率技能" >> "$REPORT_FILE"
echo "4. 合并功能相似的技能" >> "$REPORT_FILE"

echo "📄 冗余报告已生成: $REPORT_FILE"
cat "$REPORT_FILE"
