import json
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

CURSOR_API = "https://api2.cursor.sh/v1/chat/completions"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        for k, v in CORS_HEADERS.items():
            self.send_header(k, v)
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))

            api_key = body.get("apiKey", "")
            if not api_key:
                self._json(400, {"error": "apiKey is required"})
                return

            payload = json.dumps({
                "model":           body.get("model", "claude-sonnet-4-5"),
                "messages":        body.get("messages", []),
                "max_tokens":      body.get("max_tokens", 2000),
                "temperature":     0.85,
                "response_format": {"type": "json_object"},
            }).encode()

            req = urllib.request.Request(
                CURSOR_API,
                data=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type":  "application/json",
                },
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=120) as resp:
                result = resp.read()

            self._raw(200, result)

        except urllib.error.HTTPError as e:
            self._raw(e.code, e.read())
        except Exception as e:
            self._json(500, {"error": str(e)})

    def _raw(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        for k, v in CORS_HEADERS.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def _json(self, status, obj):
        self._raw(status, json.dumps(obj).encode())

    def log_message(self, *args):
        pass  # suppress default access log
