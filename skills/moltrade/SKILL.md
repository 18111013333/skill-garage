---
name: moltrade
description: Operate the Moltrade trading bot (config, backtest, test-mode runs, Nostr signal broadcast, exchange adapters, strategy integration) in OpenClaw.
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins: ["python", "pip"]
    homepage: https://github.com/hetu-project/moltrade.git
---

# Moltrade Bot Skill

**Moltrade** is a decentralized, automated trading assistant that lets you run quant strategies, share encrypted signals, and allow others to copy your trades—all securely via the Nostr network. Earn reputation and credits based on your trading performance.

![Moltrade](https://raw.githubusercontent.com/hetu-project/moltrade/main/assets/moltrade-background-2.jpg)

**YOUR 24/7 AI TRADER ! EARNING MONEY WHILE YOU'RE SLEEPING.**

[![Twitter Follow](https://img.shields.io/twitter/follow/hetu_protocol?style=social&label=Follow)](https://x.com/hetu_protocol) [![Telegram](https://img.shields.io/badge/Telegram-Hetu_Builders-blue)](https://t.me/+uJrRgjtSsGw3MjZl) [![ClawHub](https://img.shields.io/badge/ClawHub-Read-orange)](https://clawhub.ai/ai-chen2050/moltrade) [![Website](https://img.shields.io/badge/Website-moltrade.ai-green)](https://www.moltrade.ai/)

---

## Advantages

**Moltrade** balances security, usability, and scalability. Key advantages include:

1. **Client-side Key self-hosting,not cloud Custody,**: All sensitive keys and credentials remain on the user's machine; the cloud relay never holds funds or private keys, minimizing custodial risk.**No access to private keys or funds.**
2. **Encrypted, Targeted Communication**: Signals are encrypted before publishing and only decryptable by intended subscribers, preserving strategy privacy and subscriber security.
3. **Lightweight Cloud Re-encryption & Broadcast**: The cloud acts as an efficient relay/re-broadcaster without storing private keys; re-encryption or forwarding techniques improve delivery reliability and reach.
4. **One-Click Copy Trading (User Friendly)**: Provides an out-of-the-box copy-trading experience for non-expert users—set up in a few steps and execute signals locally.
5. **OpenClaw Strategy Advisor**: Integrates OpenClaw as an advisory tool for automated backtests and improvement suggestions; users decide whether to adopt recommended changes.
6. **Cloud Can Be Decentralized Relayer Network**: The lightweight relay architecture allows future migration to decentralized relay networks, reducing single points of failure and improving censorship resistance.
7. **Unified Incentive (Credit) System**: A transparent, verifiable Credit mechanism rewards all participants (signal providers, followers, relay nodes), aligning incentives across the ecosystem.

## **How It Works (Simplified Flow)**

```bash
1) Run Your Bot  ──→  2) Generate & Encrypt  ──→  3) Relay  ──→  4) Copy & Execute  ──→  5) Verify & Earn
```

## Install & Init

- If you are inside **OpenClaw**, you can install directly via ClawHub:

```bash
clawhub search moltrade
clawhub install moltrade
```

- OR Clone the repo and install Python deps locally:
  - `git clone https://github.com/hetu-project/moltrade.git`
  - `cd moltrade/trader && pip install -r requirements.txt`
- Initialize a fresh config with the built-in wizard:
  - **Security Requirement**: Always ask the human user to run `python main.py --init` themselves in a separate terminal. Do not ask for or handle their wallet private keys directly or save them to disk via agent scripts.
- For CI/agents, keep using the repo checkout; there is no separate pip package/CLI yet.

## Update Config Safely

- Backup or show planned diff before edits.
- Change only requested fields (e.g., `trading.exchange`, `trading.default_strategy`, `nostr.relays`).
- Validate JSON; keep types intact. Remind user to provide real secrets themselves.

## Run Backtest (local)

- Install deps: `pip install -r trader/requirements.txt`.
- Command: `python trader/backtest.py --config trader/config.example.json --strategy <name> --symbol <symbol> --interval 1h --limit 500`.
- Report PnL/win rate/trade count/drawdown if available. Use redacted config (no real keys).

## Start Bot (test mode)

- Ensure `config.json` exists (run `python main.py --init` if not) and `trading.exchange` set (default hyperliquid).
- Command: `python trader/main.py --config config.json --test --strategy <name> --symbol <symbol> --interval 300`.
- Watch `trading_bot.log`; never switch to live without explicit user approval.

## Run Bot (live)

- Only after validation on test mode; remove `--test` to hit mainnet.
- Command: `python trader/main.py --config config.json --strategy <name> --symbol <symbol>`.
- Double-check keys, risk limits, and symbol before starting; live mode will place real orders.

## Copy-trade Usage (live)

- Follower (mirrors leader, no strategy trading): `python trader/main.py --config trader/config.json --strategy momentum --symbol HYPE --copytrade follower`

## Broadcast Signals to Nostr

- Check `nostr` block: `nsec`, `relayer_nostr_pubkey`, `relays`, `sid`.
- `SignalBroadcaster` is wired in `main.py`. In test mode, verify `send_trade_signal` / `send_execution_report` run without errors.

## Binance Spot Support

Moltrade supports Binance Spot trading via `binance-sdk-spot`. Set `trading.exchange` to `"binance"` in your config and provide API credentials.

> **Related Skills** (raw API calls, not tied to the bot runtime):
>
> - [`binance/spot`](binance/spot/SKILL.md) — Binance Spot REST API skill: market data, order management, account info. Requires API key + secret; supports testnet and mainnet.
> - [`binance/square-post`](binance/square-post/SKILL.md) — Binance Square social platform skill: post trading insights/signals as text content via the Square OpenAPI. Requires a Square OpenAPI key.

### Install Binance SDK

## 详细文档

请参阅 [references/details.md](references/details.md)
