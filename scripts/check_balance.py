#!/usr/bin/env python3
# check_balance.py - Check SOL and SPL token balances

from solana.rpc.api import Client
from solders.pubkey import Pubkey
import sys

# ── Configuration ──────────────────────────────────────────
RPC_URL = "https://api.mainnet-beta.solana.com"
# For testing: "https://api.devnet.solana.com"
# ───────────────────────────────────────────────────────────

KNOW_MINTS = {
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
}

def get_sol_balance(client, address):
    pubkey = Pubkey.from_string(address)
    resp = client.get_balance(pubkey)
    lamports = resp['result']['value']
    sol = lamports / 1_000_000_000
    return sol, lamports

def get_token_balances(client, address):
    pubkey = Pubkey.from_string(address)
    tokens = []
    try:
        resp = client.get_token_accounts_by_owner_json_parsed(pubkey)
        accounts = resp['result']['value']
        for acct in accounts:
            info = acct['account']['data']['parsed']['info']
            mint = info['mint']
            amount = int(info['tokenAmount']['amount'])
            decimals = info['tokenAmount']['decimals']
            balance = amount / (10 ** decimals)
            symbol = next((k for k, v in KNOW_MINTS.items() if v == mint), mint[:8])
            tokens.append({"symbol": symbol, "mint": mint, "balance": balance})
    except Exception as e:
        print(f"Token fetch error (optional): {e}")
    return tokens

def check_wallet(address):
    client = Client(RPC_URL)
    sol, lamports = get_sol_balance(client, address)
    tokens = get_token_balances(client, address)

    print(f"Wallet: {address}")
    print(f"SOL: {sol:.6f} ({lamports} lamports)")
    if tokens:
        for t in tokens:
            print(f"  {t['symbol']:6s}: {t['balance']:.6f}")
    else:
        print("No SPL tokens found.")
    return {"address": address, "sol": sol, "lamports": lamports, "tokens": tokens}

if __name__ == "__main__":
    addr = sys.argv[1] if len(sys.argv) > 1 else "7g3XzqQBqvZiJAvBiR1Xg5wPZK6KtVfQqL9WzQfZb8cF"
    check_wallet(addr)
