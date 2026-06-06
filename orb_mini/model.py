"""The mini-Orb model: an attention-augmented Graph Network Simulator (GNS).

This is a compact, readable reimplementation of the *core ideas* of Orb
(Neumann et al. 2024, arXiv:2410.22570). Orb deliberately uses a
non-equivariant Message Passing Neural Network (an attention-augmented GNS)
that *learns* invariances from data rather than baking in rotational
equivariance. The pieces here mirror that design:

* **Encoder** - embeds atomic number into node features and embeds each edge's
  (RBF(distance), unit displacement vector) into edge features.
* **Processor** - a stack of message-passing blocks with *smoothed graph
  attention*: messages are weighted by softmax attention multiplied by a smooth
  distance cutoff, then aggregated; node and edge features are updated with
  residual MLPs.
* **Decoder heads** - direct prediction of energy (sum of per-atom energies),
  per-atom forces, and per-system stress. Orb predicts forces *directly* (a
  non-conservative head) rather than as the gradient of the energy, which is a
  key part of why it is fast.

The same Encoder+Processor backbone is reused for diffusion pretraining (see
``diffusion.py``); only the head differs.
"""
from __future__ import annotations

import torch
import torch.nn as nn

from .graph import AtomGraph, scatter_mean, scatter_softmax, scatter_sum
from .rbf import GaussianRBF, cosine_cutoff

MAX_ATOMIC_NUMBER = 118


def mlp(in_dim: int, hidden: int, out_dim: int, layers: int = 2) -> nn.Sequential:
    """A small MLP with SiLU activations (no activation on the output)."""
    dims = [in_dim] + [hidden] * (layers - 1) + [out_dim]
    blocks: list[nn.Module] = []
    for i in range(len(dims) - 1):
        blocks.append(nn.Linear(dims[i], dims[i + 1]))
        if i < len(dims) - 2:
            blocks.append(nn.SiLU())
    return nn.Sequential(*blocks)


class Encoder(nn.Module):
    """Maps atoms and edges to initial latent features."""

    def __init__(self, hidden: int, num_rbf: int, cutoff: float):
        super().__init__()
        self.cutoff = cutoff
        self.atom_embedding = nn.Embedding(MAX_ATOMIC_NUMBER + 1, hidden)
        self.rbf = GaussianRBF(num_rbf, cutoff)
        # edge input = RBF(distance) concat unit displacement vector (3 dims)
        self.edge_mlp = mlp(num_rbf + 3, hidden, hidden)
        self.node_mlp = mlp(hidden, hidden, hidden)

    def forward(self, graph: AtomGraph):
        pos = graph.positions
        senders, receivers = graph.edge_index
        edge_vec = pos[receivers] - pos[senders]  # (E, 3)
        dist = edge_vec.norm(dim=-1).clamp_min(1e-8)  # (E,)
        unit_vec = edge_vec / dist.unsqueeze(-1)

        edge_feat = torch.cat([self.rbf(dist), unit_vec], dim=-1)
        h_edges = self.edge_mlp(edge_feat)
        h_nodes = self.node_mlp(self.atom_embedding(graph.atomic_numbers))
        envelope = cosine_cutoff(dist, self.cutoff).unsqueeze(-1)  # (E, 1)
        return h_nodes, h_edges, envelope


class AttentionGNSLayer(nn.Module):
    """One message-passing block with smoothed graph attention.

    For each directed edge (s -> r) a message is computed from the sender, the
    receiver and the edge features. Messages are weighted by ``attention *
    envelope`` (softmax over a node's incoming edges, times the smooth cutoff),
    summed per receiver, and used to residually update node features. Edge
    features are also residually updated, matching the GNS "full" update.
    """

    def __init__(self, hidden: int):
        super().__init__()
        self.message_mlp = mlp(3 * hidden, hidden, hidden)
        self.attention_score = nn.Linear(3 * hidden, 1)
        self.node_update = mlp(2 * hidden, hidden, hidden)
        self.edge_update = mlp(2 * hidden, hidden, hidden)

    def forward(self, h_nodes, h_edges, edge_index, envelope):
        senders, receivers = edge_index
        num_nodes = h_nodes.shape[0]

        msg_input = torch.cat([h_nodes[senders], h_nodes[receivers], h_edges], dim=-1)
        messages = self.message_mlp(msg_input)

        scores = self.attention_score(msg_input)  # (E, 1)
        attention = scatter_softmax(scores, receivers, num_nodes)
        weight = attention * envelope  # smoothed graph attention
        aggregated = scatter_sum(messages * weight, receivers, num_nodes)

        h_nodes = h_nodes + self.node_update(torch.cat([h_nodes, aggregated], dim=-1))
        h_edges = h_edges + self.edge_update(torch.cat([h_edges, messages], dim=-1))
        return h_nodes, h_edges


class Backbone(nn.Module):
    """Encoder + a stack of attention-GNS processor layers.

    Shared by both the potential (energy/forces/stress) and the diffusion
    pretraining model, so that pretrained weights transfer directly.
    """

    def __init__(self, hidden: int = 128, num_layers: int = 3, num_rbf: int = 16, cutoff: float = 5.0):
        super().__init__()
        self.encoder = Encoder(hidden, num_rbf, cutoff)
        self.layers = nn.ModuleList(AttentionGNSLayer(hidden) for _ in range(num_layers))

    def forward(self, graph: AtomGraph) -> torch.Tensor:
        h_nodes, h_edges, envelope = self.encoder(graph)
        for layer in self.layers:
            h_nodes, h_edges = layer(h_nodes, h_edges, graph.edge_index, envelope)
        return h_nodes


class OrbPotential(nn.Module):
    """Universal interatomic potential: direct energy, force and stress heads."""

    def __init__(self, hidden: int = 128, num_layers: int = 3, num_rbf: int = 16, cutoff: float = 5.0):
        super().__init__()
        self.backbone = Backbone(hidden, num_layers, num_rbf, cutoff)
        self.energy_head = mlp(hidden, hidden, 1)
        self.force_head = mlp(hidden, hidden, 3)
        self.stress_head = mlp(hidden, hidden, 6)  # Voigt notation

    def forward(self, graph: AtomGraph) -> dict[str, torch.Tensor]:
        h_nodes = self.backbone(graph)
        per_atom_energy = self.energy_head(h_nodes)  # (N, 1)
        energy = scatter_sum(per_atom_energy, graph.batch, graph.num_graphs).squeeze(-1)
        forces = self.force_head(h_nodes)  # (N, 3) direct, non-conservative
        pooled = scatter_mean(h_nodes, graph.batch, graph.num_graphs)
        stress = self.stress_head(pooled)  # (G, 6)
        return {"energy": energy, "forces": forces, "stress": stress}

    def load_backbone(self, state_dict: dict) -> None:
        """Initialise the backbone from a (diffusion-)pretrained checkpoint."""
        self.backbone.load_state_dict(state_dict)
