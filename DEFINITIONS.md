# Definitions — the Agent Web

A consolidated glossary of every concept defined across the design. Crisp here;
detail in [`AGENT-WEB.md`](AGENT-WEB.md), [`ARCHITECTURE.md`](ARCHITECTURE.md),
[`CAPABILITIES.md`](CAPABILITIES.md).

## Foundations

- **Agent Web** — the **Internet of Agents**: a global network where everything is
  an agent, connected over the open web.
- **Agent** — an entity in the agent web; **a box**. **An agent is an operator** —
  it *operates* a node (device · website · platform), **reconciling it toward its
  objective**. *Source ref:* the **Kubernetes Operator** pattern (a controller that
  reconciles a resource), generalized. This is the most **stable, efficient,
  real-world** definition. Everything is an agent.
- **Box** — the canonical unit: a **sealed, signed, identifiable, callable** unit.
  Sealed substance, generative interface. Real, accountable, portable, sovereign.
- **The web** — the substrate and **home of everything**: information, standards
  (W3C), references (URIs/DIDs), vocabulary (schema.org). The agent web makes it
  **agent-actionable**.
- **Every repo is an agent** — callable via MCP / API.

## The box's primitives

- **Identity** — who an agent is; a W3C **DID** — sovereign, portable, verifiable.
  Accountability pins to **identity, not location**.
- **Provenance** — an agent's **signed history** (its worldline); who/what/when/where.
- **Capability** — an **authorized verb on a resource**; a signed **W3C VC 2.0**.
  Defined by **reference + definition + agent-language**. *Capability authorizes.*
- **Tool** — the **executable means** to perform a capability; an **MCP** function.
  *Tool executes.* (Capability authorizes; tool executes.)
- **Skill** — a **composition** of capabilities/tools into a reusable ability; a
  **signed flow**. **Official** (platform-certified) or **community** (author-signed).
- **Message** — the only interaction: a **signed, addressed, tamper-evident**
  envelope (DIDComm / mTLS), every protocol.
- **Agent-language** — the canonical **vocabulary** of verbs + meaning (schema.org
  + namespaces); the W3C **`@context`** fixes the meaning of terms.

## Ability stack

**language → capability → tool → skill** (dictionary → word → speech → sentence).
A **skill is a flow.** A **flow** is a signed, expiring, capability-gated
composition of tool invocations.

## The trinity & the loop

- **Trinity** — **Intent → Action → Outcome.** Intent is *declared* (the why,
  unprovable); action and outcome are *verified*.
- **Intent** — the desired outcome; the delegated goal/request.
- **Action** — what is done; capabilities exercised via tools.
- **Outcome** — the verified, audited result, checked against intent.
- **Objective** — the desired outcome / desired state the loop reconciles toward.
- **Agent loop = reconciliation loop** — the **deterministic, stable** control
  loop: heartbeat → **move-next over the graph** → **verify** → execute → repeat.
  Converts **unstructured → structured**; reconciles toward the objective. **No
  probabilism in the control plane.**
- **Step** — one move, **one at a time**, each with an objective: **set context →
  align on target env+outcome → act → outcome → verify → advance.**

## Structure & the graph

- **Structure** — organized, canonical, machine-legible form (the goal-state).
- **Unstructured → structured** — the loop's core work; **how the world progresses**.
- **Schema** — the structured shape/types; valid structure.
- **Graph** — the canonical structure: **nodes + edges**; the **conformance reference**.
- **Metrics** — structured, quantified, verified measurements.
- **Node** — an **identity** (a DID) in the graph.
- **Edge** — an **interaction**; trust-scored.
- **Trust score** — **earned** (provenance + reputation + attestations + conformance);
  **gates interaction.** Node creation is **open**; interaction is **trust-scored**.
- **Stability** — **conformance with the (current, growing) graph.** Non-conforming
  = drift.
- **Expansion** — **governed, conformant** growth of the graph = **progress** (vs
  ungoverned drift = decay).
- **No orphans** — everything connected/owned/recorded, or gracefully retired. **An
  orphan is a security risk.**
- **Identification** — **record every identity** (an id record) — necessary for
  governance and security. *Identification ≠ trust: record all, engage the verified.*

## State & the store

- **State** — the **structured current condition** of an agent/system: the nodes,
  edges, properties, and values at a moment. The reconciliation loop moves **state**
  toward the **objective** and holds it in **conformance with the graph**. State
  lives in the **store**; transitions are signed, versioned, audited (the worldline).
- **State store = SurrealDB** — a **multi-model** database that fits the agent web:

  | SurrealDB feature | Fit |
  |---|---|
  | **Multi-model** (graph · document · relational · key-value · time-series) | the **graph** (nodes/edges) + agent **documents** + relations + metrics |
  | **Graph relations** (record links, traversal) | **nodes = identities**, **edges = interactions** |
  | **Real-time live queries** | the **reconciliation loop** reacts to state change; subscribe / notify |
  | **Embedded ↔ server ↔ distributed** (TiKV) | **edge ↔ cloud** — matches k0s ↔ k8s |
  | **Schema-flexible** (schemafull / schemaless) | the **expanding graph** (governed schema growth) |
  | **Record-level auth & permissions** (JWT, scopes) | aligns with **capabilities / zero-trust** (our substrate layers on top) |
  | **SurrealQL · functions · events · indexes** | queries · computed **metrics** · event-driven reconciliation |
  | **HTTP / WebSocket** | **web-native** (the web substrate) |
  | **ACID transactions** | atomic state changes — consistency, **no orphans** |

  SurrealDB is the **state / graph store**: it holds the graph (nodes + edges), the
  agent state (documents), and the metrics — **embedded at the edge, distributed in
  the cloud, real-time, web-native, multi-model.** The trust substrate
  (DID / VC / zero-trust) layers **on top**: *SurrealDB stores; the kernel verifies.*

## Scope & context

- **Domain** — **the scope**: the bounded region (subject · boundary · valid inputs)
  where an agent's capabilities, environment, and authority apply. Crossing
  **re-verifies**.
- **Context** — **everything is contextual**; the `@context` fixes meaning. A domain
  sits within a context.
- **Environment** — where an agent runs (the domain's runtime).

## Agent definition (at creation)

A **signed manifest**: **capability · environment · governance policy · framework**.
*Define → sign → it becomes a box.*

## Governance & trust

- **Zero-trust** — **always verify, default-deny**; trust from provable identity +
  matching capability, **never location**; trust **expires**.
- **Governance** — **open**; the meaning/vocabulary is defined and governed in the
  open by a **vocabulary agent** that **validates · governs · maintains** the catalog.
- **Drift** — **the enemy**: non-conformant change / decay. Everything decays.
- **Anti-drift** — identity · provenance · signatures · **expiry** · reconciliation ·
  graceful retirement. **Trust is a process, not a state.**
- **Graceful retirement** — voluntary, dignified end-of-life; dependents reconciled,
  **never orphaned**.

## Repos, types, contracts

- **Repo types** — platform · vocabulary · identity · registry · service · app · gateway.
- **Contract** — a signed manifest: **type · identity · capabilities (provides/
  requires) · surface (MCP/API) · governance · conformance · provenance**.

## The motherboard (hardware) & the partition

- **Motherboard / core** — the **deterministic, stable loop**; the root of hardware
  (FPGA and/or real-time Ubuntu). The **root of trust is off the surface** (secure
  element / enclave).
- **Sidecar** — a **probabilistic worker** (LLM / GGUF), **gated** by the
  deterministic core. *If it can't be stable core → sidecar.*
- **Native (context-dependent)** — code = hardware-native · core = **k0s** ·
  network = **k8s** · surface = UI-native. **Never generic.**

## Box vs Platform

- **Box** — **open source**; the building blocks; the commons. Community participates here.
- **Platform** — **commercial**; the **arrangement** of boxes into delivered value
  (flows, packaging, **app store**, delivery, support). **The box is never closed
  to monetize.** *(Ubuntu / Canonical model.)*

## Pipeline

**define → design → build → verify → sanitize → document → sign → publish →
register** (never dangling) **→ deploy** (edge ↔ cloud).

## Standards (the commons — all W3C / open)

**DID** · **VC 2.0** · **DIDComm** · **schema.org / `@context`** · **OCI** · **SLSA** ·
**Sigstore** · **SPIFFE** · **MCP** · **k0s / k8s** · **Ubuntu / snaps**.

---

**Agent Web = the Internet of Agents.** Everything is an agent (a box). The web is
the substrate. The trinity (intent → action → outcome) runs in a deterministic
reconciliation loop that converts unstructured → structured (the graph). Nodes are
identities; interaction is trust-scored; the graph expands by governed conformance.
Zero-trust is the law; open governance the keystone; **drift the only enemy.**
