"""Composition layer: signed, expiring flows over the zero-trust kernel.

A **Flow** is a composition of capability-gated **steps** — each step invokes a
sealed agent ("box") through the kernel. A flow is **signed by its author**,
which makes it an *ownable, sellable artifact* (the held contract): provenance,
attribution, and accountability travel with it. A flow also **expires** —
anti-drift by construction: stale authority is refused before it can rot.

Manifesto -> machine:
  box         = an agent: identity + provenance + capability + audit   [kernel.py]
  composition = a Flow of steps over boxes                             [here]
  contract    = the author's signature on the flow                     [here]
  anti-drift  = signature (vs forgery) + expiry (vs trust decay) + audit (record)

A flow is composed *by reference* — it names the boxes it orchestrates and keeps
their identities intact; it never decomposes them. The flow itself is a *new*
signed identity that declares its parts (its steps), exactly the legitimate
"compose, don't forge" rule.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field, replace

from .agent import Agent
from .capability import Capability
from .identity import Identity, PublicIdentity
from .kernel import Kernel
from .message import make_message
from .util import KernelError, canonical_bytes


@dataclass(frozen=True)
class Step:
    """One move in a flow: invoke ``agent_fpr`` with (action, resource, payload)."""

    agent_fpr: str
    action: str
    resource: str
    payload: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "agent": self.agent_fpr,
            "action": self.action,
            "resource": self.resource,
            "payload": self.payload,
        }


@dataclass(frozen=True)
class SignedFlow:
    """An author-signed, expiring composition of steps — the held contract."""

    name: str
    author_fpr: str
    steps: tuple[Step, ...]
    created_at: float
    expires_at: float | None
    signature: bytes

    def signed_payload(self) -> bytes:
        return canonical_bytes(
            {
                "name": self.name,
                "author": self.author_fpr,
                "steps": [s.as_dict() for s in self.steps],
                "created_at": self.created_at,
                "expires_at": self.expires_at,
            }
        )

    def expired(self, now: float | None = None) -> bool:
        if self.expires_at is None:
            return False
        return (now if now is not None else time.time()) > self.expires_at

    def as_dict(self) -> dict:
        """A portable form — this is what you hand over when you *sell* a flow."""
        return {
            "name": self.name,
            "author": self.author_fpr,
            "steps": [s.as_dict() for s in self.steps],
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "signature": self.signature.hex(),
        }


class FlowError(KernelError):
    """A flow failed authenticity, freshness, or execution."""


class FlowExpired(FlowError):
    """The flow's authority has decayed past its expiry (drift)."""


def build_flow(
    author: Identity,
    name: str,
    steps: list[Step],
    ttl_seconds: float | None = None,
) -> SignedFlow:
    """Author composes and **signs** a flow. The signature makes it theirs."""
    created = time.time()
    expires = created + ttl_seconds if ttl_seconds is not None else None
    payload = canonical_bytes(
        {
            "name": name,
            "author": author.fingerprint,
            "steps": [s.as_dict() for s in steps],
            "created_at": created,
            "expires_at": expires,
        }
    )
    signature = author.sign(payload)
    return SignedFlow(name, author.fingerprint, tuple(steps), created, expires, signature)


def verify_flow(
    flow: SignedFlow, author_public: PublicIdentity, now: float | None = None
) -> None:
    """Anti-drift gate: the flow must be **authentic** (signature) AND **fresh** (not expired)."""
    author_public.verify(flow.signature, flow.signed_payload())  # raises VerificationError
    if flow.expired(now):
        raise FlowExpired(f"flow '{flow.name}' has expired")


class FlowRunner:
    """Executes a signed flow step-by-step through the kernel, capability-gated.

    The flow is *authored* by one identity (provenance/ownership) and *executed*
    on behalf of an ``executor`` agent that holds the capabilities for each step.
    Author and executor can differ — that is exactly "build a flow, then sell it
    to someone who runs it."
    """

    def __init__(self, kernel: Kernel):
        self.kernel = kernel

    def _capability_for(
        self, step: Step, capabilities: dict[tuple[str, str], Capability]
    ) -> Capability | None:
        # Exact match, then resource wildcard, then full wildcard.
        return (
            capabilities.get((step.action, step.resource))
            or capabilities.get((step.action, "*"))
            or capabilities.get(("*", "*"))
        )

    def run(
        self,
        flow: SignedFlow,
        author_public: PublicIdentity,
        executor: Agent,
        capabilities: dict[tuple[str, str], Capability],
    ) -> list[dict]:
        # Gate the whole flow once: authentic + not decayed.
        verify_flow(flow, author_public)
        results: list[dict] = []
        for step in flow.steps:
            cap = self._capability_for(step, capabilities)  # None -> kernel default-denies
            msg = make_message(
                executor.identity, step.agent_fpr, step.action, step.resource, step.payload
            )
            results.append(self.kernel.route(msg, cap))
        return results
