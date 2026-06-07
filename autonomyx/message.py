"""Primitive: Message.

The **only** way entities interact is by sending a signed, addressed Message.
There is no shared memory across trust boundaries — every interaction is an
explicit, verifiable envelope (sender, recipient, action, resource, payload),
signed by the sender so it is authentic and tamper-evident.
"""
from __future__ import annotations

import secrets
import time
from dataclasses import dataclass

from .identity import Identity
from .util import canonical_bytes


@dataclass(frozen=True)
class Message:
    sender_fpr: str
    recipient_fpr: str
    action: str
    resource: str
    payload: dict
    nonce: str
    timestamp: float
    signature: bytes

    def signed_payload(self) -> bytes:
        return canonical_bytes(
            {
                "sender": self.sender_fpr,
                "recipient": self.recipient_fpr,
                "action": self.action,
                "resource": self.resource,
                "payload": self.payload,
                "nonce": self.nonce,
                "timestamp": self.timestamp,
            }
        )


def make_message(
    sender: Identity,
    recipient_fpr: str,
    action: str,
    resource: str,
    payload: dict | None = None,
) -> Message:
    payload = payload or {}
    body = {
        "sender": sender.fingerprint,
        "recipient": recipient_fpr,
        "action": action,
        "resource": resource,
        "payload": payload,
        "nonce": secrets.token_hex(8),
        "timestamp": time.time(),
    }
    signature = sender.sign(canonical_bytes(body))
    return Message(
        sender_fpr=sender.fingerprint,
        recipient_fpr=recipient_fpr,
        action=action,
        resource=resource,
        payload=payload,
        nonce=body["nonce"],
        timestamp=body["timestamp"],
        signature=signature,
    )
