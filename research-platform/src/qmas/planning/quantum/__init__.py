"""Planejadores quânticos (candidatos)."""

from __future__ import annotations

from typing import Any

from qmas.core.component import Paradigm, RunOutput


class QuantumWalkPlanner:
    """Busca em árvore via caminhada quântica. Ganho teórico esperado:
    quadrático em árvores balanceadas — verificar se sobrevive ao custo
    de codificação em instâncias de planejamento reais."""

    name = "quantum_walk"
    paradigm = Paradigm.QUANTUM

    def run(self, instance: Any) -> RunOutput:
        raise NotImplementedError("formalizar após Etapa 1")
