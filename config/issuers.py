"""
Issuer Registry Configuration

For MVP we demonstrate with a demo guidance issuer; 
in production this would be a verified organisation or a registry-backed issuer.
"""

VERIFIED_ISSUERS = {
    "rlusd": {
        "name": "RLUSD Stablecoin",
        "address": "rY9n3umFAFsXNUCGLcqc19bH49Cj4oAWy",  # Replace with actual RLUSD issuer address
        "currency": "USD",
        "description": "RLUSD stablecoin for stable reference unit (unit of account, not access control)",
        "resources": [
            "Stable budgeting examples",
            "Allowance tracking in stable value",
            "Savings goal planning",
            "Financial education with stable reference"
        ],
        "is_required": False,  # Optional - enhancement only
        "purpose": "stable_reference"
    },
    "community_aid": {
        "name": "Community Aid Financial Services",
        "address": "rJcM4kRyvK3wQ8ngYZJ62iZBqbPcVGs8gT",  # Replace with your test issuer address
        "currency": "GID",  # Valid 3-character currency code
        "description": "Verified provider of financial guidance and resources",
        "resources": [
            "Financial education resources",
            "Budgeting tools",
            "Savings strategies",
            "Safe financial product information"
        ],
        "is_required": True,  # Required - this gates access
        "purpose": "financial_guidance"
    },
     "inclusive_care": {
        "name": "InclusiveCare Finance Network",
        "address": "r9ZZMzNw4Z9bPhkSZ1DhnF13f8jxeE9JCu",  # Will be replaced by script
        "currency": "ICN",
        "description": "Verified guidance issuer for individuals with intellectual disabilities and caregivers",
        "resources": [
            "SafeSpend Starter Plan",
            "Caregiver-Coach Setup Pack",
            "ScamShield Essentials",
            "Supported Decision-Making Toolkit"
        ],
        "is_required": True,
        "purpose": "financial_guidance"
    },
    "calm_bridge": {
        "name": "CalmBridge Financial Wellbeing",
        "address": "rLZu53zYBYT6fcq38uNcnVYcEeUuBe2Jd4",  # Will be replaced by script
        "currency": "CBW",
        "description": "Verified guidance issuer for financial wellbeing and stress management",
        "resources": [
            "Low-Stress Budgeting Plan",
            "Financial Anxiety Reset",
            "Gentle Debt Support Guide",
            "Comfort-First Savings Goals"
        ],
        "is_required": True,
        "purpose": "financial_guidance"
    }
}

def get_required_issuers():
    """Get list of required issuers (guidance issuer only)"""
    return [issuer for issuer in VERIFIED_ISSUERS.values() if issuer["is_required"]]

def get_optional_issuers():
    """Get list of optional issuers (RLUSD)"""
    return [issuer for issuer in VERIFIED_ISSUERS.values() if not issuer["is_required"]]

def get_issuer_by_key(issuer_key):
    """Get issuer configuration by key"""
    return VERIFIED_ISSUERS.get(issuer_key)

