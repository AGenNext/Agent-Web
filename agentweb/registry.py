"""The Registry agent — the DNS of the agent web.

A typed agent (`type = registry`) built on the autonomyx box. It holds an
**id record** for every agent that registers (**no orphans**), and provides
**register / discover / resolve / list**. Identification is mandatory (record
all); interaction stays trust-scored (recorded, not auto-trusted).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from autonomyx.agent import Agent
from autonomyx.message import Message


@dataclass
class IdRecord:
    """The record created for every identity that registers — never an orphan."""

    did: str
    type: str
    surface: str = ""
    capabilities: list[str] = field(default_factory=list)
    trust_score: float = 0.0


class Registry:
    """Registry logic: id records + register / discover / resolve / list.

    Used as an autonomyx agent handler. Every interaction is capability-gated and
    audited by the kernel; the registry only records and looks up.
    """

    type = "registry"

    def __init__(self) -> None:
        self.records: dict[str, IdRecord] = {}

    def handle(self, agent: Agent, message: Message) -> dict:
        action = message.action
        p = message.payload or {}
        if action == "register":
            rec = IdRecord(
                did=message.sender_fpr,
                type=p.get("type", "service"),
                surface=p.get("surface", ""),
                capabilities=list(p.get("capabilities", [])),
                trust_score=float(p.get("trust_score", 0.0)),
            )
            self.records[rec.did] = rec  # id record — always created (no orphans)
            return {"registered": rec.did, "type": rec.type}
        if action == "resolve":
            rec = self.records.get(p.get("did", ""))
            return {"record": asdict(rec) if rec else None}
        if action == "discover":
            want_type, want_cap = p.get("type"), p.get("capability")
            matches = [
                r.did
                for r in self.records.values()
                if (want_type is None or r.type == want_type)
                and (want_cap is None or want_cap in r.capabilities)
            ]
            return {"matches": matches}
        if action == "list":
            return {"nodes": list(self.records.keys())}
        return {"error": f"unknown action {action!r}"}
