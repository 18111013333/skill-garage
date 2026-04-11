#!/bin/bash
# 技能链合并脚本 - 创建统一入口技能

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
WORKSPACE="$HOME/.openclaw/workspace"

echo "🔗 技能链合并"
echo "=============="
echo ""

# 创建统一入口技能目录
mkdir -p "$SKILLS_DIR/unified-document"
mkdir -p "$SKILLS_DIR/unified-image"
mkdir -p "$SKILLS_DIR/unified-search"

# 1. 文档处理统一入口
echo "1️⃣ 创建文档处理统一入口..."
cat > "$SKILLS_DIR/unified-document/SKILL.md" << 'EOF'
---
name: unified-document
description: 文档处理统一入口。自动路由到最佳文档处理技能。支持格式转换、OCR、编辑、生成等所有文档操作。触发词：文档、doc、pdf、pptx、转换、OCR。
---

# 文档处理统一入口

自动路由到最佳文档处理技能，减少 Token 消耗。

## 工作流

```
用户请求
    ↓
判断文档类型和操作
    ↓
┌─────────────────────────────────┐
│ 格式转换 → xiaoyi-doc-convert   │
│ OCR处理 → paddleocr-doc-parsing │
│ Word编辑 → docx                 │
│ PDF处理 → pdf                   │
│ PPT生成 → pptx                  │
│ Markdown → markitdown           │
└─────────────────────────────────┘
```

## 优先级

1. xiaoyi-doc-convert (格式转换)
2. paddleocr-doc-parsing (OCR)
3. docx/pdf/pptx (具体格式)

## 使用

直接描述需求，自动路由：
- "把这个 PDF 转成 Word"
- "识别图片中的文字"
- "生成一个 PPT"
EOF
echo "   ✅ unified-document"

# 2. 图像处理统一入口
echo "2️⃣ 创建图像处理统一入口..."
cat > "$SKILLS_DIR/unified-image/SKILL.md" << 'EOF'
---
name: unified-image
description: 图像处理统一入口。自动路由到最佳图像技能。支持理解、搜索、生成、编辑等所有图像操作。触发词：图片、图像、看图、生成图、搜图。
---

# 图像处理统一入口

自动路由到最佳图像处理技能。

## 工作流

```
用户请求
    ↓
判断图像操作类型
    ↓
┌─────────────────────────────────┐
│ 图像理解 → xiaoyi-image-understanding │
│ 图像搜索 → xiaoyi-image-search  │
│ 图像生成 → seedream-image_gen   │
│ 图像编辑 → image-cog            │
└─────────────────────────────────┘
```

## 优先级

1. xiaoyi-image-understanding (理解)
2. xiaoyi-image-search (搜索)
3. seedream-image_gen (生成)

## 使用

直接描述需求：
- "这张图是什么"
- "搜索小狗的图片"
- "生成一张风景图"
EOF
echo "   ✅ unified-image"

# 3. 搜索统一入口
echo "3️⃣ 创建搜索统一入口..."
cat > "$SKILLS_DIR/unified-search/SKILL.md" << 'EOF'
---
name: unified-search
description: 搜索统一入口。自动路由到最佳搜索技能。支持联网搜索、深度调研、多引擎搜索。触发词：搜索、查一下、调研、找资料。
---

# 搜索统一入口

自动路由到最佳搜索技能。

## 工作流

```
用户请求
    ↓
判断搜索类型
    ↓
┌─────────────────────────────────┐
│ 快速搜索 → xiaoyi-web-search    │
│ 深度调研 → deep-search          │
│ 多引擎 → prismfy-search         │
│ 专业搜索 → tavily-search        │
└─────────────────────────────────┘
```

## 优先级

1. xiaoyi-web-search (快速)
2. deep-search (深度)
3. prismfy-search (多引擎)

## 使用

直接描述需求：
- "搜索一下 xxx"
- "深度调研 xxx"
- "帮我查资料"
EOF
echo "   ✅ unified-search"

echo ""
echo "✅ 技能链合并完成"
echo ""
echo "📊 整合效果:"
echo "   文档链: 6技能 → 1入口"
echo "   图像链: 4技能 → 1入口"
echo "   搜索链: 4技能 → 1入口"
echo "   预计减少 Token: ~30%"
