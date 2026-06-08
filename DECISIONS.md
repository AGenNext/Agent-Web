# Decisions — the discussion, recorded

The reasoning behind the design (distilled from the working discussion). The other
docs state *what*; this states *why*. Each is a decision + its rationale.

## 1. Agent Web = the Internet of Agents
The internet becomes a **mesh**; each node is **operated by an agent**. Devices,
websites, and platforms are re-formed as agents.
*Why:* one consistent model for every entity; the existing internet, made
agent-actionable.

## 2. Agent = operator
An agent is an **operator** of a node (the Kubernetes Operator pattern,
generalized) — it runs a reconciliation loop over its node.
*Why:* the most **stable, efficient, real-world** definition — a proven role, not
a vague "chatbot" or "script."

## 3. Box (open) vs Platform (commercial)
The **box** (building blocks) is open source; the **platform** (arrangement of
boxes into delivered value) is the commercial engine.
*Why:* open source is a **design system, not a business model**; **open ≠ free**;
the moat is the **arrangement and delivery**, not the parts. (Ubuntu/Canonical.)

## 4. Contracts are language-agnostic (proto)
Define contracts once in **Protocol Buffers**; generate native code per layer.
*Why:* the system is **polyglot** (native per layer); the contract must not be tied
to any one language. "Why `.py`?" → it was only a prototype target.

## 5. "Native" is context-dependent
code = hardware-native · core = k0s · network = k8s · surface = UI-native.
*Why:* never **generic**; reuse the right standard at each layer; collapsing every
layer into one (e.g. "everything k8s-native") is the wrong architecture.

## 6. Ability stack: language → capability → tool → skill
Capability **authorizes**; tool **executes**; skill **composes** (a skill is a
flow). Every action is a capability; the vocabulary reuses **schema.org** + named
command sets.
*Why:* reuse, don't invent; capability (authorization) and tool (execution) are
distinct.

## 7. The trinity: Intent → Action → Outcome
Intent is **declared** (the "why" — unprovable); action and outcome are
**verified**.
*Why:* a capability-outcome driven world; you can prove *what was done* and *what
resulted*, never the *why* (the irreducible uncertainty).

## 8. The loop = reconciliation = the graph
The deterministic loop converts **unstructured → structured**; **stability =
conformance with the graph**; the graph **keeps expanding** (governed conformance
= progress; ungoverned change = drift).
*Why:* structure is progress; the graph is the loop's state, the loop is the graph
in motion — one thing.

## 9. Nodes = identities (open); interaction = trust-scored
Anyone can create a node (**open**); **interaction is earned** (trust score from
provenance + reputation + attestations + conformance). **Identify everything**
(id record — for governance & security); engage only the verified. **No orphans**
(an orphan is a security risk).
*Why:* resolves **open vs safe** — open to join, earned to interact.

## 10. Zero-trust on open standards
Always verify, default-deny; trust from provable identity + capability, never
location; trust **expires**. Built on **W3C DID · VC 2.0 · schema.org · MCP · OCI ·
k0s/k8s · SurrealDB · Ubuntu** — all open.
*Why:* the standards are the commons; we arrange them (the platform), we don't own
them.

## 11. Stable deterministic core + probabilistic sidecars
The control plane (the loop, verify, root of trust) is **deterministic and
stable**; the LLM and other variable work are **sidecars, gated by the core**.
*If it can't be stable core → sidecar.*
*Why:* build a **reliable** system out of **unreliable** parts.

## 12. Drift is the enemy
Everything decays. Every primitive — identity, provenance, signatures, **expiry**,
reconciliation, graceful retirement — is **anti-drift machinery.**
*Why:* there is no villain; the adversary is entropy. Trust is a **process**, not a
state.

---

The full discussion lives in the working session; this is its **decision record**
— the *why* behind every *what*. New decisions should be appended here.
