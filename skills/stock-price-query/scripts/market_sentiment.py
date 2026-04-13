#!/usr/bin/env python3
"""
市场情绪分析工具
基于多维度指标计算市场整体情绪分数
"""

import json
import sys
from datetime import datetime

def calculate_sentiment(index_data):
    """
    计算市场情绪分数 (0-100)
    基于以下维度：
    - 大盘涨跌幅 (40%)
    - 成交量变化 (20%)
    - 涨跌家数比 (20%)
    - 板块轮动情况 (20%)
    """
    score = 50  # 基准分数

    # 大盘涨跌幅影响
    change_percent = index_data.get('change_percent', 0)
    if change_percent > 2:
        score += 20
    elif change_percent > 1:
        score += 10
    elif change_percent > 0:
        score += 5
    elif change_percent < -2:
        score -= 20
    elif change_percent < -1:
        score -= 10
    elif change_percent < 0:
        score -= 5

    # 成交量影响
    volume_change = index_data.get('volume_change_percent', 0)
    if volume_change > 20:
        score += 10  # 放量
    elif volume_change < -20:
        score -= 10  # 缩量

    return max(0, min(100, score))

def get_sentiment_label(score):
    """获取情绪标签"""
    if score >= 80:
        return "极度贪婪", "🟢"
    elif score >= 60:
        return "贪婪", "🟢"
    elif score >= 40:
        return "中性", "🟡"
    elif score >= 20:
        return "恐惧", "🔴"
    else:
        return "极度恐惧", "🔴"

def analyze_market(indices):
    """
    分析多个指数的市场情绪
    indices: 指数数据列表
    """
    results = []

    for idx in indices:
        score = calculate_sentiment(idx)
        label, emoji = get_sentiment_label(score)

        results.append({
            'code': idx.get('code'),
            'name': idx.get('name'),
            'sentiment_score': score,
            'sentiment_label': label,
            'emoji': emoji,
            'price': idx.get('current_price'),
            'change_percent': idx.get('change_percent')
        })

    # 计算整体市场情绪
    if results:
        avg_score = sum(r['sentiment_score'] for r in results) / len(results)
        overall_label, overall_emoji = get_sentiment_label(avg_score)
    else:
        avg_score = 50
        overall_label, overall_emoji = "中性", "🟡"

    return {
        'overall_sentiment': {
            'score': round(avg_score, 1),
            'label': overall_label,
            'emoji': overall_emoji
        },
        'indices': results,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def main():
    """主函数 - 演示模式"""
    # 演示数据
    demo_indices = [
        {'code': '000001', 'name': '上证指数', 'current_price': 3150.5, 'change_percent': 0.85, 'volume_change_percent': 15},
        {'code': '399001', 'name': '深证成指', 'current_price': 10250.3, 'change_percent': 1.2, 'volume_change_percent': 22},
        {'code': '399006', 'name': '创业板指', 'current_price': 2080.8, 'change_percent': -0.3, 'volume_change_percent': -5}
    ]

    result = analyze_market(demo_indices)

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
