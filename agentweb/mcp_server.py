"""A minimal MCP server exposing the registry agent — callable over the protocol.

Implements the MCP tool protocol (JSON-RPC 2.0 over newline-delimited stdio) by
hand — no SDK. Exposes **register / discover / resolve / list** as MCP tools,
backed by the Registry; agents are identified by real **did:key** DIDs.

Any MCP client can drive it: write JSON-RPC requests to stdin, read responses on
stdout. Run: `python -m agentweb.mcp_server`
"""
from __future__ import annotations

import json
import sys
from dataclasses import asdict

from agentweb.registry import IdRecord, Registry

TOOLS = [
    {
        "name": "register",
        "description": "Register an agent (creates an id record — no orphans).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "did": {"type": "string"},
                "type": {"type": "string"},
                "surface": {"type": "string"},
                "capabilities": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["did", "type"],
        },
    },
    {
        "name": "discover",
        "description": "Find agents by type and/or capability.",
        "inputSchema": {
            "type": "object",
            "properties": {"type": {"type": "string"}, "capability": {"type": "string"}},
        },
    },
    {
        "name": "resolve",
        "description": "Resolve a DID to its id record.",
        "inputSchema": {
            "type": "object",
            "properties": {"did": {"type": "string"}},
            "required": ["did"],
        },
    },
    {
        "name": "list",
        "description": "List all registered DIDs.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


class RegistryMCP:
    """The registry, exposed as an MCP server."""

    def __init__(self) -> None:
        self.reg = Registry()

    def call_tool(self, name: str, args: dict) -> dict:
        if name == "register":
            self.reg.records[args["did"]] = IdRecord(
                did=args["did"],
                type=args.get("type", "service"),
                surface=args.get("surface", ""),
                capabilities=list(args.get("capabilities", [])),
            )
            return {"registered": args["did"]}
        if name == "discover":
            wt, wc = args.get("type"), args.get("capability")
            return {"matches": [
                r.did for r in self.reg.records.values()
                if (wt is None or r.type == wt) and (wc is None or wc in r.capabilities)
            ]}
        if name == "resolve":
            r = self.reg.records.get(args.get("did", ""))
            return {"record": asdict(r) if r else None}
        if name == "list":
            return {"nodes": list(self.reg.records.keys())}
        raise ValueError(f"unknown tool {name!r}")

    def handle(self, req: dict) -> dict | None:
        method, rid = req.get("method"), req.get("id")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": rid, "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "agentweb-registry", "version": "0.1.0"},
                "capabilities": {"tools": {}},
            }}
        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
        if method == "tools/call":
            p = req.get("params", {})
            try:
                out = self.call_tool(p.get("name"), p.get("arguments", {}))
                return {"jsonrpc": "2.0", "id": rid,
                        "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}
            except Exception as exc:  # surface tool errors as JSON-RPC errors
                return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32000, "message": str(exc)}}
        if method and method.startswith("notifications/"):
            return None  # notifications get no response
        return {"jsonrpc": "2.0", "id": rid,
                "error": {"code": -32601, "message": f"method not found: {method}"}}

    def serve(self, stdin=sys.stdin, stdout=sys.stdout) -> None:
        for line in stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
            except json.JSONDecodeError:
                continue
            resp = self.handle(req)
            if resp is not None:
                stdout.write(json.dumps(resp) + "\n")
                stdout.flush()


def main() -> None:
    RegistryMCP().serve()


if __name__ == "__main__":
    main()
