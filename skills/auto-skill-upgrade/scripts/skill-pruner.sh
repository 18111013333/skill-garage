#!/bin/bash
# 技能精简脚本 - 优化大型 SKILL.md 文件

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
THRESHOLD=8000  # 8KB 以上视为大文件

echo "🔍 扫描大型 SKILL.md 文件..."
echo ""

for skill_dir in "$SKILLS_DIR"/*/; do
  skill_name=$(basename "$skill_dir")
  skill_file="$skill_dir/SKILL.md"
  
  if [ -f "$skill_file" ]; then
    size=$(wc -c < "$skill_file")
    lines=$(wc -l < "$skill_file")
    
    if [ "$size" -gt "$THRESHOLD" ]; then
      echo "⚠️ $skill_name: ${size}B, ${lines}行"
      
      # 检查是否有 references 目录
      if [ ! -d "$skill_dir/references" ]; then
        echo "   💡 建议: 创建 references/ 目录，移出详细文档"
      fi
      
      # 检查是否有过长的示例
      example_count=$(grep -c '```' "$skill_file" 2>/dev/null || echo 0)
      if [ "$example_count" -gt 10 ]; then
        echo "   💡 建议: 示例代码过多，移至 references/examples.md"
      fi
    fi
  fi
done

echo ""
echo "✅ 扫描完成"
