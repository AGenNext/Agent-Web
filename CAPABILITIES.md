# Capability catalog (working draft)

> **Home: this repo (`agent-web`).** Agent-Web is the home of the agent-language /
> capability vocabulary. The platform curates the canonical list **here, in the open.**

**Principle: every action is a capability** — a **common English verb** on a
resource, **namespaced** (`namespace:verb`) so its meaning is canonical (the
agent-language). Built by **pinging sources and picking concepts** — reuse
existing open command sets, don't invent. Capabilities are **scopable**
(`git:*`, `docker:build` on `resource:X`) and granted as **signed
[W3C VC 2.0](https://www.w3.org/TR/vc-data-model-2.0/)** credentials.

## Namespaces (picked from sources)

### `schema:` — human-world actions · *source: schema.org/Action*
Read · View · Watch · Listen · Use · Install · Play · Write · Draw · Paint ·
Photograph · Film · Cook · Activate · Deactivate · Suspend · Resume · Ask · Inform ·
Reply · Comment · Share · Invite · Register · Subscribe · Follow · Join · Leave ·
Arrive · Depart · Travel · Accept · Assign · Authorize · Reject · Apply · Bookmark ·
Cancel · Reserve · Schedule · Buy · Sell · Order · Pay · Quote · Rent · Donate ·
Tip · Send · Receive · Give · Take · Borrow · Lend · Return · Download · Search ·
Check · Discover · Track · Choose · Review · React · Ignore · Add · Delete ·
Replace · Win · Lose · Tie

### `git:` — version control · *source: git / GitHub*
clone · fork · init · branch · checkout · add · commit · push · pull · fetch ·
merge · rebase · tag · stash · reset · revert · cherry-pick · release · issue ·
pull-request · review · approve · request-changes · comment · label · assign ·
milestone · star · watch

### `docker:` — containers · *source: Docker / OCI*
build · run · pull · push · tag · exec · create · start · stop · restart · kill ·
rm · logs · inspect · commit · save · load · compose · prune · scan

### `k8s:` — orchestration · *source: kubectl / Kubernetes*
apply · create · get · describe · delete · edit · scale · rollout · rollback ·
drain · cordon · uncordon · label · annotate · expose · port-forward · logs · exec

### `http:` — web · *source: HTTP / REST*
get · post · put · patch · delete · head · options

### `data:` — storage · *source: SQL / CRUD*
query · select · insert · update · delete · upsert · index · join · aggregate ·
backup · restore · migrate

### `fs:` — files · *source: POSIX / filesystem*
read · write · append · list · stat · move · copy · delete · mkdir · chmod · link

### `content:` — creation · *source: content tooling*
write · draft · edit · revise · generate · summarize · translate · format ·
render · annotate · proofread · publish · template

### `security:` — defense · *source: security tooling*
scan · protect · shield · guard · detect · defend · isolate · quarantine ·
encrypt · decrypt · sign · verify · attest · monitor · patch · harden · sandbox ·
audit · revoke · block · allow · deny

### `machine:` — info exchange · *source: agent / RPC protocols*
query · request · respond · return · command · invoke · acknowledge · subscribe ·
stream · notify · authenticate · authorize · verify · negotiate · delegate ·
audit · log · ping · heartbeat

## A capability, granted

A capability is a **signed W3C VC 2.0** credential:

```
subject (DID)  may  {namespace:verb}  on  {resource}  under  {caveats}
```

issued and signed by the platform/issuer DID — **scopable, expiring, auditable,
unforgeable.**

## Growing the catalog

Built by **pinging sources and picking concepts.** Each new source = a new
namespace (cite the source). Sources still to pick from: `cloud:` (AWS/GCP/Azure
verbs), `ml:` (train/infer/finetune/evaluate), `comm:` (email/chat/call),
`finance:` (transfer/invoice/reconcile), `iot:` (sense/actuate/calibrate), `os:`
(spawn/signal/schedule). The canonical, governed list lives **here, in
`agent-web`** — curated in the open.
