"""Métricas de comparação — agnósticas ao componente.

Princípio (Rønnow et al., 2014): comparar sempre contra o MELHOR baseline
clássico disponível para aquele componente, nunca contra um baseline fraco.
"""

from __future__ import annotations

from dataclasses import dataclass

from qmas.core.component import Paradigm, TimedRun


@dataclass
class ComparisonRecord:
    """Uma linha do resultado experimental: implementação x instância."""

    component: str
    layer: str
    implementation: str
    paradigm: Paradigm
    instance_params: dict
    seed: int
    wall_time_s: float
    quality: float | None
    feasible: bool
    quality_ratio: float | None    # qualidade / qualidade da referência (se houver)


def quality_ratio(run: TimedRun, reference: TimedRun | None) -> float | None:
    if reference is None or run.output.quality is None or reference.output.quality is None:
        return None
    ref = reference.output.quality
    return run.output.quality / ref if ref != 0 else None


def time_to_solution(run: TimedRun) -> float:
    """Hoje = wall time. Alvo: TTS_99 = t * ln(1-0.99)/ln(1-p_success) para
    implementações estocásticas, com p_success estimado por replicações."""
    return run.wall_time_s
