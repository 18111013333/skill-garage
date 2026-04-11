#!/bin/bash
# 会话历史压缩脚本 - 自动摘要旧对话

WORKSPACE="$HOME/.openclaw/workspace"
SESSIONS_DIR="$HOME/.openclaw/sessions"
SUMMARY_DIR="$WORKSPACE/memory/session-summaries"

echo "📝 会话历史压缩"
echo "================"
echo ""

# 创建摘要目录
mkdir -p "$SUMMARY_DIR"

# 1. 分析会话文件
echo "1️⃣ 分析会话文件..."
if [ -d "$SESSIONS_DIR" ]; then
  # 查找超过 30 天的会话文件
  old_sessions=$(find "$SESSIONS_DIR" -name "*.jsonl*" -mtime +30 2>/dev/null | head -20)
  session_count=$(echo "$old_sessions" | grep -c "jsonl" 2>/dev/null || echo 0)
  echo "   超过 30 天的会话: $session_count 个"
  
  if [ "$session_count" -gt 0 ]; then
    echo ""
    echo "   待压缩会话:"
    echo "$old_sessions" | while read file; do
      if [ -n "$file" ]; then
        size=$(wc -c < "$file" 2>/dev/null || echo 0)
        echo "     - $(basename $file): $((size/1024))KB"
      fi
    done
  fi
else
  echo "   未找到会话目录"
fi
echo ""

# 2. 创建摘要模板
echo "2️⃣ 创建摘要模板..."
cat > "$SUMMARY_DIR/template.md" << 'EOF'
# 会话摘要模板

## 基本信息
- 会话ID: [SESSION_ID]
- 时间范围: [START] - [END]
- 消息数: [COUNT]

## 关键决策
- [决策1]
- [决策2]

## 重要学习
- [学习1]
- [学习2]

## 待办事项
- [ ] [待办1]
- [ ] [待办2]

## 相关文件
- [文件路径]

---
_此摘要由自动压缩生成_
EOF
echo "   ✅ 摘要模板已创建"
echo ""

# 3. 压缩策略
echo "3️⃣ 压缩策略:"
echo "   - 保留最近 30 天完整会话"
echo "   - 超过 30 天: 生成摘要后归档"
echo "   - 摘要保留关键决策和学习"
echo ""

# 4. 预估效果
echo "4️⃣ 预估效果:"
if [ -d "$SESSIONS_DIR" ]; then
  total_size=$(du -sb "$SESSIONS_DIR" 2>/dev/null | cut -f1)
  old_size=$(find "$SESSIONS_DIR" -name "*.jsonl*" -mtime +30 -exec du -sb {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
  
  if [ -n "$old_size" ] && [ "$old_size" -gt 0 ]; then
    # 摘要约为原大小的 10%
    compressed_size=$((old_size / 10))
    saved=$((old_size - compressed_size))
    
    echo "   会话总大小: $((total_size/1024))KB"
    echo "   可压缩大小: $((old_size/1024))KB"
    echo "   压缩后: $((compressed_size/1024))KB"
    echo "   节省: $((saved/1024))KB ($((saved*100/total_size))%)"
  else
    echo "   暂无超过 30 天的会话"
  fi
fi

echo ""
echo "✅ 会话压缩脚本就绪"
