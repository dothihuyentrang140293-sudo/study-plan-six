import json
import base64
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

CURSOR_API = "https://api.cursor.com/v1/chat/completions"

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

            # Cursor uses Basic Auth: API key as username, empty password
            basic_token = base64.b64encode(f"{api_key}:".encode()).decode()

            payload = json.dumps({
                "model":       body.get("model", "claude-3-5-sonnet-20241022"),
                "messages":    body.get("messages", []),
                "max_tokens":  body.get("max_tokens", 2000),
                "temperature": 0.85,
            }).encode()

            req = urllib.request.Request(
                CURSOR_API,
                data=payload,
                headers={
                    "Authorization": f"Basic {basic_token}",
                    "Content-Type":  "application/json",
                },
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=120) as resp:
                result = resp.read()

            self._raw(200, result)

        except urllib.error.HTTPError as e:
            body = e.read()
            try:
                err_obj = json.loads(body)
                msg = err_obj.get("error", {}).get("message") or str(err_obj)
            except Exception:
                msg = body.decode(errors="replace")
            self._json(e.code, {"error": f"Cursor API HTTP {e.code}: {msg}"})
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
        pass
