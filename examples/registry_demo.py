"""Registry agent demo — the DNS of the agent web, on the autonomyx box.

Agents register (an id record per node — no orphans); a seeker lists, discovers
by type and by capability. Every interaction is capability-gated and audited.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autonomyx import Kernel, make_message
from agentweb.registry import Registry


def main():
    core = Kernel()
    reg = Registry()
    registry = core.register_agent("registry", domain="core", handler=reg.handle)
    print(f"registry agent: {registry.fingerprint[:8]}\n")

    nodes = [
        ("vocabulary-agent", "vocabulary", ["validate", "govern", "maintain"]),
        ("identity-agent", "identity", ["issue-DID", "verify"]),
        ("buyer-app", "app", ["quote", "purchase"]),
    ]
    for name, atype, caps in nodes:
        ag = core.register_agent(name, domain="market")
        cap = core.grant_capability(ag, "register", "*")
        msg = make_message(
            ag.identity, registry.fingerprint, "register", "*",
            {"type": atype, "surface": f"mcp://{name}", "capabilities": caps},
        )
        print("register ->", core.route(msg, cap))

    seeker = core.register_agent("seeker", domain="market")
    print()
    for action, payload in [
        ("list", {}),
        ("discover", {"type": "vocabulary"}),
        ("discover", {"capability": "verify"}),
    ]:
        cap = core.grant_capability(seeker, action, "*")
        msg = make_message(seeker.identity, registry.fingerprint, action, "*", payload)
        print(f"{action} {payload} ->", core.route(msg, cap))

    print("\n--- audit (every interaction recorded) ---")
    for r in core.audit_log[-3:]:
        print(f"  {r.decision:5s} {r.action:9s} {r.reason}")


if __name__ == "__main__":
    main()
