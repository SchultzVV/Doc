"""Agente de precificação: Black-Scholes fechado + Monte Carlo.

O Monte Carlo aqui também serve de gancho experimental: amostragem é uma das
classes de problema com candidatos quânticos (amplitude estimation promete
ganho quadrático sobre MC clássico — caso de estudo possível na Etapa 2).
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from scipy.stats import norm

from qmas.agents.base import Agent
from qmas.core.contracts import TaskKind


def black_scholes_call(s: float, k: float, t: float, r: float, sigma: float) -> float:
    d1 = (math.log(s / k) + (r + sigma**2 / 2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    return s * norm.cdf(d1) - k * math.exp(-r * t) * norm.cdf(d2)


def monte_carlo_call(
    s: float, k: float, t: float, r: float, sigma: float,
    n_paths: int = 100_000, rng: np.random.Generator | None = None,
) -> tuple[float, float]:
    """Retorna (preço, erro-padrão)."""
    rng = rng or np.random.default_rng()
    z = rng.standard_normal(n_paths)
    st = s * np.exp((r - sigma**2 / 2) * t + sigma * math.sqrt(t) * z)
    payoff = np.maximum(st - k, 0.0) * math.exp(-r * t)
    return float(payoff.mean()), float(payoff.std(ddof=1) / math.sqrt(n_paths))


class PricerAgent(Agent):
    name = "pricer"
    handles = (TaskKind.PRICE,)

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        p = {k: float(payload[k]) for k in ("spot", "strike", "maturity", "rate", "vol")}
        bs = black_scholes_call(p["spot"], p["strike"], p["maturity"], p["rate"], p["vol"])
        mc, se = monte_carlo_call(p["spot"], p["strike"], p["maturity"], p["rate"], p["vol"])
        return {"black_scholes": bs, "monte_carlo": mc, "mc_std_error": se}
