#!/bin/bash
# 技能安装后钩子 - 自动触发自进化升级

SKILL_NAME="$1"
SKILLS_DIR="$HOME/.openclaw/workspace/skills"
LOG_FILE="$SKILLS_DIR/auto-skill-upgrade/logs/integration-hook.log"

mkdir -p "$(dirname "$LOG_FILE")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 新技能安装: $SKILL_NAME" >> "$LOG_FILE"

# 触发自进化
bash "$SKILLS_DIR/auto-skill-upgrade/scripts/auto-evolve.sh" >> "$LOG_FILE" 2>&1

# 发送通知
echo "✅ 技能 $SKILL_NAME 已安装并整合到架构"
