"""
Setup Issuers Script

Creates test issuer wallets for the demo.
Run this to generate issuer addresses for config/issuers.py
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.xrpl_client import XRPLClient


def setup_issuers():
    """Create issuer wallets and display addresses"""
    print("=" * 60)
    print("Setting Up Test Issuers")
    print("=" * 60)
    print()
    print("This will create testnet wallets for:")
    print("1. Guidance issuer (required)")
    print("2. RLUSD issuer (optional - you can use a known RLUSD issuer)")
    print()
    
    client = XRPLClient(testnet=True)
    
    # Create guidance issuer wallet
    print("Creating guidance issuer wallet...")
    guidance_wallet = client.create_wallet()
    print(f"✅ Guidance Issuer Created:")
    print(f"   Address: {guidance_wallet.classic_address}")
    print(f"   Seed: {guidance_wallet.seed}")
    print()
    
    # For RLUSD, we can either create one or use a known address
    print("For RLUSD issuer, you have two options:")
    print("1. Create a test RLUSD issuer (for demo)")
    print("2. Use a known RLUSD issuer address (if available)")
    print()
    
    create_rlusd = input("Create test RLUSD issuer? (y/n): ").lower().strip()
    
    if create_rlusd == 'y':
        print("Creating RLUSD issuer wallet...")
        rlusd_wallet = client.create_wallet()
        print(f"✅ RLUSD Issuer Created:")
        print(f"   Address: {rlusd_wallet.classic_address}")
        print(f"   Seed: {rlusd_wallet.seed}")
        print()
        
        rlusd_address = rlusd_wallet.classic_address
    else:
        print("Using placeholder for RLUSD issuer.")
        print("You can update this later with a real RLUSD issuer address.")
        rlusd_address = "rRLUSD_ISSUER_ADDRESS"
    
    print()
    print("=" * 60)
    print("Configuration for config/issuers.py")
    print("=" * 60)
    print()
    print("Update your config/issuers.py with these addresses:")
    print()
    print(f'    "community_aid": {{')
    print(f'        "address": "{guidance_wallet.classic_address}",')
    print(f'        ...')
    print(f'    }},')
    print()
    print(f'    "rlusd": {{')
    print(f'        "address": "{rlusd_address}",')
    print(f'        ...')
    print(f'    }}')
    print()
    print("=" * 60)
    print("⚠️  IMPORTANT: Save these seeds securely!")
    print("=" * 60)
    print()
    print("Guidance Issuer Seed:", guidance_wallet.seed)
    if create_rlusd == 'y':
        print("RLUSD Issuer Seed:", rlusd_wallet.seed)
    print()
    
    # Ask if they want to auto-update config
    auto_update = input("Auto-update config/issuers.py? (y/n): ").lower().strip()
    
    if auto_update == 'y':
        update_config_file(guidance_wallet.classic_address, rlusd_address)
        print("✅ Config file updated!")
    else:
        print("Please manually update config/issuers.py with the addresses above.")
    
    print()
    print("✅ Issuer setup complete! You can now run the full demo.")


def update_config_file(guidance_address, rlusd_address):
    """Update config/issuers.py with actual addresses"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'issuers.py')
    
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Replace guidance issuer address
    content = content.replace(
        '"address": "rYOUR_ISSUER_ADDRESS"',
        f'"address": "{guidance_address}"'
    )
    
    # Replace RLUSD issuer address
    content = content.replace(
        '"address": "rRLUSD_ISSUER_ADDRESS"',
        f'"address": "{rlusd_address}"'
    )
    
    with open(config_path, 'w') as f:
        f.write(content)


if __name__ == "__main__":
    setup_issuers()

