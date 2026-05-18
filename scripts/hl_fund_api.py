#!/usr/bin/env python3
# hl_fund_api.py - Transfer USDC from main to API wallet

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants
from eth_account import Account
import os, json

ACCOUNT_ADDRESS = os.environ["HL_ACCOUNT_ADDRESS"]
API_PRIVATE_KEY = os.environ["HL_API_PRIVATE_KEY"]

# Create exchange instance (authenticated)
exchange = Exchange(
    wallet=Account.from_key(API_PRIVATE_KEY),  # API wallet key signs trades
    base_url=constants.MAINNET_API_URL,
    account_address=ACCOUNT_ADDRESS,           # Main account address
)

# Check balances
info = Info(constants.MAINNET_API_URL, skip_ws=True)
user_state = info.user_state(ACCOUNT_ADDRESS)

# Show spot/USDC balances
if "assetPositions" in user_state:
    print("Current positions and balances:")
    print(json.dumps(user_state, indent=2)[:500])

print("\nTo transfer USDC to the API wallet:")
print("  Use Hyperliquid UI: Portfolio -> Transfer -> API Wallet")
print("  Or call exchange.usdClassTransfer(amount_usd, is_deposit=False)")
