"""Geradores de instâncias sintéticas para a varredura de H3.

Instâncias reprodutíveis (seed) parametrizadas por tamanho e densidade —
os eixos das curvas de crossover clássico <-> quântico.
"""

from __future__ import annotations

import numpy as np

from qmas.core.contracts import AgentSpec, Task, TaskKind
from qmas.coordination.problems.allocation import AllocationProblem

_KINDS = [TaskKind.EXTRACT, TaskKind.FORECAST, TaskKind.PRICE]


def random_allocation_instance(
    n_tasks: int,
    n_agents: int,
    constraint_density: float = 0.6,
    seed: int = 0,
) -> AllocationProblem:
    """Gera um GAP aleatório.

    constraint_density = fração de pares (tarefa, agente) compatíveis.
    Densidade baixa -> problema mais restrito -> mais difícil.
    """
    rng = np.random.default_rng(seed)

    tasks = [
        Task(kind=rng.choice(_KINDS), payload={}, cost_hint=float(rng.uniform(0.5, 5.0)))
        for _ in range(n_tasks)
    ]
    agents = [
        AgentSpec(name=f"agent_{j}", handles=list(_KINDS), capacity=float(rng.uniform(5, 20)))
        for j in range(n_agents)
    ]

    cost = rng.uniform(0.5, 5.0, size=(n_tasks, n_agents))
    compatible = rng.random((n_tasks, n_agents)) < constraint_density
    # garante ao menos um agente compatível por tarefa (instância factível)
    for t in range(n_tasks):
        if not compatible[t].any():
            compatible[t, rng.integers(n_agents)] = True
    cost[~compatible] = np.inf

    return AllocationProblem(tasks=tasks, agents=agents, cost=cost)


# TODO (Etapa 3): gerador a partir de traces reais de orquestração
# (logs de pipelines financeiros), preservando distribuição de custos.
