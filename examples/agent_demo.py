"""Agentic-market demo on the zero-trust canonical core.

Illustrates the Stage-3 "Reconstruction" idea from Rothschild et al. (2026):
agent-to-agent coordination where authority is delegated explicitly, every
interaction is verified, and governance is an auditable constraint baked into
the workflow rather than bolted on.

A buyer agent and a seller agent (each with a cryptographic identity and a
certificate proving lineage to the canonical root) negotiate a purchase. The
kernel enforces default-deny: the buyer can only do what its capabilities allow.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autonomyx import AuthorizationError, Kernel, make_message


def seller_handler(agent, message):
    catalog = {"widget": 4.20, "gadget": 9.99}
    if message.action == "quote":
        item = message.payload.get("item")
        return {"item": item, "unit_price": catalog.get(item), "seller": agent.name}
    if message.action == "purchase":
        item = message.payload.get("item")
        qty = message.payload.get("qty", 1)
        return {"order": item, "qty": qty, "total": round(catalog[item] * qty, 2), "status": "confirmed"}
    return {"error": "unknown action"}


def main():
    core = Kernel()
    print(f"canonical root (genesis) fingerprint: {core.root_fingerprint}\n")

    buyer = core.register_agent("buyer-agent", domain="market")
    seller = core.register_agent("seller-agent", domain="market", handler=seller_handler)
    print(f"registered {buyer}\nregistered {seller}\n")

    # The user delegates *scoped* authority to their buyer agent.
    can_quote = core.grant_capability(buyer, action="quote", resource="*")
    can_buy = core.grant_capability(
        buyer, action="purchase", resource="widget", caveats={"max_calls": 1}
    )

    # 1. Buyer agent asks the seller agent for a quote.
    q = make_message(buyer.identity, seller.fingerprint, "quote", "widget", {"item": "widget"})
    print("quote ->", core.route(q, can_quote))

    # 2. Buyer agent purchases (allowed once).
    p = make_message(buyer.identity, seller.fingerprint, "purchase", "widget", {"item": "widget", "qty": 3})
    print("purchase ->", core.route(p, can_buy))

    # 3. A second purchase is denied: the capability's max_calls caveat is spent.
    p2 = make_message(buyer.identity, seller.fingerprint, "purchase", "widget", {"item": "widget", "qty": 1})
    try:
        core.route(p2, can_buy)
    except AuthorizationError as exc:
        print("second purchase -> DENIED:", exc)

    # 4. Buyer tries to buy something its capability never covered -> denied.
    p3 = make_message(buyer.identity, seller.fingerprint, "purchase", "gadget", {"item": "gadget"})
    try:
        core.route(p3, can_buy)
    except AuthorizationError as exc:
        print("out-of-scope purchase -> DENIED:", exc)

    print("\n--- audit log (governance as an auditable constraint) ---")
    for r in core.audit_log:
        print(f"  {r.decision:5s}  {r.action:8s} {r.resource:8s}  {r.reason}")


if __name__ == "__main__":
    main()
