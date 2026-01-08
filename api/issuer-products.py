"""
Vercel Serverless Function: Get Issuer Products
Endpoint: GET /api/issuer-products?issuer=community_aid&wallet_address=r...
Returns: List of products if user has trustline
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.xrpl_client import XRPLClient
from config.issuers import VERIFIED_ISSUERS

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            issuer_key = query_params.get('issuer', [None])[0]
            wallet_address = query_params.get('wallet_address', [None])[0]
            
            if not issuer_key:
                self.wfile.write(json.dumps({'error': 'issuer parameter required'}).encode())
                return
            
            if not wallet_address:
                self.wfile.write(json.dumps({'error': 'wallet_address parameter required'}).encode())
                return
            
            # Get issuer config
            issuer = VERIFIED_ISSUERS.get(issuer_key)
            if not issuer:
                self.wfile.write(json.dumps({'error': 'Issuer not found'}).encode())
                return
            
            # Check trustline
            xrpl_client = XRPLClient(testnet=True)
            has_trustline = xrpl_client.has_trustline(
                wallet_address,
                issuer["address"],
                issuer["currency"]
            )
            
            if not has_trustline:
                self.wfile.write(json.dumps({
                    'error': 'Trustline required',
                    'message': f'Please create a trustline to {issuer["name"]} first',
                    'opt_in_url': f'/ui/opt-in.html?issuer={issuer_key}'
                }).encode())
                return
            
            # Return products
            products = issuer.get("products", [])
            response = {
                'issuer': issuer["name"],
                'issuer_address': issuer["address"],
                'has_access': True,
                'products': products,
                'wallet_address': wallet_address
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
