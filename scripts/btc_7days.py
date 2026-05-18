#!/usr/bin/env python3
# btc_7days.py - Get 7 days of BTC price history + plot summary

import urllib.request, json
from datetime import datetime, timedelta

# Binance klines: [open, high, low, close, volume, ...]
# interval: 1h = 168 candles for 7 days, 1d = 7 candles
url = ("https://api.binance.com/api/v3/klines?"
       "symbol=BTCUSDT&interval=1h&limit=168")

with urllib.request.urlopen(url, timeout=10) as r:
    candles = json.loads(r.read())

print(f"Got {len(candles)} hourly candles (7 days)")
print(f"From: {datetime.fromtimestamp(candles[0][0]/1000)}")
print(f"To:   {datetime.fromtimestamp(candles[-1][0]/1000)}")
print()

# Parse all candles
opens, highs, lows, closes, volumes = [], [], [], [], []
for c in candles:
    opens.append(float(c[1]))
    highs.append(float(c[2]))
    lows.append(float(c[3]))
    closes.append(float(c[4]))
    volumes.append(float(c[5]))

print("=== 7-Day Summary ===")
print(f"Open (7d ago): ${opens[0]:>9,.2f}")
print(f"Close (now):   ${closes[-1]:>9,.2f}")
print(f"7d Change:     {((closes[-1]/opens[0])-1)*100:+.2f}%")
print(f"Highest:       ${max(highs):>9,.2f}")
print(f"Lowest:        ${min(lows):>9,.2f}")
print(f"Avg Volume/h:  {sum(volumes)/len(volumes):>12,.1f}")
print(f"Total Volume:  {sum(volumes):>12,.1f}")

# Print last 5 candles for a snapshot
print("\n=== Last 5 Hours ===")
print(f"{'Time':20s} {'Open':>10s} {'High':>10s} {'Low':>10s} {'Close':>10s} {'Vol':>10s}")
for c in candles[-5:]:
    t = datetime.fromtimestamp(c[0]/1000).strftime("%Y-%m-%d %H:%M")
    print(f"{t:20s} {float(c[1]):>10.2f} {float(c[2]):>10.2f} {float(c[3]):>10.2f} {float(c[4]):>10.2f} {float(c[5]):>10.0f}")
