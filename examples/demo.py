"""End-to-end demo of mini-Orb.

Runs quickly on CPU:
1. A forward pass producing energy, forces and stress.
2. A rotation-invariance check (energy should be ~unchanged under rotation).
3. Diffusion pretraining, then supervised fine-tuning, showing that
   pretraining lowers the starting/converged error vs training from scratch.
"""
from __future__ import annotations

import os
import sys

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orb_mini import OrbPotential, build_radius_graph
from orb_mini.data import make_batch
from orb_mini.train import finetune_potential, pretrain_diffusion


def random_rotation() -> torch.Tensor:
    q, _ = torch.linalg.qr(torch.randn(3, 3))
    if torch.det(q) < 0:
        q[:, 0] = -q[:, 0]
    return q


def main():
    torch.manual_seed(0)
    device = torch.device("cpu")

    print("=== 1. Forward pass ===")
    model = OrbPotential(hidden=64, num_layers=3)
    graph, targets = make_batch(num_systems=2, atoms_per_system=8)
    out = model(graph)
    print(f"energy shape : {tuple(out['energy'].shape)}  -> {out['energy'].detach().numpy()}")
    print(f"forces shape : {tuple(out['forces'].shape)}")
    print(f"stress shape : {tuple(out['stress'].shape)}")

    print("\n=== 2. Rotation behaviour (learned, not enforced) ===")
    R = random_rotation()
    rotated = build_radius_graph(graph.atomic_numbers, graph.positions @ R.T, batch=graph.batch)
    out_rot = model(rotated)
    diff = (out["energy"] - out_rot["energy"]).abs().max().item()
    print(f"max |E(x) - E(Rx)| on an untrained net = {diff:.2e}  (small but nonzero)")
    print("(Orb is non-equivariant: there is NO exact rotational invariance by")
    print(" construction; approximate invariance is learned from data in training.)")

    print("\n=== 3. Pretrain + fine-tune ===")
    denoiser = pretrain_diffusion(hidden=64, steps=150, device=device)
    print()
    finetune_potential(pretrained=denoiser, hidden=64, steps=200, device=device)


if __name__ == "__main__":
    main()
