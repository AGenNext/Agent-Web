"""Synthetic atomic data for demos and tests.

Real Orb is trained on DFT datasets (MPtraj + Alexandria, both PBE/VASP). To
keep this repository self-contained and CPU-friendly, we generate small
crystalline clusters (a simple-cubic lattice near the Lennard-Jones equilibrium
spacing, with thermal jitter) and label them with a classical **Lennard-Jones**
potential, whose energy and forces are available in closed form.

Using *lattice* structures rather than uniformly-random points matters for two
reasons that mirror the real setting:

* The structures lie on a low-dimensional manifold, so **denoising-diffusion
  pretraining has signal** - the model can learn to push noisy atoms back toward
  lattice sites (random points have no such manifold).
* Atoms start near the LJ energy minimum, so energies are well-behaved instead
  of being dominated by near-singular overlaps.
"""
from __future__ import annotations

import itertools

import torch

from .graph import AtomGraph, build_radius_graph

# Lennard-Jones equilibrium pair distance r_min = 2^(1/6) * sigma.

# Lennard-Jones parameters (arbitrary units, roughly argon-like in Angstrom).
LJ_EPSILON = 1.0
LJ_SIGMA = 3.0


def lennard_jones_energy(positions: torch.Tensor) -> torch.Tensor:
    """Total Lennard-Jones energy of a cluster.

    energy = sum_{i<j} 4 eps [ (s/r)^12 - (s/r)^6 ]

    Distances are clamped to a soft minimum to avoid the r->0 singularity for
    randomly generated clusters; this clamp is part of the function, so forces
    obtained by differentiating it stay exactly consistent with it.
    """
    n = positions.shape[0]
    delta = positions.unsqueeze(1) - positions.unsqueeze(0)  # (N, N, 3): i - j
    r = delta.norm(dim=-1)  # (N, N)
    eye = torch.eye(n, dtype=torch.bool, device=positions.device)
    # Off-diagonal distances only, with a soft core to stay numerically sane.
    r = r.masked_fill(eye, 1.0).clamp_min(0.8 * LJ_SIGMA)

    sr6 = (LJ_SIGMA / r) ** 6
    sr12 = sr6 * sr6
    pair_energy = (4 * LJ_EPSILON * (sr12 - sr6)).masked_fill(eye, 0.0)
    return 0.5 * pair_energy.sum()


def lennard_jones(positions: torch.Tensor):
    """Return (energy, forces) where forces = -dE/dx via autograd.

    Using autograd guarantees the labels are physically self-consistent (forces
    are exactly the negative gradient of the energy), which is what a conservative
    reference would provide.
    """
    pos = positions.detach().clone().requires_grad_(True)
    energy = lennard_jones_energy(pos)
    (grad,) = torch.autograd.grad(energy, pos)
    return energy.detach(), -grad.detach()


LJ_RMIN = 2.0 ** (1.0 / 6.0) * LJ_SIGMA  # ~3.37


def lattice_cluster(
    n_side: int = 2,
    spacing: float = LJ_RMIN,
    jitter: float = 0.2,
    atomic_number: int = 18,
    device=None,
):
    """A simple-cubic cluster of ``n_side**3`` atoms with Gaussian jitter.

    ``jitter`` is the standard deviation (Angstrom) of random displacements from
    the ideal lattice sites - the analogue of thermal motion around equilibrium.
    """
    grid = [
        torch.tensor(c, dtype=torch.float32, device=device) * spacing
        for c in itertools.product(range(n_side), repeat=3)
    ]
    positions = torch.stack(grid)
    positions = positions + jitter * torch.randn_like(positions)
    atomic_numbers = torch.full((positions.shape[0],), atomic_number, dtype=torch.long, device=device)
    return atomic_numbers, positions


def make_batch(
    num_systems: int,
    atoms_per_system: int = 8,
    cutoff: float = 5.0,
    jitter: float = 0.2,
    device=None,
):
    """Build a batched graph plus per-system LJ energy and per-atom force labels.

    ``atoms_per_system`` must be a perfect cube (e.g. 8 = 2^3, 27 = 3^3); it sets
    the simple-cubic lattice size.
    """
    n_side = round(atoms_per_system ** (1.0 / 3.0))
    if n_side ** 3 != atoms_per_system:
        raise ValueError("atoms_per_system must be a perfect cube (e.g. 8, 27, 64)")

    all_z, all_pos, all_batch = [], [], []
    energies, forces = [], []
    for g in range(num_systems):
        z, pos = lattice_cluster(n_side=n_side, jitter=jitter, device=device)
        e, f = lennard_jones(pos)
        all_z.append(z)
        all_pos.append(pos)
        all_batch.append(torch.full((pos.shape[0],), g, dtype=torch.long, device=device))
        energies.append(e)
        forces.append(f)

    atomic_numbers = torch.cat(all_z)
    positions = torch.cat(all_pos)
    batch = torch.cat(all_batch)
    graph = build_radius_graph(atomic_numbers, positions, cutoff=cutoff, batch=batch)
    targets = {
        "energy": torch.stack(energies),  # (G,)
        "forces": torch.cat(forces),       # (N, 3)
    }
    return graph, targets
