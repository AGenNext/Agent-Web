"""Shared helpers: canonical serialization and errors.

Every signature in the kernel is computed over a *canonical* byte encoding so
that two parties always sign/verify the exact same bytes. We use compact JSON
with sorted keys.
"""
from __future__ import annotations

import json
from typing import Any


def canonical_bytes(obj: Any) -> bytes:
    """Deterministic JSON encoding used as the signed/verified payload."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


class KernelError(Exception):
    """Base class for all zero-trust kernel failures."""


class VerificationError(KernelError):
    """A signature or message-integrity check failed."""


class ProvenanceError(KernelError):
    """An identity could not prove lineage back to the canonical root."""


class AuthorizationError(KernelError):
    """Default-deny: no capability authorized the requested action."""
