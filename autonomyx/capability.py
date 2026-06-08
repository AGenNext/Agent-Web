"""Primitive: Capability (zero-trust authorization).

A **Capability** is an unforgeable, scoped grant: "issuer authorizes subject to
perform `action` on `resource`, subject to caveats." It is an object-capability
token — holding a valid, signed capability *is* the permission. Default is deny:
without a matching capability, nothing is allowed.

Caveats are additional constraints checked at use time (e.g. an expiry, or a
maximum number of invocations), enabling attenuated delegation.
"""
from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field

from .identity import Identity
from .util import AuthorizationError, canonical_bytes


def _matches(pattern: str, value: str) -> bool:
    """A grant of ``*`` matches anything; otherwise exact match."""
    return pattern == "*" or pattern == value


@dataclass(frozen=True)
class Capability:
    issuer_fpr: str
    subject_fpr: str
    action: str
    resource: str
    caveats: dict
    issued_at: float
    signature: bytes

    @property
    def id(self) -> str:
        return hashlib.sha256(self.signature).hexdigest()[:16]

    def _signed_payload(self) -> bytes:
        return canonical_bytes(
            {
                "issuer": self.issuer_fpr,
                "subject": self.subject_fpr,
                "action": self.action,
                "resource": self.resource,
                "caveats": self.caveats,
                "issued_at": self.issued_at,
            }
        )

    def authorizes(self, subject_fpr: str, action: str, resource: str) -> bool:
        return (
            self.subject_fpr == subject_fpr
            and _matches(self.action, action)
            and _matches(self.resource, resource)
        )


def grant(
    issuer: Identity,
    subject_fpr: str,
    action: str,
    resource: str,
    caveats: dict | None = None,
) -> Capability:
    """Issuer signs a capability for ``subject_fpr``."""
    caveats = caveats or {}
    payload = {
        "issuer": issuer.fingerprint,
        "subject": subject_fpr,
        "action": action,
        "resource": resource,
        "caveats": caveats,
        "issued_at": time.time(),
    }
    signature = issuer.sign(canonical_bytes(payload))
    return Capability(
        issuer_fpr=issuer.fingerprint,
        subject_fpr=subject_fpr,
        action=action,
        resource=resource,
        caveats=caveats,
        issued_at=payload["issued_at"],
        signature=signature,
    )


def check_caveats(cap: Capability, usage_count: int) -> None:
    """Enforce time- and count-based caveats. Raise AuthorizationError on fail."""
    expires_at = cap.caveats.get("expires_at")
    if expires_at is not None and time.time() > expires_at:
        raise AuthorizationError(f"capability {cap.id} expired")
    max_calls = cap.caveats.get("max_calls")
    if max_calls is not None and usage_count >= max_calls:
        raise AuthorizationError(f"capability {cap.id} exhausted ({max_calls} calls)")
