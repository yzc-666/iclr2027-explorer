"""Local receiver for scripts/browser_fetch.js.

OpenReview's API puts a browser challenge in front of anonymous scripted
requests, so the data is fetched from inside a browser tab on openreview.net
and POSTed here in batches.

    python3 scripts/receive.py            # listens on 127.0.0.1:8765
"""

import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        name = self.path.lstrip("/").split("?")[0]
        if not re.fullmatch(r"[A-Za-z0-9_\-]+", name):
            self.send_response(400)
            self._cors()
            self.end_headers()
            return
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        notes = json.loads(body)
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        (RAW_DIR / f"{name}.json").write_bytes(body)
        print(f"saved {name}.json ({len(notes)} notes, {len(body) / 1e6:.1f} MB)", flush=True)
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"listening on http://127.0.0.1:{PORT}, writing to {RAW_DIR}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
