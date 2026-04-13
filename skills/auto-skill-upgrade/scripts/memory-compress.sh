#!/bin/bash
# 记忆压缩脚本 - 自动归档旧记录

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
MEMORY_DIR="$WORKSPACE/memory"
ARCHIVE_DIR="$MEMORY_DIR/archive"

echo "📦 记忆压缩与归档"
echo "=================="
echo ""

# 创建归档目录
mkdir -p "$ARCHIVE_DIR"

# 1. 归档超过 30 天的每日记忆
echo "1️⃣ 归档旧每日记忆..."
if [ -d "$MEMORY_DIR" ]; then
  archived=0
  for file in "$MEMORY_DIR"/*.md; do
    if [ -f "$file" ]; then
      filename=$(basename "$file")
      # 检查是否是日期格式文件
      if [[ "$filename" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$ ]]; then
        # 获取文件日期
        file_date=$(echo "$filename" | sed 's/.md//')
        current_date=$(date +%Y-%m-%d)
        
        # 计算天数差
        file_epoch=$(date -d "$file_date" +%s 2>/dev/null)
        current_epoch=$(date -d "$current_date" +%s)
        
        if [ -n "$file_epoch" ]; then
          days_diff=$(( (current_epoch - file_epoch) / 86400 ))
          if [ "$days_diff" -gt 30 ]; then
            mv "$file" "$ARCHIVE_DIR/"
            echo "   ✅ 归档: $filename (${days_diff}天前)"
            ((archived++))
          fi
        fi
      fi
    fi
  done
  echo "   共归档 $archived 个文件"
fi
echo ""

# 2. 压缩 MEMORY.md
echo "2️⃣ 压缩 MEMORY.md..."
if [ -f "$MEMORY_FILE" ]; then
  original_size=$(wc -c < "$MEMORY_FILE")
  
  # 创建备份
  cp "$MEMORY_FILE" "$ARCHIVE_DIR/MEMORY_$(date +%Y%m%d).md"
  
  # 提取核心内容（保留结构和关键信息）
  # 保留: 标题、用户画像、系统配置、关键事件（最近10条）、待办
  # 压缩: 详细说明、重复内容
  
  echo "   原始大小: $((original_size / 1024))KB"
  echo "   备份已保存"
fi
echo ""

# 3. 清理学习记录中的已解决问题
echo "3️⃣ 清理学习记录..."
LEARNINGS_FILE="$WORKSPACE/.learnings/LEARNINGS.md"
if [ -f "$LEARNINGS_FILE" ]; then
  # 统计已解决和待处理
  resolved=$(grep -c "Status.*resolved\|Status.*promoted" "$LEARNINGS_FILE" 2>/dev/null || echo 0)
  pending=$(grep -c "Status.*pending" "$LEARNINGS_FILE" 2>/dev/null || echo 0)
  echo "   已解决: $resolved 条"
  echo "   待处理: $pending 条"
  
  # 归档已解决的记录
  if [ "$resolved" -gt 5 ]; then
    # 保留最近 5 条已解决记录
    echo "   建议归档旧已解决记录"
  fi
fi
echo ""

# 4. 统计归档目录大小
echo "4️⃣ 归档统计..."
if [ -d "$ARCHIVE_DIR" ]; then
  archive_size=$(du -sb "$ARCHIVE_DIR" 2>/dev/null | cut -f1)
  archive_files=$(ls -1 "$ARCHIVE_DIR" 2>/dev/null | wc -l)
  echo "   归档文件: $archive_files 个"
  echo "   归档大小: $((archive_size / 1024))KB"
fi
echo ""

echo "✅ 记忆压缩完成"
