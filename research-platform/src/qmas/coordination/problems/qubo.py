"""Representação QUBO (Quadratic Unconstrained Binary Optimization).

min x^T Q x,  x em {0,1}^n — a lingua franca entre solvers clássicos
(simulated annealing), QAOA (via Ising) e D-Wave.
Referência das formulações: Lucas (2014), "Ising formulations of many NP problems".
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class QUBO:
    Q: np.ndarray                      # matriz (n x n), triangular superior
    var_names: list[str] = field(default_factory=list)
    offset: float = 0.0

    @property
    def n(self) -> int:
        return self.Q.shape[0]

    def energy(self, x: np.ndarray) -> float:
        return float(x @ self.Q @ x) + self.offset

    def to_ising(self) -> tuple[np.ndarray, np.ndarray, float]:
        """Converte para (h, J, offset) com spins s em {-1,+1}, x = (1+s)/2.

        Necessário para o QAOA (Hamiltoniano de custo em operadores Z).
        """
        Q = (self.Q + self.Q.T) / 2.0
        n = self.n
        J = Q / 4.0
        np.fill_diagonal(J, 0.0)
        h = Q.sum(axis=1) / 2.0 - np.diag(Q) / 4.0
        offset = self.offset + Q.sum() / 4.0 + np.trace(Q) / 4.0
        return h, J, offset
