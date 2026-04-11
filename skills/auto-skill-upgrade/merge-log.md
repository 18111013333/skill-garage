# 技能整合日志

时间: 2026-04-06 10:03:16

---

## 🔄 整合操作

### 📂 技能分类
- admapix → other
- agent-browser-clawdbot → other
- agent-chronicle → other
- ai-picture-book → other
- ai-ppt-generator → other
- amazon-product-search-api-skill → search
- ansible → other
- api-gateway → other
- article-writer → other
- audio-cog → multimedia
- auto-skill-upgrade → other
- baidu-netdisk-skills → other
- baidu-search → search
- beauty-generation-api → other
- best-minds → other
- bitsoul-stock-quantization → other
- calcom-cal.com-web-design-guidelines-1.0.2 → search
- camsnap → other
- ceo-advisor → other
- chart-image → multimedia
- china-stock-analysis → other
- clawdhub → other
- clawsec-suite → other
- cn-web-search → search
- code-analysis-skills → development
- command-center → other
- copywriter → other
- cron → other
- crypto → other
- data-analysis → other
- deep-search-and-insight-synthesize → search
- deepread-ocr → other
- dingtalk-ai-table → other
- discord → other
- docker → document
- docs-cog → document
- docx → document
- eastmoney-fin-search → search
- elasticsearch → search
- eno → other
- excel-analysis → document
- file-manager → other
- find-skills → other
- free-ride → other
- frontend-design-pro → other
- getnote → other
- git → development
- good-txt-to-hwreader → other
- google-maps → other
- google-weather → other
- himalaya → other
- hot-news-aggregator → other
- image-cog → multimedia
- image-gen → multimedia
- image → multimedia
- imap-smtp-email → other
- imsg → other
- industry-stock-tracker → other
- initiation-of-coverage-or-deep-dive → other
- javascript-skills → other
- juejin-skills → other
- keyword-research → search
- klaviyo → other
- linkedin-api → other
- market-research → search
- marketing-strategy-pmm → other
- markitdown → document
- mcporter → other
- memory-setup → core
- moltguard → other
- moltrade → other
- mongodb → other
- mx-finance-data → other
- mx-finance-search → search
- mx-financial-assistant → other
- mx-macro-data → other
- mx-stocks-screener → other
- mysql → other
- nano-banana-pro → other
- nano-pdf → document
- novel-generator → other
- nutrient-openclaw → other
- obsidian → other
- ocr-local → other
- ontology → core
- openai-whisper-api → other
- openclaw-agent-optimize → other
- openclaw-skills-agent-builder-1.0.3 → other
- oracle → other
- paddleocr-doc-parsing → document
- pdf → document
- peekaboo → other
- personas → other
- pexoai-agent → other
- planning-with-files → other
- playwright → other
- poetry → other
- polymarket-trade → other
- post-job → other
- pptx → document
- prismfy-search → search
- proactivity → other
- productivity → other
- quality-documentation-manager → document
- react-best-practices → other
- research-cog → search
- risk-management-specialist → other
- scrapling-official → other
- screenshot → other
- seedream-image_gen → multimedia
- self-improving-agent → other
- self-improving-proactive-agent → other
- senior-architect → other
- senior-data-scientist → other
- senior-security → other
- sheet-cog → other
- skill-creator → other
- skill-finder-cn → other
- skill-finder → other
- skywork-ppt → other
- slides-cog → other
- spotify-player → other
- sqlite → other
- stock-price-query → other
- story-cog → other
- su-lan-paper-daily-skill → other
- t-trading → other
- taskr → other
- tavily-search-skill → search
- tdd-guide → other
- tech-news-digest → other
- technical-seo-checker → other
- tencent-cos-skill → other
- terraform → other
- topic-monitor → other
- tushare-data → other
- tushare-stock-skill → other
- tushare → other
- ui-design-system → other
- unified-document → document
- unified-image → multimedia
- unified-search → search
- university-applications → other
- verified-agent-identity → other
- video-agent → multimedia
- video-cog → multimedia
- video-subtitles → multimedia
- video-transcript-downloader → multimedia
- wan-image-video-generation-editting → multimedia
- weather → other
- web-browsing → search
- web-scraper → search
- web-scraping → search
- web-search-exa → search
- web-search-plus → search
- webapp-testing → development
- x-search → search
- xiaohongshu-all-in-one → other
- xiaoyi-doc-convert → xiaoyi
- xiaoyi-file-upload → xiaoyi
- xiaoyi-image-search → xiaoyi
- xiaoyi-image-understanding → xiaoyi
- xiaoyi-report → xiaoyi
- xiaoyi-web-search → xiaoyi
- zhipu-web-search → search

### 🔗 技能链建立
- 📄 文档转换链: xiaoyi-file-upload,xiaoyi-doc-convert
- 🖼️ 图像处理链: xiaoyi-image-search,xiaoyi-image-understanding,seedream-image_gen
- 🔍 搜索链: xiaoyi-web-search,deep-search-and-insight-synthesize

### 💡 整合建议
- ⚠️ 图像技能建议整合为统一入口
  - 建立优先级: xiaoyi-image-understanding > image-search > seedream
- ⚠️ 文档技能建议建立调用链
  - xiaoyi-doc-convert 作为统一入口，内部调用 docx/pdf/pptx

### 📊 技能统计
- 总计: 169 个技能
- 小艺系列: 6 个

---

## ✅ 整合完成

配置文件: /home/sandbox/.openclaw/workspace/skills/auto-skill-upgrade/skills-config.json
整合日志: /home/sandbox/.openclaw/workspace/skills/auto-skill-upgrade/merge-log.md
