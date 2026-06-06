"""Two-stage training, mirroring Orb's recipe.

Stage 1 - **Diffusion pretraining**: train the backbone to denoise corrupted
           ground-state structures.
Stage 2 - **Supervised fine-tuning**: transfer the pretrained backbone into an
           ``OrbPotential`` and train it on energies, forces and stresses with a
           weighted multi-task loss.

Run as a script for a quick end-to-end demonstration, or import the functions.
"""
from __future__ import annotations

import torch

from .data import make_batch
from .diffusion import DiffusionDenoiser, diffusion_loss
from .model import OrbPotential


def pretrain_diffusion(
    hidden: int = 64,
    num_layers: int = 3,
    cutoff: float = 5.0,
    steps: int = 200,
    systems_per_batch: int = 16,
    atoms_per_system: int = 8,
    jitter: float = 0.05,
    lr: float = 1e-3,
    device=None,
    log_every: int = 50,
) -> DiffusionDenoiser:
    # Near-perfect lattices act as "ground-state" structures: a crisp manifold
    # for the denoiser to learn to push noisy atoms back toward.
    denoiser = DiffusionDenoiser(hidden=hidden, num_layers=num_layers, cutoff=cutoff).to(device)
    opt = torch.optim.Adam(denoiser.parameters(), lr=lr)
    for step in range(steps):
        graph, _ = make_batch(
            systems_per_batch, atoms_per_system, cutoff=cutoff, jitter=jitter, device=device
        )
        loss = diffusion_loss(
            denoiser, graph.atomic_numbers, graph.positions, graph.batch, graph.num_graphs
        )
        opt.zero_grad()
        loss.backward()
        opt.step()
        if log_every and (step % log_every == 0 or step == steps - 1):
            print(f"[pretrain] step {step:4d}  denoise_mse={loss.item():.4f}")
    return denoiser


def finetune_potential(
    pretrained: DiffusionDenoiser | None = None,
    hidden: int = 64,
    num_layers: int = 3,
    cutoff: float = 5.0,
    steps: int = 300,
    systems_per_batch: int = 16,
    atoms_per_system: int = 8,
    lr: float = 1e-3,
    force_weight: float = 1.0,
    device=None,
    log_every: int = 50,
) -> OrbPotential:
    model = OrbPotential(hidden=hidden, num_layers=num_layers, cutoff=cutoff).to(device)
    if pretrained is not None:
        model.load_backbone(pretrained.backbone.state_dict())
        print("[finetune] initialised backbone from diffusion-pretrained weights")

    opt = torch.optim.Adam(model.parameters(), lr=lr)
    for step in range(steps):
        graph, targets = make_batch(systems_per_batch, atoms_per_system, cutoff=cutoff, device=device)
        pred = model(graph)
        energy_loss = torch.nn.functional.mse_loss(pred["energy"], targets["energy"])
        force_loss = torch.nn.functional.mse_loss(pred["forces"], targets["forces"])
        loss = energy_loss + force_weight * force_loss
        opt.zero_grad()
        loss.backward()
        opt.step()
        if log_every and (step % log_every == 0 or step == steps - 1):
            print(
                f"[finetune] step {step:4d}  E_mse={energy_loss.item():.4f}  "
                f"F_mse={force_loss.item():.4f}"
            )
    return model


def main():
    torch.manual_seed(0)
    device = torch.device("cpu")
    print("=== Stage 1: diffusion pretraining ===")
    denoiser = pretrain_diffusion(steps=200, device=device)
    print("\n=== Stage 2: supervised fine-tuning (with pretraining) ===")
    finetune_potential(pretrained=denoiser, steps=300, device=device)


if __name__ == "__main__":
    main()
