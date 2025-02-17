"""
This server is here only to satisfy Render's requirements for free deployment
It is NOT needed for bot to function
"""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

def start_http_server(port):
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"HTTP server running on port {port}")
    server.serve_forever()

def run_http_server():
    port = int(os.getenv('PORT', 8080))
    http_thread = threading.Thread(target=start_http_server, args=(port,))
    http_thread.daemon = True
    http_thread.start()