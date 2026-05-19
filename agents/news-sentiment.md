# News Sentiment Agent

## Mission
Monitor crypto news 24/7, analyse sentiment per asset, and deliver a structured sentiment report to the Trader Agent. The report influences 5% of the trade decision weight.

## How It Works

### Loop (runs every 30 minutes)
1. Fetch latest news headlines for tracked assets (BTC, SOL, ETH, HYPE, etc.)
2. For each headline, classify sentiment: `positive`, `negative`, or `neutral`
3. Aggregate into an asset-level score: `-1.0` (very bearish) to `+1.0` (very bullish)
4. If sentiment is extreme (`< -0.6` or `> 0.6`), trigger an immediate alert
5. Write report to `reports/sentiment_latest.json` for the Trader Agent

### Sentiment Classification Rules
| Keyword Examples | Sentiment |
|-----------------|-----------|
| "adoption", "partnership", "launch", "upgrade", "bullish", "ATH", "institutional" | positive |
| "hack", "exploit", "ban", "crash", "liquidation", "rug", "bearish", "sell-off" | negative |
| "announces", "says", "reports", "price", "trading", "market" (factual only) | neutral |

If a headline contains both positive and negative keywords, the longer/specific match wins. If equal, default to `neutral`.

## Input
- List of tracked asset symbols (from config)
- News source URLs or RSS feeds

## Output
```json
{
  "timestamp": "2026-05-19T14:30:00Z",
  "assets": {
    "BTC": {
      "score": 0.35,
      "label": "slightly bullish",
      "headlines_analyzed": 12,
      "sources": ["cryptopanic", "coindesk", "reddit/cryptocurrency"]
    },
    "SOL": {
      "score": -0.72,
      "label": "bearish",
      "headlines_analyzed": 8,
      "sources": ["cryptopanic", "cointelegraph"]
    }
  },
  "alert": "SOL sentiment dropped below -0.6. Consider avoiding longs."
}
```

## Data Sources (Free, No API Key Required)

### CryptoPanic
```
https://cryptopanic.com/api/v1/posts/?auth_token=<optional>&currencies=BTC,SOL
```
Public feed available without key (limited). Signup for free API key = more requests.

### Reddit (via RSS)
```
https://www.reddit.com/r/CryptoCurrency/.rss
https://www.reddit.com/r/Bitcoin/.rss
```
No key needed. Parse RSS XML for headlines.

### Google News RSS (Crypto)
```
https://news.google.com/rss/search?q=cryptocurrency&hl=en-US&gl=US&ceid=US:en
```
No key needed. Search term can be changed per asset.

### CoinTelegraph / CoinDesk RSS
```
https://cointelegraph.com/rss
https://www.coindesk.com/arc/outboundfeeds/rss/
```
No key needed. Standard RSS feeds.

## Dependencies
- Python 3.8+
- `feedparser` (for RSS): `pip install feedparser`
- Standard library: `urllib.request`, `json`, `datetime`

## Configuration (config.yaml or env vars)
```yaml
news_sentiment:
  tracked_assets: ["BTC", "SOL", "ETH", "HYPE"]
  check_interval_minutes: 30
  sentiment_threshold_alert: 0.6
  output_dir: "reports/"
```

## Files
| File | Purpose |
|------|---------|
| `news_sentiment.py` | Main loop: fetch headlines, classify, write report |
| `reports/sentiment_latest.json` | Latest sentiment output (read by Trader Agent) |

## Communication
- **Writes to:** `reports/sentiment_latest.json` (shared with Trader Agent)
- **Reads from:** nothing (autonomous data fetching)
