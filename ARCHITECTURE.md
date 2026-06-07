# Architecture — locked decisions

This records the **decided** architecture for the box (`autonomyx`) and the
platform built on it. Detail and rationale live in
[`autonomyx/README.md`](autonomyx/README.md); this is the locked summary.

## Base

**Ubuntu** — the right base *and* the right model:

- **Ubuntu Core / snaps** → sealed, signed, confined boxes
- **Chiselled** → minimal, sliced, smallest composable units
- **Real-time (PREEMPT_RT)** → the deterministic stable core
- **App store / embedded / server** → distribution + the full edge↔cloud span
- **Open snaps + Canonical** → the **open-box + commercial-platform** model

## "Native" is context-dependent

`native` alone is meaningless — it must say *native to which layer.* Never
generic; native per context:

| Layer | "native" means | Language |
|---|---|---|
| **code** | hardware-native (per silicon, never generic per cloud) | Rust |
| **core** (compute / agent loop) | kernel-native → **k0s** (minimal, conformant) | Rust |
| **runtime** | runtime-native (OCI) | Go |
| **network** | **k8s-native** (full: CNI, mesh, scale) | Go |
| **surface** | surface/UI-native (per touchpoint) | Node/React |

## Orchestration: k0s at the core, k8s at the network

Same Kubernetes API throughout (**kubernetes-native ≠ heavyweight-everywhere**):

- **Core / edge / device → k0s** — single-binary, zero-dependency, CNCF-conformant.
  The **agent loop** runs here. Minimal where it's the core.
- **Between → edge↔cluster federation** — k0s scaling to HA / fleet / GitOps
  bridging up to the network.
- **Network / cluster / datacenter → k8s (full)** — multi-node, CNI, service mesh,
  scale. Full where it's the network.

## The agent loop (the deterministic core)

The motherboard is the **stable, deterministic control loop**: heartbeat →
**move-next over the graph** → **verify** → execute → repeat.

- **Deterministic. Stable. Fixed.** No probabilism in the control plane.
- Runs on **FPGA (hardware determinism)** and/or **real-time Ubuntu (software
  determinism)**.
- The **root of trust is off the surface** (secure element / enclave).

## The box / sidecar partition

> **If it can be stable and deterministic → the core. If it can't → a sidecar.**

- **Core (stable):** the agent loop, verify, root of trust. *Never drifts.*
- **Sidecars (probabilistic):** LLM inference (**GGUF** on GPU), reasoning,
  surfaces. **Gated, verified, and audited by the core** (zero-trust at the
  core↔sidecar boundary). Swappable without touching the core.

This is how a **reliable** system is built from **unreliable** parts: the
deterministic core gates and verifies the probabilistic sidecars.

## Agent definition (at creation)

An agent is **defined declaratively** by a **signed manifest** with four parts:

| Part | What it declares | In the box |
|---|---|---|
| **Capability** | what the agent **may do** (scoped grants) | VC / capability primitive |
| **Environment** | **where / in what context** it runs (device, cloud, domain, resources) | deploy target (k0s core ↔ k8s network) + the slot/bus it plugs into |
| **Governance policy** | the **rules and constraints** it operates under (default-deny + allowed + auditable constraints) | enforced by the **deterministic core** (the verify gate) |
| **Framework** | the **execution / reasoning framework** it uses | the **probabilistic sidecar** (AG2 / MAGUS / LLM) the loop calls |

The manifest is **signed** → provenance of *who* defined it and *as what*.
**Capability and governance are enforced deterministically by the core;** the
**framework runs as a gated sidecar;** the **environment** is where it deploys.
Define → sign → it becomes a box.

### Capability — defined

A capability is a **signed grant**, defined by three things:

| Part | What it is |
|---|---|
| **Reference** | canonical, unforgeable ids: **subject** (a DID), **resource** (a URI / DID-URL), and the capability's own id |
| **Definition** | the scope: **action** (verb) on **resource** (object), with **caveats** (expiry, max-uses, conditions) |
| **Agent-language** | the canonical **vocabulary / ontology** (`@context`) that *defines the meaning* of `action` and `resource` — unambiguous, interoperable ("the platform defines the meaning," at the capability level) |

Signed by the issuer's DID → **unforgeable + provenanced.** In open-standard
form a capability **is a W3C Verifiable Credential**: issuer (DID) · subject
(DID) · grant (claims) · `@context` (agent-language) · proof (signature).

### Capability vocabulary (the list)

The **agent-language** reuses an existing open standard rather than inventing
one: **schema.org `Action`** (a canonical, widely-adopted action hierarchy) —
**plus** a human↔machine information-exchange command set.

**From schema.org `Action` (the human-world vocabulary):**

- **Consume** — Read · View · Watch · Listen · Use · Install · Play
- **Create** — Write · Draw · Paint · Photograph · Film · Cook
- **Control** — Activate · Deactivate · Suspend · Resume
- **Communicate / Interact** — Ask · Inform · Reply · Comment · Share · Invite · Register · Subscribe · Follow · Join · Leave
- **Move** — Arrive · Depart · Travel
- **Organize** — Allocate (Accept · Assign · Authorize · Reject) · Apply · Bookmark · Plan (Cancel · Reserve · Schedule)
- **Trade** — Buy · Sell · Order · Pay · Quote · Rent · Donate · Tip · PreOrder
- **Transfer** — Send · Receive · Give · Take · Borrow · Lend · Return · Download · MoneyTransfer
- **Update** — Add · Delete · Replace
- **Find** — Search · Check · Discover · Track
- **Assess** — Choose · Review · React · Ignore
- **Achieve** — Win · Lose · Tie

**Plus human↔machine information-exchange commands (the machine layer):**

- **Query / Request** · **Respond / Return** · **Command / Invoke**
- **Acknowledge / Confirm** · **Subscribe / Stream / Notify**
- **Authenticate / Authorize / Verify** · **Negotiate** · **Delegate** · **Audit / Log**

Every capability's `action` references one of these (a canonical `schema:` URL or
a machine-command id) → unambiguous, interoperable meaning. **Don't invent the
vocabulary — integrate the open one (schema.org) and extend it for machines.**

## Trust substrate (the box primitives)

Identity · Provenance · Capability · Message · Audit — sealed, signed, default-deny,
always-verify. Open-standard form: **W3C DID** (identity) · **W3C VC** (capability /
provenance) · **DIDComm / mTLS** (message). Accountability pins to the **portable
identity**, not the location (SPIFFE-style) — real, accountable, *and* portable.

## Box vs Platform

- **Box = open source** — the building blocks (this repo). Community participates
  here. *(Ubuntu / snaps.)*
- **Platform = commercial engine** — the **arrangement** of the blocks: flows,
  packaging (all formats), the **app store**, orchestration, consistent global
  delivery, support. *(Canonical model.)* The box is never closed to monetize.

## Pipeline

define → design → build → verify → **sanitize** → document → sign → publish →
**register** (registries, never dangling) → **deploy** (edge↔cloud).
Verified in the open (Verilator / Yosys / gem5 / GPGPU-Sim / Numba).

## Enemy

**Drift.** Every primitive — identity, provenance, signatures, expiry,
reconciliation (GitOps/Flux), graceful retirement — is anti-drift machinery.
Trust is a process, continuously renewed, never a held state.
