# Contributing to autonomyx (the box)

`autonomyx` — **the box** — is open source. The community participates here:
the box provides the **building blocks**; you contribute to them and build with
them. (The commercial **platform** — the *arrangement* of the building blocks —
is a separate concern and lives elsewhere. The box is never closed to monetize.)

## The box lifecycle (the production pipeline)

Every box is produced through the same auditable pipeline. A contribution moves a
box through these stages — and the output is a **signed, documented box**, never
a dangling one:

| Stage | What it means | Tooling (now → target) |
|---|---|---|
| **define** | specify the box: scope, interface, contract | README / spec / schema |
| **design** | architect the layers (core / runtime / surface), the sealed-yet-generative shape | design notes / ADRs |
| **build** | implement & compile — native per layer, portable box | Python ref → Rust/Go/JS, multi-arch image |
| **verify** | tests, conformance, signature checks | `pytest` → CI, conformance suite, `cosign verify` |
| **sanitize** | SBOM, vuln scan, secret scan, prune dangling/cruft | (target) Syft, Trivy/Grype, gitleaks |
| **document** | the manual **in** the box | README / docs |
| **sign + publish** | sign the artifact, push to a registry (never dangling) | (target) Sigstore/cosign + registry, SLSA provenance |
| **register** | register the signed box in **registries** — discoverable, verifiable, **never dangling** | (target) OCI / artifact registries |
| **deploy** | run the box on a device (core + memory + network), native per layer | (target) k8s / bare metal, portable (SPIFFE) identity |

The pipeline is itself a flow: its output should carry **signed provenance**
(SLSA-style) — the box proves *how* and *by whom* it was built.

## Developer setup

```bash
pip install cryptography pytest
python -m pytest tests/ -q          # verify
python examples/agent_demo.py       # the box: agent-to-agent + audit
python examples/flow_demo.py        # signed, expiring flows
```

## Pull requests

1. Branch from the default branch; keep PRs focused.
2. **Add or update tests** — every change goes through **verify** (the suite stays green).
3. Keep the box **native per layer** and **not generic**; keep the surface decoupled (headless).
4. Update **docs** for any behavior change (a box ships with its manual).

## Developer Certificate of Origin (DCO)

By contributing you certify the [DCO](https://developercertificate.org/). Sign
off every commit:

```bash
git commit -s -m "your message"
```

This adds a `Signed-off-by:` trailer — provenance for who authored the change.
CNCF projects require DCO; we follow that from day one.

## Scope

In scope: the **box** and its primitives (identity, provenance, capability,
message, kernel) and the **flow** composition layer. Out of scope (here): the
commercial platform, proprietary surfaces, and anything that closes the box.

See [`GOVERNANCE.md`](GOVERNANCE.md) and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
