#!/bin/bash
# 技能扫描脚本 - 扫描所有已安装技能并生成清单

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
OUTPUT_FILE="$HOME/.openclaw/workspace/skills/auto-skill-upgrade/skills-inventory.json"

echo "🔍 扫描技能目录: $SKILLS_DIR"

# 初始化 JSON 结构
echo '{"version": "1.0.0", "scanTime": "'$(date -Iseconds)'", "skills": [' > "$OUTPUT_FILE"

first=true
total=0
categories={}

# 遍历所有技能目录
for skill_dir in "$SKILLS_DIR"/*/; do
    if [ -f "$skill_dir/SKILL.md" ]; then
        skill_name=$(basename "$skill_dir")
        
        # 提取技能描述（从 SKILL.md 第一行）
        description=$(head -1 "$skill_dir/SKILL.md" | sed 's/^# //')
        
        # 检测技能类别
        category="other"
        case "$skill_name" in
            xiaoyi-*) category="xiaoyi" ;;
            *doc*|*pdf*|*pptx*|*excel*) category="document" ;;
            *image*|*video*|*audio*) category="multimedia" ;;
            *git*|*code*|*dev*) category="development" ;;
            *memory*|*brain*) category="core" ;;
            *search*|*web*) category="search" ;;
        esac
        
        # 检测依赖
        dependencies=""
        if [ -f "$skill_dir/requirements.txt" ]; then
            dependencies=$(cat "$skill_dir/requirements.txt" | tr '\n' ',' | sed 's/,$//')
        fi
        
        # 写入 JSON
        if [ "$first" = true ]; then
            first=false
        else
            echo ',' >> "$OUTPUT_FILE"
        fi
        
        cat >> "$OUTPUT_FILE" << EOF
    {
      "name": "$skill_name",
      "path": "$skill_dir",
      "description": "$description",
      "category": "$category",
      "dependencies": "$dependencies",
      "hasScripts": $([ -d "$skill_dir/scripts" ] && echo 'true' || echo 'false'),
      "hasConfig": $([ -f "$skill_dir/config" ] && echo 'true' || echo 'false')
    }
EOF
        
        ((total++))
        echo "  ✅ $skill_name [$category]"
    fi
done

# 完成 JSON
echo '], "total": '$total', "categories": {' >> "$OUTPUT_FILE"

# 统计各类别数量
for cat in xiaoyi document multimedia development core search other; do
    count=$(grep -c "\"category\": \"$cat\"" "$OUTPUT_FILE" 2>/dev/null || echo 0)
    echo "\"$cat\": $count," >> "$OUTPUT_FILE"
done

echo '"_placeholder": 0}}' >> "$OUTPUT_FILE"

echo ""
echo "📊 扫描完成: 共 $total 个技能"
echo "📄 清单已保存: $OUTPUT_FILE"
