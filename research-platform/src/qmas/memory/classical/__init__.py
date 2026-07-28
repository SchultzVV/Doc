"""Memória clássica (baselines): store episódico com recuperação por embedding."""

from __future__ import annotations

from typing import Any

from qmas.core.component import Paradigm, RunOutput


class EpisodicStore:
    name = "episodic_store"
    paradigm = Paradigm.CLASSICAL

    def run(self, instance: Any) -> RunOutput:
        raise NotImplementedError("formalizar após Etapa 1")
