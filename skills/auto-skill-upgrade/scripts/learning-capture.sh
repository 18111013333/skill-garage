#!/bin/bash
# 学习捕获脚本 - 自动记录学习和错误

LEARNINGS_DIR="$HOME/.openclaw/workspace/.learnings"
ONTOLOGY_DIR="$HOME/.openclaw/workspace/memory/ontology"

# 参数
TYPE="$1"  # learning, error, feature
TITLE="$2"
DETAILS="$3"
PRIORITY="${4:-medium}"

generate_id() {
  echo "$(date '+%Y%m%d')-$(date '+%H%M')"
}

case "$TYPE" in
  learning)
    cat >> "$LEARNINGS_DIR/LEARNINGS.md" << EOF

## [LRN-$(generate_id)] best_practice

**Logged**: $(date -Iseconds)
**Priority**: $PRIORITY
**Status**: pending
**Area**: auto_captured

### Summary
$TITLE

### Details
$DETAILS

### Metadata
- Source: auto_capture
- Tags: auto-evolution

---
EOF
    echo "✅ 学习已记录: $TITLE"
    ;;
    
  error)
    cat >> "$LEARNINGS_DIR/ERRORS.md" << EOF

## [ERR-$(generate_id)] auto_captured

**Logged**: $(date -Iseconds)
**Priority**: $PRIORITY
**Status**: pending
**Area**: auto_captured

### Summary
$TITLE

### Error
\`\`\`
$DETAILS
\`\`\`

### Context
自动捕获的错误

---
EOF
    echo "✅ 错误已记录: $TITLE"
    ;;
    
  feature)
    cat >> "$LEARNINGS_DIR/FEATURE_REQUESTS.md" << EOF

## [FEAT-$(generate_id)] auto_captured

**Logged**: $(date -Iseconds)
**Priority**: $PRIORITY
**Status**: pending

### Title
$TITLE

### Description
$DETAILS

---
EOF
    echo "✅ 功能请求已记录: $TITLE"
    ;;
    
  *)
    echo "用法: $0 <learning|error|feature> <title> <details> [priority]"
    exit 1
    ;;
esac

# 更新知识图谱
if [ -f "$ONTOLOGY_DIR/graph.jsonl" ]; then
  entity_type="Learning"
  [ "$TYPE" = "error" ] && entity_type="Error"
  [ "$TYPE" = "feature" ] && entity_type="FeatureRequest"
  
  echo "{\"op\":\"create\",\"entity\":{\"id\":\"$(generate_id)\",\"type\":\"$entity_type\",\"properties\":{\"title\":\"$TITLE\",\"priority\":\"$PRIORITY\",\"status\":\"pending\",\"created_at\":\"$(date -Iseconds)\"}}}" >> "$ONTOLOGY_DIR/graph.jsonl"
fi
