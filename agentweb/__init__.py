"""agentweb — typed agents built on the autonomyx box.

The first instantiation of the Agent Web definition: typed agents (registry,
identity, vocabulary, ...) running on the zero-trust kernel. Each is an operator
of its node; each is callable, capability-gated, audited.
"""
from .registry import IdRecord, Registry

__all__ = ["Registry", "IdRecord"]
