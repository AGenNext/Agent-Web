"""Real W3C Verifiable Credentials (VC 2.0) — issue and verify.

A capability is issued as a **signed VC**: the issuer (a did:key) signs a
credential about a subject. Verification resolves the issuer DID back to its key
and checks the signature over the canonical credential. Simplified VC 2.0 shape,
**real crypto** (Ed25519 over the canonical bytes).
Spec: https://www.w3.org/TR/vc-data-model-2.0/
"""
from __future__ import annotations

import time

from autonomyx.identity import Identity
from autonomyx.util import VerificationError, canonical_bytes
from agentweb.did import did_for, verifier_for

VC_CONTEXT = ["https://www.w3.org/ns/credentials/v2"]


def issue_vc(issuer: Identity, subject_did: str, claim: dict, ttl_seconds: int | None = None) -> dict:
    """Issue a signed Verifiable Credential about `subject_did`."""
    now = time.time()
    cred = {
        "@context": VC_CONTEXT,
        "type": ["VerifiableCredential"],
        "issuer": did_for(issuer),
        "validFrom": now,
        "validUntil": (now + ttl_seconds) if ttl_seconds is not None else None,
        "credentialSubject": {"id": subject_did, **claim},
    }
    signature = issuer.sign(canonical_bytes(cred))
    cred["proof"] = {
        "type": "Ed25519Signature2020",
        "verificationMethod": did_for(issuer),
        "proofValue": signature.hex(),
    }
    return cred


def verify_vc(vc: dict, now: float | None = None) -> bool:
    """Verify a VC: signature valid (issuer DID), and not expired."""
    proof = vc.get("proof")
    issuer_did = vc.get("issuer")
    if not proof or not issuer_did:
        return False
    cred = {k: v for k, v in vc.items() if k != "proof"}
    try:
        verifier_for(issuer_did).verify(bytes.fromhex(proof["proofValue"]), canonical_bytes(cred))
    except (VerificationError, ValueError, KeyError):
        return False
    valid_until = vc.get("validUntil")
    if valid_until is not None and (now if now is not None else time.time()) > valid_until:
        return False
    return True
