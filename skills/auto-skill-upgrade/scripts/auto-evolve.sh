#!/bin/bash
# 自进化自动触发脚本 v2 - 每次学习新技能时自动升级

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
LEARNINGS_DIR="$HOME/.openclaw/workspace/.learnings"
ONTOLOGY_DIR="$HOME/.openclaw/workspace/memory/ontology"
LOG_FILE="$SKILLS_DIR/auto-skill-upgrade/logs/auto-evolve.log"
STATS_FILE="$SKILLS_DIR/auto-skill-upgrade/usage-stats.json"
CONFIG_FILE="$SKILLS_DIR/auto-skill-upgrade/skills-config.json"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$LEARNINGS_DIR"
mkdir -p "$ONTOLOGY_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "========================================="
log "自进化自动升级触发"
log "========================================="

# 1. 检查新技能
log "1️⃣ 检查新技能..."
current_skills=$(ls -1 "$SKILLS_DIR" | grep -v "^\." | wc -l)
last_count_file="$SKILLS_DIR/auto-skill-upgrade/.last_skill_count"

if [ -f "$last_count_file" ]; then
  last_count=$(cat "$last_count_file")
else
  last_count=0
fi

new_count=0
if [ "$current_skills" -gt "$last_count" ]; then
  new_count=$((current_skills - last_count))
  log "✅ 检测到 $new_count 个新技能"
  
  # 记录新技能
  new_skills=$(comm -23 <(ls -1 "$SKILLS_DIR" | grep -v "^\." | sort) <(cat "$SKILLS_DIR/auto-skill-upgrade/.last_skills_list" 2>/dev/null | sort))
  if [ -n "$new_skills" ]; then
    log "新技能列表:"
    echo "$new_skills" | while read skill; do
      [ -n "$skill" ] && log "  + $skill"
    done
  fi
else
  log "⏭️ 无新技能"
fi

# 2. 运行技能升级
log "2️⃣ 运行技能升级..."
if [ -f "$SKILLS_DIR/auto-skill-upgrade/scripts/upgrade-skills.sh" ]; then
  bash "$SKILLS_DIR/auto-skill-upgrade/scripts/upgrade-skills.sh" >> "$LOG_FILE" 2>&1
fi

# 3. 更新知识图谱
log "3️⃣ 更新知识图谱..."
if [ -f "$SKILLS_DIR/auto-skill-upgrade/scripts/update-ontology.sh" ]; then
  bash "$SKILLS_DIR/auto-skill-upgrade/scripts/update-ontology.sh" >> "$LOG_FILE" 2>&1
fi

# 4. 检测冗余
log "4️⃣ 检测冗余技能..."
if [ -f "$SKILLS_DIR/auto-skill-upgrade/scripts/detect-redundancy.sh" ]; then
  bash "$SKILLS_DIR/auto-skill-upgrade/scripts/detect-redundancy.sh" >> "$LOG_FILE" 2>&1
fi

# 5. 更新使用统计
log "5️⃣ 更新使用统计..."
if [ -f "$STATS_FILE" ] && command -v jq &> /dev/null; then
  # 为新技能添加统计条目
  echo "$new_skills" | while read skill; do
    if [ -n "$skill" ]; then
      tmp=$(mktemp)
      jq --arg skill "$skill" --arg ts "$(date -Iseconds)" '
        if .stats[$skill] | not then
          .stats[$skill] = {"count": 0, "lastUsed": null, "category": "unknown"}
        end
      ' "$STATS_FILE" > "$tmp" && mv "$tmp" "$STATS_FILE"
    fi
  done
  log "  ✅ 使用统计已更新"
fi

# 6. 记录学习
log "6️⃣ 记录自进化学习..."
learning_entry="
## [LRN-$(date '+%Y%m%d')-$(date '+%H%M')] auto_evolution

**Logged**: $(date -Iseconds)
**Priority**: medium
**Status**: resolved
**Area**: self_evolution

### Summary
自动检测到 $new_count 个新技能，已完成架构升级

### Details
- 技能总数: $current_skills
- 新增技能: $new_count
- 冗余检测: 已完成
- 知识图谱: 已更新
- 使用统计: 已更新

### Metadata
- Source: auto_evolution
- Tags: self-evolution, auto-upgrade

---
"
echo "$learning_entry" >> "$LEARNINGS_DIR/LEARNINGS.md"

# 7. 更新计数
echo "$current_skills" > "$last_count_file"
ls -1 "$SKILLS_DIR" | grep -v "^\." > "$SKILLS_DIR/auto-skill-upgrade/.last_skills_list"

log "========================================="
log "✅ 自进化升级完成"
log "技能总数: $current_skills"
log "========================================="
