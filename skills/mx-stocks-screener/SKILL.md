---
name: mx_stocks_screener
description: 基于东方财富数据库，支持通过自然语言输入筛选A港美股、基金、债券等多种资产，支持多元指标筛选，含技术面、消息面、基本面及市场情绪等，可用于全球资产速筛、跨市场监控、投资组合构建、策略回测等场景。返回结果包含数据说明及 csv 文件。Natural language screener for investment assets across global markets, including A-shares, ETFs, bonds, HK and US stocks, and funds. It enables multi-dimensional filtering via technical, fundamental, sentiment and news indicators. Ideal for global asset selection, cross-market monitoring, portfolio construction and strategy backtesting.
metadata:
  {
    "openclaw": {
      "requires": {
        "env":["EM_API_KEY"]
      },
      "install": [
        {
          "id": "pip-deps",
          "kind": "python",
          "package": "httpx",
          "label": "Install Python dependencies"
        }
      ]
    }
  }
---

# 选股 / 选板块 / 选基金

通过**自然语言查询**进行选股，数据来自于妙想大模型服务，支持以下类型：
- **A股**、**港股**、**美股**
- **基金**、**ETF**、**可转债**、**板块**

## 密钥来源与安全说明

- 本技能仅使用一个环境变量：`EM_API_KEY`。
- `EM_API_KEY` 由东方财富妙想服务（`https://ai.eastmoney.com/mxClaw`）签发，用于其接口鉴权。
- 在提供密钥前，请先确认密钥来源、可用范围、有效期及是否支持重置/撤销。
- 禁止在代码、提示词、日志或输出文件中硬编码/明文暴露密钥。

## 功能范围

### 基础选股能力
- 按股价、市值、涨跌幅、市盈率等**财务/行情指标**筛选
- 按**技术信号**筛选（如连续上涨、突破均线等）
- 按**主营业务、主要产品**筛选
- 按**行业/概念板块**筛选成分股
- 获取**指数成分股**
- **推荐**股票、基金、板块
- 按多种**复合条件**（如且、或、非、排序等）的逻辑组合筛选

### A股进阶查询（部分场景）
除基础选股外，还支持A股上市公司的以下查询场景：
- 高管信息、股东信息
- 龙虎榜数据
- 分红、并购、增发、回购
- 主营区域
- 券商金股

> **注意**：上述仅为部分示例，实际支持的条件远多于列举内容

### **查询示例**

| 类型     | query                    | select-type |
|----------|--------------------------|----------|
| 选A股   | 股价大于500元的股票、创业板市盈率最低的50只 | A股 |
| 选港股   | 港股的科技龙头                  | 港股 |
| 选美股   | 纳斯达克市值前30、苹果产业链美股   | 美股 |
| 选板块   | 今天涨幅最大板块                 | 板块 |
| 选基金   | 白酒主题基金、新能源混合基金近一年收益排名 | 基金 |
| 选ETF   | 规模超2亿的电力ETF              | ETF |
| 选可转债 | 价格低于110元、溢价率超5个点的可转债 | 可转债 |

## 前提条件

### 1. 注册东方财富妙想账号

访问 https://ai.eastmoney.com/mxClaw 注册账号并获取API_KEY。

### 2. 配置 Token

```bash
# macOS 添加到 ~/.zshrc，Linux 添加到 ~/.bashrc
export EM_API_KEY="your_api_key_here"
```


## 详细文档

请参阅 [references/details.md](references/details.md)
