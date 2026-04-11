---
name: industry_stock_tracker
description: >
  依托东方财富数据库，面向行业或个股，产出跟踪类报告（含日报/周报/月报、研报及结构化跟踪解读）。
  满足以下任一条件即触发：（1）用户明确索要「报告」「研报」「跟踪分析」或定期跟踪类文稿；（2）用户点名的行业、板块、指数、个股（名称或代码），并期望系统化、可成文的近况跟踪或梳理。
  典型说法如「写一份 XX 行业报告」「跟踪 XX 股票」「生成 XX 日报」「看看 XX 最近怎么样并出报告」等。
metadata:
  {
    "openclaw": {
      "requires": {
        "env":["EM_API_KEY"]
      }
    }
  }
---

# 行业/个股跟踪报告生成 Skill

## 概述

本 skill 用于将用户自然语言问题交给脚本 `scripts/generate_industry_stock_tracker_report.py`，
由脚本调用远程报告服务并返回统一 JSON 结果。输出包含标题、总结内容与附件本地保存路径（DOCX/PDF）。

## 环境变量

| 变量名 | 说明 | 默认 |
|---|---|---|
| `EM_API_KEY` | 接口鉴权密钥（必填） | 无 |

### 配置 `EM_API_KEY`

```bash
# macOS / Linux
export EM_API_KEY="your_api_key_here"
```

```powershell
# Windows PowerShell
$env:EM_API_KEY="your_api_key_here"
```

## 核心工作流

1) 将用户原始问题原样作为 `query` 传入脚本。
2) 脚本调用接口生成报告并获取“总结”章节。
3) 若接口返回 `wordBase64/pdfBase64`，脚本会落地为本地附件文件并返回路径。
4) 将脚本标准输出（JSON）直接作为 skill 输出依据，不做与脚本冲突的二次改写。

命令行参数调用方式：

```
python3 {baseDir}/scripts/generate_industry_stock_tracker_report.py --query "{{query}}"
```

注意：**禁止调用 任何「后台执行、稍后汇报」的方式跑本脚本**，只能在当前会话中同步等待到命令完成，拿到 stdout 的结果后再继续，否则会导致本 Skill 失败。

## 输出格式规范

接口返回后，必须严格按以下模板输出，不得增删标题、不得改变顺序、不得添加额外章节：

### 标题
直接使用接口返回的 `title` 字段，单独成行。

### 正文
如果接口返回的 `content` 字段有相关行业报告信息，则原文透传；
否则读取接口返回的附件文件内容，总结相关报告信息返回，记住保证返回的正文内容非空。

### 附件
接口返回 pdf 以及 docx 格式文件的保存路径。

### 分享链接
直接使用接口返回的 `share_url` 字段，单独成行。文案必须按以下固定格式输出：

```
{标题}

{正文}

完整报告：
- PDF：{pdf_path}

## 详细文档

请参阅 [references/details.md](references/details.md)
