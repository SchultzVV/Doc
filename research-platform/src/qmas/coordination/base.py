"""Protocolo comum dos solvers — clássicos e quânticos são intercambiáveis.

Essa interface é o que permite ao Dispatcher trocar o backend sem que
o orquestrador saiba, e ao benchmark comparar todos com as mesmas métricas.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Protocol

from qmas.core.contracts import Assignment
from qmas.coordination.problems.allocation import AllocationProblem


@dataclass
class SolverResult:
    assignment: Assignment
    wall_time_s: float
    solver_name: str
    metadata: dict


class Solver(Protocol):
    name: str

    def solve(self, problem: AllocationProblem) -> Assignment: ...


class TimedSolver:
    """Mixin: mede time-to-solution (métrica primária da Etapa 3)."""

    name = "timed"

    def solve_timed(self, problem: AllocationProblem) -> SolverResult:
        t0 = time.perf_counter()
        assignment = self.solve(problem)  # type: ignore[attr-defined]
        return SolverResult(
            assignment=assignment,
            wall_time_s=time.perf_counter() - t0,
            solver_name=self.name,
            metadata={},
        )
