"""autonomyx - a minimal zero-trust kernel for a canonical agent OS.

Native primitives:
  Identity     - an Ed25519 keypair; the origin id (fingerprint) of every entity
  Provenance   - signed certificate chains proving same-origin lineage to the root
  Capability   - unforgeable, scoped, caveated grants (object-capability authz)
  Message      - the only interaction: a signed, addressed envelope
  Agent        - identity + provenance + domain + handler
  Kernel       - the canonical core: genesis root, registration, default-deny routing

Trust derives only from a verifiable lineage back to the canonical root and a
matching capability; never from network location. Every interaction is verified
and audited.
"""
from .agent import Agent
from .capability import Capability, grant
from .identity import Identity, PublicIdentity
from .kernel import AuditRecord, Kernel
from .message import Message, make_message
from .provenance import Certificate, issue_certificate, verify_chain
from .util import AuthorizationError, KernelError, ProvenanceError, VerificationError

__all__ = [
    "Identity",
    "PublicIdentity",
    "Certificate",
    "issue_certificate",
    "verify_chain",
    "Capability",
    "grant",
    "Message",
    "make_message",
    "Agent",
    "Kernel",
    "AuditRecord",
    "KernelError",
    "VerificationError",
    "ProvenanceError",
    "AuthorizationError",
]
