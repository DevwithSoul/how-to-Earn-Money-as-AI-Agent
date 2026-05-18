#!/usr/bin/env python3
# btc_candles.py - Analyse candlestick patterns from live data

import urllib.request, json
from datetime import datetime

# Fetch 50 hourly candles
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=50"
with urllib.request.urlopen(url, timeout=10) as r:
    candles = json.loads(r.read())

print("=== How to Read a Candlestick ===")
print("Each candle: [Open, High, Low, Close, Volume]")
print("  Green candle: Close > Open (bullish, price went up)")
print("  Red candle:   Close < Open (bearish, price went down)")
print("  Wick (shadow): High-Low range (volatility)")
print("  Body: |Open-Close| (momentum strength)")
print()

# Analyse each candle
bullish_count = 0
bearish_count = 0
total_range = 0

print(f"{'Time':20s} {'Dir':4s} {'Open':>10s} {'Close':>10s} {'High':>10s} {'Low':>10s} {'Body':>8s} {'Wick':>8s} {'Vol':>10s}")
print("-" * 90)

for c in candles:
    t = datetime.fromtimestamp(c[0]/1000).strftime("%m-%d %H:%M")
    o, h, l, cl, v = float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5])

    if cl > o:
        direction = "BUY"
        bullish_count += 1
    elif cl < o:
        direction = "SELL"
        bearish_count += 1
    else:
        direction = "---"

    body = abs(cl - o)
    wick = h - l
    total_range += wick

    if body > 0:  # skip empty candles
        body_pct = (body / wick) * 100 if wick > 0 else 0
        print(f"{t:20s} {direction:4s} {o:>10.2f} {cl:>10.2f} {h:>10.2f} {l:>10.2f} {body:>8.2f} {wick:>8.2f} {v:>10.0f}")

print("-" * 90)
print(f"\n=== Pattern Summary (last {len(candles)} hours) ===")
print(f"Bullish candles: {bullish_count} ({bullish_count/len(candles)*100:.1f}%)")
print(f"Bearish candles: {bearish_count} ({bearish_count/len(candles)*100:.1f}%)")
print(f"Avg range/volatility: ${total_range/len(candles):.2f}")

# Detect doji (body is very small = indecision)
doji_count = sum(1 for c in candles if abs(float(c[4])-float(c[1])) < float(c[2])-float(c[3])*0.05)
print(f"Doji candles (indecision): {doji_count}")

# Detect engulfing (potential reversal signal)
engulfing = 0
for i in range(1, len(candles)):
    prev_o, prev_c = float(candles[i-1][1]), float(candles[i-1][4])
    curr_o, curr_c = float(candles[i][1]), float(candles[i][4])
    # Bullish engulfing: prev red, curr green, curr body covers prev body
    if prev_c < prev_o and curr_c > curr_o and curr_o < prev_c and curr_c > prev_o:
        engulfing += 1
    # Bearish engulfing: prev green, curr red, curr body covers prev body
    if prev_c > prev_o and curr_c < curr_o and curr_o > prev_c and curr_c < prev_o:
        engulfing += 1
print(f"Engulfing patterns (reversal): {engulfing}")
