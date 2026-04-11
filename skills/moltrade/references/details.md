
```bash
pip install binance-sdk-spot
```

### Config Fields

Add a `binance` block alongside the existing `trading` block:

```json
{
  "trading": {
    "exchange": "binance",
    "default_symbol": "BTCUSDT",
    "default_strategy": "momentum"
  },
  "binance": {
    "api_key": "your_mainnet_api_key",
    "api_secret": "your_mainnet_api_secret",
    "testnet_api_key": "your_testnet_api_key",
    "testnet_api_secret": "your_testnet_api_secret"
  }
}
```

> **Note**: Binance testnet uses keys generated separately at <https://testnet.binance.vision> (GitHub login required). Mainnet keys do **not** work on the testnet.

### Testnet (–-test)

When `--test` is passed the bot routes all requests to `testnet.binance.vision` and uses `binance.testnet_api_key` / `testnet_api_secret`. If testnet keys are absent it falls back to mainnet keys, which will cause auth errors against the testnet endpoint.

```bash
python trader/main.py --config config.json --test --strategy momentum --symbol BTCUSDT
```

### Live Trading

```bash
python trader/main.py --config config.json --strategy momentum --symbol BTCUSDT
```

### Backtest

```bash
python trader/backtest.py --config trader/config.example.json --strategy momentum --symbol BTCUSDT --interval 1h --limit 500
```

### Supported Interface

`BinanceClient` (`trader/binance_api.py`) implements the same interface as `HyperliquidClient`:

| Method                                                 | Description                                                   |
| ------------------------------------------------------ | ------------------------------------------------------------- |
| `get_candles(symbol, interval, limit)`                 | K-line data as `[ts, open, high, low, close, vol]`            |
| `get_balance(asset)`                                   | Free balance for an asset (default `"USDT"`)                  |
| `get_positions()`                                      | Non-zero asset balances (spot has no margin positions)        |
| `get_open_orders()`                                    | All current open orders                                       |
| `place_order(symbol, is_buy, size, price, order_type)` | LIMIT or MARKET order with auto lot-size / tick-size rounding |
| `cancel_order(order_id, symbol)`                       | Cancel by order ID                                            |
| `cancel_all_orders(symbol)`                            | Cancel all orders (optionally for one symbol)                 |
| `get_ticker_price(symbol)`                             | Latest traded price                                           |

## Uniswap V3 Support

Moltrade supports decentralized swaps on EVM chains using Uniswap V3 Router via `web3`. Set `trading.exchange` to `"uniswap"` in your config. Note that DEX swaps are atomic; there are no open limit orders or margin positions, and price charting requires an external oracle (currently returns empty or mock data locally).

### Install Web3

```bash
pip install web3
```

### Config Fields

Add a `uniswap` block alongside the existing `trading` block:

```json
{
  "trading": {
    "exchange": "uniswap",
    "default_symbol": "WETH",
    "default_strategy": "momentum"
  },
  "uniswap": {
    "rpc_url": "https://eth-mainnet.g.alchemy.com/v2/...",
    "private_key": "your_wallet_private_key",
    "chain_id": 1,
    "router_address": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
    "slippage_tolerance": 0.005,
    "default_token_in": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "default_token_out": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
  }
}
```

## Polymarket Support

Moltrade supports prediction markets on Polymarket via the official `py-clob-client`. Set `trading.exchange` to `"polymarket"` in your config.

### Install CLOB Client

```bash
pip install py-clob-client
```

### Config Fields

Add a `polymarket` block alongside the existing `trading` block:

```json
{
  "trading": {
    "exchange": "polymarket",
    "default_symbol": "TOKEN_ID_HERE",
    "default_strategy": "momentum"
  },
  "polymarket": {
    "api_key": "your_polymarket_api_key",
    "api_secret": "your_polymarket_api_secret",
    "api_passphrase": "your_polymarket_api_passphrase",
    "private_key": "your_wallet_private_key",
    "chain_id": 137
  }
}
```

## Add Exchange Adapter

- Implement adapter in `trader/exchanges/` matching `HyperliquidClient` interface (`get_candles`, `get_balance`, `get_positions`, `place_order`, etc.).
- Register in `trader/exchanges/factory.py` keyed by `trading.exchange`.
- Update config `trading.exchange` and rerun backtest/test-mode.

## Integrate New Strategy

- Follow `trader/strategies/INTEGRATION.md` to subclass `BaseStrategy` and register in `get_strategy`.
- Add config under `strategies.<name>`; backtest, then test-mode before live.

## Safety / Secrets

- Never print or commit private keys, mnemonics, nsec, or shared keys.
- Default to test mode; require explicit consent for live trading.
