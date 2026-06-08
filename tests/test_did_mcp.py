"""Tests for real did:key DIDs and the registry MCP server."""
from __future__ import annotations

import json

from autonomyx.identity import Identity
from agentweb.did import did_for, public_from_did, verifier_for
from agentweb.mcp_server import RegistryMCP


# ---- did:key (real W3C DID) -----------------------------------------------

def test_did_key_format_and_roundtrip():
    ident = Identity()
    did = did_for(ident)
    assert did.startswith("did:key:z6Mk")  # canonical Ed25519 did:key prefix
    assert public_from_did(did) == ident.public.public_bytes


def test_did_resolves_and_verifies_signature():
    ident = Identity()
    did = did_for(ident)
    msg = b"agent web is real"
    verifier_for(did).verify(ident.sign(msg), msg)  # raises if invalid


def test_did_rejects_tampered():
    import pytest
    from autonomyx.util import VerificationError
    ident = Identity()
    did = did_for(ident)
    sig = ident.sign(b"original")
    with pytest.raises(VerificationError):
        verifier_for(did).verify(sig, b"tampered")


# ---- MCP server ------------------------------------------------------------

def _call(s, rid, method, params=None):
    return s.handle({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}})


def test_mcp_initialize():
    r = _call(RegistryMCP(), 1, "initialize")
    assert r["result"]["serverInfo"]["name"] == "agentweb-registry"


def test_mcp_tools_list():
    r = _call(RegistryMCP(), 2, "tools/list")
    names = {t["name"] for t in r["result"]["tools"]}
    assert {"register", "discover", "resolve", "list"} <= names


def test_mcp_register_discover_resolve():
    s = RegistryMCP()
    did = did_for(Identity())
    reg = _call(s, 3, "tools/call",
                {"name": "register", "arguments": {"did": did, "type": "identity", "capabilities": ["verify"]}})
    assert json.loads(reg["result"]["content"][0]["text"])["registered"] == did
    disc = _call(s, 4, "tools/call", {"name": "discover", "arguments": {"capability": "verify"}})
    assert did in json.loads(disc["result"]["content"][0]["text"])["matches"]
    res = _call(s, 5, "tools/call", {"name": "resolve", "arguments": {"did": did}})
    assert json.loads(res["result"]["content"][0]["text"])["record"]["type"] == "identity"


def test_mcp_unknown_method():
    assert "error" in _call(RegistryMCP(), 6, "bogus/method")
