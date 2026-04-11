#!/usr/bin/env python3
"""
财经新闻聚合工具
从多个来源聚合财经新闻，支持关键词过滤和情感分析
"""

import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re

class NewsAggregator:
    """财经新闻聚合器"""

    def __init__(self):
        self.sources = [
            'sina_finance',
            'eastmoney',
            'xueqiu',
            'wallstreet_cn',
            'yicai'
        ]
        self.cache = []
        self.cache_time = None

    def fetch_news(self, keywords: List[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """
        获取新闻（演示模式返回模拟数据）
        实际使用时需要接入真实API
        """
        # 演示数据
        demo_news = [
            {
                'title': '央行宣布降准0.5个百分点，释放长期资金约1万亿元',
                'source': 'sina_finance',
                'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'url': 'https://finance.sina.com.cn/demo/1',
                'summary': '中国人民银行决定于2026年4月15日下调金融机构存款准备金率0.5个百分点...',
                'sentiment': 'positive',
                'related_stocks': ['银行', '证券']
            },
            {
                'title': '科技股集体反弹，半导体板块领涨',
                'source': 'eastmoney',
                'time': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M'),
                'url': 'https://www.eastmoney.com/demo/2',
                'summary': '今日科技股全线反弹，半导体板块涨幅超过3%，多只个股涨停...',
                'sentiment': 'positive',
                'related_stocks': ['半导体', '芯片', '科技']
            },
            {
                'title': '美联储会议纪要显示通胀担忧持续',
                'source': 'wallstreet_cn',
                'time': (datetime.now() - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M'),
                'url': 'https://wallstreetcn.com/demo/3',
                'summary': '美联储最新会议纪要显示，官员们对通胀前景仍持谨慎态度...',
                'sentiment': 'neutral',
                'related_stocks': ['美股', '黄金']
            },
            {
                'title': '新能源汽车销量创新高，比亚迪月销突破30万',
                'source': 'yicai',
                'time': (datetime.now() - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M'),
                'url': 'https://www.yicai.com/demo/4',
                'summary': '比亚迪3月新能源汽车销量达到30.2万辆，同比增长45%...',
                'sentiment': 'positive',
                'related_stocks': ['比亚迪', '002594', '新能源汽车']
            },
            {
                'title': '房地产政策持续优化，多地取消限购',
                'source': 'xueqiu',
                'time': (datetime.now() - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M'),
                'url': 'https://xueqiu.com/demo/5',
                'summary': '多个城市相继出台房地产优化政策，取消限购限贷...',
                'sentiment': 'positive',
                'related_stocks': ['房地产', '万科', '保利']
            }
        ]

        # 关键词过滤
        if keywords:
            filtered = []
            for news in demo_news:
                title_match = any(kw.lower() in news['title'].lower() for kw in keywords)
                summary_match = any(kw.lower() in news['summary'].lower() for kw in keywords)
                stock_match = any(kw.lower() in str(news['related_stocks']).lower() for kw in keywords)
                if title_match or summary_match or stock_match:
                    filtered.append(news)
            return filtered[:limit]

        return demo_news[:limit]

    def analyze_sentiment(self, news_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析新闻整体情绪"""
        if not news_list:
            return {'overall': 'neutral', 'score': 50}

        sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
        total = sum(sentiment_map.get(n.get('sentiment', 'neutral'), 0) for n in news_list)
        avg = total / len(news_list)

        if avg > 0.3:
            overall = 'positive'
            score = 50 + avg * 50
        elif avg < -0.3:
            overall = 'negative'
            score = 50 + avg * 50
        else:
            overall = 'neutral'
            score = 50

        return {
            'overall': overall,
            'score': round(score, 1),
            'positive_count': sum(1 for n in news_list if n.get('sentiment') == 'positive'),
            'negative_count': sum(1 for n in news_list if n.get('sentiment') == 'negative'),
            'neutral_count': sum(1 for n in news_list if n.get('sentiment') == 'neutral')
        }

    def get_market_brief(self) -> Dict[str, Any]:
        """生成市场简报"""
        news = self.fetch_news(limit=10)
        sentiment = self.analyze_sentiment(news)

        # 提取关键主题
        all_stocks = []
        for n in news:
            all_stocks.extend(n.get('related_stocks', []))

        from collections import Counter
        top_topics = Counter(all_stocks).most_common(5)

        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'news_count': len(news),
            'sentiment': sentiment,
            'top_topics': [{'topic': t[0], 'count': t[1]} for t in top_topics],
            'headlines': [n['title'] for n in news[:5]]
        }

def main():
    """主函数"""
    aggregator = NewsAggregator()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'search':
            keywords = sys.argv[2:] if len(sys.argv) > 2 else []
            result = aggregator.fetch_news(keywords=keywords)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif command == 'brief':
            result = aggregator.get_market_brief()
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif command == 'sentiment':
            news = aggregator.fetch_news()
            result = aggregator.analyze_sentiment(news)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        else:
            print(f"未知命令: {command}")
            print("用法: python news_aggregator.py [search|brief|sentiment] [keywords...]")
    else:
        # 默认输出市场简报
        result = aggregator.get_market_brief()
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
