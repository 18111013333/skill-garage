#!/bin/bash
# 发布脚本 - 从使用版同步到发布版，然后发布
# 使用方法: ./publish.sh [版本号]

set -e

WORKSPACE="$HOME/.openclaw/workspace/skills"
HOMO_DIR="$WORKSPACE/yaoyao-memory-homo"
PUBLISH_DIR="$WORKSPACE/yaoyao-memory"

if [ -z "$1" ]; then
    echo "用法: ./publish.sh <版本号>"
    exit 1
fi
VERSION="$1"

echo "=========================================="
echo "🚀 发布流程"
echo "=========================================="

# 步骤1: 从使用版同步到发布版
echo ""
echo "📂 步骤1: 同步使用版 → 发布版..."
rsync -av --exclude='publish.sh' --exclude='publish-clean.sh' \
    --exclude='__pycache__' --exclude='*.pyc' \
    "$HOMO_DIR/" "$PUBLISH_DIR/"
echo "✅ 同步完成"

# 步骤2: 在发布版执行清理
echo ""
echo "📦 步骤2: 执行隐私清理..."
cd "$PUBLISH_DIR"
./publish-clean.sh

# 步骤3: 验证
echo ""
echo "🔍 步骤3: 验证清理结果..."
for f in embeddings_cache.json persona_update.json user_config.json samba.json llm_config.json; do
    if [ -f "config/$f" ]; then
        rm -f "config/$f"
        echo "✅ 已删除 config/$f"
    fi
done

# 步骤4: 更新版本号
echo ""
echo "📝 步骤4: 更新版本号为 $VERSION..."
sed -i "s/version: [0-9.]*/version: $VERSION/" SKILL.md
echo "✅ 版本号更新完成"

# 步骤5: 发布
echo ""
echo "📤 步骤5: 发布到 ClaWHub..."
clawhub publish skills/yaoyao-memory --version "$VERSION"

# 步骤6: 隐藏
echo ""
echo "🙈 步骤6: 隐藏..."
clawhub hide --yes yaoyao-memory

echo ""
echo "=========================================="
echo "✅ 发布完成! 版本 $VERSION (已隐藏)"
echo "=========================================="
