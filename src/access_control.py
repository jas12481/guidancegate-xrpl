"""
Access Control

Gates resources based on trustlines. Only guidance issuer trustline is required.
RLUSD trustline is optional and doesn't gate access.
"""
from src.xrpl_client import XRPLClient
from config.issuers import VERIFIED_ISSUERS, get_required_issuers


class AccessControl:
    """Manages resource access based on trustlines"""
    
    def __init__(self, xrpl_client):
        """
        Initialize access control
        
        Args:
            xrpl_client: XRPLClient instance
        """
        self.client = xrpl_client
    
    def check_access(self, user_address):
        """
        Check if user has access to resources
        
        Access is granted if user has trustline to guidance issuer.
        RLUSD trustline is optional and doesn't affect access.
        
        Args:
            user_address: User's XRPL address
            
        Returns:
            Dictionary with access status and permitted resources
        """
        trustlines = self.client.get_user_trustlines(user_address)
        
        # Check required issuers (guidance issuer only)
        required_issuers = get_required_issuers()
        has_access = False
        permitted_resources = []
        
        for issuer in required_issuers:
            has_tl = self.client.has_trustline(
                user_address,
                issuer["address"],
                issuer["currency"]
            )
            
            if has_tl:
                has_access = True
                permitted_resources.extend(issuer["resources"])
        
        # Check RLUSD trustline (optional, informational only)
        rlusd_issuer = VERIFIED_ISSUERS.get("rlusd")
        has_rlusd = False
        if rlusd_issuer:
            has_rlusd = self.client.has_trustline(
                user_address,
                rlusd_issuer["address"],
                rlusd_issuer["currency"]
            )
        
        if has_access:
            return {
                "has_access": True,
                "permitted_resources": permitted_resources,
                "has_rlusd_trustline": has_rlusd,
                "message": f"✅ Access granted! You have access to {len(permitted_resources)} resource categories."
            }
        else:
            missing = [issuer["name"] for issuer in required_issuers]
            return {
                "has_access": False,
                "permitted_resources": [],
                "has_rlusd_trustline": has_rlusd,
                "message": f"❌ Access denied. Please create trustline to: {', '.join(missing)}",
                "required_actions": [
                    {
                        "type": "create_trustline",
                        "issuer": issuer["name"],
                        "reason": f"Required to access {issuer['description']}"
                    }
                    for issuer in required_issuers
                ]
            }
    
    def format_rlusd_example(self, amount, description):
        """
        Format financial example using RLUSD as unit of account
        
        RLUSD is used as reference unit regardless of trustline status.
        
        Args:
            amount: Amount in RLUSD
            description: Description of the example
            
        Returns:
            Formatted example dictionary
        """
        return {
            "amount": f"{amount} RLUSD",
            "description": description,
            "note": "Amounts shown in RLUSD (1 RLUSD = 1 USD) for stable reference. RLUSD trustline not required."
        }

