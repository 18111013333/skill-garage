- 分类文章：`POST https://api.juejin.cn/recommend_api/v1/article/recommend_cate_feed`
- 标签列表：`POST https://api.juejin.cn/tag_api/v1/query_category_tags`

### 📝 功能二：文章自动发布

| 子功能 | 说明 |
|--------|------|
| 浏览器登录 | 通过 Playwright 打开掘金登录页面，用户扫码或密码登录后自动获取 Cookie |
| Cookie 管理 | 保存、加载、验证 Cookie 状态 |
| Markdown 解析 | 读取本地 Markdown 文件，提取标题、正文内容 |
| 文章发布 | 通过掘金 API 创建草稿并发布，支持设置分类、标签、摘要、封面图 |
| 草稿管理 | 支持保存为草稿而不立即发布 |

**API 接口**：
- 创建草稿：`POST https://api.juejin.cn/content_api/v1/article_draft/create`
- 发布文章：`POST https://api.juejin.cn/content_api/v1/article/publish`
- 获取标签：`POST https://api.juejin.cn/tag_api/v1/query_category_tags`

**鉴权方式**：Cookie 鉴权（通过 Playwright 浏览器登录获取）

### 📥 功能三：文章下载

| 子功能 | 说明 |
|--------|------|
| 单篇下载 | 通过文章 URL 下载单篇文章，保存为 Markdown |
| 批量下载 | 下载指定作者的所有/部分文章 |
| 格式转换 | 将掘金文章 HTML 内容转换为标准 Markdown |
| 图片处理 | 可选下载文章中的图片到本地 |
| 元数据保留 | 保留文章标题、作者、发布时间、标签等元信息 |

**API 接口**：
- 文章详情：`POST https://api.juejin.cn/content_api/v1/article/detail`
- 用户文章列表：`POST https://api.juejin.cn/content_api/v1/article/query_list`

## 技术架构

```
juejin/
├── SKILL.md              # 技能定义文档
├── README.md             # 项目说明文档
├── requirements.txt      # Python 依赖
├── juejin_skill/         # 主模块
│   ├── __init__.py
│   ├── config.py         # 配置管理
│   ├── api.py            # 掘金 API 封装
│   ├── auth.py           # 登录鉴权（Playwright）
│   ├── hot_articles.py   # 热门文章排行榜
│   ├── publisher.py      # 文章发布
│   ├── downloader.py     # 文章下载
│   └── utils.py          # 工具函数
└── output/               # 下载文章输出目录
```

## 环境要求

- Python >= 3.9
- Playwright（用于浏览器登录）
- 网络可访问 https://juejin.cn/

## Prompt 示例

```
用户：帮我获取掘金前端分类的热门文章排行榜
AI：正在获取掘金前端分类的热门文章...

用户：把 ./my-article.md 发布到掘金，分类选前端，标签加上 Vue.js 和 TypeScript
AI：正在登录掘金账号并发布文章...

用户：下载这篇掘金文章 https://juejin.cn/post/7300000000000000000
AI：正在下载文章并转换为 Markdown 格式...
```
