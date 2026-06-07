# Trust & accountability — term · contract · source

The trust layer, each construct with its **term**, **contract**, and **source ref**.
Trust is **earned and verified**, never assumed; everything is **recorded**.

## Trust score

- **Term** — a derived measure of how trustworthy a node is; **gates interaction**
  (node creation is open; engagement is earned).
- **Contract** — `{ node: DID, score: 0..1, inputs: {provenance, reputation, attestations, conformance}, computed_at, decay }`
- **Source ref** — **web of trust** (PGP); **EigenTrust**; reputation systems;
  SSI trust registries.

## Reputation

- **Term** — a node's accumulated **track record** — did its past outcomes meet
  their objectives and conform?
- **Contract** — `{ node: DID, outcomes: [{objective, met: bool, at}], score }`
- **Source ref** — reputation systems; outcome history; PageRank-style scoring.

## Attestation

- **Term** — a **signed statement** by one node vouching for a claim about another
  (a verifiable credential).
- **Contract** — `{ issuer: DID, subject: DID, claim, proof }`
- **Source ref** — **W3C VC**; **in-toto** attestations; **SLSA**; web of trust.

## Conformance

- **Term** — whether a node/artifact **aligns with the graph / schema / contract**
  (the stability test; non-conforming = drift).
- **Contract** — `{ subject, schema: @context, conforms: bool, report }`
- **Source ref** — **CNCF conformance** (Certified Kubernetes); **JSON Schema**
  validation; W3C conformance.

## Provenance

- **Term** — the **signed lineage** (worldline) of an artifact/identity: who · what ·
  when · where, back to a root.
- **Contract** — `{ subject, chain: [signed events], root }`
- **Source ref** — **W3C PROV**; **SLSA** provenance; **Sigstore / Rekor**; git history.

## Audit

- **Term** — the **tamper-evident record** of every interaction (the accountability
  log). Identify everything; record all.
- **Contract** — `{ entries: [{who, what, when, where, decision, reason}], append_only }`
- **Source ref** — audit logs; **transparency logs** (Rekor); the four Ds.

---

**Trust = earned (score) + verified (zero-trust) + recorded (audit).** No orphans;
nothing untracked.
