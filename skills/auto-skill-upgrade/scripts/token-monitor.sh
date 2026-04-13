#!/bin/bash
# Token 监控脚本 - 分析和优化 Token 消耗

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
WORKSPACE="$HOME/.openclaw/workspace"
REPORT_FILE="$SKILLS_DIR/auto-skill-upgrade/token-report.md"

echo "📊 Token 消耗分析"
echo "=================="
echo ""

# 1. 计算 SKILL.md 总大小
total_skill_size=0
skill_count=0
for skill_dir in "$SKILLS_DIR"/*/; do
  if [ -f "$skill_dir/SKILL.md" ]; then
    size=$(wc -c < "$skill_dir/SKILL.md")
    total_skill_size=$((total_skill_size + size))
    skill_count=$((skill_count + 1))
  fi
done

# 估算 Token (1 token ≈ 4 bytes)
total_skill_tokens=$((total_skill_size / 4))
avg_skill_tokens=$((total_skill_tokens / skill_count))

echo "📁 SKILL.md 分析:"
echo "   技能数: $skill_count"
echo "   总大小: $((total_skill_size / 1024))KB"
echo "   估算 Token: ${total_skill_tokens}K"
echo "   平均 Token: ${avg_skill_tokens}K/技能"
echo ""

# 2. 计算 MEMORY.md 大小
if [ -f "$WORKSPACE/MEMORY.md" ]; then
  memory_size=$(wc -c < "$WORKSPACE/MEMORY.md")
  memory_tokens=$((memory_size / 4))
  echo "📝 MEMORY.md:"
  echo "   大小: $((memory_size / 1024))KB"
  echo "   估算 Token: ${memory_tokens}K"
  echo ""
fi

# 3. 计算每日记忆大小
memory_dir="$WORKSPACE/memory"
if [ -d "$memory_dir" ]; then
  daily_size=$(du -sb "$memory_dir" 2>/dev/null | cut -f1)
  daily_tokens=$((daily_size / 4))
  echo "📂 memory/ 目录:"
  echo "   大小: $((daily_size / 1024))KB"
  echo "   估算 Token: ${daily_tokens}K"
  echo ""
fi

# 4. 计算知识图谱大小
ontology_file="$WORKSPACE/memory/ontology/graph.jsonl"
if [ -f "$ontology_file" ]; then
  ontology_size=$(wc -c < "$ontology_file")
  ontology_tokens=$((ontology_size / 4))
  echo "🧠 知识图谱:"
  echo "   大小: $((ontology_size / 1024))KB"
  echo "   估算 Token: ${ontology_tokens}K"
  echo ""
fi

# 5. 生成报告
cat > "$REPORT_FILE" << EOF
# Token 消耗报告

生成时间: $(date '+%Y-%m-%d %H:%M:%S')

---

## 📊 Token 消耗统计

| 组件 | 大小 | 估算 Token |
|------|------|------------|
| SKILL.md (总计) | $((total_skill_size / 1024))KB | ${total_skill_tokens}K |
| MEMORY.md | $((memory_size / 1024))KB | ${memory_tokens}K |
| memory/ 目录 | $((daily_size / 1024))KB | ${daily_tokens}K |
| 知识图谱 | $((ontology_size / 1024))KB | ${ontology_tokens}K |

---

## 📈 优化建议

### 高优先级
1. **懒加载**: 只加载 P0 技能 (减少 70%)
2. **SKILL.md 精简**: 目标 <2KB/技能
3. **技能链合并**: 减少重复加载

### 中优先级
4. **记忆压缩**: 定期归档旧记录
5. **会话摘要**: 超过 50 轮自动摘要

---

## 🎯 目标

| 指标 | 当前 | 目标 |
|------|------|------|
| 启动 Token | ~${total_skill_tokens}K | ~150K |
| 平均技能 Token | ~${avg_skill_tokens}K | ~2K |

EOF

echo "📄 报告已生成: $REPORT_FILE"
