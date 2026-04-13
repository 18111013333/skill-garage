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
