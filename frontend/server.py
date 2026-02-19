#!/usr/bin/env python3
"""
HTTP server that properly serves the frontend with index.html as default.
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = 8080
FRONTEND_DIR = Path(__file__).parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests - serve index.html for root"""
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        return super().do_GET()
    
    def end_headers(self):
        """Add caching headers"""
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        return super().end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{self.client_address[0]}] {format % args}")

def run_server():
    """Start the frontend HTTP server"""
    try:
        os.chdir(FRONTEND_DIR)
        print(f"\n{'='*50}")
        print(f"🌐 Student KPI Frontend Server")
        print(f"{'='*50}")
        print(f"📍 URL: http://localhost:{PORT}")
        print(f"📁 Directory: {FRONTEND_DIR}")
        print(f"✅ Server starting... Press Ctrl+C to stop\n")
        
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == "__main__":
    run_server()
