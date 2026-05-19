# Data Analyst Agent

## Mission
Scan the markets for actionable opportunities: top gainers, top losers, unusual volume spikes, and emerging patterns. Package findings into trade ideas and send them to the Backtester Agent for verification.

## How It Works

### Loop (runs every 60 minutes)
1. Request current market data from **Data Getter Agent** (top movers, volume leaders)
2. Filter for assets that meet minimum criteria (liquidity, volume, volatility)
3. For each candidate, request additional data (order book, funding rate, recent candles)
4. Analyse for patterns (breakout, reversal, momentum continuation)
5. Package as a structured trade idea for the Backtester Agent
6. If no candidates meet criteria, report "no opportunities found"

### Gainers & Losers Detection

**Gainer criteria (must meet ALL):**
- Price change +5% or more in last 24h
- 24h volume > $1,000,000
- Not a honeypot / flagged token (DEX pairs only)
- At least 100 trades in last 24h

**Loser criteria (must meet ALL):**
- Price change -5% or more in last 24h
- 24h volume > $1,000,000
- At least 100 trades in last 24h

**Volume spike criteria:**
- Current 1h volume > 3x average 24h hourly volume

### Pattern Recognition

The Data Analyst checks for these basic patterns on the 1h chart (last 24 candles):

| Pattern | Detection Rule | Signal |
|---------|---------------|--------|
| Bullish Engulfing | Previous candle red, current green, current body fully covers previous | Reversal up |
| Bearish Engulfing | Previous candle green, current red, current body fully covers previous | Reversal down |
| Doji | Body < 5% of total range | Indecision, potential reversal |
| 3 Green Soldiers | 3 consecutive bullish candles, each closing higher | Strong uptrend |
| 3 Black Crows | 3 consecutive bearish candles, each closing lower | Strong downtrend |
| Breakout | Price closes above recent 24h high with volume spike | Momentum long |
| Breakdown | Price closes below recent 24h low with volume spike | Momentum short |

### Data Request Flow
```
Data Analyst Agent
  │
  ├──> Data Getter Agent: "top gainers last 24h"
  ├──> Data Getter Agent: "top losers last 24h"
  ├──> Data Getter Agent: "volume spikes last 1h"
  │
  └── for each candidate:
       ├──> Data Getter Agent: "klines symbol interval=1h limit=24"
       ├──> Data Getter Agent: "orderbook symbol"
       └──> Data Getter Agent: "ticker symbol 24hr"
```

## Output: Trade Idea
```json
{
  "trade_idea_id": "ti_20260519_001",
  "asset": "SOL",
  "direction": "long",
  "entry_zone": {
    "min": 84.50,
    "max": 85.50
  },
  "stop_loss": 82.00,
  "take_profit": 92.00,
  "pattern": "bullish_engulfing",
  "confidence": "medium",
  "reasoning": "Bullish engulfing on 1h after 8h downtrend. Volume 2x average. SOL funding rate neutral.",
  "market_data": {
    "24h_change": "+6.2%",
    "24h_volume": "$340M",
    "volume_spike": true
  }
}
```

## Dependencies
- Python 3.8+
- Standard library: `urllib.request`, `json`, `datetime`, `math`
- No external pip packages required (uses Data Getter Agent for all API access)

## Configuration
```yaml
data_analyst:
  check_interval_minutes: 60
  min_volume_usd: 1000000
  min_24h_change_pct: 5.0
  min_trades_24h: 100
  tracked_markets:
    - cex: ["BTCUSDT", "SOLUSDT", "ETHUSDT"]
    - dexs: ["solana"]
  output_dir: "reports/"
```

## Files
| File | Purpose |
|------|---------|
| `data_analyst.py` | Main scan loop, pattern recognition, trade idea generation |
| `reports/trade_ideas_latest.json` | Output read by Backtester Agent |

## Communication
- **Calls:** Data Getter Agent (for market data)
- **Writes to:** `reports/trade_ideas_latest.json` (read by Backtester Agent)
