#!/bin/bash
# 配置加载器 - 按需加载配置

UNIFIED_CONFIG="$HOME/.openclaw/workspace/unified-config.yaml"

# 加载 API 密钥
load_api_keys() {
  if [ -f "$HOME/.openclaw/workspace/.env" ]; then
    source "$HOME/.openclaw/workspace/.env"
  fi
}

# 加载技能索引
load_skill_index() {
  local index_file="$HOME/.openclaw/workspace/skills/auto-skill-upgrade/skill-index.json"
  if [ -f "$index_file" ]; then
    cat "$index_file"
  fi
}

# 获取技能优先级
get_skill_priority() {
  local skill=$1
  # 从配置中获取优先级
  echo "P1"
}

# 主入口
case "$1" in
  api)
    load_api_keys
    ;;
  skills)
    load_skill_index
    ;;
  priority)
    get_skill_priority "$2"
    ;;
  *)
    load_api_keys
    ;;
esac
