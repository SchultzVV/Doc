"""Planejadores clássicos (baselines)."""

from __future__ import annotations

from typing import Any

from qmas.core.component import Paradigm, RunOutput


class MCTSPlanner:
    """Monte Carlo Tree Search — baseline planejado. TODO: formalizar o
    espaço de estados junto com a versão quântica (mesma instância)."""

    name = "mcts"
    paradigm = Paradigm.CLASSICAL

    def run(self, instance: Any) -> RunOutput:
        raise NotImplementedError("formalizar após Etapa 1")
