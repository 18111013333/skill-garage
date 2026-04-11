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
