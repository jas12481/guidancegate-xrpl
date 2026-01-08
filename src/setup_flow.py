"""
Setup Flow

Handles user setup: checking trustline status and creating required trustlines.
Only guidance issuer trustline is required; RLUSD is optional.
"""
from src.xrpl_client import XRPLClient
from config.issuers import VERIFIED_ISSUERS, get_required_issuers, get_optional_issuers


class SetupFlow:
    """Manages user setup flow"""
    
    def __init__(self, xrpl_client):
        """
        Initialize setup flow
        
        Args:
            xrpl_client: XRPLClient instance
        """
        self.client = xrpl_client
    
    def check_setup_status(self, user_address):
        """
        Check if user has completed setup
        
        Only guidance issuer trustline is required.
        RLUSD trustline is optional (informational only).
        
        Args:
            user_address: User's XRPL address
            
        Returns:
            Dictionary with setup status
        """
        trustlines = self.client.get_user_trustlines(user_address)
        
        # Check required issuers (guidance issuer only)
        required_issuers = get_required_issuers()
        required_status = []
        
        for issuer in required_issuers:
            has_tl = self.client.has_trustline(
                user_address,
                issuer["address"],
                issuer["currency"]
            )
            required_status.append({
                "issuer": issuer,
                "has_trustline": has_tl
            })
        
        # Check optional issuers (RLUSD)
        optional_issuers = get_optional_issuers()
        optional_status = []
        
        for issuer in optional_issuers:
            has_tl = self.client.has_trustline(
                user_address,
                issuer["address"],
                issuer["currency"]
            )
            optional_status.append({
                "issuer": issuer,
                "has_trustline": has_tl
            })
        
        # Setup is complete if all required trustlines exist
        has_all_required = all(status["has_trustline"] for status in required_status)
        
        return {
            "has_all_required": has_all_required,
            "required_issuers": required_status,
            "optional_issuers": optional_status,
            "setup_complete": has_all_required,
            "missing_required": [
                status["issuer"]["name"] 
                for status in required_status 
                if not status["has_trustline"]
            ]
        }
    
    def create_guidance_issuer_trustline(self, wallet):
        """
        Create trustline to guidance issuer (required)
        
        Args:
            wallet: User's wallet
            
        Returns:
            Dictionary with result
        """
        guidance_issuer = VERIFIED_ISSUERS["community_aid"]
        
        result = self.client.create_trustline(
            wallet,
            guidance_issuer["address"],
            guidance_issuer["currency"]
        )
        
        if result.is_successful():
            return {
                "success": True,
                "issuer": guidance_issuer["name"],
                "tx_hash": result.result.get("hash"),
                "ledger_index": result.result.get("ledger_index"),
                "message": f"✅ Trustline created for {guidance_issuer['name']}"
            }
        else:
            return {
                "success": False,
                "error": result.result,
                "message": "❌ Trustline creation failed"
            }
    
    def create_rlusd_trustline(self, wallet):
        """
        Create RLUSD trustline (optional enhancement)
        
        Args:
            wallet: User's wallet
            
        Returns:
            Dictionary with result
        """
        rlusd_issuer = VERIFIED_ISSUERS["rlusd"]
        
        result = self.client.create_trustline(
            wallet,
            rlusd_issuer["address"],
            rlusd_issuer["currency"]
        )
        
        if result.is_successful():
            return {
                "success": True,
                "issuer": rlusd_issuer["name"],
                "tx_hash": result.result.get("hash"),
                "ledger_index": result.result.get("ledger_index"),
                "message": f"✅ RLUSD trustline created (optional enhancement)"
            }
        else:
            return {
                "success": False,
                "error": result.result,
                "message": "❌ RLUSD trustline creation failed"
            }
    
    def complete_setup(self, wallet):
        """
        Complete user setup: create required trustlines
        
        Only creates guidance issuer trustline (required).
        RLUSD trustline is optional and not created here.
        
        Args:
            wallet: User's wallet
            
        Returns:
            Dictionary with setup results
        """
        setup_status = self.check_setup_status(wallet.classic_address)
        
        results = []
        
        # Create required trustlines (guidance issuer only)
        for status in setup_status["required_issuers"]:
            if not status["has_trustline"]:
                issuer = status["issuer"]
                print(f"Creating trustline for {issuer['name']}...")
                result = self.client.create_trustline(
                    wallet,
                    issuer["address"],
                    issuer["currency"]
                )
                
                if result.is_successful():
                    results.append({
                        "success": True,
                        "issuer": issuer["name"],
                        "tx_hash": result.result.get("hash")
                    })
                else:
                    results.append({
                        "success": False,
                        "issuer": issuer["name"],
                        "error": result.result
                    })
        
        # Check if RLUSD trustline exists (informational)
        rlusd_status = setup_status["optional_issuers"][0] if setup_status["optional_issuers"] else None
        has_rlusd = rlusd_status["has_trustline"] if rlusd_status else False
        
        return {
            "setup_complete": all(r["success"] for r in results),
            "trustlines_created": results,
            "has_rlusd_trustline": has_rlusd,
            "message": "Setup complete! Guidance issuer trustline created." if results else "Setup already complete."
        }

