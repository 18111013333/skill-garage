1. **筛选**: 只保留符合 venue_filter 的论文
2. **去重**: 排除已记录的论文
3. **排序**:
   - `relevance`: 按搜索相关性
   - `date`: 按发布日期（最新优先）
   - `citations`: 按引用数（最高优先）

### 第五步：更新论文记录

将新论文添加到 `~/paper-daily/data/papers.json`:

```json
{
  "papers": {
    "2501.12345": {
      "title": "论文标题",
      "authors": ["作者1", "作者2"],
      "arxiv_id": "2501.12345",
      "url": "https://arxiv.org/abs/2501.12345",
      "venue": "NeurIPS 2025",
      "venue_rank": "CCF-A",
      "first_seen": "2025-01-25",
      "keywords": ["LLM", "agents"],
      "citation_history": [
        {"date": "2025-01-25", "count": 15}
      ]
    }
  }
}
```

### 第六步：生成 Markdown

使用以下格式：

```markdown
# 📚 每日论文速递 - {YYYY-MM-DD}

**研究方向**: {关键词}
**筛选条件**: 顶会顶刊 (CCF-A / CORE A* / CORE A)
**论文数量**: {N}

---

## 1. {论文标题}

**基本信息**
- 作者: {作者列表}
- 发布: {YYYY-MM-DD}
- 会议/期刊: {venue} ({venue_rank})
- 引用数: {citation_count} 📈
- arXiv: [{arXiv ID}]({链接})

**主要贡献**
{贡献总结}

**方法**
{方法描述}

**实验**
{实验结果}

**结论**
{主要结论}

---
```

### 第七步：保存并上传

1. Write 保存到 `~/paper-daily/papers/YYYY-MM-DD-{关键词}.md`
2. Write 更新 `~/paper-daily/data/papers.json`
3. Bash: `cd ~/paper-daily && git add . && git commit -m "📚 Daily papers: {关键词}" && git push`

---

## 模式 B: 引用更新模式 (--update)

### 执行步骤

1. 读取 `~/paper-daily/data/papers.json`
2. 对每篇已记录的论文:
   - WebFetch Semantic Scholar API 获取最新引用数
   - 添加新的引用记录到 citation_history
3. Write 更新 papers.json
4. 输出更新摘要（引用数增长最多的论文）
5. Git commit & push

---

## 模式 C: 报告生成模式 (--report)

### 执行步骤

1. 读取 papers.json
2. 计算每篇论文的引用增长:
   - 过去 7 天增长
   - 过去 30 天增长
   - 总引用数
3. 生成报告 `~/paper-daily/reports/YYYY-MM-citation-report.md`:

```markdown
# 📊 引用追踪报告 - {YYYY-MM}

## 引用增长 Top 10 (过去 30 天)

| 排名 | 论文 | 会议 | 当前引用 | 30天增长 | 增长率 |
|-----|------|-----|---------|---------|-------|
| 1 | [标题](链接) | NeurIPS | 150 | +45 | +30% |
| 2 | ... | ... | ... | ... | ... |

## 新晋热门论文 (首次记录后快速增长)

...

## 按研究方向统计

| 方向 | 论文数 | 平均引用 | 最高引用 |
|-----|-------|---------|---------|
| LLM agents | 15 | 32 | 150 |
| ... | ... | ... | ... |
```

4. Git commit & push

---

## 注意事项

1. **去重机制**: 已记录的论文不会重复出现在每日总结中
2. **引用更新**: 即使跳过已记录论文，仍会更新其引用数
3. **顶会识别**: 通过 venue 字段匹配 venues.json 中的会议列表
4. **API 限制**: Semantic Scholar API 有速率限制，每秒不超过 10 次请求
5. **预印本处理**: 如果 arXiv 论文标注了接收会议，使用该会议信息
