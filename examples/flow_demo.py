"""Signed-flow demo: build a flow, sign it, run it through the zero-trust kernel.

The manifesto, as a machine:
  - compose a multi-step flow over sealed agents ("boxes"),
  - SIGN it (the author owns it; it could be used or sold),
  - run it capability-gated with a full audit trail,
  - and watch anti-drift refuse a tampered flow and an expired flow.
"""
from __future__ import annotations

import os
import sys
from dataclasses import replace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autonomyx import Identity, Kernel
from autonomyx.flow import FlowExpired, FlowRunner, Step, build_flow, verify_flow
from autonomyx.util import VerificationError


def seller_handler(agent, message):
    catalog = {"widget": 4.20}
    if message.action == "quote":
        return {"item": message.resource, "unit_price": catalog.get(message.resource)}
    if message.action == "purchase":
        qty = message.payload.get("qty", 1)
        return {
            "order": message.resource,
            "qty": qty,
            "total": round(catalog[message.resource] * qty, 2),
            "status": "confirmed",
        }
    return {"error": "unknown"}


def main():
    core = Kernel()
    buyer = core.register_agent("buyer", domain="market")  # the executor
    seller = core.register_agent("seller", domain="market", handler=seller_handler)  # a box

    # An author composes + SIGNS a procurement flow — the ownable, sellable artifact.
    author = Identity()
    flow = build_flow(
        author,
        "buy-widget",
        [
            Step(seller.fingerprint, "quote", "widget", {}),
            Step(seller.fingerprint, "purchase", "widget", {"qty": 3}),
        ],
        ttl_seconds=3600,
    )
    print(
        f"signed flow '{flow.name}' by author {author.fingerprint[:8]} "
        f"({len(flow.steps)} steps, expires in 1h)"
    )

    # The executor holds the capabilities for each step (default-deny otherwise).
    caps = {
        ("quote", "widget"): core.grant_capability(buyer, "quote", "widget"),
        ("purchase", "widget"): core.grant_capability(buyer, "purchase", "widget"),
    }

    print("\n--- run ---")
    for result in FlowRunner(core).run(flow, author.public, buyer, caps):
        print("  ", result)

    # Anti-drift 1: a tampered flow is refused — the signature no longer matches.
    tampered = replace(flow, steps=(replace(flow.steps[1], payload={"qty": 999}),))
    try:
        verify_flow(tampered, author.public)
    except VerificationError:
        print("\ntampered flow   -> REJECTED (signature mismatch)")

    # Anti-drift 2: an expired flow is refused — its authority has decayed.
    stale = build_flow(author, "stale", [Step(seller.fingerprint, "quote", "widget")], ttl_seconds=-1)
    try:
        verify_flow(stale, author.public)
    except FlowExpired as exc:
        print(f"expired flow    -> REJECTED ({exc})")

    print("\n--- audit log ---")
    for record in core.audit_log:
        print(f"  {record.decision:5s} {record.action:8s} {record.resource:8s}  {record.reason}")


if __name__ == "__main__":
    main()
