"""Camada 4 — Coordenação multiagente.

Pergunta de pesquisa: algoritmos quânticos ajudam a coordenação entre
agentes (consenso, alocação de recursos, negociação, roteamento)?

NOTA DE ESCOPO: o experimento de alocação de tarefas (GAP -> QUBO -> QAOA)
implementado aqui é UM caso particular desta camada — não a hipótese
principal da tese. Ele existe porque foi o primeiro componente formalizado,
não porque a revisão bibliográfica já o tenha apontado como o mais promissor.
"""

from __future__ import annotations

from typing import Any

from qmas.core.component import (
    ComponentUnderStudy, Implementation, Layer, Paradigm, RunOutput,
)
from qmas.coordination.base import TimedSolver
from qmas.coordination.instances import random_allocation_instance
from qmas.coordination.problems.allocation import AllocationProblem


class _SolverAdapter:
    """Adapta um solver (interface antiga) ao contrato Implementation."""

    def __init__(self, solver: TimedSolver, paradigm: Paradigm) -> None:
        self._solver = solver
        self.name = solver.name
        self.paradigm = paradigm

    def run(self, instance: AllocationProblem) -> RunOutput:
        assignment = self._solver.solve(instance)  # type: ignore[attr-defined]
        return RunOutput(
            value=assignment,
            # menor custo = melhor; harness maximiza, então invertemos o sinal
            quality=-assignment.objective_value if assignment.feasible else None,
            feasible=assignment.feasible,
        )


def task_allocation_component(with_quantum: bool = True) -> ComponentUnderStudy:
    """Factory do componente 'alocação de tarefas' (experimento 001)."""
    from qmas.coordination.classical.solvers import (
        CpSatSolver, GreedySolver, SimulatedAnnealingSolver,
    )

    implementations: list[Implementation] = [
        _SolverAdapter(GreedySolver(), Paradigm.CLASSICAL),
        _SolverAdapter(SimulatedAnnealingSolver(), Paradigm.CLASSICAL),
    ]
    if with_quantum:
        from qmas.coordination.quantum.solvers import QAOASolver
        implementations.append(_SolverAdapter(QAOASolver(), Paradigm.QUANTUM))

    return ComponentUnderStudy(
        layer=Layer.COORDINATION,
        name="task_allocation",
        question=(
            "A alocação de tarefas a agentes (GAP) apresenta vantagem mensurável "
            "quando resolvida por QAOA/annealing versus os melhores baselines clássicos?"
        ),
        instance_generator=random_allocation_instance,
        implementations=implementations,
        reference=_SolverAdapter(CpSatSolver(time_limit_s=300), Paradigm.CLASSICAL),
    )
