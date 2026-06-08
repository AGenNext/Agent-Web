"""Zero-trust kernel tests. Run: python -m pytest tests/test_kernel.py -q"""
from __future__ import annotations

import time

import pytest

from autonomyx import (
    AuthorizationError,
    Identity,
    Kernel,
    ProvenanceError,
    VerificationError,
    make_message,
)
from autonomyx.capability import grant
from autonomyx.provenance import issue_certificate, verify_chain


def echo_handler(agent, message):
    return {"echo": message.payload, "by": agent.name}


def build():
    k = Kernel()
    buyer = k.register_agent("buyer", domain="market", handler=echo_handler)
    seller = k.register_agent("seller", domain="market", handler=echo_handler)
    return k, buyer, seller


def test_authorized_message_is_delivered():
    k, buyer, seller = build()
    cap = k.grant_capability(buyer, action="quote", resource="widget")
    msg = make_message(buyer.identity, seller.fingerprint, "quote", "widget", {"qty": 3})
    result = k.route(msg, cap)
    assert result["echo"] == {"qty": 3}
    assert k.audit_log[-1].decision == "allow"


def test_default_deny_without_capability():
    k, buyer, seller = build()
    msg = make_message(buyer.identity, seller.fingerprint, "quote", "widget")
    with pytest.raises(AuthorizationError):
        k.route(msg)  # no capability -> denied
    assert k.audit_log[-1].decision == "deny"


def test_capability_scope_is_enforced():
    k, buyer, seller = build()
    cap = k.grant_capability(buyer, action="quote", resource="widget")
    # Same capability, different action -> denied.
    msg = make_message(buyer.identity, seller.fingerprint, "purchase", "widget")
    with pytest.raises(AuthorizationError):
        k.route(msg, cap)


def test_tampered_message_rejected():
    k, buyer, seller = build()
    cap = k.grant_capability(buyer, action="quote", resource="widget")
    msg = make_message(buyer.identity, seller.fingerprint, "quote", "widget", {"qty": 1})
    # Forge the payload after signing.
    tampered = msg.__class__(**{**msg.__dict__, "payload": {"qty": 999}})
    with pytest.raises(VerificationError):
        k.route(tampered, cap)


def test_forged_identity_has_no_provenance():
    k, buyer, seller = build()
    # An outsider key never registered / certified by the root.
    outsider = Identity()
    cap = k.grant_capability(buyer, action="quote", resource="widget")
    msg = make_message(outsider, seller.fingerprint, "quote", "widget")
    with pytest.raises(ProvenanceError):
        k.route(msg, cap)  # unknown sender / no lineage


def test_forged_capability_rejected():
    k, buyer, seller = build()
    # Attacker mints their own "capability" with a non-root key.
    attacker = Identity()
    forged = grant(attacker, buyer.fingerprint, "quote", "widget")
    msg = make_message(buyer.identity, seller.fingerprint, "quote", "widget")
    with pytest.raises((AuthorizationError, VerificationError)):
        k.route(msg, forged)


def test_caveat_max_calls():
    k, buyer, seller = build()
    cap = k.grant_capability(buyer, "quote", "widget", caveats={"max_calls": 1})
    m1 = make_message(buyer.identity, seller.fingerprint, "quote", "widget")
    k.route(m1, cap)  # first call ok
    m2 = make_message(buyer.identity, seller.fingerprint, "quote", "widget")
    with pytest.raises(AuthorizationError):
        k.route(m2, cap)  # exhausted


def test_caveat_expiry():
    k, buyer, seller = build()
    cap = k.grant_capability(buyer, "quote", "widget", caveats={"expires_at": time.time() - 1})
    msg = make_message(buyer.identity, seller.fingerprint, "quote", "widget")
    with pytest.raises(AuthorizationError):
        k.route(msg, cap)


def test_wildcard_capability():
    k, buyer, seller = build()
    cap = k.grant_capability(buyer, action="*", resource="*")
    for action in ("quote", "purchase", "cancel"):
        msg = make_message(buyer.identity, seller.fingerprint, action, "anything")
        assert k.route(msg, cap)["by"] == "seller"


def test_chain_verifies_to_root():
    k, buyer, _ = build()
    leaf = verify_chain(buyer.chain, k.root_fingerprint)
    assert leaf.fingerprint == buyer.fingerprint


def test_chain_rejects_wrong_root():
    k, buyer, _ = build()
    with pytest.raises(ProvenanceError):
        verify_chain(buyer.chain, "deadbeef" * 4)
