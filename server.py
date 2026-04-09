from http.server import HTTPServer, SimpleHTTPRequestHandler
import json, urllib.request, urllib.error, os, ssl

# Disable SSL verification for proxied requests (some envs have cert issues)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    from anthropic import Anthropic
    client = Anthropic()
    HAS_ANTHROPIC = True
except:
    HAS_ANTHROPIC = False

def proxy_fetch(url):
    """Fetch external URL server-side to avoid CORS"""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        return resp.read().decode('utf-8')
    except Exception as e:
        return json.dumps({"error": str(e)})

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/yahoo/'):
            # Proxy Yahoo Finance requests
            params = self.path.split('/api/yahoo/')[1]
            url = f'https://query1.finance.yahoo.com/v8/finance/chart/{params}'
            data = proxy_fetch(url)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data.encode())
        elif self.path == '/api/fx':
            data = proxy_fetch('https://api.exchangerate-api.com/v4/latest/USD')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data.encode())
        elif self.path.startswith('/api/news'):
            from_date = self.path.split('from=')[1].split('&')[0] if 'from=' in self.path else '2026-01-01'
            to_date = self.path.split('to=')[1].split('&')[0] if 'to=' in self.path else '2026-04-03'
            url = f'https://finnhub.io/api/v1/company-news?symbol=NVO&from={from_date}&to={to_date}&token=demo'
            data = proxy_fetch(url)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data.encode())
        else:
            if self.path == '/' or self.path == '':
                self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/api/chat':
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            if HAS_ANTHROPIC:
                try:
                    msg = client.messages.create(
                        model="claude_sonnet_4_6",
                        max_tokens=1000,
                        system=body.get('system', ''),
                        messages=body.get('messages', [])
                    )
                    result = json.dumps({"content": [{"text": msg.content[0].text}]})
                except Exception as e:
                    result = json.dumps({"content": [{"text": f"API error: {str(e)}\n\n-- Prism"}]})
            else:
                result = json.dumps({"content": [{"text": "Prism is temporarily unavailable. The Anthropic API is not configured on this server.\n\n-- Prism"}]})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(result.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        if '/api/' in str(args[0]):
            SimpleHTTPRequestHandler.log_message(self, format, *args)

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 5000), Handler)
    print("Prism NVO server running on port 5000")
    server.serve_forever()
