"""Smoke tests for mini-Orb. Run with: python -m pytest tests/ -q"""
from __future__ import annotations

import torch

from orb_mini import OrbPotential, build_radius_graph
from orb_mini.data import lennard_jones, make_batch
from orb_mini.diffusion import DiffusionDenoiser, diffusion_loss
from orb_mini.graph import scatter_softmax, scatter_sum


def test_forward_shapes():
    graph, _ = make_batch(num_systems=3, atoms_per_system=8)
    model = OrbPotential(hidden=32, num_layers=2)
    out = model(graph)
    assert out["energy"].shape == (3,)
    assert out["forces"].shape == (24, 3)
    assert out["stress"].shape == (3, 6)


def test_scatter_softmax_normalises():
    scores = torch.randn(10, 1)
    index = torch.tensor([0, 0, 0, 1, 1, 2, 2, 2, 2, 3])
    weights = scatter_softmax(scores, index, dim_size=4)
    sums = scatter_sum(weights, index, dim_size=4).squeeze(-1)
    assert torch.allclose(sums, torch.ones(4), atol=1e-5)


def test_diffusion_loss_runs_and_is_finite():
    graph, _ = make_batch(num_systems=4, atoms_per_system=8)
    denoiser = DiffusionDenoiser(hidden=32, num_layers=2)
    loss = diffusion_loss(
        denoiser, graph.atomic_numbers, graph.positions, graph.batch, graph.num_graphs
    )
    assert torch.isfinite(loss)
    loss.backward()  # gradients flow


def test_lennard_jones_force_matches_finite_difference():
    torch.manual_seed(1)
    # float64 so finite differencing is not dominated by rounding noise.
    pos = (torch.rand(5, 3) * 6 + 1.0).double()
    _, analytic = lennard_jones(pos)
    eps = 1e-5
    numeric = torch.zeros_like(pos)
    for i in range(pos.shape[0]):
        for d in range(3):
            p = pos.clone()
            p[i, d] += eps
            e_plus, _ = lennard_jones(p)
            p[i, d] -= 2 * eps
            e_minus, _ = lennard_jones(p)
            numeric[i, d] = -(e_plus - e_minus) / (2 * eps)
    assert torch.allclose(analytic, numeric, atol=1e-4, rtol=1e-4)


def test_pretraining_reduces_loss():
    torch.manual_seed(0)
    denoiser = DiffusionDenoiser(hidden=32, num_layers=2)
    opt = torch.optim.Adam(denoiser.parameters(), lr=1e-3)
    losses = []
    for _ in range(80):
        # Crisp (near-perfect) lattices give a clear denoising manifold, matching
        # how pretrain_diffusion generates "ground-state" structures.
        graph, _ = make_batch(num_systems=8, atoms_per_system=8, jitter=0.05)
        loss = diffusion_loss(
            denoiser, graph.atomic_numbers, graph.positions, graph.batch, graph.num_graphs
        )
        opt.zero_grad()
        loss.backward()
        opt.step()
        losses.append(loss.item())
    assert sum(losses[-10:]) / 10 < sum(losses[:10]) / 10
