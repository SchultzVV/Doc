"""A abstração central da plataforma: Componente Sob Estudo.

O desenho experimental da tese é sempre o mesmo, independente da camada:

    Multi-Agent System
        -> Component Under Study
            -> Classical Implementation
            -> Quantum Implementation
        -> Experimental Comparison

Nenhuma camada é privilegiada. A revisão bibliográfica (Etapa 1) decide
QUAIS componentes viram objeto de experimento; este módulo só garante que
qualquer um deles seja comparável sob o mesmo protocolo.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Protocol, runtime_checkable


class Layer(str, Enum):
    """As camadas candidatas — nenhuma é a hipótese principal."""

    PLANNING = "planning"          # tree search, MCTS, HTN...
    RETRIEVAL = "retrieval"        # RAG, busca vetorial, similaridade
    MEMORY = "memory"              # episódica, longo prazo, stores
    COORDINATION = "coordination"  # consenso, alocação, negociação, roteamento
    LEARNING = "learning"          # QML: classificação, regressão, forecast
    REASONING = "reasoning"        # circuitos como etapas de raciocínio (exploratória)


class Paradigm(str, Enum):
    CLASSICAL = "classical"
    QUANTUM = "quantum"
    HYBRID = "hybrid"


@dataclass
class RunOutput:
    """Saída padronizada de uma execução — o que o harness compara."""

    value: Any                     # resultado específico do componente
    quality: float | None = None   # métrica de qualidade (maior = melhor); None se n/a
    feasible: bool = True
    metadata: dict = field(default_factory=dict)


@runtime_checkable
class Implementation(Protocol):
    """Uma implementação (clássica OU quântica) de um componente.

    Contrato mínimo: mesmo tipo de instância entra, RunOutput sai.
    É isso que torna clássico e quântico intercambiáveis no experimento.
    """

    name: str
    paradigm: Paradigm

    def run(self, instance: Any) -> RunOutput: ...


@dataclass
class TimedRun:
    implementation: str
    paradigm: Paradigm
    output: RunOutput
    wall_time_s: float


def timed(impl: Implementation, instance: Any) -> TimedRun:
    t0 = time.perf_counter()
    out = impl.run(instance)
    return TimedRun(
        implementation=impl.name,
        paradigm=impl.paradigm,
        output=out,
        wall_time_s=time.perf_counter() - t0,
    )


@dataclass
class ComponentUnderStudy:
    """Empacota tudo que um experimento precisa saber sobre um componente.

    Cada camada fornece uma factory que devolve isto; o harness em
    qmas.experiments consome sem saber de qual camada veio.
    """

    layer: Layer
    name: str
    question: str                                   # a pergunta de pesquisa da camada
    instance_generator: Callable[..., Any]          # (params, seed) -> instância
    implementations: list[Implementation]
    reference: Implementation | None = None         # baseline exato/ótimo, se existir

    def classical(self) -> list[Implementation]:
        return [i for i in self.implementations if i.paradigm == Paradigm.CLASSICAL]

    def quantum(self) -> list[Implementation]:
        return [i for i in self.implementations if i.paradigm == Paradigm.QUANTUM]
