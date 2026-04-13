---
name: dingtalk-ai-table
description: 钉钉 AI 表格（多维表）操作技能。使用 mcporter CLI 连接钉钉官方新版 AI 表格 MCP server，基于 baseId / tableId / fieldId / recordId 体系执行 Base、Table、Field、Record 的查询与增删改。适用于创建 AI 表格、搜索表格、读取表结构、批量增删改记录、批量建字段、更新字段配置、按模板建表等场景。需要配置 DINGTALK_MCP_URL 或直接使用 Streamable HTTP URL。
version: 0.6.0
metadata:
  author: Marila@Dingtalk
  category: productivity
  tags:
    - dingtalk
    - spreadsheet
    - mcp
    - automation
    - data-management
  documentation: https://github.com/aliramw/dingtalk-ai-table
  support: https://github.com/aliramw/dingtalk-ai-table/issues
  openclaw:
    requires:
      env:
        - DINGTALK_MCP_URL
        - OPENCLAW_WORKSPACE
      bins:
        - mcporter
        - python3
    primaryEnv: DINGTALK_MCP_URL
    homepage: https://github.com/aliramw/dingtalk-ai-table
---

# 钉钉 AI 表格操作（新版 MCP）

## 🚀 5 分钟快速开始

### 1️⃣ 列出我的表格
```bash
mcporter call '<DINGTALK_MCP_URL>' .list_bases limit=5
```

### 2️⃣ 创建新表格
```bash
mcporter call '<DINGTALK_MCP_URL>' .create_base baseName='我的项目'
```

### 3️⃣ 添加记录
```bash
mcporter call '<DINGTALK_MCP_URL>' .create_records \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","records":[{"cells":{"fld_name":"张三"}}]}'
```

### 4️⃣ 查询记录
```bash
mcporter call '<DINGTALK_MCP_URL>' .query_records \
  --args '{"baseId":"base_xxx","tableId":"tbl_xxx","limit":10}'
```

### 5️⃣ 批量导入
```bash
python3 scripts/import_records.py base_xxx tbl_xxx data.csv
```

---

## 核心概念

按 **新版 MCP schema** 工作：
- Base：`baseId`
- Table：`tableId`
- Field：`fieldId`
- Record：`recordId`

不要再用旧版 `dentryUuid / sheetIdOrName / fieldIdOrName`。

推荐使用 `mcporter 0.8.1` 及以上版本。

输出模式兼容说明：
- `mcporter 0.8.1+` 可直接调用
- 更低版本需要显式加 `--output text`
- AI 表格 MCP 无论使用哪种模式，返回体本身都是标准 JSON；差异主要在 `mcporter` 的输出处理方式

## 版本守门规则（每个 MCP Server 地址只强制检查一次）

在真正开始任何 AI 表格操作前，必须先检查当前 `mcporter` 注册的 `dingtalk-ai-table` MCP server 实际返回的 tools schema。**但这个检查不该每次都重复做；同一个 MCP Server 地址只需要强制检查一次。**

### 一次性检查策略

1. 先读取当前 `mcporter` 里 `dingtalk-ai-table` 对应的 MCP Server 地址。
2. 用这个地址生成一个本地检查标记（例如基于完整 URL 或其 hash）。
3. 在工作区保存检查结果，例如放到：

```text
~/.openclaw/workspace/.cache/dingtalk-ai-table/
```

建议文件名模式：

```text
schema-check-<url-hash>.json
```

4. 如果当前地址对应的检查标记已经存在，并且结果是“已确认新版 schema”，则**跳过重复检查**，直接继续后续 AI 表格操作。
5. 只有在以下情况才重新强制检查：
   - 第一次运行，没有检查标记

## 详细文档

请参阅 [references/details.md](references/details.md)
