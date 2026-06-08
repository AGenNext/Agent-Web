"""Graph construction and scatter utilities.

Orb represents an atomic system as a graph: nodes are atoms (embedded by atomic
number) and edges connect atoms within a cutoff radius. This module builds such
radius graphs (optionally batched) and provides the segment/scatter operations
used by the message-passing layers.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass
class AtomGraph:
    """A (possibly batched) atomic graph.

    Attributes:
        atomic_numbers: (N,) long tensor of element Z per atom.
        positions:      (N, 3) float tensor of Cartesian coordinates (Angstrom).
        edge_index:     (2, E) long tensor; row 0 = sender, row 1 = receiver.
        batch:          (N,) long tensor mapping each atom to its system index.
        num_graphs:     number of independent systems in the batch.
    """

    atomic_numbers: torch.Tensor
    positions: torch.Tensor
    edge_index: torch.Tensor
    batch: torch.Tensor
    num_graphs: int

    @property
    def num_nodes(self) -> int:
        return self.atomic_numbers.shape[0]


def build_radius_graph(
    atomic_numbers: torch.Tensor,
    positions: torch.Tensor,
    cutoff: float = 5.0,
    batch: torch.Tensor | None = None,
) -> AtomGraph:
    """Connect every pair of atoms within ``cutoff`` (no periodic images).

    Edges are only created between atoms belonging to the same system (per the
    ``batch`` vector). This is a plain O(N^2) construction which is fine for the
    small systems used in the demo; production potentials use neighbour lists.
    """
    n = atomic_numbers.shape[0]
    if batch is None:
        batch = torch.zeros(n, dtype=torch.long, device=positions.device)
    num_graphs = int(batch.max().item()) + 1 if n > 0 else 0

    # Pairwise distances.
    delta = positions.unsqueeze(0) - positions.unsqueeze(1)  # (N, N, 3)
    dist = delta.norm(dim=-1)  # (N, N)

    same_system = batch.unsqueeze(0) == batch.unsqueeze(1)
    not_self = ~torch.eye(n, dtype=torch.bool, device=positions.device)
    mask = (dist < cutoff) & same_system & not_self

    senders, receivers = mask.nonzero(as_tuple=True)
    edge_index = torch.stack([senders, receivers], dim=0)
    return AtomGraph(atomic_numbers, positions, edge_index, batch, num_graphs)


def scatter_sum(src: torch.Tensor, index: torch.Tensor, dim_size: int) -> torch.Tensor:
    """Sum ``src`` rows into ``dim_size`` buckets given by ``index``."""
    out = src.new_zeros((dim_size,) + src.shape[1:])
    idx = index.view((-1,) + (1,) * (src.dim() - 1)).expand_as(src)
    out.scatter_add_(0, idx, src)
    return out


def scatter_mean(src: torch.Tensor, index: torch.Tensor, dim_size: int) -> torch.Tensor:
    total = scatter_sum(src, index, dim_size)
    count = scatter_sum(torch.ones_like(src[:, :1]), index, dim_size).clamp_min(1.0)
    return total / count


def scatter_softmax(scores: torch.Tensor, index: torch.Tensor, dim_size: int) -> torch.Tensor:
    """Numerically-stable softmax over groups defined by ``index``.

    ``scores`` has shape (E, 1); the softmax is computed independently for each
    receiver node (the group), which is exactly the attention normalisation used
    in Orb's smoothed graph attention.
    """
    # Subtract per-group max for stability.
    max_per_group = src_max(scores, index, dim_size)
    scores = scores - max_per_group[index]
    exp = scores.exp()
    denom = scatter_sum(exp, index, dim_size)[index].clamp_min(1e-16)
    return exp / denom


def src_max(src: torch.Tensor, index: torch.Tensor, dim_size: int) -> torch.Tensor:
    """Per-group maximum (used only for softmax stabilisation)."""
    out = src.new_full((dim_size,) + src.shape[1:], float("-inf"))
    idx = index.view((-1,) + (1,) * (src.dim() - 1)).expand_as(src)
    out.scatter_reduce_(0, idx, src, reduce="amax", include_self=True)
    # Empty groups stay at -inf; replace with 0 so they don't propagate NaNs.
    out = torch.where(torch.isinf(out), torch.zeros_like(out), out)
    return out
