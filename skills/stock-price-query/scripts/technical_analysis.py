#!/usr/bin/env python3
"""
技术分析工具
支持常用技术指标计算：MA、EMA、RSI、MACD、布林带等
"""

import json
import sys
from typing import List, Dict, Any

def calculate_sma(prices: List[float], period: int) -> List[float]:
    """简单移动平均线"""
    if len(prices) < period:
        return []

    sma = []
    for i in range(period - 1, len(prices)):
        avg = sum(prices[i - period + 1:i + 1]) / period
        sma.append(avg)
    return sma

def calculate_ema(prices: List[float], period: int) -> List[float]:
    """指数移动平均线"""
    if len(prices) < period:
        return []

    multiplier = 2 / (period + 1)
    ema = [sum(prices[:period]) / period]  # 初始SMA

    for price in prices[period:]:
        ema.append((price - ema[-1]) * multiplier + ema[-1])

    return ema

def calculate_rsi(prices: List[float], period: int = 14) -> List[float]:
    """相对强弱指数"""
    if len(prices) < period + 1:
        return []

    gains = []
    losses = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        gains.append(max(0, change))
        losses.append(max(0, -change))

    rsi_values = []

    # 初始平均
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        rsi_values.append(round(rsi, 2))

    return rsi_values

def calculate_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, List[float]]:
    """MACD指标"""
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)

    if len(ema_fast) < len(ema_slow):
        ema_fast = ema_fast[-(len(ema_slow)):]

    macd_line = [f - s for f, s in zip(ema_fast, ema_slow)]
    signal_line = calculate_ema(macd_line, signal) if len(macd_line) >= signal else []
    histogram = [m - s for m, s in zip(macd_line[-len(signal_line):], signal_line)] if signal_line else []

    return {
        'macd': macd_line[-20:] if len(macd_line) > 20 else macd_line,
        'signal': signal_line[-20:] if len(signal_line) > 20 else signal_line,
        'histogram': histogram[-20:] if len(histogram) > 20 else histogram
    }

def calculate_bollinger(prices: List[float], period: int = 20, std_dev: float = 2) -> Dict[str, List[float]]:
    """布林带"""
    if len(prices) < period:
        return {'upper': [], 'middle': [], 'lower': []}

    import statistics

    middle = calculate_sma(prices, period)
    upper = []
    lower = []

    for i in range(period - 1, len(prices)):
        window = prices[i - period + 1:i + 1]
        std = statistics.stdev(window)
        upper.append(middle[i - period + 1] + std_dev * std)
        lower.append(middle[i - period + 1] - std_dev * std)

    return {
        'upper': upper[-20:] if len(upper) > 20 else upper,
        'middle': middle[-20:] if len(middle) > 20 else middle,
        'lower': lower[-20:] if len(lower) > 20 else lower
    }

def analyze_trend(prices: List[float]) -> Dict[str, Any]:
    """综合趋势分析"""
    if len(prices) < 30:
        return {'error': '数据不足，至少需要30个价格点'}

    current_price = prices[-1]

    # 计算各指标
    sma_20 = calculate_sma(prices, 20)
    sma_50 = calculate_sma(prices, 50) if len(prices) >= 50 else []
    ema_12 = calculate_ema(prices, 12)
    rsi = calculate_rsi(prices)
    macd = calculate_macd(prices)
    bollinger = calculate_bollinger(prices)

    # 趋势判断
    trend = 'neutral'
    signals = []

    # MA趋势
    if sma_20 and current_price > sma_20[-1]:
        signals.append('价格在MA20上方')
    elif sma_20:
        signals.append('价格在MA20下方')

    # RSI判断
    rsi_value = rsi[-1] if rsi else 50
    if rsi_value > 70:
        signals.append('RSI超买')
    elif rsi_value < 30:
        signals.append('RSI超卖')

    # MACD判断
    if macd['histogram']:
        if macd['histogram'][-1] > 0:
            signals.append('MACD多头')
        else:
            signals.append('MACD空头')

    # 综合判断
    bullish_signals = sum(1 for s in signals if '上方' in s or '超卖' in s or '多头' in s)
    bearish_signals = sum(1 for s in signals if '下方' in s or '超买' in s or '空头' in s)

    if bullish_signals > bearish_signals:
        trend = 'bullish'
    elif bearish_signals > bullish_signals:
        trend = 'bearish'

    return {
        'current_price': current_price,
        'trend': trend,
        'signals': signals,
        'indicators': {
            'rsi': rsi_value,
            'sma_20': sma_20[-1] if sma_20 else None,
            'sma_50': sma_50[-1] if sma_50 else None,
            'ema_12': ema_12[-1] if ema_12 else None,
            'macd': macd['macd'][-1] if macd['macd'] else None,
            'macd_signal': macd['signal'][-1] if macd['signal'] else None,
            'bollinger_upper': bollinger['upper'][-1] if bollinger['upper'] else None,
            'bollinger_lower': bollinger['lower'][-1] if bollinger['lower'] else None
        }
    }

def main():
    """主函数 - 演示模式"""
    # 演示数据：模拟30天的收盘价
    demo_prices = [
        100, 102, 101, 103, 105, 104, 106, 108, 107, 109,
        111, 110, 112, 114, 113, 115, 117, 116, 118, 120,
        119, 121, 123, 122, 124, 126, 125, 127, 129, 128
    ]

    result = analyze_trend(demo_prices)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
