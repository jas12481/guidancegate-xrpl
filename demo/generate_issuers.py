"""
Generate Issuers Script (Non-Interactive)

Automatically creates test issuer wallets and updates config/issuers.py
Generates wallets for any issuer with placeholder addresses
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.xrpl_client import XRPLClient
from config.issuers import VERIFIED_ISSUERS


def is_placeholder_address(address):
    """Check if address is a placeholder that needs to be generated"""
    return "xxxxxxxxx" in address.lower() or address.startswith("rYOUR_") or address.startswith("rRLUSD_")


def generate_issuers():
    """Generate issuer wallets and update config"""
    print("=" * 60)
    print("Generating Test Issuers")
    print("=" * 60)
    print()
    
    client = XRPLClient(testnet=True)
    
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'issuers.py')
    
    with open(config_path, 'r') as f:
        content = f.read()
    
    wallets_created = []
    
    # Check each issuer and generate wallet if needed
    for issuer_key, issuer in VERIFIED_ISSUERS.items():
        if is_placeholder_address(issuer["address"]):
            print(f"Creating wallet for {issuer['name']}...")
            wallet = client.create_wallet()
            print(f"✅ {issuer['name']}:")
            print(f"   Address: {wallet.classic_address}")
            print(f"   Seed: {wallet.seed}")
            print()
            
            # Replace placeholder in config
            old_address = issuer["address"]
            content = content.replace(
                f'"address": "{old_address}"',
                f'"address": "{wallet.classic_address}"'
            )
            
            wallets_created.append({
                "name": issuer["name"],
                "address": wallet.classic_address,
                "seed": wallet.seed
            })
        else:
            print(f"Skipping {issuer['name']} - already has address: {issuer['address']}")
    
    if wallets_created:
        # Write updated config
        with open(config_path, 'w') as f:
            f.write(content)
        
        print("=" * 60)
        print("✅ Config file updated automatically!")
        print("=" * 60)
        print()
        print("⚠️  IMPORTANT: Save these seeds if you need to use these wallets again:")
        print()
        for wallet_info in wallets_created:
            print(f"{wallet_info['name']} Seed: {wallet_info['seed']}")
        print()
        print("✅ You can now run the full demo: python demo/demo.py")
    else:
        print("✅ All issuers already have addresses configured!")
        print("   No wallets needed to be generated.")
    
    print()


if __name__ == "__main__":
    generate_issuers()

