"""Radial basis functions and smooth cutoff envelopes.

Orb represents each directed edge by a *normalised displacement vector* and a
Gaussian Radial Basis Function (RBF) expansion of the interatomic distance
(see Orb, Neumann et al. 2024, arXiv:2410.22570). This module implements both
the RBF and a smooth cosine cutoff used to make message passing decay smoothly
to zero at the cutoff radius.
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn


class GaussianRBF(nn.Module):
    """Gaussian radial basis expansion of a scalar distance.

    phi_k(d) = exp(-gamma * (d - mu_k)^2), with ``num_rbf`` centres ``mu_k``
    spread evenly over ``[0, cutoff]``. The centres are learnable, matching the
    flexibility used in modern message-passing potentials.
    """

    def __init__(self, num_rbf: int = 16, cutoff: float = 5.0):
        super().__init__()
        self.num_rbf = num_rbf
        self.cutoff = cutoff
        centres = torch.linspace(0.0, cutoff, num_rbf)
        # Width chosen so neighbouring Gaussians overlap sensibly.
        gamma = (num_rbf / cutoff) ** 2
        self.centres = nn.Parameter(centres)
        self.register_buffer("gamma", torch.tensor(float(gamma)))

    def forward(self, dist: torch.Tensor) -> torch.Tensor:
        # dist: (E,) -> (E, num_rbf)
        diff = dist.unsqueeze(-1) - self.centres.unsqueeze(0)
        return torch.exp(-self.gamma * diff * diff)


def cosine_cutoff(dist: torch.Tensor, cutoff: float) -> torch.Tensor:
    """Smooth cosine cutoff envelope in ``[0, 1]``.

    phi(d) = 0.5 * (cos(pi * d / cutoff) + 1) for d < cutoff, else 0. This is the
    "distance-based cutoff function" that Orb multiplies into its smoothed graph
    attention so that the influence of an edge decays smoothly to zero.
    """
    env = 0.5 * (torch.cos(math.pi * dist / cutoff) + 1.0)
    return torch.where(dist < cutoff, env, torch.zeros_like(env))
