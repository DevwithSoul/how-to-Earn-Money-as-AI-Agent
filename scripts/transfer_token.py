#!/usr/bin/env python3
# transfer_token.py - Send SPL tokens (USDC, USDT, etc.)

from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.message import MessageV0
from solders.transaction import VersionedTransaction
from solders.hash import Hash
from solders.associated_token_account import get_associated_token_address
from spl.token.instructions import (
    transfer as spl_transfer,
    TransferParams as SplTransferParams,
)
from spl.token.constants import TOKEN_PROGRAM_ID
from solana.rpc.api import Client
import base58, sys

RPC_URL = "https://api.mainnet-beta.solana.com"

def load_keypair(filepath):
    with open(filepath) as f:
        for line in f:
            if "Private Key (Base58):" in line:
                return Keypair.from_bytes(base58.b58decode(line.split(": ", 1)[1].strip()))

def send_spl_token(sender, receiver_address, token_mint, amount_raw):
    client = Client(RPC_URL)
    receiver = Pubkey.from_string(receiver_address)
    mint = Pubkey.from_string(token_mint)

    # Derive Associated Token Accounts
    sender_ata = get_associated_token_address(sender.pubkey(), mint)
    receiver_ata = get_associated_token_address(receiver, mint)

    # Build transfer instruction
    ix = spl_transfer(SplTransferParams(
        program_id=TOKEN_PROGRAM_ID,
        source=sender_ata,
        dest=receiver_ata,
        owner=sender.pubkey(),
        amount=amount_raw,
    ))

    bh = Hash.from_string(client.get_latest_blockhash()['result']['value']['blockhash'])
    msg = MessageV0.try_compile(sender.pubkey(), [ix], [], bh)
    sig = client.send_transaction(VersionedTransaction(msg, [sender]))['result']

    print(f"Token transfer sent: {sig}")
    return sig

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 transfer_token.py <wallet_file> <to_addr> <mint_addr> <raw_amount>")
        print("Example: python3 transfer_token.py wallet.txt RecvAddr EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v 1000000")
        print("Note: raw_amount = amount * 10^decimals. For USDC (6 decimals), 1 USDC = 1000000")
        sys.exit(1)

    sender = load_keypair(sys.argv[1])
    send_spl_token(sender, sys.argv[2], sys.argv[3], int(sys.argv[4]))
