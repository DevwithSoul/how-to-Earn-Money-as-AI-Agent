#!/usr/bin/env python3
# hl_connect.py - Test Hyperliquid API connection

from hyperliquid.info import Info
from hyperliquid.utils import constants
import os

# Configuration - use environment variables for security
ACCOUNT_ADDRESS = os.environ.get("HL_ACCOUNT_ADDRESS")
API_PRIVATE_KEY = os.environ.get("HL_API_PRIVATE_KEY")

if not ACCOUNT_ADDRESS:
    print("Error: Set HL_ACCOUNT_ADDRESS environment variable")
    print("Example: export HL_ACCOUNT_ADDRESS='0xYourMainWalletAddress'")
    raise SystemExit(1)

# Connect to mainnet (use constants.TESTNET_API_URL for testing)
info = Info(constants.MAINNET_API_URL, skip_ws=True)

# Query user state (public data - no auth needed)
user_state = info.user_state(ACCOUNT_ADDRESS)
print("Connection successful!")
print(f"Account: {ACCOUNT_ADDRESS}")

# Show perpetuals meta data
meta, ctxs = info.meta_and_asset_ctxs()
print(f"Available perpetuals: {len(meta['universe'])}")

# Show first 5 assets
for i, asset in enumerate(meta['universe'][:5]):
    ctx = ctxs[i]
    print(f"  {asset['name']:10s}  mark: {ctx['markPx']:12s}  funding: {ctx['funding']}")
