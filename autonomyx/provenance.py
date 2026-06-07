"""Primitive: Provenance (same-origin lineage).

A **Certificate** is a signed statement: "issuer attests that this subject key
belongs to this domain." A **chain** of certificates proves that a subject
descends from the canonical root — this is the "same-origin" test. Trust comes
*only* from a verifiable chain back to the genesis fingerprint; network location
is irrelevant.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

from .identity import Identity, PublicIdentity
from .util import ProvenanceError, VerificationError, canonical_bytes


@dataclass(frozen=True)
class Certificate:
    issuer_fpr: str
    subject_fpr: str
    subject_pubkey: bytes  # raw Ed25519 public bytes of the subject
    domain: str
    issued_at: float
    signature: bytes

    def _signed_payload(self) -> bytes:
        return canonical_bytes(
            {
                "issuer": self.issuer_fpr,
                "subject": self.subject_fpr,
                "subject_pubkey": self.subject_pubkey.hex(),
                "domain": self.domain,
                "issued_at": self.issued_at,
            }
        )


def issue_certificate(
    issuer: Identity, subject: PublicIdentity, domain: str
) -> Certificate:
    """Issuer signs a certificate binding ``subject`` to ``domain``."""
    payload = {
        "issuer": issuer.fingerprint,
        "subject": subject.fingerprint,
        "subject_pubkey": subject.public_bytes.hex(),
        "domain": domain,
        "issued_at": time.time(),
    }
    signature = issuer.sign(canonical_bytes(payload))
    return Certificate(
        issuer_fpr=issuer.fingerprint,
        subject_fpr=subject.fingerprint,
        subject_pubkey=subject.public_bytes,
        domain=domain,
        issued_at=payload["issued_at"],
        signature=signature,
    )


def verify_chain(chain: list[Certificate], root_fpr: str) -> PublicIdentity:
    """Verify a certificate chain and return the leaf's public identity.

    The chain is ordered root-first. Each certificate must be signed by the
    *previous* certificate's subject (the root cert is self-issued by the
    genesis key). Raises ProvenanceError if the lineage does not reach
    ``root_fpr``.
    """
    if not chain:
        raise ProvenanceError("empty certificate chain")
    if chain[0].issuer_fpr != root_fpr:
        raise ProvenanceError("chain does not originate at the canonical root")

    issuer_pub = PublicIdentity.from_bytes(chain[0].subject_pubkey)
    # The root certificate is self-signed: issuer key == subject key.
    if chain[0].issuer_fpr != chain[0].subject_fpr:
        raise ProvenanceError("root certificate must be self-issued")

    for cert in chain:
        try:
            issuer_pub.verify(cert.signature, cert._signed_payload())
        except VerificationError as exc:
            raise ProvenanceError(
                f"broken link at subject {cert.subject_fpr}"
            ) from exc
        if issuer_pub.fingerprint != cert.issuer_fpr:
            raise ProvenanceError("issuer fingerprint mismatch in chain")
        # Next link must be signed by this cert's subject.
        issuer_pub = PublicIdentity.from_bytes(cert.subject_pubkey)

    return issuer_pub  # leaf identity
