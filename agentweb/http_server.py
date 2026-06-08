"""HTTP surface for the registry agent — Kubernetes-deployable (a real port).

Exposes the registry's MCP tools over HTTP JSON-RPC (POST /) plus a /healthz
probe. Reuses `RegistryMCP`. Standard library only (no deps beyond the box).
Run: `python -m agentweb.http_server`  (PORT env, default 8080)
"""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

from agentweb.mcp_server import RegistryMCP

_mcp = RegistryMCP()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):  # noqa: N802
        if self.path == "/healthz":
            return self._send(200, {"status": "ok"})
        self._send(404, {"error": "not found"})

    def do_POST(self):  # noqa: N802 — JSON-RPC endpoint
        length = int(self.headers.get("Content-Length", 0))
        try:
            req = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return self._send(400, {"error": "bad json"})
        resp = _mcp.handle(req)
        self._send(200, resp if resp is not None else {})

    def log_message(self, *args):  # quiet
        pass


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", "8080"))
    print(f"agentweb registry HTTP on :{port}", flush=True)
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
