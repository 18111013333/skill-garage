# 技能恢复计划

## 概述

- **总技能数**: 158 个
- **当前激活**: 17 个
- **存档技能**: 141 个
- **存档路径**: `_archive/old_skills_20260410/skills/`

---

## 技能分类统计

| 层级 | 技能数 | 主要类别 |
|------|--------|----------|
| L1 core | 12 | 身份、规则、生命周期、对话、推荐 |
| L2 memory_context | 5 | 记忆、存储 |
| L3 orchestration | 7 | 自动化、监控、策略 |
| L4 execution | 35 | 搜索、图像、视频、音频、文档、浏览器、内容、代码 |
| L5 governance | 5 | 安全、风险、质量 |
| L6 infrastructure | 77 | DevOps、云服务、API、社交、金融、新闻、营销、生产力 |

---

## 恢复优先级

### P0 - 核心必需 (立即恢复)
| 技能 | 功能 | 层级 |
|------|------|------|
| `memory` | 记忆管理 | L2 |
| `unified-search` | 统一搜索 | L4 |
| `image` | 图像处理 | L4 |
| `web-browsing` | 网页浏览 | L4 |

### P1 - 重要功能 (优先恢复)
| 技能 | 功能 | 层级 |
|------|------|------|
| `code-analysis-skills` | 代码分析 | L4 |
| `data-analysis` | 数据分析 | L4 |
| `article-writer` | 文章写作 | L4 |
| `video-cog` | 视频处理 | L4 |
| `audio-cog` | 音频处理 | L4 |
| `playwright` | 浏览器自动化 | L4 |

### P2 - 实用功能 (按需恢复)
| 技能 | 功能 | 层级 |
|------|------|------|
| `china-stock-analysis` | A股分析 | L6 |
| `hot-news-aggregator` | 热点新闻 | L6 |
| `xiaohongshu-all-in-one` | 小红书 | L6 |
| `bilibili-all-in-one` | B站 | L6 |
| `dingtalk-ai-table` | 钉钉 | L6 |

### P3 - 可选功能 (暂不恢复)
| 技能 | 功能 | 层级 |
|------|------|------|
| `poetry` | 诗歌生成 | L4 |
| `novel-generator` | 小说生成 | L4 |
| `spotify-player` | Spotify | L6 |
| `sonoscli` | Sonos | L6 |

---

## 恢复命令

### 恢复单个技能
```bash
# 复制技能到激活目录
cp -r _archive/old_skills_20260410/skills/<skill_name> skills/

# 或使用 ClawHub 安装
npx clawhub@latest install <skill_name>
```

### 批量恢复 P0 技能
```bash
cd /home/sandbox/.openclaw/workspace
cp -r _archive/old_skills_20260410/skills/memory skills/
cp -r _archive/old_skills_20260410/skills/unified-search skills/
cp -r _archive/old_skills_20260410/skills/image skills/
cp -r _archive/old_skills_20260410/skills/web-browsing skills/
```

### 恢复所有技能
```bash
cd /home/sandbox/.openclaw/workspace
cp -r _archive/old_skills_20260410/skills/* skills/
```

---

## 技能生命周期管理

### 技能状态
| 状态 | 描述 | 路径 |
|------|------|------|
| `active` | 激活使用 | `skills/` |
| `archived` | 存档保留 | `_archive/old_skills_20260410/skills/` |
| `frozen` | 冻结禁用 | `_archive/old_skills_20260410/skills/_frozen/` |
| `pending` | 待审核 | `_archive/old_review_pending_20260410/` |

### 技能成熟度
| 级别 | 描述 | 条件 |
|------|------|------|
| `incubating` | 孵化期 | 新技能，< 30 天 |
| `growing` | 成长期 | 使用 > 10 次，评分 > 3.0 |
| `mature` | 成熟期 | 使用 > 100 次，评分 > 4.0 |
| `deprecated` | 废弃期 | 90 天未使用 |

---

## 注意事项

1. **不要一次性恢复所有技能** - 会影响性能
2. **按优先级逐步恢复** - P0 → P1 → P2 → P3
3. **定期清理不常用技能** - 移动到存档
4. **保持技能注册表更新** - 记录所有变更

---

## 来源
- 存档日期: 2026-04-10
- 存档原因: 六层架构重构
- 原始技能数: 158 个
