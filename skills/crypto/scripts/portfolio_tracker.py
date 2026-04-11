#!/usr/bin/env python3
"""
投资组合追踪工具
支持多币种、多交易所的资产追踪和收益计算
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 配置文件路径
CONFIG_DIR = Path.home() / '.config' / 'crypto'
PORTFOLIO_FILE = CONFIG_DIR / 'portfolio.json'

def ensure_config_dir():
    """确保配置目录存在"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_portfolio():
    """加载投资组合"""
    if PORTFOLIO_FILE.exists():
        with open(PORTFOLIO_FILE, 'r') as f:
            return json.load(f)
    return {'holdings': [], 'history': []}

def save_portfolio(portfolio):
    """保存投资组合"""
    ensure_config_dir()
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)

def add_holding(symbol, amount, buy_price, exchange='binance', buy_date=None):
    """添加持仓"""
    portfolio = load_portfolio()

    holding = {
        'id': f"{symbol}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'symbol': symbol,
        'amount': float(amount),
        'buy_price': float(buy_price),
        'exchange': exchange,
        'buy_date': buy_date or datetime.now().strftime('%Y-%m-%d'),
        'created_at': datetime.now().isoformat()
    }

    portfolio['holdings'].append(holding)
    save_portfolio(portfolio)

    return {'status': 'success', 'holding': holding}

def remove_holding(holding_id):
    """移除持仓"""
    portfolio = load_portfolio()
    original_count = len(portfolio['holdings'])

    portfolio['holdings'] = [h for h in portfolio['holdings'] if h['id'] != holding_id]

    if len(portfolio['holdings']) < original_count:
        save_portfolio(portfolio)
        return {'status': 'success', 'message': f'已移除持仓 {holding_id}'}
    else:
        return {'status': 'error', 'message': f'未找到持仓 {holding_id}'}

def calculate_performance(current_prices):
    """
    计算投资组合表现
    current_prices: {symbol: current_price} 字典
    """
    portfolio = load_portfolio()

    if not portfolio['holdings']:
        return {'status': 'empty', 'message': '投资组合为空'}

    results = []
    total_cost = 0
    total_value = 0

    for holding in portfolio['holdings']:
        symbol = holding['symbol']
        current_price = current_prices.get(symbol, holding['buy_price'])

        cost = holding['amount'] * holding['buy_price']
        value = holding['amount'] * current_price
        pnl = value - cost
        pnl_percent = (pnl / cost * 100) if cost > 0 else 0

        total_cost += cost
        total_value += value

        results.append({
            'symbol': symbol,
            'amount': holding['amount'],
            'buy_price': holding['buy_price'],
            'current_price': current_price,
            'cost': cost,
            'value': value,
            'pnl': pnl,
            'pnl_percent': round(pnl_percent, 2),
            'exchange': holding['exchange']
        })

    total_pnl = total_value - total_cost
    total_pnl_percent = (total_pnl / total_cost * 100) if total_cost > 0 else 0

    return {
        'status': 'success',
        'holdings': results,
        'summary': {
            'total_cost': round(total_cost, 2),
            'total_value': round(total_value, 2),
            'total_pnl': round(total_pnl, 2),
            'total_pnl_percent': round(total_pnl_percent, 2),
            'holding_count': len(results)
        },
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def list_holdings():
    """列出所有持仓"""
    portfolio = load_portfolio()
    return {
        'status': 'success',
        'holdings': portfolio['holdings'],
        'count': len(portfolio['holdings'])
    }

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python portfolio_tracker.py <command> [args]")
        print("命令:")
        print("  add <symbol> <amount> <buy_price> [exchange]  - 添加持仓")
        print("  remove <holding_id>                            - 移除持仓")
        print("  list                                           - 列出持仓")
        print("  performance <price_json>                       - 计算收益")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 5:
            print("用法: add <symbol> <amount> <buy_price> [exchange]")
            sys.exit(1)
        result = add_holding(
            sys.argv[2],
            sys.argv[3],
            sys.argv[4],
            sys.argv[5] if len(sys.argv) > 5 else 'binance'
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == 'remove':
        if len(sys.argv) < 3:
            print("用法: remove <holding_id>")
            sys.exit(1)
        result = remove_holding(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == 'list':
        result = list_holdings()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == 'performance':
        if len(sys.argv) < 3:
            print("用法: performance '<price_json>'")
            print("示例: performance '{\"BTC/USDT\": 70000, \"ETH/USDT\": 3500}'")
            sys.exit(1)
        prices = json.loads(sys.argv[2])
        result = calculate_performance(prices)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(f"未知命令: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
