"""Recuperação quântica (candidatos — expectativa negativa a testar)."""

from __future__ import annotations

from typing import Any

from qmas.core.component import Paradigm, RunOutput


class GroverRetriever:
    """Busca não estruturada via Grover (ganho quadrático em queries ao
    oráculo). A questão experimental não é o ganho assintótico, e sim se o
    custo de construir o oráculo/codificar o corpus o anula (H2/H3)."""

    name = "grover"
    paradigm = Paradigm.QUANTUM

    def run(self, instance: Any) -> RunOutput:
        raise NotImplementedError("formalizar oráculo após Etapa 1")
