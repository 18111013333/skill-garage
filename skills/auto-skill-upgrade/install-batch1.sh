#!/bin/bash
# ClawHub Top 200 技能批量下载脚本
# 生成时间: 2026-04-06 03:26:00

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
LOG_FILE="$SKILLS_DIR/auto-skill-upgrade/install-log.md"
REPORT_FILE="$SKILLS_DIR/auto-skill-upgrade/install-report.md"

# 待安装技能列表
SKILLS=(
    "polymarket-trade"
    "admapix"
    "nano-banana-pro"
    "obsidian"
    "skill-finder-cn"
    "ai-ppt-generator"
    "peekaboo"
    "spotify-player"
    "oracle"
    "camsnap"
    "imsg"
    "mx-macro-data"
)

# 初始化日志
echo "# ClawHub 技能安装日志" > "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

total=${#SKILLS[@]}
success=0
failed=0
failed_list=()

echo "🚀 开始安装 $total 个技能..."
echo ""

for skill in "${SKILLS[@]}"; do
    echo "📦 安装: $skill"
    echo "### $skill" >> "$LOG_FILE"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
    
    # 安装技能
    if npx clawhub@latest install "$skill" 2>&1 | tee -a "$LOG_FILE"; then
        ((success++))
        echo "✅ 成功: $skill"
        echo "状态: ✅ 成功" >> "$LOG_FILE"
    else
        ((failed++))
        failed_list+=("$skill")
        echo "❌ 失败: $skill"
        echo "状态: ❌ 失败" >> "$LOG_FILE"
    fi
    
    echo "" >> "$LOG_FILE"
    
    # 速率限制：每次安装后等待 2 秒
    sleep 2
done

# 生成报告
echo "# ClawHub 技能安装报告" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "完成时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "## 📊 统计" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| 指标 | 数量 |" >> "$REPORT_FILE"
echo "|------|------|" >> "$REPORT_FILE"
echo "| 总计 | $total |" >> "$REPORT_FILE"
echo "| 成功 | $success |" >> "$REPORT_FILE"
echo "| 失败 | $failed |" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [ $failed -gt 0 ]; then
    echo "## ❌ 失败列表" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    for skill in "${failed_list[@]}"; do
        echo "- $skill" >> "$REPORT_FILE"
    done
fi

echo ""
echo "========================================="
echo "📊 安装完成"
echo "  总计: $total"
echo "  成功: $success"
echo "  失败: $failed"
echo "========================================="
echo ""
echo "📄 详细日志: $LOG_FILE"
echo "📄 安装报告: $REPORT_FILE"
