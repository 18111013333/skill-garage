#!/bin/bash
# 技能推荐系统 - 根据用户行为推荐技能

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
STATS_FILE="$SKILLS_DIR/auto-skill-upgrade/usage-stats.json"
CONFIG_FILE="$SKILLS_DIR/auto-skill-upgrade/skills-config.json"
RECOMMEND_FILE="$SKILLS_DIR/auto-skill-upgrade/recommendations.md"

# 技能关联规则（哪些技能经常一起使用）
declare -A SKILL_ASSOCIATIONS=(
    ["xiaoyi-web-search"]="deep-search-and-insight-synthesize,prismfy-search"
    ["xiaoyi-image-understanding"]="xiaoyi-image-search,seedream-image_gen"
    ["xiaoyi-doc-convert"]="docx,pdf,pptx,markitdown"
    ["git"]="docker,terraform,ansible"
    ["article-writer"]="copywriter,personas,best-minds"
    ["china-stock-analysis"]="tushare,mx-finance-data,stock-price-query"
    ["data-analysis"]="excel-analysis,chart-image"
    ["video-cog"]="video-agent,video-subtitles,audio-cog"
)

# 任务类型推荐
declare -A TASK_RECOMMENDATIONS=(
    ["搜索调研"]="xiaoyi-web-search,deep-search-and-insight-synthesize,prismfy-search"
    ["文档处理"]="xiaoyi-doc-convert,docx,pdf,pptx"
    ["图像处理"]="xiaoyi-image-understanding,xiaoyi-image-search,seedream-image_gen"
    ["代码开发"]="git,docker,code-analysis-skills,webapp-testing"
    ["内容创作"]="article-writer,copywriter,story-cog,personas"
    ["金融分析"]="china-stock-analysis,tushare,mx-finance-data"
    ["数据分析"]="data-analysis,excel-analysis,chart-image"
    ["视频处理"]="video-cog,video-agent,video-subtitles"
    ["自动化"]="playwright,cron,scrapling-official"
)

# 根据使用历史推荐
recommend_by_history() {
    local top_skill="$1"
    
    if [ -n "${SKILL_ASSOCIATIONS[$top_skill]}" ]; then
        echo "基于 '$top_skill' 的使用，推荐:"
        echo "${SKILL_ASSOCIATIONS[$top_skill]}" | tr ',' '\n' | while read skill; do
            echo "  - $skill"
        done
    fi
}

# 根据任务类型推荐
recommend_by_task() {
    local task_type="$1"
    
    if [ -n "${TASK_RECOMMENDATIONS[$task_type]}" ]; then
        echo "任务 '$task_type' 推荐技能:"
        echo "${TASK_RECOMMENDATIONS[$task_type]}" | tr ',' '\n' | while read skill; do
            # 检查是否已安装
            if [ -d "$SKILLS_DIR/$skill" ]; then
                echo "  ✅ $skill (已安装)"
            else
                echo "  ⏳ $skill (未安装)"
            fi
        done
    else
        echo "未知任务类型: $task_type"
        echo "可用任务类型: ${!TASK_RECOMMENDATIONS[@]}"
    fi
}

# 智能推荐（基于使用频率）
smart_recommend() {
    if [ ! -f "$STATS_FILE" ]; then
        echo "⚠️ 统计文件不存在"
        return
    fi
    
    if command -v jq &> /dev/null; then
        # 获取最常用的技能
        local top_skill=$(jq -r '.stats | to_entries | sort_by(-.value.count) | .[0].key // empty' "$STATS_FILE" 2>/dev/null)
        
        if [ -n "$top_skill" ]; then
            echo "🎯 基于您的使用习惯，推荐:"
            recommend_by_history "$top_skill"
        else
            echo "💡 暂无足够使用数据，推荐核心技能:"
            echo "  - xiaoyi-web-search"
            echo "  - xiaoyi-image-understanding"
            echo "  - xiaoyi-doc-convert"
        fi
    fi
}

# 生成推荐报告
generate_recommendations() {
    cat > "$RECOMMEND_FILE" << EOF
# 技能推荐报告

生成时间: $(date '+%Y-%m-%d %H:%M:%S')

---

## 🎯 智能推荐

EOF

    smart_recommend >> "$RECOMMEND_FILE"
    
    cat >> "$RECOMMEND_FILE" << EOF

---

## 📋 任务类型推荐

| 任务类型 | 推荐技能 |
|----------|----------|
EOF

    for task in "${!TASK_RECOMMENDATIONS[@]}"; do
        echo "| $task | ${TASK_RECOMMENDATIONS[$task]} |" >> "$RECOMMEND_FILE"
    done
    
    cat >> "$RECOMMEND_FILE" << EOF

---

## 🔗 技能关联

| 技能 | 关联技能 |
|------|----------|
EOF

    for skill in "${!SKILL_ASSOCIATIONS[@]}"; do
        echo "| $skill | ${SKILL_ASSOCIATIONS[$skill]} |" >> "$RECOMMEND_FILE"
    done
    
    echo ""
    echo "📄 推荐报告已生成: $RECOMMEND_FILE"
}

# 主逻辑
case "${1:-}" in
    history)
        recommend_by_history "$2"
        ;;
    task)
        recommend_by_task "$2"
        ;;
    smart)
        smart_recommend
        ;;
    generate)
        generate_recommendations
        ;;
    list-tasks)
        echo "可用任务类型:"
        echo "${!TASK_RECOMMENDATIONS[@]}" | tr ' ' '\n'
        ;;
    *)
        echo "用法: $0 <history|task|smart|generate|list-tasks> [args]"
        echo ""
        echo "  history <skill>   - 基于技能推荐"
        echo "  task <type>       - 基于任务推荐"
        echo "  smart             - 智能推荐"
        echo "  generate          - 生成推荐报告"
        echo "  list-tasks        - 列出任务类型"
        ;;
esac
