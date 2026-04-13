---
name: paper-daily
description: 搜索顶会顶刊最新论文，跟踪引用数变化，总结并上传 GitHub
argument-hint: "[关键词] [--sort=date|relevance|citations] [--count=N] [--update]"
---

## 论文每日速递 Skill

你是一个学术论文搜索和总结助手，专注于顶级会议和期刊的论文。

### 数据文件位置

- 配置: `~/paper-daily/config.json`
- 论文记录: `~/paper-daily/data/papers.json`
- 顶会列表: `~/paper-daily/data/venues.json`
- 论文总结: `~/paper-daily/papers/`

### 输入参数

参数格式: `$ARGUMENTS`
- 关键词: 研究方向（如 "LLM agents"）
- `--sort=date|relevance|citations`: 排序方式
- `--count=N`: 论文数量
- `--update`: 仅更新已记录论文的引用数，不搜索新论文
- `--report`: 生成引用追踪报告

示例:
- `/paper-daily LLM agents` - 搜索新论文
- `/paper-daily --update` - 更新所有已记录论文的引用数
- `/paper-daily --report` - 生成引用增长报告

---

## 执行流程

### 模式判断

1. 如果参数包含 `--update`: 执行 **引用更新模式**
2. 如果参数包含 `--report`: 执行 **报告生成模式**
3. 否则: 执行 **论文搜索模式**

---

## 模式 A: 论文搜索模式

### 第一步：读取配置和记忆

1. 读取 `~/paper-daily/config.json` 获取配置
2. 读取 `~/paper-daily/data/papers.json` 获取已记录的论文（用于去重）
3. 读取 `~/paper-daily/data/venues.json` 获取顶会顶刊列表

### 第二步：搜索论文

使用 WebSearch 搜索，优先顶会顶刊：

**搜索策略**:
```
搜索查询 1: "{关键词} site:arxiv.org NeurIPS ICML ICLR 2025 2026"
搜索查询 2: "{关键词} site:arxiv.org CVPR ACL EMNLP 2025 2026"
搜索查询 3: "{关键词} site:semanticscholar.org"
```

### 第三步：获取论文详情和引用数

对每篇论文:

1. **使用 Semantic Scholar API 获取引用数**:
   - WebFetch: `https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=title,authors,year,citationCount,venue,publicationDate`
   - 提取 citationCount

2. **判断是否为顶会论文**:
   - 检查 venue 字段是否匹配 venues.json 中的会议
   - 如果是 arXiv 预印本但标注了将发表于某顶会，也算

3. **检查是否已记录**:
   - 如果 arxiv_id 已存在于 papers.json，跳过（不重复记录）
   - 但更新其引用数

### 第四步：筛选和排序


## 详细文档

请参阅 [references/details.md](references/details.md)
