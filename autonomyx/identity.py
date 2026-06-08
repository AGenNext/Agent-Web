"""Primitive: Identity.

Every entity in the system — the canonical root, every agent, (and implicitly
every message and capability it signs) — *is* an Ed25519 keypair. The public
key's hex digest is the entity's **fingerprint**: its origin id. There is no
notion of trust without an identity, so identity is native, not optional.
"""
from __future__ import annotations

import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)

from .util import VerificationError


def _fingerprint(public_bytes: bytes) -> str:
    return hashlib.sha256(public_bytes).hexdigest()[:32]


class PublicIdentity:
    """The public half of an identity: a verifying key + fingerprint."""

    def __init__(self, public_key: Ed25519PublicKey):
        self._public_key = public_key
        self.public_bytes = public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
        self.fingerprint = _fingerprint(self.public_bytes)

    @classmethod
    def from_bytes(cls, raw: bytes) -> "PublicIdentity":
        return cls(Ed25519PublicKey.from_public_bytes(raw))

    def verify(self, signature: bytes, message: bytes) -> None:
        """Raise VerificationError unless ``signature`` is valid for ``message``."""
        try:
            self._public_key.verify(signature, message)
        except InvalidSignature as exc:  # pragma: no cover - exercised in tests
            raise VerificationError(
                f"bad signature for identity {self.fingerprint}"
            ) from exc

    def __repr__(self) -> str:
        return f"PublicIdentity({self.fingerprint})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PublicIdentity) and other.public_bytes == self.public_bytes


class Identity:
    """A full keypair able to sign on behalf of its fingerprint."""

    def __init__(self, private_key: Ed25519PrivateKey | None = None):
        self._private_key = private_key or Ed25519PrivateKey.generate()
        self.public = PublicIdentity(self._private_key.public_key())

    @property
    def fingerprint(self) -> str:
        return self.public.fingerprint

    def sign(self, message: bytes) -> bytes:
        return self._private_key.sign(message)

    def __repr__(self) -> str:
        return f"Identity({self.fingerprint})"
