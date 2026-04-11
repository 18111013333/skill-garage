#!/bin/bash
# 自动清理脚本 - 清理低使用率或冗余技能

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
STATS_FILE="$SKILLS_DIR/auto-skill-upgrade/usage-stats.json"
CONFIG_FILE="$SKILLS_DIR/auto-skill-upgrade/skills-config.json"
CLEANUP_LOG="$SKILLS_DIR/auto-skill-upgrade/cleanup-log.md"
DISABLED_DIR="$SKILLS_DIR/.disabled"

# 创建禁用目录
mkdir -p "$DISABLED_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$CLEANUP_LOG"
}

# 禁用技能（移动到 .disabled 目录）
disable_skill() {
    local skill_name="$1"
    local reason="$2"
    
    if [ -d "$SKILLS_DIR/$skill_name" ]; then
        mv "$SKILLS_DIR/$skill_name" "$DISABLED_DIR/"
        log "🚫 已禁用: $skill_name (原因: $reason)"
        
        # 更新配置
        if command -v jq &> /dev/null && [ -f "$CONFIG_FILE" ]; then
            tmp=$(mktemp)
            jq --arg skill "$skill_name" '
                .disabledSkills = (.disabledSkills // []) + [$skill]
            ' "$CONFIG_FILE" > "$tmp" && mv "$tmp" "$CONFIG_FILE"
        fi
    fi
}

# 启用技能
enable_skill() {
    local skill_name="$1"
    
    if [ -d "$DISABLED_DIR/$skill_name" ]; then
        mv "$DISABLED_DIR/$skill_name" "$SKILLS_DIR/"
        log "✅ 已启用: $skill_name"
        
        # 更新配置
        if command -v jq &> /dev/null && [ -f "$CONFIG_FILE" ]; then
            tmp=$(mktemp)
            jq --arg skill "$skill_name" '
                .disabledSkills = (.disabledSkills // []) | map(select(. != $skill))
            ' "$CONFIG_FILE" > "$tmp" && mv "$tmp" "$CONFIG_FILE"
        fi
    fi
}

# 检测冗余技能
detect_redundant() {
    local redundant_list="$SKILLS_DIR/auto-skill-upgrade/redundant-skills.txt"
    
    log "🔍 检测冗余技能..."
    
    # 图像处理冗余（保留 xiaoyi-image-understanding）
    local image_skills=$(grep -l "image\|图片\|图像" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | grep -v xiaoyi | wc -l)
    if [ "$image_skills" -gt 5 ]; then
        log "⚠️ 图像技能冗余: $image_skills 个 (建议保留 xiaoyi-image-understanding)"
    fi
    
    # 文档处理冗余（保留 xiaoyi-doc-convert）
    local doc_skills=$(grep -l "doc\|pdf\|文档" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | grep -v xiaoyi | wc -l)
    if [ "$doc_skills" -gt 5 ]; then
        log "⚠️ 文档技能冗余: $doc_skills 个 (建议保留 xiaoyi-doc-convert)"
    fi
    
    # 搜索冗余（保留 xiaoyi-web-search）
    local search_skills=$(grep -l "search\|搜索" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | grep -v xiaoyi | wc -l)
    if [ "$search_skills" -gt 5 ]; then
        log "⚠️ 搜索技能冗余: $search_skills 个 (建议保留 xiaoyi-web-search)"
    fi
}

# 清理零使用技能
cleanup_zero_usage() {
    local days="${1:-30}"
    local threshold_date=$(date -d "-$days days" +%s 2>/dev/null || date -v-${days}d +%s)
    
    log "🧹 清理 $days 天内零使用的技能..."
    
    if [ ! -f "$STATS_FILE" ]; then
        log "⚠️ 统计文件不存在，跳过清理"
        return
    fi
    
    # 获取零使用技能列表
    if command -v jq &> /dev/null; then
        local zero_skills=$(jq -r '.stats | to_entries[] | select(.value.count == 0) | .key' "$STATS_FILE" 2>/dev/null)
        
        if [ -n "$zero_skills" ]; then
            echo "$zero_skills" | while read skill; do
                # 检查是否为核心技能
                local is_core=$(jq -r --arg skill "$skill" '
                    .categories.core | index($skill) // -1
                ' "$CONFIG_FILE" 2>/dev/null)
                
                if [ "$is_core" = "-1" ] && [ "$is_core" != "null" ]; then
                    log "💡 建议禁用: $skill (零使用)"
                    # 不自动禁用，只记录建议
                else
                    log "⏭️ 跳过核心技能: $skill"
                fi
            done
        fi
    fi
}

# 生成清理报告
generate_cleanup_report() {
    local report="$SKILLS_DIR/auto-skill-upgrade/cleanup-report.md"
    
    cat > "$report" << EOF
# 技能清理报告

生成时间: $(date '+%Y-%m-%d %H:%M:%S')

---

## 📊 清理统计

| 指标 | 数值 |
|------|------|
| 总技能数 | $(ls -1 "$SKILLS_DIR" | grep -v "^\." | wc -l) |
| 已禁用 | $(ls -1 "$DISABLED_DIR" 2>/dev/null | wc -l) |
| 零使用 | $(jq '[.stats[] | select(.count == 0)] | length' "$STATS_FILE" 2>/dev/null || echo "N/A") |

---

## 🚫 已禁用技能

\`\`\`
$(ls -1 "$DISABLED_DIR" 2>/dev/null || echo "无")
\`\`\`

---

## 💡 清理建议

EOF

    detect_redundant >> "$report"
    
    echo "📄 报告已生成: $report"
}

# 主逻辑
case "${1:-}" in
    disable)
        disable_skill "$2" "$3"
        ;;
    enable)
        enable_skill "$2"
        ;;
    detect)
        detect_redundant
        ;;
    cleanup)
        cleanup_zero_usage "${2:-30}"
        ;;
    report)
        generate_cleanup_report
        ;;
    list-disabled)
        ls -1 "$DISABLED_DIR" 2>/dev/null
        ;;
    *)
        echo "用法: $0 <disable|enable|detect|cleanup|report|list-disabled> [args]"
        echo ""
        echo "  disable <skill> [reason]  - 禁用技能"
        echo "  enable <skill>            - 启用技能"
        echo "  detect                    - 检测冗余技能"
        echo "  cleanup [days]            - 清理零使用技能"
        echo "  report                    - 生成清理报告"
        echo "  list-disabled             - 列出已禁用技能"
        ;;
esac
