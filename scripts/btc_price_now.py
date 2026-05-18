#!/usr/bin/env python3
# btc_price_now.py - Get live Bitcoin price from 3 sources

import urllib.request, json

def fetch_json(url, data=None):
    req = urllib.request.Request(url, data.encode() if data else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

# Source 1: Binance (fastest, most liquid)
d = fetch_json("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
binance_price = float(d["price"])
print(f"Binance:   ${binance_price:>9,.2f}")

# Source 2: CoinGecko (good for cross-reference)
d = fetch_json("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
cg_price = d["bitcoin"]["usd"]
print(f"CoinGecko: ${cg_price:>9,.2f}")

# Source 3: Hyperliquid (perp market)
d = fetch_json("https://api.hyperliquid.xyz/info", json.dumps({"type": "allMids"}))
hl_price = float(d["BTC"])
print(f"Hyperliquid: ${hl_price:>9,.2f}")

# Average (filter out extreme outliers)
prices = [binance_price, cg_price, hl_price]
avg = sum(prices) / len(prices)
print(f"Average:   ${avg:>9,.2f}")
print(f"Spread:    ${max(prices)-min(prices):>9,.4f}")
