# Core constructs — term · contract · source

The load-bearing constructs, each with its **term**, **contract** (field schema),
and **source ref** (the existing standard it reuses — *reuse, don't invent*).

## Graph

- **Term** — the canonical structure: **nodes** (identities) + **edges**
  (interactions); the conformance reference; keeps expanding (governed).
- **Contract** — `{ nodes: [Node], edges: [Edge], schema: @context, version }`
- **Source ref** — **Labeled Property Graph** + **RDF / W3C**; **SurrealDB** graph
  model; **schema.org** for node/edge meaning.

## Contract

- **Term** — a **signed manifest** declaring an entity's structure and interface
  (fields · provides · requires); the agreement everything conforms to.
- **Contract** — `{ subject: DID, type, fields, provides, requires, @context, conformance, proof }`
- **Source ref** — **Design by Contract** (Meyer); **JSON Schema** / **OpenAPI**;
  **W3C VC 2.0** (the signed-manifest form); **CNCF conformance**.

## Loop

- **Term** — the **deterministic reconciliation loop**: heartbeat → move-next over
  the graph → verify → execute → repeat; converts unstructured → structured;
  reconciles state toward the objective.
- **Contract** — `{ state, objective, graph, step: (set-context → align → act → outcome → verify → advance), tick, halt }`
- **Source ref** — **control loop** / **MAPE-K** (autonomic computing);
  **Kubernetes controller** reconciliation; **GitOps / Flux**.

## Building block

- **Term** — the **box**: the canonical, sealed, signed, composable unit. Agents
  and components are building blocks; compose, don't decompose.
- **Contract** — = the **Agent / Box** contract (`id · type · capabilities ·
  surface · governance · conformance · provenance · proof`).
- **Source ref** — **OCI** (container) / **snap**; **microservice**; **CNCF**;
  Lego-brick composability (sealed + studs).

---

**Every definition carries a source ref** — reuse the open standard, don't invent.
That is the agent-language principle, applied to the constructs themselves.
