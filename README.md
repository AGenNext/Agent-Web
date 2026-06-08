# Agent Web

**The Internet of Agents** — a world where the internet is a **mesh** and **each
node is operated by an agent**. Devices, websites, and platforms re-formed as
**agents**: sealed, signed, callable, capability-bearing boxes, connected
**zero-trust** over the open web.

> **Status:** the **definition is complete** and a **runnable proof-of-concept**
> proves the core model. The polyglot product is mostly unbuilt — see
> [`TODO.md`](TODO.md).

## The idea in one breath

**Agent = operator** (the Kubernetes Operator pattern, generalized): each agent
operates its node via a **deterministic reconciliation loop** that turns
**intent → action → outcome**, converting **unstructured → structured** (the
**graph**), reconciling toward an **objective**, in conformance with the graph.
Every interaction is **signed, capability-gated, trust-scored, audited.** Nodes are
identities (open to create); interaction is earned (trust-scored). **No orphans.
Drift is the only enemy.**

## Start here

| Doc | What |
|---|---|
| [`AGENT-WEB.md`](AGENT-WEB.md) | the theory — Internet of Agents, trinity, loop, graph, trust, governance |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | the locked design — base, native-per-context, agent loop, steps, stack |
| [`DEFINITIONS.md`](DEFINITIONS.md) | every **term** |
| [`CONTRACTS.md`](CONTRACTS.md) | every entity's **contract** (field schema) |
| [`CORE.md`](CORE.md) | graph · contract · loop · building block · kernel · runtime · framework (term · contract · source) |
| [`REPOS.md`](REPOS.md) | the 7 repo/agent types (term + contract) |
| [`CAPABILITIES.md`](CAPABILITIES.md) | the capability catalog (every action is a capability) |
| [`proto/agentweb.proto`](proto/agentweb.proto) | the **language-agnostic** contracts (generate Rust/Go/TS/Python) |
| [`TODO.md`](TODO.md) | the task list — built vs pending |

## Proof of concept (runnable)

- **`autonomyx/`** — the zero-trust **box/kernel**: identity · provenance ·
  capability · message · audit, default-deny, plus signed **flows**.
- **`agentweb/registry.py`** — the first typed agent: the **registry** (DNS).

```bash
pip install cryptography pytest
python -m pytest tests/ -q            # kernel + flows + registry (green)
python examples/agent_demo.py         # agent-to-agent + audit trail
python examples/registry_demo.py      # the registry (DNS)
```

Python is the **prototype that validates the design**; the **canonical contracts
are language-agnostic proto.**

## Codegen (one source → every language)

```bash
make gen     # proto/agentweb.proto -> Python + Go  (Rust/TS configured)
```

## Box vs Platform

- **Box = open** — the building blocks (agents, catalog, standards). The commons.
- **Platform = commercial** — the arrangement of boxes into delivered value. **The
  box is never closed to monetize.** *(The Ubuntu / Canonical model.)*

## Open by design

Open governance, open standards — W3C **DID** · **VC 2.0** · **schema.org** · **MCP**
· **OCI** · **k0s/k8s** · **SurrealDB** · **Ubuntu** — aiming for **CNCF Sandbox**.
See [`CONTRIBUTING.md`](CONTRIBUTING.md) · [`GOVERNANCE.md`](GOVERNANCE.md) ·
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) · [`LICENSE`](LICENSE).

## Also in this repo

- **`orb_mini/`** — an early, **unrelated** reference implementation of the *Orb
  neural network potential* (this session's first tangent). Not part of the Agent
  Web; kept as-is. See [`orb_mini/README.md`](orb_mini/README.md) if curious.
