#!/bin/bash
# realtime-monitor.sh - 实时监控脚本
# 用于 heartbeat 或 cron 触发的后台监控

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$BASE_DIR")"
STATE_FILE="$BASE_DIR/.monitor-state.json"

# 初始化状态文件
init_state() {
    if [ ! -f "$STATE_FILE" ]; then
        cat > "$STATE_FILE" << EOF
{
  "last_upgrade": "$(date -Iseconds)",
  "last_skill_count": 168,
  "last_health_score": 100,
  "upgrade_count": 0
}
EOF
    fi
}

# 检查是否需要升级
check_upgrade_needed() {
    local last_upgrade=$(jq -r '.last_upgrade' "$STATE_FILE" 2>/dev/null)
    local now=$(date +%s)
    local last=$(date -d "$last_upgrade" +%s 2>/dev/null || echo "0")
    local diff=$(( (now - last) / 3600 ))  # 小时差
    
    if [ "$diff" -ge 6 ]; then
        echo "⏰ 距离上次升级已 $diff 小时，建议执行自动升级"
        return 0
    fi
    return 1
}

# 检查技能变化
check_skill_changes() {
    local current_count=$(ls -d "$WORKSPACE_DIR/skills"/*/ 2>/dev/null | wc -l)
    local last_count=$(jq -r '.last_skill_count' "$STATE_FILE" 2>/dev/null)
    
    if [ "$current_count" -ne "$last_count" ]; then
        echo "📦 技能数量变化: $last_count → $current_count"
        jq ".last_skill_count = $current_count" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
        return 0
    fi
    return 1
}

# 检查架构健康度
check_health_score() {
    local report="$BASE_DIR/architecture-report.md"
    if [ -f "$report" ]; then
        local current_score=$(grep "健康度" "$report" | grep -oP '\d+' | head -1)
        local last_score=$(jq -r '.last_health_score' "$STATE_FILE" 2>/dev/null)
        
        if [ -n "$current_score" ] && [ "$current_score" -lt 90 ]; then
            echo "⚠️ 架构健康度下降: $last_score → $current_score"
            return 0
        fi
    fi
    return 1
}

# 主监控逻辑
main() {
    init_state
    
    echo "🔍 实时监控检查 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=========================================="
    
    local need_upgrade=false
    
    # 检查各项指标
    if check_upgrade_needed; then
        need_upgrade=true
    fi
    
    if check_skill_changes; then
        need_upgrade=true
    fi
    
    if check_health_score; then
        need_upgrade=true
    fi
    
    # 输出建议
    echo ""
    if [ "$need_upgrade" = true ]; then
        echo "💡 建议: 执行自动升级"
        echo "🤖 OMEGA_FINAL 自动执行模式已启用"
        
        # 自动执行升级
        echo "🚀 自动执行升级..."
        bash "$BASE_DIR/scripts/auto-upgrade-ultimate.sh"
    else
        echo "✅ 系统状态良好，无需升级"
    fi
}

main "$@"
