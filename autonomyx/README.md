# autonomyx — the canonical box for trustworthy, composable agents

> **The idea is integration, not invention.** Every concept here already exists —
> cryptographic identity, provenance, capabilities, signing, conformance,
> composition. What's missing is a project that **packages them into one sealed,
> signed, canonical unit — *the box* — with a manual inside, and a path to deliver
> it everywhere with consistent behavior.** That box is `autonomyx`.

`autonomyx` is a minimal **zero-trust kernel** plus a **signed-flow composition
layer**. It is the *smallest canonical unit* of a trustworthy agent system — and
everything larger (flows, surfaces, platforms) composes from it.

**Status: proof of concept.** The core — the box and signed flows — is built,
tested, and runnable. It is an educational reference and a foundation, **not yet
a production platform.** The roadmap below is honest about the gap.

---

## What the box is

A **box** is a sealed, signed, identifiable unit built from native primitives:

| Primitive | What it is |
|---|---|
| **Identity** | an Ed25519 keypair; the fingerprint is the unit's origin id |
| **Provenance** | signed certificate chains proving lineage to a canonical root |
| **Capability** | unforgeable, scoped, caveated grants (object-capability authz) |
| **Message** | the only interaction — a signed, addressed, tamper-evident envelope |
| **Kernel** | the canonical core: registration + **always-verify, default-deny** routing + audit |

A **flow** composes boxes: a capability-gated sequence of steps, **signed by its
author** (ownable, sellable), that **expires** (anti-drift) and is fully audited.

**The enemy is drift.** Every primitive is anti-drift machinery: identity vs
anonymity, provenance vs history-loss, signatures vs forgery, **expiry vs trust
decay**, audit vs the unrecorded. Trust is not a state you hold — it is a process
you continuously renew.

## Quickstart

```bash
pip install cryptography pytest

python examples/agent_demo.py     # agent-to-agent market with an audit trail
python examples/flow_demo.py      # a signed, expiring flow; tampered & stale flows refused
python -m pytest tests/test_kernel.py tests/test_flow.py -q   # 19 passing
```

## The layered architecture (the design principle)

The box is native at each layer — and **not generic** at any of them:

| Layer | Native to | Strategy | Fitting language |
|---|---|---|---|
| **Core** | the kernel / silicon | hardware-native (specific) | **Rust** |
| **Container** | the runtime | cloud-native (**portable**) | **Go** |
| **Network** | communication | **every protocol** (universal) | — |
| **Surface (UI)** | each touchpoint | **surface-native** (specific) | **Node / React** |

Portability lives in the **box/manifest**; the **code is native to its layer**.
Accountability pins to the **portable identity**, not the location — so the box is
**real** (runs on a device: core + memory + network), **accountable** (signed
identity), and **portable** (move it across any provider — no lock-in).

This repo currently implements the **logic of the box and flows in one reference
language (Python)** — the conceptual kernel — not yet the polyglot, layered,
hardened deployment. That is the build-out.

## What the proof of concept demonstrates

- the **box**: identity + provenance + capability + audit, sealed and signed;
- **composition**: signed, expiring, capability-gated flows over boxes;
- **anti-drift**: signature (vs forgery) + expiry (vs decay) + audit (the record);
- **zero-trust**: default-deny, accountability pinned to identity;
- all of it **tested and runnable** — code, not a manifesto.

## Roadmap (the honest gap to the full box)

- [ ] **Polyglot layers** — Rust core, Go runtime, JS/React surfaces.
- [ ] **Headless, multi-surface** delivery — one core, many native heads, one consistent experience (n = 1 to n = ∞).
- [ ] **Portable workload identity** (SPIFFE/SPIRE) + attestation; root key in an HSM/enclave (the core off the surface).
- [ ] **Natural-language flow builder** compiling to declarative, signed flows.
- [ ] **Open, governed contract** + conformance, so flows work at all surfaces.
- [ ] **Provenance → value**: signed usage/attribution rails (use or sell a flow).
- [ ] **The manual *in* the box** + consistent global delivery.

## Box vs Platform — the keystone

Two distinct things, two distinct models:

- **The box is open source.** It is the **building blocks** — the canonical unit
  and its primitives. **This repo *is* the box.** The community participates
  *here*: contributing to, and building with, the open box. Once the box is built,
  the community can participate *because the box provides the building blocks.*
  (Design system / commons.)
- **The platform is the commercial engine.** A platform is **not** a box — it is
  the **arrangement of the building blocks** into delivered value: flows,
  orchestration, the consistent global experience, the absorbed operational
  burden. That arrangement — operated and delivered — is where the **commercial**
  value lives.

> **Open box (building blocks, commons) + commercial platform (arrangement of the
> blocks).** You build the platform **on** the open box. You never close the box to
> monetize — *open ≠ free, and open source is a design system, not the business
> model.* The moat is the **arrangement and delivery** (the platform), not the
> building blocks (the box).

**The precedent is Ubuntu.** The **box is like Ubuntu** — an open, complete,
packaged, documented, registry-published, deployable distribution, free to use,
built openly with a community. The **platform is like Canonical** — the
commercial engine (support contracts, Pro, services) built *around* the open box,
not by closing it. **Use the box for free, or contract with the platform** — same
model, proven at scale.

**Even sharper: Ubuntu Core.** Ubuntu Core is built **entirely from snaps** —
signed, confined, atomic packages — is **immutable** and **transactional** (atomic
updates with rollback), **secure by design** (confinement keeps the core off the
surface), and runs on **real devices** at the edge. That *is* the box model: a
system **composed of signed, sealed, confined boxes**, immutable and anti-drift by
construction, real on the device. `autonomyx` is that idea for **agents** — in
Ubuntu Core every snap is a box; here **every box is an agent.**

We take the **model, not the product.** Ubuntu Core (e.g. the recently-launched
**UC26**) is the **precedent that proves the pattern works** — not a base we build
on, fork, or depend on. `autonomyx` is its **own box, for agents, built
independently** from first principles.

## Open by design

`autonomyx` is **open governance, not a walled garden** — the keystone of the
whole design. The contract and meaning are meant to be a **commons**, operated in
the open. We intend to grow this **collaboratively with the community** and to
pursue **CNCF Sandbox** as the project matures.

See [`CONTRIBUTING.md`](../CONTRIBUTING.md), [`GOVERNANCE.md`](../GOVERNANCE.md),
[`CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md), and [`LICENSE`](../LICENSE).
