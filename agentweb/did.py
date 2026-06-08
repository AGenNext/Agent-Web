"""did:key — a real W3C DID derived from an Ed25519 public key.

did:key is a deterministic, self-contained DID method: no registry, no network —
the DID *is* the public key, multicodec + multibase encoded. We derive it from the
autonomyx Ed25519 identity, giving every agent a standards-compliant DID that can
be resolved back to its verifying key.
Spec: https://w3c-ccg.github.io/did-method-key/
"""
from __future__ import annotations

from autonomyx.identity import Identity, PublicIdentity

_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_ED25519_PUB_PREFIX = b"\xed\x01"  # multicodec ed25519-pub (varint)


def _b58encode(data: bytes) -> str:
    n = int.from_bytes(data, "big")
    out = ""
    while n > 0:
        n, r = divmod(n, 58)
        out = _B58[r] + out
    pad = len(data) - len(data.lstrip(b"\x00"))  # leading zero bytes -> '1'
    return "1" * pad + out


def _b58decode(s: str) -> bytes:
    n = 0
    for ch in s:
        n = n * 58 + _B58.index(ch)
    body = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    pad = len(s) - len(s.lstrip("1"))
    return b"\x00" * pad + body


def did_key(public_bytes: bytes) -> str:
    """Encode a 32-byte Ed25519 public key as a `did:key:z...` string."""
    return "did:key:z" + _b58encode(_ED25519_PUB_PREFIX + public_bytes)


def public_from_did(did: str) -> bytes:
    """Recover the raw Ed25519 public key from a `did:key` string."""
    if not did.startswith("did:key:z"):
        raise ValueError("not a base58btc did:key")
    payload = _b58decode(did[len("did:key:z"):])
    if payload[:2] != _ED25519_PUB_PREFIX:
        raise ValueError("not an ed25519 did:key")
    return payload[2:]


def did_for(identity: Identity) -> str:
    """The did:key for an autonomyx Identity."""
    return did_key(identity.public.public_bytes)


def verifier_for(did: str) -> PublicIdentity:
    """Resolve a `did:key` to a PublicIdentity that can verify signatures."""
    return PublicIdentity.from_bytes(public_from_did(did))
