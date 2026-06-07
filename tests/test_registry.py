"""Registry agent tests. Run: python -m pytest tests/test_registry.py -q"""
from __future__ import annotations

import pytest

from autonomyx import AuthorizationError, Kernel, make_message
from agentweb.registry import Registry


def setup():
    k = Kernel()
    reg = Registry()
    registry = k.register_agent("registry", "core", handler=reg.handle)
    return k, reg, registry


def _register(k, registry, name, atype, caps):
    ag = k.register_agent(name, "market")
    cap = k.grant_capability(ag, "register", "*")
    msg = make_message(
        ag.identity, registry.fingerprint, "register", "*",
        {"type": atype, "capabilities": caps, "surface": f"mcp://{name}"},
    )
    return ag, k.route(msg, cap)


def test_register_creates_id_record():
    k, reg, registry = setup()
    ag, res = _register(k, registry, "v", "vocabulary", ["validate"])
    assert res["registered"] == ag.fingerprint
    assert ag.fingerprint in reg.records  # id record created — no orphans


def test_discover_by_capability():
    k, reg, registry = setup()
    _register(k, registry, "v", "vocabulary", ["validate", "govern"])
    _register(k, registry, "s", "service", ["quote"])
    seeker = k.register_agent("seeker", "market")
    cap = k.grant_capability(seeker, "discover", "*")
    msg = make_message(seeker.identity, registry.fingerprint, "discover", "*", {"capability": "validate"})
    assert len(k.route(msg, cap)["matches"]) == 1


def test_discover_by_type():
    k, reg, registry = setup()
    _register(k, registry, "v", "vocabulary", ["validate"])
    _register(k, registry, "i", "identity", ["verify"])
    seeker = k.register_agent("seeker", "market")
    cap = k.grant_capability(seeker, "discover", "*")
    msg = make_message(seeker.identity, registry.fingerprint, "discover", "*", {"type": "identity"})
    assert len(k.route(msg, cap)["matches"]) == 1


def test_resolve():
    k, reg, registry = setup()
    ag, _ = _register(k, registry, "id", "identity", ["verify"])
    seeker = k.register_agent("seeker", "market")
    cap = k.grant_capability(seeker, "resolve", "*")
    msg = make_message(seeker.identity, registry.fingerprint, "resolve", "*", {"did": ag.fingerprint})
    assert k.route(msg, cap)["record"]["type"] == "identity"


def test_register_requires_capability():
    k, reg, registry = setup()
    ag = k.register_agent("x", "market")
    msg = make_message(ag.identity, registry.fingerprint, "register", "*", {"type": "app"})
    with pytest.raises(AuthorizationError):
        k.route(msg, None)  # default-deny: no capability
