"""agentweb — typed agents built on the autonomyx box.

The first instantiation of the Agent Web definition: typed agents running on the
zero-trust kernel, with real W3C DIDs (did:key) and a callable MCP surface.
"""
from .did import did_for, did_key, public_from_did, verifier_for
from .identity import IdentityAgent
from .mcp_server import RegistryMCP
from .registry import IdRecord, Registry

__all__ = [
    "Registry",
    "IdRecord",
    "IdentityAgent",
    "RegistryMCP",
    "did_key",
    "did_for",
    "public_from_did",
    "verifier_for",
]
