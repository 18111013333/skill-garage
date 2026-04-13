#!/usr/bin/env python3
"""
风险评估工具
基于多维度指标评估投资风险
"""

import json
import sys
from typing import Dict, List, Any
from datetime import datetime

class RiskAssessment:
    """风险评估工具"""

    # 风险等级定义
    RISK_LEVELS = {
        'very_low': {'name': '极低风险', 'score_range': (0, 20), 'color': '🟢'},
        'low': {'name': '低风险', 'score_range': (20, 40), 'color': '🟢'},
        'medium': {'name': '中等风险', 'score_range': (40, 60), 'color': '🟡'},
        'high': {'name': '高风险', 'score_range': (60, 80), 'color': '🟠'},
        'very_high': {'name': '极高风险', 'score_range': (80, 100), 'color': '🔴'}
    }

    def __init__(self):
        pass

    def assess_stock_risk(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """评估单只股票风险"""
        risk_factors = []

        # 1. 波动率风险
        volatility = stock_data.get('volatility', 0)
        volatility_score = self._score_volatility(volatility)
        risk_factors.append({
            'factor': '波动率',
            'score': volatility_score,
            'detail': f'30日波动率: {volatility:.2f}%'
        })

        # 2. 市值风险
        market_cap = stock_data.get('market_cap', 0)
        market_cap_score = self._score_market_cap(market_cap)
        risk_factors.append({
            'factor': '市值规模',
            'score': market_cap_score,
            'detail': f'市值: {self._format_market_cap(market_cap)}'
        })

        # 3. 流动性风险
        volume = stock_data.get('avg_volume', 0)
        liquidity_score = self._score_liquidity(volume)
        risk_factors.append({
            'factor': '流动性',
            'score': liquidity_score,
            'detail': f'日均成交额: {self._format_volume(volume)}'
        })

        # 4. 估值风险
        pe_ratio = stock_data.get('pe_ratio', 0)
        valuation_score = self._score_valuation(pe_ratio)
        risk_factors.append({
            'factor': '估值水平',
            'score': valuation_score,
            'detail': f'市盈率: {pe_ratio:.2f}'
        })

        # 5. 趋势风险
        trend = stock_data.get('trend', 'neutral')
        trend_score = self._score_trend(trend)
        risk_factors.append({
            'factor': '趋势风险',
            'score': trend_score,
            'detail': f'当前趋势: {trend}'
        })

        # 计算综合风险分数
        total_score = sum(f['score'] for f in risk_factors) / len(risk_factors)
        risk_level = self._get_risk_level(total_score)

        return {
            'symbol': stock_data.get('symbol', 'UNKNOWN'),
            'name': stock_data.get('name', 'Unknown'),
            'total_risk_score': round(total_score, 1),
            'risk_level': risk_level['name'],
            'risk_emoji': risk_level['color'],
            'risk_factors': risk_factors,
            'recommendation': self._get_recommendation(total_score),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def assess_portfolio_risk(self, holdings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """评估投资组合风险"""
        if not holdings:
            return {'error': '投资组合为空'}

        # 计算各持仓风险
        holding_risks = []
        for holding in holdings:
            risk = self.assess_stock_risk(holding)
            holding_risks.append(risk)

        # 计算组合风险
        weights = [h.get('weight', 1/len(holdings)) for h in holdings]
        weighted_risk = sum(r['total_risk_score'] * w for r, w in zip(holding_risks, weights))

        # 计算集中度风险
        concentration_score = self._calculate_concentration_risk(weights)
        holding_risks.append({
            'factor': '集中度风险',
            'score': concentration_score,
            'detail': f'最大持仓占比: {max(weights)*100:.1f}%'
        })

        # 计算相关性风险（简化版）
        correlation_score = 30  # 默认中等相关性风险

        portfolio_level = self._get_risk_level(weighted_risk)

        return {
            'portfolio_risk_score': round(weighted_risk, 1),
            'risk_level': portfolio_level['name'],
            'risk_emoji': portfolio_level['color'],
            'holdings': holding_risks,
            'diversification_score': round(100 - concentration_score, 1),
            'recommendation': self._get_portfolio_recommendation(weighted_risk, concentration_score),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def _score_volatility(self, volatility: float) -> float:
        """波动率评分"""
        if volatility < 15:
            return 10
        elif volatility < 25:
            return 25
        elif volatility < 40:
            return 50
        elif volatility < 60:
            return 75
        else:
            return 90

    def _score_market_cap(self, market_cap: float) -> float:
        """市值评分（小市值风险更高）"""
        if market_cap > 1000000000000:  # 1万亿以上
            return 15
        elif market_cap > 100000000000:  # 1000亿以上
            return 30
        elif market_cap > 10000000000:  # 100亿以上
            return 50
        elif market_cap > 1000000000:  # 10亿以上
            return 70
        else:
            return 90

    def _score_liquidity(self, volume: float) -> float:
        """流动性评分"""
        if volume > 10000000000:  # 100亿以上
            return 10
        elif volume > 1000000000:  # 10亿以上
            return 25
        elif volume > 100000000:  # 1亿以上
            return 45
        elif volume > 10000000:  # 1000万以上
            return 65
        else:
            return 85

    def _score_valuation(self, pe_ratio: float) -> float:
        """估值评分"""
        if pe_ratio <= 0:
            return 80  # 亏损企业风险高
        elif pe_ratio < 15:
            return 20
        elif pe_ratio < 30:
            return 35
        elif pe_ratio < 50:
            return 55
        elif pe_ratio < 100:
            return 75
        else:
            return 90

    def _score_trend(self, trend: str) -> float:
        """趋势评分"""
        trend_scores = {
            'strong_bullish': 20,
            'bullish': 35,
            'neutral': 50,
            'bearish': 70,
            'strong_bearish': 85
        }
        return trend_scores.get(trend, 50)

    def _calculate_concentration_risk(self, weights: List[float]) -> float:
        """计算集中度风险"""
        if not weights:
            return 50
        max_weight = max(weights)
        return min(100, max_weight * 150)  # 最大持仓占比越高，风险越高

    def _get_risk_level(self, score: float) -> Dict[str, str]:
        """获取风险等级"""
        for level, info in self.RISK_LEVELS.items():
            if info['score_range'][0] <= score < info['score_range'][1]:
                return info
        return self.RISK_LEVELS['very_high']

    def _get_recommendation(self, score: float) -> str:
        """获取投资建议"""
        if score < 30:
            return '风险较低，适合稳健型投资者'
        elif score < 50:
            return '风险适中，建议适度配置'
        elif score < 70:
            return '风险较高，建议控制仓位'
        else:
            return '风险很高，谨慎投资'

    def _get_portfolio_recommendation(self, risk_score: float, concentration: float) -> str:
        """获取组合建议"""
        recommendations = []

        if risk_score > 60:
            recommendations.append('组合整体风险偏高，建议增加低风险资产')
        if concentration > 50:
            recommendations.append('持仓集中度过高，建议分散投资')

        if not recommendations:
            recommendations.append('组合风险配置合理，继续保持')

        return '；'.join(recommendations)

    def _format_market_cap(self, market_cap: float) -> str:
        """格式化市值"""
        if market_cap >= 1000000000000:
            return f'{market_cap/1000000000000:.2f}万亿'
        elif market_cap >= 100000000:
            return f'{market_cap/100000000:.2f}亿'
        else:
            return f'{market_cap/10000:.2f}万'

    def _format_volume(self, volume: float) -> str:
        """格式化成交额"""
        if volume >= 100000000:
            return f'{volume/100000000:.2f}亿'
        elif volume >= 10000:
            return f'{volume/10000:.2f}万'
        else:
            return f'{volume:.2f}'

def main():
    """主函数"""
    assessor = RiskAssessment()

    # 演示数据
    demo_stock = {
        'symbol': '600519',
        'name': '贵州茅台',
        'volatility': 22.5,
        'market_cap': 2100000000000,
        'avg_volume': 3500000000,
        'pe_ratio': 28.5,
        'trend': 'bullish'
    }

    result = assessor.assess_stock_risk(demo_stock)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
