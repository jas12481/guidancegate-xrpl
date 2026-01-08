"""
Vercel Serverless Function: Get Issuer Information

Endpoint: GET /api/issuer-info/{issuer_key}
Returns: {"name": "...", "address": "...", "currency": "...", "description": "..."}
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import urlparse, parse_qs

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.issuers import get_issuer_by_key


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            # Extract issuer key from path
            # Path format: /api/issuer-info/community_aid
            path = self.path
            path_parts = [p for p in path.split('/') if p]
            
            # Find issuer-info in path and get next part
            issuer_key = None
            if 'issuer-info' in path_parts:
                idx = path_parts.index('issuer-info')
                if idx + 1 < len(path_parts):
                    issuer_key = path_parts[idx + 1]
            
            # Also check query params as fallback
            if not issuer_key:
                parsed = urlparse(self.path)
                query_params = parse_qs(parsed.query)
                issuer_key = query_params.get('issuer', [None])[0]
            
            if not issuer_key:
                self.wfile.write(json.dumps({'error': 'Issuer key required in path or query'}).encode())
                return
            
            issuer = get_issuer_by_key(issuer_key)
            
            if not issuer:
                self.wfile.write(json.dumps({'error': f'Issuer "{issuer_key}" not found'}).encode())
                return
            
            response = {
                'name': issuer['name'],
                'address': issuer['address'],
                'currency': issuer['currency'],
                'description': issuer['description']
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())

