# TODO — the Agent Web

The durable task list. **Done = the definition + a runnable PoC. Pending = the
product.** Checked items are built and on PR #1.

## ✅ Phase 0 — Definition & proof (done)

- [x] Full definition — `AGENT-WEB.md` · `ARCHITECTURE.md` · `DEFINITIONS.md` ·
      `CONTRACTS.md` · `REPOS.md` · `CORE.md` · `CAPABILITIES.md`
- [x] Language-agnostic contracts — `proto/agentweb.proto`
- [x] Runnable PoC — `autonomyx` (kernel + signed flows), 24 tests green
- [x] First agent — the **registry** (DNS): register/discover/resolve, no orphans
- [x] Open-source foundation — LICENSE · CONTRIBUTING · GOVERNANCE · CODE_OF_CONDUCT

## Phase 1 — Codegen & real standards

- [x] **protoc codegen** — one proto → **Python + Go** generated (`make gen`); Rust/TS configured
- [ ] Real **W3C DID** (replace bespoke fingerprints with DIDs)
- [ ] Real **W3C VC 2.0** for capabilities
- [ ] **MCP** servers — expose agents as callable MCP tools
- [ ] **DIDComm** (or mTLS) for the message layer

## Phase 2 — Build the agents (typed)

- [ ] **identity** — root of trust: issue-DID · issue-VC · verify · revoke
- [ ] **vocabulary** — validate · govern · maintain the catalog (self-governance)
- [ ] **service** — capability provider
- [ ] **app** — end-user experience
- [ ] **gateway** — surface / touchpoints
- [ ] **platform** — host & arrange agents

## Phase 3 — State, graph & trust

- [ ] **SurrealDB** — the state / graph store (nodes + edges + schema)
- [ ] **Graph conformance** — verify; reconcile non-conforming (anti-drift)
- [ ] **Trust score** — provenance + reputation + attestations + conformance
- [ ] **Reconciliation loop** over the graph (unstructured → structured)

## Phase 4 — Flows, skills & surfaces

- [ ] **NL flow builder** — natural language → declarative signed flow
- [ ] **Skill catalog** — official (certified) vs community
- [ ] **Surfaces** — surface-native heads (web · mobile · desktop · voice)

## Phase 5 — Productionize (polyglot)

- [ ] **Rust** core / kernel (deterministic loop, hardware-native)
- [ ] **Go** runtime (container, k8s-native)
- [ ] **JS/TS** surface
- [ ] Harden: signatures, conformance tests, audit, SBOM/Sigstore/SLSA

## Phase 6 — Deploy & platform

- [ ] **k0s** (edge) / **k8s** (network) deployment
- [ ] Single-artifact delivery (snap / k0s-style box)
- [ ] **App store** + packaging (all formats)
- [ ] Hardware path: FPGA core + secure-element root of trust (later)

## Housekeeping

- [x] **Top-level README** — Agent Web front door + index of all docs
- [ ] **`GRAPH.md`** — the concrete current graph schema
- [ ] Index all docs from the README

---

*Definition complete; proof runs; product mostly unbuilt. This list is the gap.*
