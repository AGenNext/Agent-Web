# Repos — term + contract for each type

Every repo is an agent of a **type**. Here is each type's **term** (what it is) and
**contract** (what it provides / requires). Generic agent contract:
[`CONTRACTS.md`](CONTRACTS.md). Components (agent · capability · tool · skill ·
message · node · edge): terms in [`DEFINITIONS.md`](DEFINITIONS.md), contracts in
`CONTRACTS.md`.

## platform

**Term** — the core substrate agent that **hosts and arranges** agents into
delivered value; the commercial engine.

| Contract | Value |
|---|---|
| `type` | platform |
| `provides` | arrange · package · deliver · app-store · support · govern |
| `requires` | (all types) |
| `surface` | MCP / API |
| `governance` | defines & **operates** the platform contract (in the open) |
| `conformance` | hosts only signed, conformant agents |

## vocabulary

**Term** — the agent that **validates · governs · maintains** the agent-language
(capability catalog); the `@context` authority.

| Contract | Value |
|---|---|
| `type` | vocabulary |
| `provides` | validate · govern · maintain (over the catalog) |
| `requires` | content:* · git:* (on the catalog) |
| `surface` | MCP / API |
| `governance` | open; curates the canonical vocabulary |
| `conformance` | every term namespaced, defined, signed |

## identity

**Term** — the agent that **issues and anchors** DIDs + VCs; the root of trust.

| Contract | Value |
|---|---|
| `type` | identity |
| `provides` | authenticate · authorize · verify · issue-DID · issue-VC · revoke · attest |
| `requires` | (root key — off the surface) |
| `surface` | MCP / API |
| `governance` | root of trust; revocation registry |
| `conformance` | DID · VC 2.0 |

## registry

**Term** — the **discovery** agent — where agents are listed, found, resolved (the
"DNS" of the agent web).

| Contract | Value |
|---|---|
| `type` | registry |
| `provides` | register · discover · resolve · list · search |
| `requires` | machine:query |
| `surface` | MCP / API |
| `governance` | **id record for every node; no orphans** |
| `conformance` | resolves DID → contract → surface |

## service

**Term** — a **capability provider** — exposes verbs (tools / backends); the
workhorse agent.

| Contract | Value |
|---|---|
| `type` | service |
| `provides` | (its specific capabilities / tools) |
| `requires` | (its dependencies) |
| `surface` | MCP / API |
| `governance` | capability-gated, audited |
| `conformance` | tools = catalog verbs |

## app

**Term** — a specific **end-user application / experience**; the user-facing agent.

| Contract | Value |
|---|---|
| `type` | app |
| `provides` | (app-specific capabilities) |
| `requires` | service · identity · gateway |
| `surface` | gateway / UI |
| `governance` | per the user's delegated intent |
| `conformance` | caters to the **user lifecycle** |

## gateway

**Term** — a **surface** agent — exposes the agent web to a **touchpoint** (web /
mobile / voice / …); translates between the web and the touchpoint.

| Contract | Value |
|---|---|
| `type` | gateway |
| `provides` | surface-native UI · protocol translation (every protocol) |
| `requires` | app · service |
| `surface` | the touchpoint (surface-native) |
| `governance` | per-touchpoint; consistent experience |
| `conformance` | **surface-native, not generic** |
