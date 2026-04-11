```

**What if it picks wrong?** Override it: `python3 scripts/search.py -p tavily -q "your query"`

**Debug routing:** `python3 scripts/search.py --explain-routing -q "your query"`

---

## 📖 Usage Examples

### Let Auto-Routing Choose (Recommended)

```bash
python3 scripts/search.py -q "Tesla Model 3 price"
python3 scripts/search.py -q "explain machine learning"
python3 scripts/search.py -q "latest AI policy updates in Germany"
python3 scripts/search.py -q "startups like Figma"
```

### Force a Specific Provider

```bash
python3 scripts/search.py -p serper -q "weather Berlin"
python3 scripts/search.py -p tavily -q "quantum computing" --depth advanced
python3 scripts/search.py -p querit -q "latest AI policy updates in Germany"
python3 scripts/search.py -p exa --similar-url "https://stripe.com" --category company
python3 scripts/search.py -p you -q "breaking tech news" --include-news
python3 scripts/search.py -p searxng -q "linux distros" --engines "google,bing"
```

---

## ⚙ Configuration

```json
{
  "auto_routing": {
    "enabled": true,
    "fallback_provider": "serper",
    "confidence_threshold": 0.3,
    "disabled_providers": []
  },
  "serper": {"country": "us", "language": "en"},
  "tavily": {"depth": "advanced"},
  "exa": {"type": "neural"},
  "you": {"country": "US", "include_news": true},
  "searxng": {"instance_url": "https://your-instance.example.com"}
}
```

---

## 📊 Provider Comparison

| Feature | Serper | Tavily | Exa | Perplexity | You.com | SearXNG |
|---------|:------:|:------:|:---:|:----------:|:-------:|:-------:|
| Speed | ⚡⚡⚡ | ⚡⚡ | ⚡⚡ | ⚡⚡ | ⚡⚡⚡ | ⚡⚡ |
| Direct Answers | ✗ | ✗ | ✗ | ✓✓ | ✗ | ✗ |
| Citations | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| Factual Accuracy | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Semantic Understanding | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Full Page Content | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ |
| Shopping/Local | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Find Similar Pages | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| RAG-Optimized | ✗ | ✓ | ✗ | ✗ | ✓✓ | ✗ |
| Privacy-First | ✗ | ✗ | ✗ | ✗ | ✗ | ✓✓ |
| API Cost | $$ | $$ | $$ | Via Kilo | $ | **FREE** |

---

## ❓ Common Questions

### Do I need API keys for all providers?
**No.** You only need keys for providers you want to use. Start with one (Serper recommended), add more later.

### Which provider should I start with?
**Serper** — fastest, cheapest, largest free tier (2,500 queries/month), and handles most queries well.

### What if I run out of free queries?
The skill automatically falls back to your other configured providers. Or switch to SearXNG (unlimited, self-hosted).

### How much does this cost?
- **Free tiers:** 2,500 (Serper) + 1,000 (Tavily) + 1,000 (Exa) = 4,500+ free searches/month
- **SearXNG:** Completely free (just ~$5/mo if you self-host on a VPS)
- **Paid plans:** Start around $10-50/month depending on provider

### Is SearXNG really private?
**Yes, if self-hosted.** You control the server, no tracking, no profiling. Public instances depend on the operator's policy.

### How do I set up SearXNG?
```bash
# Docker (5 minutes)
docker run -d -p 8080:8080 searxng/searxng
```
Then enable JSON API in `settings.yml`. See [docs.searxng.org](https://docs.searxng.org/admin/installation.html).

### Why did it route my query to the "wrong" provider?
Sometimes queries are ambiguous. Use `--explain-routing` to see why, then override with `-p provider` if needed.

---

## 🔄 Automatic Fallback

If one provider fails (rate limit, timeout, error), the skill automatically tries the next provider. You'll see `routing.fallback_used: true` in the response when this happens.

---

## 📤 Output Format

```json
{
  "provider": "serper",
  "query": "iPhone 16 price",
  "results": [{"title": "...", "url": "...", "snippet": "...", "score": 0.95}],
  "routing": {
    "auto_routed": true,
    "provider": "serper",
    "confidence": 0.78,
    "confidence_level": "high"
  }
}
```

---

## ⚠ Important Note

**Tavily, Serper, and Exa are NOT core OpenClaw providers.**

❌ Don't modify `~/.openclaw/openclaw.json` for these  
✅ Use this skill's scripts — keys auto-load from `.env`

---

## 🔒 Security

**SearXNG SSRF Protection:** The SearXNG instance URL is validated with defense-in-depth:
- Enforces `http`/`https` schemes only
- Blocks cloud metadata endpoints (169.254.169.254, metadata.google.internal)
- Resolves hostnames and blocks private/internal IPs (loopback, RFC1918, link-local, reserved)
- Operators who intentionally self-host on private networks can set `SEARXNG_ALLOW_PRIVATE=1`

## 📚 More Documentation

- **[FAQ.md](FAQ.md)** — Detailed answers to more questions
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — Fix common errors
- **[README.md](README.md)** — Full technical reference

---

## 🔗 Quick Links

- [Serper](https://serper.dev) — Google Search API
- [Tavily](https://tavily.com) — AI Research Search
- [Exa](https://exa.ai) — Neural Search
- [Perplexity](https://www.perplexity.ai) — AI-Synthesized Answers (via [Kilo Gateway](https://kilo.ai))
- [You.com](https://api.you.com) — RAG/Real-time Search
- [SearXNG](https://docs.searxng.org) — Privacy-First Meta-Search
