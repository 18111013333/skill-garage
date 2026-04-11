#!/bin/bash
# 知识图谱补全脚本 - 添加缺失的技能实体

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
ONTOLOGY_FILE="$HOME/.openclaw/workspace/memory/ontology/graph.jsonl"
CONFIG_FILE="$SKILLS_DIR/auto-skill-upgrade/skills-config.json"

log() {
    echo "[$(date '+%H:%M:%S')] $1"
}

# 获取分类
get_category() {
    local skill="$1"
    
    if [ -f "$CONFIG_FILE" ] && command -v jq &> /dev/null; then
        jq -r --arg skill "$skill" '
            .categories | to_entries[] | 
            select(.value | index($skill)) | 
            .key
        ' "$CONFIG_FILE" 2>/dev/null | head -1
    else
        # 简单分类
        case "$skill" in
            xiaoyi-*) echo "xiaoyi" ;;
            *doc*|*pdf*|*pptx*) echo "document" ;;
            *image*|*video*|*audio*) echo "multimedia" ;;
            *search*|*web*) echo "search" ;;
            *git*|*docker*|*code*) echo "development" ;;
            self-improving*|ontology|memory*|find-skills|skill-creator|auto-skill-upgrade|moltguard) echo "core" ;;
            *) echo "other" ;;
        esac
    fi
}

# 检查实体是否存在
entity_exists() {
    local skill="$1"
    grep -q "\"skill_$skill\"" "$ONTOLOGY_FILE" 2>/dev/null
}

# 添加技能实体
add_skill_entity() {
    local skill="$1"
    local category=$(get_category "$skill")
    local timestamp=$(date -Iseconds)
    
    cat >> "$ONTOLOGY_FILE" << EOF
{"op":"create","entity":{"id":"skill_$skill","type":"Skill","properties":{"name":"$skill","category":"$category","priority":50,"status":"active","installed_at":"$timestamp"}}}
EOF
}

# 主流程
log "🔍 扫描技能目录..."
total_skills=$(ls -1 "$SKILLS_DIR" | grep -v "^\." | wc -l)
log "📊 总技能数: $total_skills"

# 检查图谱中已有的技能
existing_skills=$(grep -o '"skill_[^"]*"' "$ONTOLOGY_FILE" 2>/dev/null | sed 's/"skill_//;s/"$//' | sort -u)
existing_count=$(echo "$existing_skills" | grep -c . 2>/dev/null || echo 0)
log "📊 图谱已有: $existing_count"

# 找出缺失的技能
missing_count=0
added_count=0

for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    
    # 跳过隐藏目录
    [[ "$skill_name" == .* ]] && continue
    
    if ! echo "$existing_skills" | grep -q "^$skill_name$"; then
        ((missing_count++))
        add_skill_entity "$skill_name"
        ((added_count++))
        log "  + $skill_name"
    fi
done

log ""
log "📊 统计:"
log "  - 缺失: $missing_count"
log "  - 已添加: $added_count"
log "  - 图谱总计: $((existing_count + added_count))"

# 更新分类实体
log ""
log "🔄 更新分类实体..."

if [ -f "$CONFIG_FILE" ] && command -v jq &> /dev/null; then
    for category in $(jq -r '.categories | keys[]' "$CONFIG_FILE" 2>/dev/null); do
        skills=$(jq -r --arg cat "$category" '.categories[$cat] | join(",")' "$CONFIG_FILE" 2>/dev/null)
        priority=$(jq -r --arg cat "$category" '.priority[$cat] // 50' "$CONFIG_FILE" 2>/dev/null)
        
        # 检查分类实体是否存在
        if ! grep -q "\"cat_$category\"" "$ONTOLOGY_FILE" 2>/dev/null; then
            cat >> "$ONTOLOGY_FILE" << EOF
{"op":"create","entity":{"id":"cat_$category","type":"Category","properties":{"name":"$category","priority":$priority,"description":"$category 技能分类","skills":["${skills//,/", "}"]}}}
EOF
            log "  + 分类: $category"
        fi
    done
fi

log ""
log "✅ 知识图谱补全完成"
