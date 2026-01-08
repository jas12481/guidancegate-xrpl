"""
XRPL Client Wrapper

Handles XRPL connection, trustline queries, and trustline creation.
Based on patterns from: https://github.com/RippleDevRel/xrpl-js-python-simple-scripts
"""
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountLines
from xrpl.models.transactions import TrustSet
from xrpl.transaction import submit_and_wait
from xrpl.wallet import Wallet, generate_faucet_wallet


def text_to_hex(text):
    """
    Convert text to hex with proper padding for XRPL currency codes
    
    Args:
        text: Currency code text (max 20 characters)
        
    Returns:
        Hex string padded to 40 characters
        
    Raises:
        ValueError: If text is longer than 20 characters
    """
    if len(text) > 20:
        raise ValueError("Text must be 20 characters or less")
    # Convert to hex and remove '0x' prefix
    hex_text = text.encode('ascii').hex().upper()
    # Pad with zeros to make it exactly 40 characters
    return hex_text.ljust(40, '0')


def format_currency_code(currency):
    """
    Format currency code for XRPL
    
    Args:
        currency: Currency code string (e.g., "USD", "GID", "RLUSD")
        
    Returns:
        Formatted currency code (3-char codes as-is, longer codes as hex)
    """
    # 3-character currency codes can be used directly
    if len(currency) == 3:
        return currency
    # Longer codes need hex conversion
    else:
        return text_to_hex(currency)


class XRPLClient:
    """Wrapper for XRPL operations"""
    
    def __init__(self, testnet=True):
        """
        Initialize XRPL client
        
        Args:
            testnet: If True, use testnet; otherwise use mainnet
        """
        if testnet:
            self.client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
        else:
            self.client = JsonRpcClient("https://xrplcluster.com")
        self.testnet = testnet
    
    def get_user_trustlines(self, user_address):
        """
        Query all trustlines for a user account
        
        Args:
            user_address: XRPL address to query
            
        Returns:
            List of trustline objects
        """
        request = AccountLines(
            account=user_address,
            ledger_index="validated"
        )
        response = self.client.request(request)
        return response.result.get("lines", [])
    
    def has_trustline(self, user_address, issuer_address, currency):
        """
        Check if user has specific trustline
        
        Args:
            user_address: User's XRPL address
            issuer_address: Issuer's XRPL address
            currency: Currency code (e.g., "USD", "GID", "RLUSD")
            
        Returns:
            True if trustline exists, False otherwise
        """
        # Format currency to match how it's stored on ledger
        currency_formatted = format_currency_code(currency)
        
        trustlines = self.get_user_trustlines(user_address)
        return any(
            line["account"] == issuer_address and 
            line["currency"] == currency_formatted
            for line in trustlines
        )
    
    def create_trustline(self, wallet, issuer_address, currency, limit="1000000000"):
        """
        Create a trustline (TrustSet transaction)
        
        Follows the pattern from:
        https://github.com/RippleDevRel/xrpl-js-python-simple-scripts
        
        Args:
            wallet: XRPL wallet object
            issuer_address: Issuer's XRPL address
            currency: Currency code (e.g., "USD", "GID", "RLUSD")
            limit: Maximum amount to trust (default: 1000000000)
            
        Returns:
            Transaction result object
        """
        # Format currency code (3-char codes as-is, longer codes as hex)
        currency_formatted = format_currency_code(currency)
        
        # Prepare trust set transaction with dictionary for limit_amount
        # Pattern matches official scripts
        trust_set_tx = TrustSet(
            account=wallet.classic_address,
            limit_amount={
                "currency": currency_formatted,
                "issuer": issuer_address,
                "value": str(limit)
            }
        )
        
        # Submit and wait for validation (synchronous)
        # Pattern: submit_and_wait(transaction, client, wallet)
        response = submit_and_wait(trust_set_tx, self.client, wallet)
        
        return response
    
    def create_wallet(self):
        """Generate a new testnet wallet from faucet"""
        if not self.testnet:
            raise ValueError("Can only generate wallet on testnet")
        return generate_faucet_wallet(self.client)
    
    def import_wallet(self, seed):
        """Import wallet from seed"""
        return Wallet.from_seed(seed)

