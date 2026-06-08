"""Signed-flow tests. Run: python -m pytest tests/test_flow.py -q"""
from __future__ import annotations

from dataclasses import replace

import pytest

from autonomyx import AuthorizationError, Identity, Kernel, VerificationError
from autonomyx.flow import FlowExpired, FlowRunner, Step, build_flow, verify_flow


def seller_handler(agent, message):
    return {"action": message.action, "resource": message.resource, "ok": True}


def setup():
    k = Kernel()
    buyer = k.register_agent("buyer", "market")
    seller = k.register_agent("seller", "market", handler=seller_handler)
    author = Identity()
    return k, buyer, seller, author


def test_flow_signs_and_verifies():
    _, _, seller, author = setup()
    flow = build_flow(author, "f", [Step(seller.fingerprint, "quote", "widget")])
    verify_flow(flow, author.public)  # does not raise


def test_forged_author_rejected():
    _, _, seller, author = setup()
    flow = build_flow(author, "f", [Step(seller.fingerprint, "quote", "widget")])
    attacker = Identity()
    with pytest.raises(VerificationError):
        verify_flow(flow, attacker.public)


def test_tampered_flow_rejected():
    _, _, seller, author = setup()
    flow = build_flow(author, "f", [Step(seller.fingerprint, "purchase", "widget", {"qty": 1})])
    tampered = replace(flow, steps=(replace(flow.steps[0], payload={"qty": 999}),))
    with pytest.raises(VerificationError):
        verify_flow(tampered, author.public)


def test_expired_flow_rejected():
    _, _, seller, author = setup()
    flow = build_flow(author, "f", [Step(seller.fingerprint, "quote", "widget")], ttl_seconds=-1)
    with pytest.raises(FlowExpired):
        verify_flow(flow, author.public)


def test_flow_runs_all_steps():
    k, buyer, seller, author = setup()
    flow = build_flow(
        author,
        "f",
        [
            Step(seller.fingerprint, "quote", "widget"),
            Step(seller.fingerprint, "purchase", "widget", {"qty": 2}),
        ],
    )
    caps = {
        ("quote", "widget"): k.grant_capability(buyer, "quote", "widget"),
        ("purchase", "widget"): k.grant_capability(buyer, "purchase", "widget"),
    }
    results = FlowRunner(k).run(flow, author.public, buyer, caps)
    assert len(results) == 2
    assert all(r["ok"] for r in results)


def test_step_without_capability_denied():
    k, buyer, seller, author = setup()
    flow = build_flow(author, "f", [Step(seller.fingerprint, "purchase", "widget")])
    caps = {("quote", "widget"): k.grant_capability(buyer, "quote", "widget")}
    with pytest.raises(AuthorizationError):
        FlowRunner(k).run(flow, author.public, buyer, caps)


def test_wildcard_capability_runs_flow():
    k, buyer, seller, author = setup()
    flow = build_flow(
        author,
        "f",
        [Step(seller.fingerprint, a, "widget") for a in ("quote", "purchase", "cancel")],
    )
    caps = {("*", "*"): k.grant_capability(buyer, "*", "*")}
    results = FlowRunner(k).run(flow, author.public, buyer, caps)
    assert len(results) == 3


def test_signed_flow_is_portable():
    _, _, seller, author = setup()
    flow = build_flow(author, "f", [Step(seller.fingerprint, "quote", "widget")])
    d = flow.as_dict()
    assert d["author"] == author.fingerprint
    assert d["signature"]  # hex signature present -> hand it over to use or sell
