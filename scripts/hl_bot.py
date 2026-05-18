#!/usr/bin/env python3
# hl_bot.py - Automated trading bot skeleton (runs 24/7)

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants
from eth_account import Account
import os, time, json
from datetime import datetime

ACCOUNT_ADDRESS = os.environ["HL_ACCOUNT_ADDRESS"]
API_PRIVATE_KEY = os.environ["HL_API_PRIVATE_KEY"]
TRADE_ASSET = os.environ.get("HL_ASSET", "BTC")

exchange = Exchange(
    wallet=Account.from_key(API_PRIVATE_KEY),
    base_url=constants.MAINNET_API_URL,
    account_address=ACCOUNT_ADDRESS,
)
info = Info(constants.MAINNET_API_URL, skip_ws=True)

# Parameters (tune these)
CHECK_INTERVAL = 300          # seconds (5 min)
POSITION_SIZE = 0.0001       # in asset units
MA_SHORT = 20                 # periods
MA_LONG = 100                 # periods
price_history = []

def get_mid_price(asset):
    mids = info.all_mids()
    return float(mids[asset])

def sma(data, period):
    if len(data) < period:
        return None
    return sum(data[-period:]) / period

print(f"Bot started at {datetime.now()}")
print(f"Trading: {TRADE_ASSET}, check every {CHECK_INTERVAL}s")

while True:
    try:
        price = get_mid_price(TRADE_ASSET)
        price_history.append(price)
        timestamp = datetime.now().strftime("%H:%M:%S")

        short_sma = sma(price_history, MA_SHORT)
        long_sma = sma(price_history, MA_LONG)

        if short_sma and long_sma:
            print(f"{timestamp}  price={price:.1f}  sma{MA_SHORT}={short_sma:.1f}  sma{MA_LONG}={long_sma:.1f}")

            # Placeholder: add your buy/sell logic here
            if short_sma > long_sma:
                # Bullish signal -> long
                # exchange.order(TRADE_ASSET, True, POSITION_SIZE, {"market": {}}, False)
                pass
            elif short_sma < long_sma:
                # Bearish signal -> short
                # exchange.order(TRADE_ASSET, False, POSITION_SIZE, {"market": {}}, False)
                pass

        time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nBot stopped by user.")
        break
    except Exception as e:
        print(f"Error: {e}, retrying in 60s...")
        time.sleep(60)
