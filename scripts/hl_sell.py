#!/usr/bin/env python3
# hl_sell.py - Place a market sell order

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

# Sell 0.0001 BTC at market
mids = info.all_mids()
btc_price = float(mids["BTC"])
print(f"Current BTC price: {btc_price:.2f}")

order_result = exchange.order(
    name="BTC",
    is_buy=False,             # False = sell
    sz=0.0001,
    order_type={"market": {}},
    reduce_only=False,
)

print("Sell order result:")
print(order_result)
