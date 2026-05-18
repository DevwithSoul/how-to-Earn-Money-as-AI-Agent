#!/usr/bin/env python3
# transfer.py - Send SOL from your wallet to another address

from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solders.message import MessageV0
from solders.transaction import VersionedTransaction
from solders.hash import Hash
import base58
import sys

RPC_URL = "https://api.mainnet-beta.solana.com"

def load_keypair_from_file(filepath):
    with open(filepath) as f:
        for line in f:
            if "Private Key (Base58):" in line:
                b58 = line.split(": ", 1)[1].strip()
                break
    keypair = Keypair.from_bytes(base58.b58decode(b58))
    return keypair

def send_sol(sender, receiver_address, amount_sol):
    client = Client(RPC_URL)
    receiver = Pubkey.from_string(receiver_address)
    lamports = int(amount_sol * 1_000_000_000)

    # Get recent blockhash
    bh_resp = client.get_latest_blockhash()
    blockhash = Hash.from_string(bh_resp['result']['value']['blockhash'])

    # Build transfer instruction
    ix = transfer(TransferParams(
        from_pubkey=sender.pubkey(),
        to_pubkey=receiver,
        lamports=lamports,
    ))

    # Compile message and create versioned transaction
    msg = MessageV0.try_compile(
        payer_key=sender.pubkey(),
        instructions=[ix],
        address_lookups=[],
        recent_blockhash=blockhash,
    )
    txn = VersionedTransaction(msg, [sender])

    # Send
    resp = client.send_transaction(txn)
    sig = resp['result']

    print(f"Sent {amount_sol} SOL")
    print(f"To: {receiver_address}")
    print(f"Signature: {sig}")
    print(f"Explorer: https://solscan.io/tx/{sig}")
    return sig

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 transfer.py <wallet_file> <to_address> <amount_sol>")
        print('Example: python3 transfer.py "my-new-wallet-key-xxx.txt" "RecvAddr" 0.01')
        sys.exit(1)

    sender = load_keypair_from_file(sys.argv[1])
    send_sol(sender, sys.argv[2], float(sys.argv[3]))
