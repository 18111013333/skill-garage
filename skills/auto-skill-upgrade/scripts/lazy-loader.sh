#!/bin/bash
# 懒加载机制 - 按需加载技能

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
QUICK_LOAD="$SKILLS_DIR/auto-skill-upgrade/quick-load.txt"
CACHE_FILE="$SKILLS_DIR/auto-skill-upgrade/.loaded_skills"

# 初始化缓存
if [ ! -f "$CACHE_FILE" ]; then
  touch "$CACHE_FILE"
fi

# 检查技能是否已加载
is_loaded() {
  grep -q "^$1$" "$CACHE_FILE" 2>/dev/null
}

# 标记技能为已加载
mark_loaded() {
  echo "$1" >> "$CACHE_FILE"
}

# 加载核心技能 (P0)
load_core_skills() {
  echo "📦 加载核心技能 (P0)..."
  while read skill; do
    # 跳过注释和空行
    [[ "$skill" =~ ^#.*$ ]] && continue
    [[ -z "$skill" ]] && continue
    
    if ! is_loaded "$skill"; then
      if [ -d "$SKILLS_DIR/$skill" ]; then
        echo "  ✅ $skill"
        mark_loaded "$skill"
      fi
    else
      echo "  ⏭️ $skill (已加载)"
    fi
  done < "$QUICK_LOAD"
}

# 按需加载技能
load_skill() {
  local skill="$1"
  
  if is_loaded "$skill"; then
    echo "⏭️ $skill 已在缓存中"
    return 0
  fi
  
  if [ -d "$SKILLS_DIR/$skill" ]; then
    echo "📦 加载 $skill..."
    mark_loaded "$skill"
    return 0
  else
    echo "❌ 技能 $skill 不存在"
    return 1
  fi
}

# 按类别加载
load_category() {
  local category="$1"
  echo "📦 加载类别: $category"
  
  ls -1 "$SKILLS_DIR" | while read skill; do
    if [ -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
      if grep -q "$category" "$SKILLS_DIR/$skill/SKILL.md" 2>/dev/null; then
        load_skill "$skill"
      fi
    fi
  done
}

# 清除缓存
clear_cache() {
  > "$CACHE_FILE"
  echo "🗑️ 缓存已清除"
}

# 显示已加载技能
show_loaded() {
  echo "📋 已加载技能:"
  cat "$CACHE_FILE" 2>/dev/null | nl
}

# 主逻辑
case "$1" in
  core)
    load_core_skills
    ;;
  skill)
    load_skill "$2"
    ;;
  category)
    load_category "$2"
    ;;
  clear)
    clear_cache
    ;;
  list)
    show_loaded
    ;;
  *)
    echo "用法: $0 <core|skill|category|clear|list> [参数]"
    echo ""
    echo "命令:"
    echo "  core          - 加载所有核心技能 (P0)"
    echo "  skill <name>  - 加载指定技能"
    echo "  category <cat>- 加载指定类别技能"
    echo "  clear         - 清除加载缓存"
    echo "  list          - 显示已加载技能"
    ;;
esac
