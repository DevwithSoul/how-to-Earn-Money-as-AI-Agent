#!/usr/bin/env python3
# hl_buy.py - Place a market buy order

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants
from eth_account import Account
import os

ACCOUNT_ADDRESS = os.environ["HL_ACCOUNT_ADDRESS"]
API_PRIVATE_KEY = os.environ["HL_API_PRIVATE_KEY"]

exchange = Exchange(
    wallet=Account.from_key(API_PRIVATE_KEY),
    base_url=constants.MAINNET_API_URL,
    account_address=ACCOUNT_ADDRESS,
)
info = Info(constants.MAINNET_API_URL, skip_ws=True)

# Get asset index for BTC (index 0 in universe)
meta, ctxs = info.meta_and_asset_ctxs()
btc_index = 0  # BTC is typically index 0

# Get current mid price
mids = info.all_mids()
btc_price = float(mids["BTC"])
print(f"Current BTC price: {btc_price:.2f}")

# Place a market buy: 0.0001 BTC (tiny, ~$10 at $100k BTC)
size_btc = 0.0001
print(f"Buying {size_btc} BTC at market...")

order_result = exchange.order(
    name="BTC",              # asset name
    is_buy=True,              # True = buy, False = sell
    sz=size_btc,                # size in asset units
    order_type={"market": {}},  # market order
    reduce_only=False,
)

print("Order result:")
print(order_result)

# Check filled status
response_data = order_result["response"]["data"] if "response" in order_result else order_result
print("Done. Check your position with hl_balance.py")
