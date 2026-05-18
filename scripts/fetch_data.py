#!/usr/bin/env python3
# fetch_data.py - Test all free data sources

import urllib.request, json

def fetch(url, data=None):
    req = urllib.request.Request(url, data=data.encode() if data else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

print("=== Binance ===")
d = fetch("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
print(f"BTC: ${d['price']}")

print("\n=== CoinGecko ===")
d = fetch("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,solana&vs_currencies=usd")
print(f"BTC: ${d['bitcoin']['usd']}, SOL: ${d['solana']['usd']}")

print("\n=== Hyperliquid ===")
d = fetch("https://api.hyperliquid.xyz/info", json.dumps({"type": "allMids"}))
print(f"BTC: ${float(d['BTC']):.2f}, SOL: ${float(d['SOL']):.2f}")

print("\n=== Fear & Greed ===")
d = fetch("https://api.alternative.me/fng/?limit=1")
v = d['data'][0]
print(f"F&G: {v['value']}/100 - {v['value_classification']}")

print("\nAll data sources working.")
