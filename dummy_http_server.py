"""
This server is here only to satisfy Render's requirements for free deployment
It is NOT needed for bot to function
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Bot is running!')

def start_http_server(port=8080):
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"HTTP server running on port {port}")
    server.serve_forever()

def run_http_server():
    http_thread = threading.Thread(target=start_http_server)
    http_thread.daemon = True
    http_thread.start()