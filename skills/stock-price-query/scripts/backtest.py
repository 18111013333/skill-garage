#!/usr/bin/env python3
"""
投资策略回测工具
模拟历史数据验证投资策略效果
"""

import json
import sys
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import random

class Backtester:
    """投资策略回测器"""

    def __init__(self, initial_capital: float = 100000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0
        self.trades = []
        self.equity_curve = []

    def run_backtest(self, price_data: List[float], strategy: Dict[str, Any]) -> Dict[str, Any]:
        """运行回测"""
        self.capital = self.initial_capital
        self.position = 0
        self.trades = []
        self.equity_curve = []

        for i, price in enumerate(price_data):
            # 计算指标
            signal = self._generate_signal(price_data[:i+1], strategy)

            # 执行交易
            if signal == 'buy' and self.capital > 0:
                shares = self.capital / price
                self.position += shares
                self.capital = 0
                self.trades.append({
                    'type': 'buy',
                    'price': price,
                    'shares': shares,
                    'day': i
                })

            elif signal == 'sell' and self.position > 0:
                self.capital = self.position * price
                self.trades.append({
                    'type': 'sell',
                    'price': price,
                    'shares': self.position,
                    'day': i
                })
                self.position = 0

            # 记录权益曲线
            equity = self.capital + self.position * price
            self.equity_curve.append(equity)

        # 计算绩效
        return self._calculate_performance()

    def _generate_signal(self, prices: List[float], strategy: Dict) -> str:
        """生成交易信号"""
        if len(prices) < strategy.get('ma_period', 20):
            return 'hold'

        strategy_type = strategy.get('type', 'ma_cross')

        if strategy_type == 'ma_cross':
            return self._ma_cross_signal(prices, strategy)
        elif strategy_type == 'rsi':
            return self._rsi_signal(prices, strategy)
        elif strategy_type == 'macd':
            return self._macd_signal(prices, strategy)
        else:
            return 'hold'

    def _ma_cross_signal(self, prices: List[float], strategy: Dict) -> str:
        """均线交叉信号"""
        fast_period = strategy.get('fast_period', 5)
        slow_period = strategy.get('slow_period', 20)

        if len(prices) < slow_period:
            return 'hold'

        fast_ma = sum(prices[-fast_period:]) / fast_period
        slow_ma = sum(prices[-slow_period:]) / slow_period

        if len(prices) > slow_period + 1:
            prev_fast = sum(prices[-fast_period-1:-1]) / fast_period
            prev_slow = sum(prices[-slow_period-1:-1]) / slow_period

            if fast_ma > slow_ma and prev_fast <= prev_slow:
                return 'buy'
            elif fast_ma < slow_ma and prev_fast >= prev_slow:
                return 'sell'

        return 'hold'

    def _rsi_signal(self, prices: List[float], strategy: Dict) -> str:
        """RSI信号"""
        period = strategy.get('rsi_period', 14)
        oversold = strategy.get('oversold', 30)
        overbought = strategy.get('overbought', 70)

        if len(prices) < period + 1:
            return 'hold'

        # 计算RSI
        gains = []
        losses = []
        for i in range(1, min(period + 1, len(prices))):
            change = prices[-i] - prices[-i-1]
            if change > 0:
                gains.append(change)
            else:
                losses.append(abs(change))

        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 0

        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        if rsi < oversold:
            return 'buy'
        elif rsi > overbought:
            return 'sell'

        return 'hold'

    def _macd_signal(self, prices: List[float], strategy: Dict) -> str:
        """MACD信号"""
        # 简化实现
        return 'hold'

    def _calculate_performance(self) -> Dict[str, Any]:
        """计算绩效指标"""
        if not self.equity_curve:
            return {'error': '无交易数据'}

        final_equity = self.equity_curve[-1]
        total_return = (final_equity - self.initial_capital) / self.initial_capital * 100

        # 计算最大回撤
        max_drawdown = 0
        peak = self.equity_curve[0]
        for equity in self.equity_curve:
            if equity > peak:
                peak = equity
            drawdown = (peak - equity) / peak * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        # 计算夏普比率（简化）
        returns = []
        for i in range(1, len(self.equity_curve)):
            ret = (self.equity_curve[i] - self.equity_curve[i-1]) / self.equity_curve[i-1]
            returns.append(ret)

        if returns:
            avg_return = sum(returns) / len(returns)
            variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
            std_dev = variance ** 0.5
            sharpe = (avg_return * 252) / (std_dev * (252 ** 0.5)) if std_dev > 0 else 0
        else:
            sharpe = 0

        # 胜率
        winning_trades = 0
        total_trades = len(self.trades) // 2
        for i in range(0, len(self.trades) - 1, 2):
            if i + 1 < len(self.trades):
                buy = self.trades[i]
                sell = self.trades[i + 1]
                if sell['price'] > buy['price']:
                    winning_trades += 1

        win_rate = winning_trades / total_trades * 100 if total_trades > 0 else 0

        return {
            'initial_capital': self.initial_capital,
            'final_equity': round(final_equity, 2),
            'total_return': round(total_return, 2),
            'max_drawdown': round(max_drawdown, 2),
            'sharpe_ratio': round(sharpe, 2),
            'win_rate': round(win_rate, 2),
            'total_trades': total_trades,
            'trades': self.trades
        }

def generate_demo_data(days: int = 252) -> List[float]:
    """生成演示数据"""
    prices = [100]
    for _ in range(days - 1):
        change = random.gauss(0.001, 0.02)
        new_price = prices[-1] * (1 + change)
        prices.append(max(1, new_price))
    return prices

def main():
    """主函数"""
    backtester = Backtester(100000)

    # 演示数据
    price_data = generate_demo_data(252)

    # 策略配置
    strategy = {
        'type': 'ma_cross',
        'fast_period': 5,
        'slow_period': 20
    }

    result = backtester.run_backtest(price_data, strategy)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
