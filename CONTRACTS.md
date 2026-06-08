# Contracts — the Agent Web

The formal **contract** (field schema) for each entity. The **terms** are in
[`DEFINITIONS.md`](DEFINITIONS.md); this is their **structure.** Every contract is
a **signed manifest** (provenance), expressed in the agent-language (`@context`),
scoped to a domain, verified zero-trust, and conformant to the graph.

## Agent (the box)

| Field | Type / value |
|---|---|
| `id` | DID |
| `type` | platform · vocabulary · identity · registry · service · app · gateway |
| `capabilities.provides` | [ capability ] |
| `capabilities.requires` | [ capability ] |
| `environment` | domain · runtime · resources |
| `governance` | policy (default-deny + allowed + auditable constraints) |
| `framework` | the execution / reasoning framework (sidecar) |
| `surface` | MCP / API endpoint(s) |
| `trust_score` | derived (provenance + reputation + attestations + conformance) |
| `provenance` | signed worldline (git history) |
| `proof` | signature (DID) |

## Capability (= W3C VC 2.0)

| Field | Type / value |
|---|---|
| `@context` | agent-language (schema.org + namespaces) |
| `issuer` | DID |
| `subject` | DID |
| `action` | `namespace:verb` (from the catalog) |
| `resource` | URI / DID-URL |
| `caveats` | { expires_at, max_calls, conditions } |
| `proof` | signature (issuer DID) |

## Tool

| Field | Type / value |
|---|---|
| `name` | `namespace:verb` (the capability it implements) |
| `input` | JSON Schema |
| `output` | JSON Schema |
| `requires` | capability (the authorization gate) |
| `implementation` | deterministic (core) \| probabilistic (sidecar) |
| `proof` | signature (provider DID) |

## Skill / Flow

| Field | Type / value |
|---|---|
| `name` | id |
| `author` | DID |
| `steps` | [ step ] (ordered / graph) |
| `requires` | [ capability ] |
| `official` | bool (platform-certified) vs community (author-signed) |
| `expires_at` | timestamp |
| `proof` | signature (author DID) |

## Step

| Field | Type / value |
|---|---|
| `objective` | desired outcome of the step |
| `context` | current state · environment · inputs |
| `target` | env + outcome (aligned before acting) |
| `action` | capability + tool |
| `verify` | outcome vs objective (+ metrics) |

## Message

| Field | Type / value |
|---|---|
| `sender` | DID |
| `recipient` | DID |
| `action` | `namespace:verb` |
| `resource` | URI |
| `payload` | object |
| `nonce` | unique |
| `timestamp` | time |
| `proof` | signature (sender DID) |

## Node

| Field | Type / value |
|---|---|
| `id` | DID |
| `type` | (agent type) |
| `properties` | trust_score · capabilities · contract |
| `provenance` | signed |

## Edge

| Field | Type / value |
|---|---|
| `type` | grants · calls · trusts · derives-from · composes · in-domain · conforms-to |
| `from` | DID |
| `to` | DID / resource |
| `properties` | weight (trust) · caveats |
| `proof` | signature |

---

Every contract is **signed** (provenance), **scoped** (domain), **verified**
(zero-trust), and **conformant** to the graph schema. *Define → sign → it is real.*
