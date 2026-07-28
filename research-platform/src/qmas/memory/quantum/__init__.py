"""Memória quântica (candidatos): memórias associativas quânticas (QAM).

Mesmo alerta da camada de recuperação: o gargalo de escrita/codificação
(qRAM) é o provável fator limitante — medir, não assumir.
"""

from __future__ import annotations

from typing import Any

from qmas.core.component import Paradigm, RunOutput


class QuantumAssociativeMemory:
    name = "qam"
    paradigm = Paradigm.QUANTUM

    def run(self, instance: Any) -> RunOutput:
        raise NotImplementedError("formalizar após Etapa 1")
