"""
Quick Test Script

Tests XRPL connection and checks trustlines for existing issuer addresses.
Run this first to verify your setup works.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.xrpl_client import XRPLClient
from config.issuers import VERIFIED_ISSUERS


def quick_test():
    """Test XRPL connection and check trustlines for issuer addresses"""
    print("=" * 60)
    print("Quick XRPL Connection Test")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Connection
        print("1. Testing XRPL connection...")
        client = XRPLClient(testnet=True)
        print("   ✅ Connected to XRPL testnet")
        print()
        
        # Test 2: Read issuer addresses from config
        print("2. Reading issuer addresses from config...")
        print(f"   Found {len(VERIFIED_ISSUERS)} issuers in configuration")
        print()
        
        # Test 3: Check trustlines for each issuer
        print("3. Checking trustlines for each issuer address...")
        print()
        
        total_trustlines = 0
        issuer_results = []
        
        for issuer_key, issuer in VERIFIED_ISSUERS.items():
            address = issuer["address"]
            name = issuer["name"]
            currency = issuer["currency"]
            is_required = issuer.get("is_required", False)
            
            print(f"   Checking: {name}")
            print(f"   Address: {address}")
            print(f"   Currency: {currency} ({'Required' if is_required else 'Optional'})")
            
            try:
                trustlines = client.get_user_trustlines(address)
                trustline_count = len(trustlines)
                total_trustlines += trustline_count
                
                if trustline_count > 0:
                    print(f"   ✅ Found {trustline_count} trustline(s):")
                    for tl in trustlines[:5]:  # Show first 5 trustlines
                        tl_currency = tl.get("currency", "N/A")
                        tl_limit = tl.get("limit", "N/A")
                        tl_counterparty = tl.get("account", "N/A")
                        print(f"      - {tl_currency} from {tl_counterparty[:20]}... (limit: {tl_limit})")
                    if trustline_count > 5:
                        print(f"      ... and {trustline_count - 5} more")
                else:
                    print(f"   ℹ️  No trustlines found (this is normal for new issuers)")
                
                issuer_results.append({
                    "name": name,
                    "address": address,
                    "trustline_count": trustline_count,
                    "status": "success"
                })
                
            except Exception as e:
                print(f"   ❌ Error checking trustlines: {e}")
                issuer_results.append({
                    "name": name,
                    "address": address,
                    "trustline_count": 0,
                    "status": "error",
                    "error": str(e)
                })
            
            print()
        
        # Summary
        print("=" * 60)
        print("Test Summary")
        print("=" * 60)
        print(f"Total issuers checked: {len(VERIFIED_ISSUERS)}")
        print(f"Total trustlines found: {total_trustlines}")
        print()
        
        successful_checks = sum(1 for r in issuer_results if r["status"] == "success")
        print(f"✅ Successfully checked: {successful_checks}/{len(issuer_results)} issuers")
        
        if total_trustlines > 0:
            print(f"✅ Found trustlines across {sum(1 for r in issuer_results if r['trustline_count'] > 0)} issuer(s)")
        
        print()
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        print()
        print("Next step: Run 'python demo/demo.py'")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ Test failed!")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("Troubleshooting:")
        print("1. Check internet connection")
        print("2. Verify XRPL testnet is accessible")
        print("3. Check if issuer addresses in config/issuers.py are valid")
        return False
    
    return True


if __name__ == "__main__":
    quick_test()

