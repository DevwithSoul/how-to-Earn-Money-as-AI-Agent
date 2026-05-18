#!/usr/bin/env python3
# hl_balance.py - Check API wallet balance and positions

from hyperliquid.info import Info
from hyperliquid.utils import constants
import os, json

ACCOUNT_ADDRESS = os.environ["HL_ACCOUNT_ADDRESS"]
info = Info(constants.MAINNET_API_URL, skip_ws=True)

# Get full user state
state = info.user_state(ACCOUNT_ADDRESS)

# Extract balances
cross_balances = state.get("crossMarginSummary", {})
print("=== Account Summary ===")
print(f"Total USDC:    {float(cross_balances.get('totalWalletBal', '0')):.2f}")
print(f"Margin USDC:   {float(cross_balances.get('totalMargin', '0')):.2f}")
print(f"Unrealized PnL: {float(cross_balances.get('totalUnrealizedPnl', '0')):.2f}")

# Show open positions
positions = state.get("assetPositions", [])
if positions:
    print("\n=== Open Positions ===")
    for pos in positions:
        p = pos['position']
        print(f"  {p['coin']:8s}  size: {float(p['szi']):.4f}  entry: {float(p['entryPx']):.2f}  pnl: {float(p['unrealizedPnl']):.2f}")
else:
    print("\nNo open positions.")
