"""Primitive: the Canonical Core (zero-trust kernel).

The kernel is the single authoritative root of trust and the minimal runtime
that hosts agents. It owns the **genesis** identity that every lineage proves
back to, registers agents (issuing their certificates), mints capabilities, and
mediates *every* interaction through one path: ``route``.

``route`` is **default-deny** and **always-verify**. On every message it:
  1. verifies the sender's signature (authenticity + integrity),
  2. verifies the sender's certificate chain back to genesis (same-origin
     provenance),
  3. confirms the recipient is a registered agent,
  4. requires a capability that authorizes (action, resource) for the sender,
     and enforces that capability's caveats,
  5. delivers to the recipient and records an auditable log entry.

No step is skippable; there is no implicit trust from being "inside."
"""
from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

from .agent import Agent
from .capability import Capability, check_caveats, grant
from .identity import Identity
from .message import Message
from .provenance import Certificate, issue_certificate, verify_chain
from .util import AuthorizationError, ProvenanceError, VerificationError


@dataclass
class AuditRecord:
    timestamp: float
    sender: str
    recipient: str
    action: str
    resource: str
    decision: str  # "allow" or "deny"
    reason: str
    capability_id: str | None = None


class Kernel:
    def __init__(self, root_domain: str = "core"):
        # The canonical origin: a single genesis key all lineage proves back to.
        self.genesis = Identity()
        self.root_domain = root_domain
        # Self-issued root certificate (issuer == subject == genesis).
        self._root_cert = issue_certificate(self.genesis, self.genesis.public, root_domain)
        self._agents: dict[str, Agent] = {}
        self._capabilities: dict[str, Capability] = {}
        self._usage: dict[str, int] = {}
        self.audit_log: list[AuditRecord] = []

    @property
    def root_fingerprint(self) -> str:
        return self.genesis.fingerprint

    # --- registration & authority -------------------------------------------------

    def register_agent(
        self,
        name: str,
        domain: str,
        handler: Callable[[Agent, Message], dict] | None = None,
    ) -> Agent:
        """Create an agent, issue its certificate from the root, and host it."""
        identity = Identity()
        cert = issue_certificate(self.genesis, identity.public, domain)
        chain = [self._root_cert, cert]
        agent = Agent(name, identity, domain, chain, handler)
        self._agents[agent.fingerprint] = agent
        return agent

    def grant_capability(
        self,
        subject: Agent,
        action: str,
        resource: str,
        caveats: dict | None = None,
    ) -> Capability:
        """Root mints a capability for an agent and registers it for caveat tracking."""
        cap = grant(self.genesis, subject.fingerprint, action, resource, caveats)
        self._capabilities[cap.id] = cap
        self._usage[cap.id] = 0
        return cap

    # --- the one interaction path -------------------------------------------------

    def route(self, message: Message, capability: Capability | None = None) -> dict:
        """Verify and (if authorized) deliver a message. Default-deny."""
        recipient = self._agents.get(message.recipient_fpr)
        sender = self._agents.get(message.sender_fpr)

        # 1. integrity / authenticity
        if sender is None:
            self._record(message, "deny", "unknown sender")
            raise ProvenanceError("unknown sender")
        try:
            sender.identity.public.verify(message.signature, message.signed_payload())
        except VerificationError:
            self._record(message, "deny", "bad message signature")
            raise

        # 2. same-origin provenance back to genesis
        try:
            verify_chain(sender.chain, self.root_fingerprint)
        except ProvenanceError:
            self._record(message, "deny", "provenance failure")
            raise

        # 3. recipient must exist
        if recipient is None:
            self._record(message, "deny", "unknown recipient")
            raise ProvenanceError("unknown recipient")

        # 4. authorization — default deny without a valid capability
        if capability is None:
            self._record(message, "deny", "no capability supplied")
            raise AuthorizationError("default-deny: no capability supplied")
        self._verify_capability(capability, message)

        # 5. deliver + audit
        self._usage[capability.id] = self._usage.get(capability.id, 0) + 1
        result = recipient.handle(message)
        self._record(message, "allow", "authorized", capability.id)
        return result

    def _verify_capability(self, cap: Capability, message: Message) -> None:
        # Capability must be signed by the root (authority) and unmodified.
        try:
            self.genesis.public.verify(cap.signature, cap._signed_payload())
        except VerificationError:
            self._record(message, "deny", "forged capability")
            raise
        if cap.issuer_fpr != self.root_fingerprint:
            self._record(message, "deny", "capability not issued by root")
            raise AuthorizationError("capability issuer is not the canonical root")
        if not cap.authorizes(message.sender_fpr, message.action, message.resource):
            self._record(message, "deny", "capability does not cover action", cap.id)
            raise AuthorizationError(
                f"no capability authorizes {message.action} on {message.resource}"
            )
        try:
            check_caveats(cap, self._usage.get(cap.id, 0))
        except AuthorizationError as exc:
            self._record(message, "deny", str(exc), cap.id)
            raise

    def _record(self, message: Message, decision: str, reason: str, cap_id: str | None = None) -> None:
        self.audit_log.append(
            AuditRecord(
                timestamp=time.time(),
                sender=message.sender_fpr,
                recipient=message.recipient_fpr,
                action=message.action,
                resource=message.resource,
                decision=decision,
                reason=reason,
                capability_id=cap_id,
            )
        )
