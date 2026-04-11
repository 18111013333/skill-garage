#!/bin/bash
# 技能升级脚本 - 完整的技能库升级流程

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
UPGRADE_DIR="$SKILLS_DIR/auto-skill-upgrade"
LOG_DIR="$UPGRADE_DIR/logs"
BACKUP_DIR="$UPGRADE_DIR/backups"

echo "🚀 开始技能库升级..."
echo ""

# 创建必要目录
mkdir -p "$LOG_DIR" "$BACKUP_DIR"

# 时间戳
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
UPGRADE_LOG="$LOG_DIR/upgrade_$TIMESTAMP.log"

# 初始化升级日志
cat > "$UPGRADE_LOG" << EOF
# 技能库升级日志

时间: $(date '+%Y-%m-%d %H:%M:%S')
版本: $TIMESTAMP

---

## 🔄 升级流程

EOF

# 1. 备份当前配置
echo "### 1️⃣ 备份配置" | tee -a "$UPGRADE_LOG"
backup_file="$BACKUP_DIR/config_$TIMESTAMP.json"
if [ -f "$UPGRADE_DIR/skills-config.json" ]; then
    cp "$UPGRADE_DIR/skills-config.json" "$backup_file"
    echo "✅ 配置已备份: $backup_file" | tee -a "$UPGRADE_LOG"
else
    echo "⚠️ 无现有配置，将创建新配置" | tee -a "$UPGRADE_LOG"
fi
echo "" | tee -a "$UPGRADE_LOG"

# 2. 扫描技能
echo "### 2️⃣ 扫描技能" | tee -a "$UPGRADE_LOG"
if [ -f "$UPGRADE_DIR/scripts/scan-skills.sh" ]; then
    bash "$UPGRADE_DIR/scripts/scan-skills.sh" 2>&1 | tee -a "$UPGRADE_LOG"
else
    echo "❌ 扫描脚本不存在" | tee -a "$UPGRADE_LOG"
fi
echo "" | tee -a "$UPGRADE_LOG"

# 3. 检测冲突
echo "### 3️⃣ 检测冲突" | tee -a "$UPGRADE_LOG"
if [ -f "$UPGRADE_DIR/scripts/detect-conflicts.sh" ]; then
    bash "$UPGRADE_DIR/scripts/detect-conflicts.sh" 2>&1 | tee -a "$UPGRADE_LOG"
else
    echo "❌ 冲突检测脚本不存在" | tee -a "$UPGRADE_LOG"
fi
echo "" | tee -a "$UPGRADE_LOG"

# 4. 整合技能
echo "### 4️⃣ 整合技能" | tee -a "$UPGRADE_LOG"
if [ -f "$UPGRADE_DIR/scripts/merge-skills.sh" ]; then
    bash "$UPGRADE_DIR/scripts/merge-skills.sh" 2>&1 | tee -a "$UPGRADE_LOG"
else
    echo "❌ 整合脚本不存在" | tee -a "$UPGRADE_LOG"
fi
echo "" | tee -a "$UPGRADE_LOG"

# 5. 更新 MEMORY.md
echo "### 5️⃣ 更新记忆系统" | tee -a "$UPGRADE_LOG"
MEMORY_FILE="$HOME/.openclaw/workspace/MEMORY.md"
if [ -f "$MEMORY_FILE" ]; then
    # 统计技能
    total_skills=$(find "$SKILLS_DIR" -maxdepth 1 -type d | tail -n +2 | wc -l)
    xiaoyi_skills=$(find "$SKILLS_DIR" -maxdepth 1 -type d -name "xiaoyi-*" | wc -l)
    
    # 添加升级记录到 MEMORY.md
    echo "" >> "$MEMORY_FILE"
    echo "---" >> "$MEMORY_FILE"
    echo "" >> "$MEMORY_FILE"
    echo "## 🔄 技能升级记录 - $(date '+%Y-%m-%d')" >> "$MEMORY_FILE"
    echo "" >> "$MEMORY_FILE"
    echo "- 总技能数: $total_skills" >> "$MEMORY_FILE"
    echo "- 小艺系列: $xiaoyi_skills" >> "$MEMORY_FILE"
    echo "- 升级日志: $UPGRADE_LOG" >> "$MEMORY_FILE"
    
    echo "✅ MEMORY.md 已更新" | tee -a "$UPGRADE_LOG"
fi
echo "" | tee -a "$UPGRADE_LOG"

# 6. 生成升级报告
echo "### 6️⃣ 升级报告" | tee -a "$UPGRADE_LOG"
echo "" | tee -a "$UPGRADE_LOG"

# 统计
total=$(find "$SKILLS_DIR" -maxdepth 1 -type d | tail -n +2 | wc -l)
xiaoyi=$(find "$SKILLS_DIR" -maxdepth 1 -type d -name "xiaoyi-*" | wc -l)
doc=$(find "$SKILLS_DIR" -maxdepth 1 -type d \( -name "*doc*" -o -name "*pdf*" -o -name "*pptx*" \) | wc -l)
core=$(find "$SKILLS_DIR" -maxdepth 1 -type d \( -name "*memory*" -o -name "*brain*" -o -name "*self-improvement*" -o -name "ontology" \) | wc -l)

cat << EOF | tee -a "$UPGRADE_LOG"
## 📊 技能库统计

| 类别 | 数量 |
|------|------|
| 总计 | $total |
| 小艺系列 | $xiaoyi |
| 文档处理 | $doc |
| 核心技能 | $core |

## ✅ 升级完成

- 配置文件: $UPGRADE_DIR/skills-config.json
- 技能清单: $UPGRADE_DIR/skills-inventory.json
- 冲突报告: $UPGRADE_DIR/conflicts-report.md
- 整合日志: $UPGRADE_DIR/merge-log.md
- 升级日志: $UPGRADE_LOG

EOF

echo ""
echo "🎉 技能库升级完成！"
echo "📄 详细日志: $UPGRADE_LOG"
