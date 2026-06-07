> **This repository contains two independent projects:**
> 1. **`orb_mini/`** — a reference implementation of the Orb neural network potential (below).
> 2. **`autonomyx/`** — a zero-trust kernel for a canonical agent OS. See [the autonomyx section](#autonomyx--a-zero-trust-kernel-for-a-canonical-agent-os).

# mini-Orb

A compact, **runnable** reference implementation of the core ideas in:

> **Orb: A Fast, Scalable Neural Network Potential**
> Mark Neumann, James Gin, Benjamin Rhodes, Steven Bennett, Zhiyi Li,
> Hitarth Choubisa, Arthur Hussey, Jonathan Godwin (Orbital Materials), Oct 2024.
> arXiv: [2410.22570](https://arxiv.org/abs/2410.22570) ·
> HF: [hf.co/papers/2410.22570](https://huggingface.co/papers/2410.22570)

This repo is **two things in one**:

1. A **deep-dive summary** of the paper (below).
2. A small **PyTorch implementation** (`orb_mini/`) of the model's key
   components — an attention-augmented Graph Network Simulator with
   denoising-diffusion pretraining — that trains end-to-end on CPU against a
   synthetic Lennard-Jones reference. It is an *educational* reimplementation,
   **not** a reproduction of the released Orb weights or benchmark numbers.

> ⚠️ **Naming note.** This "Orb" is Orbital Materials' *interatomic potential*
> for materials simulation. It is **unrelated** to the **World ID "Orb"**
> (the iris-scanning biometric device from Tools for Humanity / Worldcoin).
> Same word, completely different projects.

---

## 1. The paper, in depth

### What problem it solves
A **universal interatomic potential** is an ML model that, given the elements
and 3D positions of atoms, predicts the system's **energy**, the **forces** on
each atom, and the **stress** on the cell — fast enough to drive molecular
dynamics (MD), Monte Carlo (MC), and geometry/cell optimization. These replace
quantum-mechanical DFT calculations (accurate but very expensive) with a learned
surrogate.

### Headline results
- **3–6× faster** than other universal potentials at the time of release.
- **31% lower error** on the **Matbench Discovery** benchmark vs prior methods.
- **Stable** in MD/MC simulations across a range of out-of-distribution
  materials.
- **Diffusion pretraining** gives broad accuracy gains of **17–70%**.

### Architectural choice: learn invariances, don't enforce them
Most leading potentials (e.g. MACE, NequIP) are **E(3)-equivariant** — rotational
symmetry is baked into the network with spherical harmonics / tensor products.
That is data-efficient but computationally heavy.

Orb takes the opposite bet: a **non-equivariant** **Graph Network-based
Simulator (GNS)** — a Message Passing Neural Network (MPNN) — that **learns**
the relevant invariances from large data. Removing the equivariance machinery is
a big part of why it's fast and scalable.

### The model
- **Graph construction.** Atoms are nodes; edges connect atoms within a
  **cutoff radius**. Nodes carry a learned **embedding of atomic number**.
  Directed edges carry the **normalized displacement vector** plus a
  **Gaussian RBF** expansion of the interatomic distance.
- **Backbone (processor).** A stack of message-passing blocks augmented with
  **smoothed graph attention**: messages between atoms are weighted by attention
  scores **multiplied by a smooth distance-cutoff envelope**, so an edge's
  influence decays smoothly to zero at the cutoff. Node and edge features are
  updated with residual MLPs.
- **Heads.** Energy is a **sum of per-atom energies**; **forces** and
  **stress** are predicted by **direct heads** (read out from node/graph
  features) rather than as gradients of the energy. Direct (non-conservative)
  force prediction is another speed lever. (Trade-off: energy and forces are
  not guaranteed to be exactly consistent — a point later Orb versions and other
  works revisit.)

### Diffusion pretraining (the key idea)
Orb is trained in **two stages**:

1. **Denoising-diffusion pretraining** on **ground-state (equilibrium)
   structures**. A forward process adds Gaussian noise to atomic positions with
   a scale that grows over diffusion time; the network learns to **denoise** —
   undo the corruption. Because equilibrium structures lie on a
   low-dimensional manifold, this teaches a strong, physically-meaningful
   representation of atomic geometry *without needing energy/force labels*.
2. **Supervised fine-tuning** as a potential: the pretrained backbone
   initializes the energy/force/stress model, trained on labeled data.

Pretraining helped **universally (17–70%)**, even on the large Alexandria
dataset.

### Training data
Orb combines **MPtraj** (Materials Project trajectories, the dataset used to
train CHGNet) with **Alexandria** — chosen because both use **PBE**
exchange-correlation functionals and **VASP** for relaxations, so the labels are
consistent. Alexandria is ~an order of magnitude larger than MPtraj.

### Evaluation
Beyond Matbench Discovery (formation-energy / stability prediction), Orb is
assessed as a practical simulator: **geometry optimization**, **Monte Carlo**,
and **molecular-dynamics stability** on out-of-distribution materials.

### Takeaways
- A **scalable, non-equivariant** GNN can beat equivariant models on
  speed *and* accuracy when paired with enough data and the right pretraining.
- **Self-supervised diffusion pretraining** on structures is a broadly useful
  recipe for materials foundation models.
- **Direct** energy/force/stress prediction trades exact energy-conservation for
  speed.

---

## 2. The implementation

### Layout
```
orb_mini/
  rbf.py         Gaussian radial basis + smooth cosine cutoff envelope
  graph.py       radius-graph construction + scatter/segment ops
  model.py       Encoder, attention-GNS layer, Backbone, OrbPotential heads
  diffusion.py   denoising-diffusion pretraining objective (x0-prediction)
  data.py        synthetic Lennard-Jones lattice data (energy + forces)
  train.py       two-stage training: pretrain -> fine-tune
examples/demo.py end-to-end demo (forward pass, rotation check, train)
tests/           pytest smoke tests
```

### How it maps to the paper
| Paper concept | Where |
|---|---|
| Atom-type embedding + RBF/unit-vector edge features | `model.Encoder`, `rbf.GaussianRBF` |
| Smoothed graph attention (attention × distance cutoff) | `model.AttentionGNSLayer`, `rbf.cosine_cutoff` |
| GNS processor with residual node/edge updates | `model.AttentionGNSLayer`, `model.Backbone` |
| Direct energy (sum of per-atom) / force / stress heads | `model.OrbPotential` |
| Denoising-diffusion pretraining on ground states | `diffusion.py`, `train.pretrain_diffusion` |
| Backbone transfer to the potential | `OrbPotential.load_backbone` |

### Honest simplifications (vs real Orb)
- **Toy labels.** Trains against a classical **Lennard-Jones** reference on
  small lattice clusters, not DFT (MPtraj/Alexandria). The point is to exercise
  the *mechanics*, not reproduce accuracy.
- **No periodic boundary conditions** in the neighbor search (O(N²), fine for
  tiny systems).
- **x0-prediction** diffusion objective (predict displacement back to the clean
  structure) instead of time-conditioned ε-prediction — simpler and well-posed
  without feeding the noise level to the network. See `diffusion.py` for the
  rationale.
- Much smaller than the released models (a few layers, ~64-dim features).

### Quickstart
```bash
pip install -r requirements.txt        # torch (CPU is fine) + pytest

python examples/demo.py                 # forward pass + rotation check + training
python -m orb_mini.train                # just the two-stage training
python -m pytest tests/ -q              # smoke tests
```

Example demo output (abridged):
```
=== 1. Forward pass ===
energy shape : (2,)   forces shape : (16, 3)   stress shape : (2, 6)

=== 2. Rotation behaviour (learned, not enforced) ===
max |E(x) - E(Rx)| on an untrained net = 4.40e-06  (small but nonzero)

=== 3. Pretrain + fine-tune ===
[pretrain] step    0  denoise_mse=0.0729
[pretrain] step  149  denoise_mse=0.0685
[finetune] initialised backbone from diffusion-pretrained weights
[finetune] step    0  E_mse=161.27  F_mse=12.84
[finetune] step  199  E_mse=3.30    F_mse=16.18
```

---

## References
- Neumann et al., *Orb: A Fast, Scalable Neural Network Potential*, 2024 —
  [arXiv:2410.22570](https://arxiv.org/abs/2410.22570)
- Orbital Materials technical blog —
  [Introducing the Orb AI-based interatomic potential](https://www.orbitalindustries.com/posts/technical-blog-introducing-the-orb-ai-based-interatomic-potential)
- Batzner et al., *NequIP* (E(3)-equivariant baseline) —
  [arXiv:2101.03164](https://arxiv.org/abs/2101.03164)

---

# autonomyx — a zero-trust kernel for a canonical agent OS

`autonomyx/` is a minimal, runnable substrate for **agent-to-agent systems**
where trust is never assumed. It operationalizes the infrastructure that
Rothschild et al. (*Guiding the AI Disruption to the Good Place*, 2026) name as
the binding constraint on **Stage 3 "Reconstruction"**: trust & accountability,
machine-legible interoperability, and governance compiled into the workflow as
**auditable constraints** rather than bolted on afterward.

The design fuses **same-origin** trust with **zero-trust** enforcement by
redefining "origin" as *cryptographic lineage* rather than network location:
the only thing that confers trust is a provable chain back to the **canonical
core**, re-verified on every interaction.

### Native primitives
| Primitive | What it is | Module |
|---|---|---|
| **Identity** | An Ed25519 keypair; its fingerprint is the entity's origin id | `identity.py` |
| **Provenance** | Signed certificate chains proving same-origin lineage to the root | `provenance.py` |
| **Capability** | Unforgeable, scoped, caveated grants (object-capability authz) | `capability.py` |
| **Message** | The only interaction: a signed, addressed, tamper-evident envelope | `message.py` |
| **Agent** | identity + provenance chain + domain + handler | `agent.py` |
| **Kernel** | The canonical core: genesis root, registration, **default-deny** routing + audit | `kernel.py` |

### The one rule: `Kernel.route` is always-verify, default-deny
Every message passes the same gauntlet — (1) sender signature, (2) certificate
chain back to genesis, (3) recipient exists, (4) a capability authorizes
`(action, resource)` and its caveats hold — then is delivered and **audited**.
No step is skippable; there is no implicit trust from being "inside."

### Quickstart
```bash
pip install cryptography
python examples/agent_demo.py            # agent-to-agent market with an audit trail
python -m pytest tests/test_kernel.py -q  # 11 passing
```

Demo output (abridged):
```
quote    -> {'item': 'widget', 'unit_price': 4.2, ...}
purchase -> {'order': 'widget', 'qty': 3, 'total': 12.6, 'status': 'confirmed'}
second purchase     -> DENIED: capability ... exhausted (1 calls)
out-of-scope purchase -> DENIED: no capability authorizes purchase on gadget

--- audit log ---
  allow  quote    widget    authorized
  allow  purchase widget    authorized
  deny   purchase widget    capability ... exhausted (1 calls)
  deny   purchase gadget    capability does not cover action
```

### Scope & honest limits
A teaching-grade reference, not production: in-memory registry/audit (no
persistence), a single genesis root (no threshold/decentralized root or
revocation lists yet), no transport layer or replay-cache across processes, and
domains are recorded but cross-domain policy beyond capabilities is left open.
The primitives are the point; hardening is future work.

### References
- Rothschild, Hofman, Mobius, Lucier, et al., *Guiding the AI Disruption to the
  Good Place* (Microsoft Research), 2026 — [arXiv:2605.29207](https://arxiv.org/abs/2605.29207)
- Rothschild et al., *The Agentic Economy*, Communications of the ACM, 2026
