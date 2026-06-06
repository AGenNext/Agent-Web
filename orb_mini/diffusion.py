"""Denoising-diffusion pretraining.

A central finding of Orb (Neumann et al. 2024) is that *diffusion pretraining*
on ground-state structures gives large, universal accuracy gains (reported
improvements of 17-70%) before the model is fine-tuned as a potential.

The recipe (Section: "Diffusion pretraining"):

1. Take a ground-state (equilibrium) structure with positions x0.
2. Forward process: add Gaussian noise, x_t = x0 + sigma_t * eps, where the
   noise scale sigma_t grows with the diffusion time t and eps ~ N(0, I).
3. Train the network to denoise - here we predict the noise eps from the noisy
   structure (an equivalent parameterisation of the score / x0 target).

The denoiser reuses the *same* Encoder+Processor backbone as the potential, with
a per-atom 3-vector output head. After pretraining, the backbone weights are
transferred to ``OrbPotential`` and fine-tuned on energies/forces/stresses.
"""
from __future__ import annotations

import torch
import torch.nn as nn

from .graph import AtomGraph, build_radius_graph
from .model import Backbone, mlp


class DiffusionDenoiser(nn.Module):
    """Backbone + a per-atom 3-vector head that predicts the displacement back
    to the clean structure (the "x0-prediction" parameterisation).

    We predict ``x0 - x_t`` (the vector from each noisy atom toward where it
    should sit) rather than the raw noise ``eps``. Because we do not feed the
    noise level to the network, predicting ``eps`` would be ill-posed (the scale
    is unknown from a single snapshot), whereas the displacement to the clean
    manifold is well-defined. Production diffusion models instead condition the
    network on the diffusion time, which makes eps-prediction well-posed too.
    """

    def __init__(self, hidden: int = 128, num_layers: int = 3, num_rbf: int = 16, cutoff: float = 5.0):
        super().__init__()
        self.cutoff = cutoff
        self.backbone = Backbone(hidden, num_layers, num_rbf, cutoff)
        self.denoise_head = mlp(hidden, hidden, 3)

    def forward(self, graph: AtomGraph) -> torch.Tensor:
        h_nodes = self.backbone(graph)
        return self.denoise_head(h_nodes)  # predicted (x0 - x_t), (N, 3)


def sigma_schedule(t: torch.Tensor, sigma_min: float = 0.01, sigma_max: float = 0.5) -> torch.Tensor:
    """Log-linear noise schedule: sigma grows geometrically with time t in [0, 1]."""
    log_min, log_max = torch.log(torch.tensor(sigma_min)), torch.log(torch.tensor(sigma_max))
    return torch.exp(log_min + t * (log_max - log_min))


def diffusion_loss(
    denoiser: DiffusionDenoiser,
    atomic_numbers: torch.Tensor,
    positions: torch.Tensor,
    batch: torch.Tensor,
    num_graphs: int,
) -> torch.Tensor:
    """One denoising-diffusion training step loss (MSE, x0-prediction).

    A separate diffusion time is sampled per *system*; all atoms in a system
    share that time/noise scale, as in standard structure-diffusion setups. The
    target is the displacement ``x0 - x_t`` back toward the clean structure.
    """
    device = positions.device
    t = torch.rand(num_graphs, device=device)  # (G,)
    sigma = sigma_schedule(t)  # (G,)
    sigma_per_atom = sigma[batch].unsqueeze(-1)  # (N, 1)

    eps = torch.randn_like(positions)
    noisy_positions = positions + sigma_per_atom * eps
    target = positions - noisy_positions  # = -sigma * eps, points back to x0

    # Rebuild the graph on the noisy coordinates (connectivity follows geometry).
    noisy_graph = build_radius_graph(
        atomic_numbers, noisy_positions, cutoff=denoiser.cutoff, batch=batch
    )
    pred = denoiser(noisy_graph)
    return nn.functional.mse_loss(pred, target)
