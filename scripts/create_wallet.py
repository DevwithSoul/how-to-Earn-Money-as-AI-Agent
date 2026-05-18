#!/usr/bin/env python3
# create_wallet.py - Generate a Solana wallet and save to disk

from solders.keypair import Keypair
import base58
import os

def create_and_save_wallet(output_prefix="my-new-wallet"):
    """Generate a new Solana keypair and save the private key + address."""

    # 1. Generate a new random keypair (Ed25519)
    keypair = Keypair()

    # 2. Public address (base58-encoded)
    public_key = str(keypair.pubkey())

    # 3. Private key as bytes, then base58-encode it
    private_key_bytes = bytes(keypair.secret())
    private_key_b58 = base58.b58encode(private_key_bytes).decode()

    # 4. Save to file: my-new-wallet-key-<ADDRESS>.txt
    filename = f"{output_prefix}-key-{public_key}.txt"

    with open(filename, "w") as f:
        f.write(f"Public Address: {public_key}\n")
        f.write(f"Private Key (Base58): {private_key_b58}\n")
        f.write(f"Private Key (Hex): {private_key_bytes.hex()}\n")

    print(f"Public Address: {public_key}")
    print(f"Saved to: {filename}")

    return {
        "public_key": public_key,
        "private_key_b58": private_key_b58,
        "filename": filename
    }

if __name__ == "__main__":
    result = create_and_save_wallet()
    print("\nIMPORTANT: Keep your private key secret. Never share it.")
