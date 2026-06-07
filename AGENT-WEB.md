# Agent Web — the Internet of Agents

**Agent Web is the Internet of Agents.** Just as the Internet of Things connected
*things*, the Agent Web connects **agents** — autonomous, signed, callable,
capability-bearing entities — over the open web.

This is the unifying model — a "theory of everything" for the agent world: **one
consistent model for every entity.**

## The one law: everything is an agent

Every entity is an **agent** — a *box*: a sealed, signed, identifiable, callable
unit. **Repos, apps, services, vocabularies, devices, and the representatives of
humans — all are agents.** Every repo is an agent; every agent is a box. One
model for everything.

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
