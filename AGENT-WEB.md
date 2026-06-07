# Agent Web — the Internet of Agents

**Agent Web is the Internet of Agents.** Just as the Internet of Things connected
*things*, the Agent Web connects **agents** — autonomous, signed, callable,
capability-bearing entities — over the open web.

We are defining a world where **the internet is a mesh** — a zero-trust,
identity-based, every-protocol fabric — and **each node is operated by an agent.**
Every node is an agent; every connection is a **trust-scored, capability-gated,
signed** interaction. The mesh is the network; the agents are the nodes.

The nodes are the things that **already make up the internet — devices,
websites, platforms** — each re-formed as an **agent**:

- **Devices** → device agents (edge / gateway / service; the box on real hardware).
- **Websites** → website agents (app / gateway; each site an agent — capabilities,
  callable, signed).
- **Platforms** → platform agents (host and arrange other agents).

The existing internet **becomes** the agent mesh — every device, site, and
platform an agent-operated node.

This is the unifying model — a "theory of everything" for the agent world: **one
consistent model for every entity.**

## The one law: everything is an agent

Every entity is an **agent** — a *box*: a sealed, signed, identifiable, callable
unit. **Repos, apps, services, vocabularies, devices, and the representatives of
humans — all are agents.** Every repo is an agent; every agent is a box. One
model for everything.

## The theory: Intent → Action → Outcome (the trinity)

The agent world is **outcome-driven** and **capability-mediated.** Its irreducible
concept is a trinity:

| | What | Verifiable? |
|---|---|---|
| **Intent** | the desired outcome — the goal/request, delegated (NL → declarative) | **declared** — the "why" (not provable, like the 4 Ds' *why*) |
| **Action** | what is done to fulfil it — capabilities exercised via tools, composed as skills/flows | **verifiable** — capability-gated, signed (who/what/when/where) |
| **Outcome** | the result — what actually happened, checked against the intent | **verifiable** — audited (the worldline) |

- You **delegate intent.**
- The agent **acts** — through the ability stack (language → capability → tool →
  skill/flow), **authorized and gated** by the deterministic core.
- The **outcome** is **verified and audited**, then checked against the intent.

**The deterministic loop *is* this trinity:** intent in → move-next over the graph,
exercising gated capabilities/tools → outcome verified and recorded.

**Intent is declared; action and outcome are verified.** The gap between intent and
outcome is where risk lives — **verification and audit measure and close it.** You
can prove *what was done* and *what resulted*; you can only *declare* the *why*.
That is the honest shape of a capability-outcome driven world: **delegate intent,
act under capability, verify the outcome.**

## How it progresses: unstructured → structured

The agent's **reconciliation loop converts the unstructured into the structured.**
That is its core work — and how the world progresses.

- **Input — unstructured:** intent (natural language), raw data, the messy world.
- **Loop — reconcile:** the deterministic loop interprets it, gates it through
  capabilities, and reconciles it **against the schema and the agent-language.**
- **Output — structured:** a **graph** (relationships) conforming to a **schema**
  (shape), producing **outcomes** with **metrics** (measured, verified).

| Concept | What |
|---|---|
| **Structure** | organized, canonical, machine-legible form (the goal-state) |
| **Schema** | the structured *shape / types* — valid structure |
| **Graph** | structured *relationships* — nodes + edges (flow · knowledge · agent network) |
| **Metrics** | structured *measurements* — quantified, verified outcomes |

Mapped to the trinity: **unstructured intent → structured action** (via the schema /
agent-language / capabilities) **→ measured outcome** (metrics, verified). The loop
**structures** intent into action and **measures** the outcome.

And it is **continuous** — reconciliation re-structures against **drift** (the
unstructured, the decay). Structure is **held and grown against entropy.**

**That is how the world progresses:** the agent web converts the unstructured world
into structured, machine-legible, actionable form — continuously, verifiably, one
reconciliation loop at a time. **Progress = accumulated structure, held against
drift.**

### The graph keeps expanding

The graph is **living, not frozen.** As agents reconcile unstructured → structured
— adding capabilities, joining domains, structuring new knowledge — **the graph
keeps expanding.** Growth *is* progress.

But growth is **governed**, and that is the key distinction:

- **Expansion** — *conformant, governed* additions: new nodes/edges validated by
  the governance agent, no contradictions, versioned, without breaking existing
  conformance. **This is progress.**
- **Drift** — *non-conformant, ungoverned* change. Rejected or reconciled back.

So **the graph expands by conformant growth and is held against drift.** Both
change the graph; one is governed progress, the other is decay. Stability is
**conformance with the *current, growing* graph** — dynamic, not frozen. The
graph never stops expanding; it only refuses to expand *non-conformantly.*

### Nodes are identities; interaction is trust-scored

- **A node is an identity** — every node in the graph is an agent's **DID.**
- **Node creation is open** — identity is self-sovereign; **any new identity can
  create a node.** The graph is permissionless to *join.*
- **But interaction is trust-scored** — you do **not** trust every node equally.
  **Every interaction (edge · capability grant · message) is gated by the
  counterparty's *trust score*.**

**Trust is earned, not granted by existence.** A node's **trust score** is built
from:

- **provenance** — verifiable lineage (chain to a trusted root; attestations),
- **reputation** — past outcomes and audit history (did it deliver? conform?),
- **attestations** — VCs vouching for it (web of trust),
- **conformance** — alignment with the graph (non-conformance lowers it).

This resolves **open vs safe:** **open to create a node (permissionless),
trust-scored to interact (earned).** Sybil / fake identities are cheap to *create*
but earn *low trust* — so they get limited interaction. **Zero-trust verifies**
every interaction cryptographically; the **trust score weights** how much to
engage after verifying. *Verify the identity; weight the interaction by trust.*

**Identify everything; interact selectively.** When a new identity appears:

- **always create an *id record*** — record the identity in the graph (known,
  tracked, auditable),
- **but do not interact** until trust is established (trust-scored).

**Identification is necessary for governance and security** — you cannot govern
or secure what you cannot identify. So **everything is identified and recorded**
(even untrusted identities — you record the threat too); **only the trusted are
interacted with.** *Identification ≠ trust: record all; engage the verified.*

**No orphans.** Every thing is **connected, owned, recorded, and accountable** —
**no orphan nodes** (every node is in the graph, with provenance and an id
record), **no dangling artifacts** (every box signed and registered, never
dangling), **no unowned resources or processes.** **An orphan is a security risk** — an
untracked thing you cannot govern or secure, exactly where attacks hide (orphan
processes, dangling images, unowned resources, abandoned keys). The reconciliation
loop leaves **no orphans:** everything is **connected/owned or gracefully
retired.** On retirement, dependents are reconciled — **never orphaned.**

## What an agent is (the box)

| Part | What | Standard |
|---|---|---|
| **Identity** | who it is — sovereign, portable (not location) | W3C **DID** |
| **Provenance** | its signed history (the worldline) | signed commits · VCs · SLSA |
| **Capabilities** | what it may do — verbs on resources | W3C **VC 2.0** + the catalog |
| **Core** | the deterministic loop: heartbeat → move-next → verify | the motherboard |
| **Sidecars** | the probabilistic workers (LLM/GGUF), gated by the core | — |
| **Surface** | how it is called | **MCP** · API · web (every protocol) |

Sealed substance, generative interface. **Real** (runs on a device: core + memory
+ network), **accountable** (signed identity), **portable** (move it — identity,
not location), **sovereign** (you hold the key).

## The substrate: the web

The web **contains the information** and is the **home of everything.** Agents are
addressed by **URIs / DIDs**, speak the shared vocabulary (**schema.org** + the
[capability catalog](CAPABILITIES.md)), and call each other over **MCP / API /
HTTP** — every protocol. The standards are all **W3C / open.** The Agent Web is
the web made **agent-actionable.**

## The law: zero-trust

Every interaction is a **signed, capability-gated, verified, audited** message.
Trust derives from **provable identity + a matching capability** — never from
location — and it **expires** (trust is a process, not a state). **Default-deny,
always-verify.**

## Governance: open, by agents

The **meaning** — the capability vocabulary / agent-language — is defined and
governed **in the open**, by a **vocabulary agent** (itself a box) that
**validates · governs · maintains** the catalog. The system governs itself with
its own primitives. **Open meaning, never captured.**

## Box vs Platform

- **Box = open** — the building blocks (agents, the catalog, the standards). The
  commons. The community participates here.
- **Platform = commercial** — the **arrangement** of agents into delivered value:
  flows, packaging (all formats), the app store, consistent global delivery,
  support. **The box is never closed to monetize.** (The Ubuntu / Canonical model.)

## Repo types & contracts (build the internet first)

Build the **internet** — the typed, contracted, addressable substrate — *before*
the agents. Every repo is an agent of a **type**, and every agent exposes a
**contract**: a signed manifest declaring how it is called and what it does. The
agents plug into the contracts; the contracts come first.

### Types

| Type | Role |
|---|---|
| **platform** | the core substrate — hosts and arranges agents (the commercial engine) |
| **vocabulary** | validates · governs · maintains the agent-language / capability catalog |
| **identity** | issues and anchors DIDs + VCs — the root of trust |
| **registry** | discovery — where agents are listed and found |
| **service** | a capability provider — exposes verbs (tools / backends) |
| **app** | a specific end-user application / experience |
| **gateway** | a surface — exposes the agent web to a touchpoint (web / mobile / voice / …) |

### Contract (every agent-repo declares, signed)

| Field | Declares |
|---|---|
| **type** | one of the types above |
| **identity** | its DID |
| **capabilities** | verbs it **provides** and verbs it **requires** (from the catalog) |
| **surface** | how it is called — **MCP / API** endpoint(s), every protocol |
| **governance** | its policy (default-deny + allowed + auditable constraints) |
| **conformance** | what its type requires it to implement |
| **provenance** | signed — git history is the worldline |

The contract is the agent's **manifest** (capability · environment · governance ·
framework) **+ type + surface**, signed. **Define the types and contracts first —
that is the internet.** The agents plug into it.

## The enemy: drift

Everything decays. Every primitive — identity, provenance, signatures, expiry,
reconciliation (GitOps), graceful retirement — is **anti-drift machinery.** The
Agent Web is held against drift, continuously. There is no enemy but drift.

---

**Agent Web = the Internet of Agents.**
Everything is an agent. Every agent is a signed, callable box. The web is the
substrate. Zero-trust is the law. Open governance is the keystone. Drift is the
enemy.

*That is the world we are defining.*
