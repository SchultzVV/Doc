"""Baselines clássicos FORTES — requisito metodológico central (Rønnow et al., 2014).

Três níveis: exato (CP-SAT), guloso (piso) e simulated annealing (heurística
comparável em espírito ao quantum annealing).
"""

from __future__ import annotations

import numpy as np

from qmas.core.contracts import Assignment
from qmas.coordination.problems.allocation import AllocationProblem
from qmas.coordination.base import TimedSolver


class CpSatSolver(TimedSolver):
    """Exato via OR-Tools CP-SAT. Referência de qualidade (approx ratio = 1)."""

    name = "cpsat"

    def __init__(self, time_limit_s: float = 60.0) -> None:
        self.time_limit_s = time_limit_s

    def solve(self, problem: AllocationProblem) -> Assignment:
        from ortools.sat.python import cp_model

        nt, na = len(problem.tasks), len(problem.agents)
        model = cp_model.CpModel()
        x = {(t, a): model.new_bool_var(f"x_{t}_{a}")
             for t in range(nt) for a in range(na)
             if np.isfinite(problem.cost[t, a])}

        for t in range(nt):
            model.add_exactly_one(x[t, a] for a in range(na) if (t, a) in x)
        # TODO: restrição de capacidade quando cost virar consumo por par

        model.minimize(sum(int(problem.cost[t, a] * 100) * v for (t, a), v in x.items()))

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.time_limit_s
        status = solver.solve(model)
        feasible = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)

        mapping = {}
        if feasible:
            for (t, a), v in x.items():
                if solver.value(v):
                    mapping[problem.tasks[t].id] = problem.agents[a].name
        return Assignment(
            mapping=mapping,
            objective_value=solver.objective_value / 100 if feasible else float("inf"),
            feasible=feasible,
        )


class GreedySolver(TimedSolver):
    """Cada tarefa vai para o agente compatível mais barato. Piso de qualidade."""

    name = "greedy"

    def solve(self, problem: AllocationProblem) -> Assignment:
        mapping, total = {}, 0.0
        for t, task in enumerate(problem.tasks):
            a = int(np.argmin(problem.cost[t]))
            if not np.isfinite(problem.cost[t, a]):
                return Assignment(mapping={}, objective_value=float("inf"), feasible=False)
            mapping[task.id] = problem.agents[a].name
            total += problem.cost[t, a]
        return Assignment(mapping=mapping, objective_value=total, feasible=True)


class SimulatedAnnealingSolver(TimedSolver):
    """SA sobre o QUBO — mesmo espaço de busca que os solvers quânticos."""

    name = "sim_annealing"

    def __init__(self, n_sweeps: int = 1000, seed: int | None = None) -> None:
        self.n_sweeps = n_sweeps
        self.rng = np.random.default_rng(seed)

    def solve(self, problem: AllocationProblem) -> Assignment:
        qubo = problem.to_qubo()
        x = self.rng.integers(0, 2, size=qubo.n).astype(float)
        energy = qubo.energy(x)
        betas = np.geomspace(0.1, 10.0, self.n_sweeps)  # schedule geométrico

        for beta in betas:
            for i in self.rng.permutation(qubo.n):
                x[i] = 1 - x[i]
                new_e = qubo.energy(x)  # TODO: delta-energy O(n) em vez de O(n^2)
                if new_e < energy or self.rng.random() < np.exp(-beta * (new_e - energy)):
                    energy = new_e
                else:
                    x[i] = 1 - x[i]

        return _decode_qubo_solution(x, problem, energy)


def _decode_qubo_solution(
    x: np.ndarray, problem: AllocationProblem, energy: float
) -> Assignment:
    """Bitstring -> Assignment; infactível se alguma tarefa não tem agente único."""
    na = len(problem.agents)
    mapping = {}
    for t, task in enumerate(problem.tasks):
        chosen = [a for a in range(na) if x[t * na + a] > 0.5]
        if len(chosen) != 1 or not np.isfinite(problem.cost[t, chosen[0]]):
            return Assignment(mapping={}, objective_value=energy, feasible=False)
        mapping[task.id] = problem.agents[chosen[0]].name
    return Assignment(mapping=mapping, objective_value=energy, feasible=True)
