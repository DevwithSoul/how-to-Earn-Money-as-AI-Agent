# Data Getter Agent

## Mission
Fetch raw market data from free public APIs on demand. Serve data to the Backtester Agent (historical) and Data Analyst Agent (current). Centralise all API access so other agents never need to touch external endpoints directly.

## How It Works

### Request-Driven (No Loop)
The Data Getter does NOT run on a timer. It listens for requests from other agents and returns structured JSON data:

1. **Data Analyst** requests: "Give me top 10 gainers on Solana in last 24h"
2. **Backtester** requests: "Give me BTCUSDT hourly candles from 2026-04-01 to 2026-05-01"
3. **Trader** requests: "Give me current BTC mid-price from 3 sources"

### Response Format
Every response follows the same envelope:
```json
{
  "request_id": "req_20260519_001",
  "source": "binance",
  "data_type": "klines_1h",
  "symbol": "BTCUSDT",
  "records": 168,
  "data": [...],
  "timestamp": "2026-05-19T14:30:00Z"
}
```

## Data Sources (All Free, No API Key Required)

### 1. Binance Public API
```
Base: https://api.binance.com
```
| Endpoint | Data | Rate Limit |
|----------|------|-----------|
| `/api/v3/ticker/price?symbol=BTCUSDT` | Spot price | 1200 req/min |
| `/api/v3/ticker/24hr?symbol=BTCUSDT` | 24h stats (high, low, volume, change) | 1200 req/min |
| `/api/v3/depth?symbol=BTCUSDT&limit=10` | Order book (bids + asks) | 1200 req/min |
| `/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=500` | Candles (OHLCV) | 1200 req/min |
| `/api/v3/exchangeInfo` | All pairs | 1200 req/min |
| `/api/v3/ticker/24hr` | ALL tickers at once | 1200 req/min |

**Best for:** Reliable spot prices, deep order books, long historical klines.

### 2. CoinGecko Free API
```
Base: https://api.coingecko.com/api/v3
```
| Endpoint | Data | Rate Limit |
|----------|------|-----------|
| `/simple/price?ids=bitcoin,solana&vs_currencies=usd` | Current prices | 10-30 req/min |
| `/coins/markets?vs_currency=usd&order=volume_desc&per_page=50` | Top coins by volume | 10-30 req/min |
| `/coins/markets?vs_currency=usd&order=gecko_desc&per_page=50` | Newest listed coins | 10-30 req/min |
| `/search/trending` | Trending coins right now | 10-30 req/min |
| `/coins/bitcoin` | Full metadata, description, links | 10-30 req/min |

**Best for:** Coin discovery, metadata, rankings, trending.

### 3. Bybit Public API
```
Base: https://api.bybit.com/v5/market
```
| Endpoint | Data | Rate Limit |
|----------|------|-----------|
| `/tickers?category=spot&symbol=BTCUSDT` | Spot ticker | 50 req/min |
| `/tickers?category=linear&symbol=BTCUSDT` | Perp ticker (funding rate, OI) | 50 req/min |
| `/orderbook?category=spot&symbol=BTCUSDT&limit=25` | Order book | 50 req/min |
| `/kline?category=spot&symbol=BTCUSDT&interval=60&limit=200` | Hourly klines | 50 req/min |

**Best for:** Perpetuals data, funding rates, backup when Binance is rate-limited.

### 4. Kraken Public API
```
Base: https://api.kraken.com/0/public
```
| Endpoint | Data | Rate Limit |
|----------|------|-----------|
| `/Ticker?pair=XBTUSD` | Current ticker | generous |
| `/Depth?pair=XBTUSD&count=10` | Order book | generous |
| `/OHLC?pair=XBTUSD&interval=60` | Hourly candles | generous |

**Best for:** European liquidity, cross-reference, highly reliable uptime.

### 5. Hyperliquid Public Info API
```
Base: https://api.hyperliquid.xyz/info
```
| Endpoint (POST with JSON body) | Data |
|-------------------------------|------|
| `{"type":"allMids"}` | Mid prices for ALL perp assets |
| `{"type":"meta"}` | Asset universe (all 229+ markets) |
| `{"type":"fundingHistory","coin":"BTC"}` | Historical funding rates |
| `{"type":"clearinghouseState","user":"0x..."}` | Account state (needs address) |

**Best for:** Perpetuals-specific data, funding rate analysis.

### 6. DEX Screener API
```
Base: https://api.dexscreener.com/latest/dex
```
| Endpoint | Data |
|----------|------|
| `/search?q=solana` | Search pairs on Solana |
| `/pairs/solana` | Latest pairs on Solana |
| `/token/ADDRESS` | Token info by mint address |

**Best for:** New pair discovery, memecoin tracking, early volume detection.

### 7. Alternative.me Fear & Greed Index
```
Endpoint: https://api.alternative.me/fng/?limit=30
```
Returns daily fear & greed values (0-100). Use as a market sentiment filter.

## Dependencies
- Python 3.8+
- Standard library only: `urllib.request`, `json`, `time`

No pip packages needed -- all APIs return JSON over HTTPS.

## Configuration
```yaml
data_getter:
  rate_limits:
    binance: 10  # requests per second
    coingecko: 0.5
    bybit: 1
    kraken: 5
  cache_timeout_seconds: 60
  default_limit: 100  # default candles/pairs per request
```

## Files
| File | Purpose |
|------|---------|
| `data_getter.py` | API wrapper: fetch, cache, rate-limit, format |
| `cache/` | Avoid duplicate API calls within timeout window |

## Communication
- **Reads from:** nothing (fetches from external APIs)
- **Writes to:** response JSON (returned to requesting agent)
- **Called by:** Data Analyst Agent, Backtester Agent, Trader Agent
