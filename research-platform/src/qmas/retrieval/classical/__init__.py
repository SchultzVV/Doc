"""Recuperação clássica (baselines)."""

from __future__ import annotations

from typing import Any

from qmas.core.component import Paradigm, RunOutput


class BruteForceVectorSearch:
    """Busca vetorial exata (produto interno) — baseline. Adicionar HNSW/
    FAISS como baseline forte antes de qualquer comparação quântica."""

    name = "brute_force_vector"
    paradigm = Paradigm.CLASSICAL

    def run(self, instance: Any) -> RunOutput:
        import numpy as np

        query, corpus, k = instance["query"], instance["corpus"], instance.get("k", 5)
        scores = np.asarray(corpus) @ np.asarray(query)
        top = np.argsort(scores)[::-1][:k]
        return RunOutput(value=top.tolist(), quality=float(scores[top].sum()))
