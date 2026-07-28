"""Orquestrador do sistema multiagente — agnóstico ao componente sob estudo.

Máquina de estados PLAN -> ALLOCATE -> EXECUTE -> AGGREGATE. A etapa de
alocação é INJETADA (qualquer callable que satisfaça o contrato), de modo
que o orquestrador funciona igualmente com um alocador clássico, quântico
ou híbrido — ele não assume onde a vantagem quântica está.

O HybridSelector materializa H4/H5: um orquestrador capaz de escolher
dinamicamente entre implementações clássicas e quânticas de um componente.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Callable

from qmas.core.component import Implementation, RunOutput
from qmas.core.contracts import AgentSpec, Assignment, Message, Task

Allocator = Callable[[list[Task], list[AgentSpec]], Assignment]


class State(str, Enum):
    PLAN = "plan"
    ALLOCATE = "allocate"
    EXECUTE = "execute"
    AGGREGATE = "aggregate"
    DONE = "done"
    FAILED = "failed"


class Orchestrator:
    def __init__(self, agents: dict[str, Any], allocator: Allocator) -> None:
        self.agents = agents
        self.allocator = allocator
        self.state = State.PLAN

    def run(self, tasks: list[Task]) -> dict[str, Message]:
        specs = [AgentSpec(name=a.name, handles=list(a.handles)) for a in self.agents.values()]

        self.state = State.ALLOCATE
        assignment = self.allocator(tasks, specs)
        if not assignment.feasible:
            self.state = State.FAILED
            raise RuntimeError("alocação infactível")

        self.state = State.EXECUTE
        results: dict[str, Message] = {}
        for task in _in_dependency_order(tasks):
            results[task.id] = self.agents[assignment.mapping[task.id]](task)

        self.state = State.AGGREGATE
        # TODO: agregação/validação cruzada dos resultados
        self.state = State.DONE
        return results


class HybridSelector:
    """Seleciona, por instância, qual implementação de um componente executar.

    Hoje: política injetada (ou primeira clássica como default seguro).
    Alvo (H4): política calibrada pelas curvas de crossover medidas nos
    experimentos — f(tamanho, estrutura, custo de codificação, ruído).
    """

    def __init__(
        self,
        implementations: list[Implementation],
        policy: Callable[[Any, list[Implementation]], Implementation] | None = None,
    ) -> None:
        if not implementations:
            raise ValueError("nenhuma implementação registrada")
        self.implementations = implementations
        self.policy = policy or (lambda _instance, impls: impls[0])

    def run(self, instance: Any) -> RunOutput:
        chosen = self.policy(instance, self.implementations)
        return chosen.run(instance)


def _in_dependency_order(tasks: list[Task]) -> list[Task]:
    """Ordenação topológica ingênua; substituir por grafo real (networkx)."""
    done: set[str] = set()
    ordered: list[Task] = []
    pending = list(tasks)
    while pending:
        progress = False
        for t in list(pending):
            if all(d in done for d in t.depends_on):
                ordered.append(t)
                done.add(t.id)
                pending.remove(t)
                progress = True
        if not progress:
            raise ValueError("ciclo de dependências")
    return ordered
