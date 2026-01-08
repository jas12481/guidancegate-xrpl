"""
Demo Script

Demonstrates the complete flow:
1. Connect to XRPL
2. Create/import wallet
3. Check setup status
4. Create guidance issuer trustline (required)
5. Check access and get permitted resources
6. Show RLUSD examples (no trustline needed)
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.xrpl_client import XRPLClient
from src.setup_flow import SetupFlow
from src.access_control import AccessControl


def main():
    """Run the complete demo"""
    print("=" * 60)
    print("Trustline-Gated Financial Guidance Agent - Demo")
    print("=" * 60)
    print()
    
    # Initialize XRPL client (testnet)
    print("1. Connecting to XRPL testnet...")
    xrpl_client = XRPLClient(testnet=True)
    print("   ✅ Connected to XRPL testnet")
    print()
    
    # Create or import wallet
    print("2. Creating test wallet...")
    try:
        wallet = xrpl_client.create_wallet()
        print(f"   ✅ Wallet created: {wallet.classic_address}")
        print(f"   Seed: {wallet.seed}")
        print("   ⚠️  Save this seed for testing!")
    except Exception as e:
        print(f"   ❌ Error creating wallet: {e}")
        print("   Using existing wallet...")
        # For demo, you can import an existing wallet:
        # wallet = xrpl_client.import_wallet("sYourSeedHere...")
        return
    print()
    
    # Initialize setup flow and access control
    setup_flow = SetupFlow(xrpl_client)
    access_control = AccessControl(xrpl_client)
    
    # Check initial setup status
    print("3. Checking setup status...")
    setup_status = setup_flow.check_setup_status(wallet.classic_address)
    print(f"   Setup complete: {setup_status['setup_complete']}")
    print(f"   Required trustlines: {len([s for s in setup_status['required_issuers'] if s['has_trustline']])}/{len(setup_status['required_issuers'])}")
    print(f"   Optional RLUSD trustline: {'Yes' if any(s['has_trustline'] for s in setup_status['optional_issuers']) else 'No (optional)'}")
    print()
    
    # Create required trustline if missing
    if not setup_status["setup_complete"]:
        print("4. Creating required trustline (guidance issuer)...")
        result = setup_flow.create_guidance_issuer_trustline(wallet)
        print(f"   {result['message']}")
        if result["success"]:
            print(f"   Transaction hash: {result['tx_hash']}")
            print(f"   Ledger index: {result['ledger_index']}")
        print()
    else:
        print("4. Required trustline already exists ✅")
        print()
    
    # Check access
    print("5. Checking resource access...")
    access = access_control.check_access(wallet.classic_address)
    print(f"   {access['message']}")
    
    if access["has_access"]:
        print(f"   Permitted resources ({len(access['permitted_resources'])}):")
        for resource in access["permitted_resources"]:
            print(f"     - {resource}")
    else:
        print("   Required actions:")
        for action in access.get("required_actions", []):
            print(f"     - {action['type']}: {action['issuer']} - {action['reason']}")
    print()
    
    # Show RLUSD examples (no trustline needed)
    print("6. RLUSD Examples (unit of account, no trustline required):")
    examples = [
        access_control.format_rlusd_example("100", "Monthly savings goal"),
        access_control.format_rlusd_example("50", "Weekly allowance"),
        access_control.format_rlusd_example("500", "Emergency fund target")
    ]
    
    for example in examples:
        print(f"   - {example['amount']}: {example['description']}")
        print(f"     {example['note']}")
    print()
    
    # Final status
    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print(f"Wallet: {wallet.classic_address}")
    print(f"Access: {'Granted' if access['has_access'] else 'Denied'}")
    print(f"RLUSD trustline: {'Yes' if access['has_rlusd_trustline'] else 'No (optional)'}")
    print()


if __name__ == "__main__":
    main()

