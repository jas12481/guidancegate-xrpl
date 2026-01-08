"""
Vercel Serverless Function: Check Trustline Status

Endpoint: POST /api/check-trustline
Body: {"wallet_address": "r..."}
Returns: {"opted_in": bool, "opted_in_issuers": [...], "allowed_resources": [...]}
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.xrpl_client import XRPLClient
from config.issuers import VERIFIED_ISSUERS


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            user_address = data.get('wallet_address')
            
            if not user_address:
                self.wfile.write(json.dumps({'error': 'wallet_address required'}).encode())
                return
            
            # Initialize XRPL client
            xrpl_client = XRPLClient(testnet=True)
            
            # Check all required issuers
            required_issuers = [
                issuer for issuer in VERIFIED_ISSUERS.values() 
                if issuer.get("is_required", False)
            ]
            
            opted_in_issuers = []
            allowed_resources = []
            
            for issuer in required_issuers:
                has_tl = xrpl_client.has_trustline(
                    user_address,
                    issuer["address"],
                    issuer["currency"]
                )
                
                if has_tl:
                    opted_in_issuers.append(issuer["name"])
                    allowed_resources.extend(issuer.get("resources", []))
            
            opted_in = len(opted_in_issuers) > 0
            
            response = {
                'opted_in': opted_in,
                'opted_in_issuers': opted_in_issuers,
                'allowed_resources': allowed_resources,
                'wallet_address': user_address
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

