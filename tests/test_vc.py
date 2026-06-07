"""Tests for real W3C Verifiable Credentials (VC 2.0)."""
from __future__ import annotations

import time

from autonomyx.identity import Identity
from agentweb.did import did_for
from agentweb.vc import issue_vc, verify_vc


def test_issue_and_verify():
    issuer, subject = Identity(), Identity()
    vc = issue_vc(issuer, did_for(subject), {"capability": "git:push", "resource": "repo:x"})
    assert vc["issuer"] == did_for(issuer)
    assert vc["credentialSubject"]["id"] == did_for(subject)
    assert vc["proof"]["proofValue"]
    assert verify_vc(vc) is True


def test_tampered_subject_rejected():
    issuer, subject = Identity(), Identity()
    vc = issue_vc(issuer, did_for(subject), {"capability": "git:push"})
    vc["credentialSubject"]["capability"] = "security:revoke"  # tamper
    assert verify_vc(vc) is False


def test_forged_issuer_rejected():
    issuer, attacker, subject = Identity(), Identity(), Identity()
    vc = issue_vc(issuer, did_for(subject), {"capability": "git:push"})
    vc["issuer"] = did_for(attacker)  # claim a different issuer
    assert verify_vc(vc) is False


def test_expired_rejected():
    issuer, subject = Identity(), Identity()
    vc = issue_vc(issuer, did_for(subject), {"capability": "git:push"}, ttl_seconds=-1)
    assert verify_vc(vc) is False


def test_valid_within_ttl():
    issuer, subject = Identity(), Identity()
    vc = issue_vc(issuer, did_for(subject), {"capability": "git:push"}, ttl_seconds=3600)
    assert verify_vc(vc, now=time.time() + 10) is True
