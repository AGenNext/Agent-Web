"""An Agent = Identity + provenance chain + a domain + a handler.

The agent is deliberately thin: the canonical agent is *domain-agnostic*. A
concrete agent is this shell plus (a) the domain it is bound to via its
certificate and (b) a handler implementing what it does. Everything else
(authority, trust) lives in the kernel and the primitives.
"""
from __future__ import annotations

from collections.abc import Callable

from .identity import Identity
from .message import Message
from .provenance import Certificate


class Agent:
    def __init__(
        self,
        name: str,
        identity: Identity,
        domain: str,
        chain: list[Certificate],
        handler: Callable[["Agent", Message], dict] | None = None,
    ):
        self.name = name
        self.identity = identity
        self.domain = domain
        self.chain = chain
        self.handler = handler or (lambda agent, msg: {"ok": True})

    @property
    def fingerprint(self) -> str:
        return self.identity.fingerprint

    def handle(self, message: Message) -> dict:
        """Process a delivered (already kernel-verified) message."""
        return self.handler(self, message)

    def __repr__(self) -> str:
        return f"Agent({self.name}@{self.domain}:{self.fingerprint[:8]})"
