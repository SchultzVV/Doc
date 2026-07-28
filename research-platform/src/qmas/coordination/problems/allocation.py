"""Alocação de tarefas a agentes como Generalized Assignment Problem (GAP).

Variáveis binárias x[t,a] = 1 se a tarefa t vai para o agente a.
Objetivo: min custo total. Restrições (penalizadas no QUBO):
  (1) cada tarefa em exatamente um agente compatível;
  (2) capacidade de cada agente respeitada.

Este é o componente-alvo da hipótese H1: formulação natural como QUBO,
compatível com QAOA e quantum annealing.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from qmas.core.contracts import AgentSpec, Task


@dataclass
class AllocationProblem:
    tasks: list[Task]
    agents: list[AgentSpec]
    cost: np.ndarray          # (n_tasks x n_agents); inf se incompatível

    def n_binary_vars(self) -> int:
        return len(self.tasks) * len(self.agents)

    def to_qubo(self, penalty: float = 10.0) -> "QUBO":
        """Penaliza restrição (1): (sum_a x[t,a] - 1)^2 por tarefa.

        TODO: restrição de capacidade (2) exige variáveis de folga binárias
        (encoding log) — implementar na Etapa 2/3.
        """
        from qmas.coordination.problems.qubo import QUBO

        nt, na = len(self.tasks), len(self.agents)
        n = nt * na
        idx = lambda t, a: t * na + a  # noqa: E731
        Q = np.zeros((n, n))
        offset = 0.0

        for t in range(nt):
            for a in range(na):
                c = self.cost[t, a]
                Q[idx(t, a), idx(t, a)] += c if np.isfinite(c) else penalty * 10
            # penalidade (sum_a x - 1)^2 = sum x - 2 sum x + 2 sum_{a<b} x_a x_b + 1
            for a in range(na):
                Q[idx(t, a), idx(t, a)] -= penalty
                for b in range(a + 1, na):
                    Q[idx(t, a), idx(t, b)] += 2 * penalty
            offset += penalty

        names = [f"x[{t.id},{ag.name}]" for t in self.tasks for ag in self.agents]
        return QUBO(Q=Q, var_names=names, offset=offset)


def build_allocation_problem(tasks: list[Task], agents: list[AgentSpec]) -> AllocationProblem:
    cost = np.full((len(tasks), len(agents)), np.inf)
    for i, task in enumerate(tasks):
        for j, spec in enumerate(agents):
            if task.kind in spec.handles:
                cost[i, j] = task.cost_hint  # refinamento: custo por par (t, a)
    return AllocationProblem(tasks=tasks, agents=agents, cost=cost)
