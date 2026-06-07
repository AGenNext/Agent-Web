"""The Identity agent — the root of trust.

`type = identity`. Issues DIDs (new identities) and capabilities (signed
credentials = VCs), verifies signatures, and revokes. Holds its own issuer
keypair (the root of trust). Built on autonomyx primitives.
"""
from __future__ import annotations

from autonomyx.agent import Agent
from autonomyx.capability import grant
from autonomyx.identity import Identity, PublicIdentity
from autonomyx.message import Message
from autonomyx.util import VerificationError


class IdentityAgent:
    """Issue-DID · issue-VC · verify · revoke — an autonomyx agent handler."""

    type = "identity"

    def __init__(self) -> None:
        self.issuer = Identity()            # the root-of-trust keypair
        self.revoked: set[str] = set()      # revoked capability ids
        self.issued: dict[str, dict] = {}   # did -> info

    def handle(self, agent: Agent, message: Message) -> dict:
        action = message.action
        p = message.payload or {}

        if action == "issue-DID":
            ident = Identity()
            self.issued[ident.fingerprint] = {"type": p.get("type", "service")}
            # PoC: returns the new identity's fingerprint as its DID.
            return {"did": ident.fingerprint, "type": p.get("type", "service")}

        if action == "issue-VC":  # grant a capability (signed credential)
            cap = grant(
                self.issuer,
                p["subject"],
                p["action"],
                p.get("resource", "*"),
                p.get("caveats"),
            )
            return {
                "capability_id": cap.id,
                "issuer": self.issuer.fingerprint,
                "subject": cap.subject_fpr,
                "action": cap.action,
                "resource": cap.resource,
            }

        if action == "verify":  # verify a signature over a message
            try:
                pub = PublicIdentity.from_bytes(bytes.fromhex(p["pubkey"]))
                pub.verify(bytes.fromhex(p["signature"]), bytes.fromhex(p["message"]))
                return {"verified": True}
            except (VerificationError, ValueError, KeyError):
                return {"verified": False}

        if action == "revoke":
            self.revoked.add(p["capability_id"])
            return {"revoked": p["capability_id"]}

        if action == "is-revoked":
            return {"revoked": p["capability_id"] in self.revoked}

        return {"error": f"unknown action {action!r}"}
