#!/bin/bash
# 使用频率追踪脚本 - 记录技能使用情况

STATS_FILE="$HOME/.openclaw/workspace/skills/auto-skill-upgrade/usage-stats.json"
CONFIG_FILE="$HOME/.openclaw/workspace/skills/auto-skill-upgrade/skills-config.json"

# 记录技能使用
track_usage() {
    local skill_name="$1"
    local timestamp=$(date -Iseconds)
    
    if [ ! -f "$STATS_FILE" ]; then
        echo '{"version":"1.0.0","stats":{}}' > "$STATS_FILE"
    fi
    
    # 使用 jq 更新统计（如果可用）
    if command -v jq &> /dev/null; then
        tmp=$(mktemp)
        jq --arg skill "$skill_name" --arg ts "$timestamp" '
            if .stats[$skill] then
                .stats[$skill].count += 1 |
                .stats[$skill].lastUsed = $ts
            else
                .stats[$skill] = {"count": 1, "lastUsed": $ts, "category": "unknown"}
            end |
            .lastUpdate = $ts
        ' "$STATS_FILE" > "$tmp" && mv "$tmp" "$STATS_FILE"
    else
        # 简单追加日志
        echo "$(date '+%Y-%m-%d %H:%M:%S') USAGE $skill_name" >> "$HOME/.openclaw/workspace/skills/auto-skill-upgrade/usage.log"
    fi
}

# 获取低使用率技能
get_low_usage() {
    local threshold="${1:-5}"
    
    if command -v jq &> /dev/null && [ -f "$STATS_FILE" ]; then
        jq -r --argjson thresh "$threshold" '
            .stats | to_entries[] | 
            select(.value.count < $thresh) | 
            "\(.key): \(.value.count)"
        ' "$STATS_FILE"
    fi
}

# 获取热门技能
get_top_skills() {
    local limit="${1:-10}"
    
    if command -v jq &> /dev/null && [ -f "$STATS_FILE" ]; then
        jq -r --argjson limit "$limit" '
            .stats | to_entries | 
            sort_by(-.value.count) | 
            .[:$limit] | 
            .[] | 
            "\(.key): \(.value.count) uses"
        ' "$STATS_FILE"
    fi
}

# 生成使用报告
generate_report() {
    local report_file="$HOME/.openclaw/workspace/skills/auto-skill-upgrade/usage-report.md"
    
    cat > "$report_file" << EOF
# 技能使用报告

生成时间: $(date '+%Y-%m-%d %H:%M:%S')

---

## 📊 使用统计

EOF

    if command -v jq &> /dev/null && [ -f "$STATS_FILE" ]; then
        local total=$(jq '.stats | length' "$STATS_FILE")
        local total_uses=$(jq '[.stats[].count] | add // 0' "$STATS_FILE")
        local active=$(jq '[.stats[] | select(.count > 0)] | length' "$STATS_FILE")
        
        cat >> "$report_file" << EOF
| 指标 | 数值 |
|------|------|
| 总技能数 | $total |
| 总使用次数 | $total_uses |
| 活跃技能 | $active |
| 未使用技能 | $((total - active)) |

---

## 🔥 热门技能 (Top 10)

\`\`\`
$(get_top_skills 10)
\`\`\`

---

## 💤 低使用率技能 (使用 < 5 次)

\`\`\`
$(get_low_usage 5)
\`\`\`

EOF
    else
        echo "⚠️ jq 未安装或统计文件不存在" >> "$report_file"
    fi
    
    echo "📄 报告已生成: $report_file"
}

# 主逻辑
case "${1:-}" in
    track)
        track_usage "$2"
        ;;
    low)
        get_low_usage "${2:-5}"
        ;;
    top)
        get_top_skills "${2:-10}"
        ;;
    report)
        generate_report
        ;;
    *)
        echo "用法: $0 <track|low|top|report> [skill_name|threshold|limit]"
        echo ""
        echo "  track <skill>  - 记录技能使用"
        echo "  low [n]        - 获取使用次数 < n 的技能"
        echo "  top [n]        - 获取使用次数最高的 n 个技能"
        echo "  report         - 生成使用报告"
        ;;
esac
